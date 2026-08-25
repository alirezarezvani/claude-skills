#!/usr/bin/env python3
"""model_arithmetic.py — parameters, FLOPs and activation memory for a layer stack.

Chapter 6 makes the point that the real cost of depth in training is activation memory:
the backward pass needs the forward activations, which is why gradient checkpointing
trades compute for memory. Chapter 9 makes the receptive-field and parameter-sharing
arithmetic explicit. This tool does that arithmetic for a declared stack, and — the part
that catches real bugs — refuses to continue when one layer's output shape cannot feed
the next.

Shapes are per example, excluding the batch dimension. FLOPs are per example, per
forward pass; a training step costs roughly 3x a forward pass (forward + backward).

Layer types: input, linear, conv2d, pool2d, flatten, embedding, layernorm, activation,
dropout, mha (multi-head self-attention), lstm, gru.

Standard library only. No frameworks, no network calls.

Exit codes:
    0  the stack is consistent and the report was produced
    2  usage error (argparse)
    4  the spec could not be parsed (bad JSON, unknown layer type, missing field)
    5  shape mismatch between consecutive layers — the offending layer is named
"""

from __future__ import annotations

import argparse
import json
import math
import sys

BYTES_PER_ELEMENT = {"fp32": 4, "tf32": 4, "fp16": 2, "bf16": 2, "fp8": 1}

# A multiply-accumulate is counted as 2 FLOPs. --convention mac reports MACs instead.
FLOPS_PER_MAC = 2


class SpecError(ValueError):
    """The spec is malformed: bad JSON, unknown layer, or a missing field."""


class ShapeError(ValueError):
    """A layer cannot consume the shape the previous layer produced."""


def _require(layer: dict, key: str, index: int):
    if key not in layer:
        raise SpecError(f"layer {index} ({layer.get('type', '?')}) is missing '{key}'")
    return layer[key]


def _prod(shape: tuple[int, ...]) -> int:
    total = 1
    for dim in shape:
        total *= dim
    return total


def step(layer: dict, shape: tuple[int, ...], index: int) -> tuple[tuple[int, ...], int, int]:
    """Return (output_shape, parameters, macs) for one layer given its input shape."""
    kind = _require(layer, "type", index)

    if kind == "input":
        return tuple(_require(layer, "shape", index)), 0, 0

    if kind == "linear":
        units = int(_require(layer, "units", index))
        if len(shape) != 1:
            raise ShapeError(
                f"layer {index} (linear) needs a 1-D input, got {shape}. "
                "Insert a flatten layer, or use a per-token linear on a 2-D sequence "
                "by declaring the shape as [features]."
            )
        bias = bool(layer.get("bias", True))
        params = shape[0] * units + (units if bias else 0)
        return (units,), params, shape[0] * units

    if kind == "conv2d":
        filters = int(_require(layer, "filters", index))
        kernel = int(_require(layer, "kernel", index))
        stride = int(layer.get("stride", 1))
        padding = layer.get("padding", "same")
        if len(shape) != 3:
            raise ShapeError(
                f"layer {index} (conv2d) needs a 3-D input (C, H, W), got {shape}"
            )
        channels, height, width = shape
        if padding == "same":
            out_h, out_w = math.ceil(height / stride), math.ceil(width / stride)
        elif padding == "valid":
            out_h = (height - kernel) // stride + 1
            out_w = (width - kernel) // stride + 1
        else:
            raise SpecError(f"layer {index} (conv2d): padding must be 'same' or 'valid'")
        if out_h <= 0 or out_w <= 0:
            raise ShapeError(
                f"layer {index} (conv2d) with kernel {kernel} and stride {stride} "
                f"reduces {height}x{width} to {out_h}x{out_w} — the kernel is larger "
                "than the feature map."
            )
        groups = int(layer.get("groups", 1))
        if channels % groups or filters % groups:
            raise SpecError(
                f"layer {index} (conv2d): groups={groups} does not divide "
                f"in_channels={channels} and filters={filters}"
            )
        bias = bool(layer.get("bias", True))
        params = (kernel * kernel * (channels // groups) * filters) + (filters if bias else 0)
        macs = kernel * kernel * (channels // groups) * filters * out_h * out_w
        return (filters, out_h, out_w), params, macs

    if kind == "pool2d":
        size = int(layer.get("size", 2))
        stride = int(layer.get("stride", size))
        if len(shape) != 3:
            raise ShapeError(f"layer {index} (pool2d) needs a 3-D input, got {shape}")
        channels, height, width = shape
        out_h = (height - size) // stride + 1
        out_w = (width - size) // stride + 1
        if out_h <= 0 or out_w <= 0:
            raise ShapeError(
                f"layer {index} (pool2d) reduces {height}x{width} to {out_h}x{out_w}"
            )
        return (channels, out_h, out_w), 0, 0

    if kind == "flatten":
        return (_prod(shape),), 0, 0

    if kind == "embedding":
        vocab = int(_require(layer, "vocab", index))
        dim = int(_require(layer, "dim", index))
        seq = int(layer.get("seq_len", shape[0] if shape else 1))
        return (seq, dim), vocab * dim, 0  # a lookup, not a matmul

    if kind == "layernorm":
        features = shape[-1]
        return shape, 2 * features, 0

    if kind in ("activation", "dropout"):
        return shape, 0, 0

    if kind == "mha":
        # Multi-head self-attention over a (seq, d_model) input.
        if len(shape) != 2:
            raise ShapeError(
                f"layer {index} (mha) needs a 2-D input (seq_len, d_model), got {shape}"
            )
        seq, d_model = shape
        heads = int(layer.get("heads", 8))
        if d_model % heads:
            raise SpecError(
                f"layer {index} (mha): d_model={d_model} is not divisible by heads={heads}"
            )
        # 4 projections (Q, K, V, O), each d_model x d_model.
        params = 4 * d_model * d_model + (4 * d_model if layer.get("bias", True) else 0)
        proj_macs = 4 * seq * d_model * d_model
        # Scores (seq x seq x d_model) and the weighted value sum, both quadratic in seq.
        attn_macs = 2 * seq * seq * d_model
        return shape, params, proj_macs + attn_macs

    if kind in ("lstm", "gru"):
        if len(shape) != 2:
            raise ShapeError(
                f"layer {index} ({kind}) needs a 2-D input (seq_len, features), got {shape}"
            )
        seq, features = shape
        units = int(_require(layer, "units", index))
        gates = 4 if kind == "lstm" else 3
        params = gates * (features * units + units * units + 2 * units)
        macs = seq * gates * (features * units + units * units)
        out = (seq, units) if layer.get("return_sequences", True) else (units,)
        return out, params, macs

    raise SpecError(f"layer {index}: unknown layer type {kind!r}")


def analyse(spec: dict, dtype: str, convention: str) -> dict:
    layers = spec.get("layers")
    if not isinstance(layers, list) or not layers:
        raise SpecError("spec must contain a non-empty 'layers' list")
    if layers[0].get("type") != "input":
        raise SpecError("the first layer must be of type 'input'")

    width = BYTES_PER_ELEMENT[dtype]
    shape: tuple[int, ...] = ()
    rows = []
    total_params = 0
    total_macs = 0
    total_activations = 0

    for index, layer in enumerate(layers):
        shape, params, macs = step(layer, shape, index)
        activations = _prod(shape)
        total_params += params
        total_macs += macs
        # The input layer's tensor is not a stored intermediate activation.
        if index > 0:
            total_activations += activations
        rows.append({
            "index": index,
            "type": layer["type"],
            "name": layer.get("name", layer["type"]),
            "output_shape": list(shape),
            "parameters": params,
            "macs": macs,
            "flops": macs * FLOPS_PER_MAC,
            "activation_elements": activations,
        })

    compute = total_macs if convention == "mac" else total_macs * FLOPS_PER_MAC
    return {
        "dtype": dtype,
        "convention": convention,
        "layers": rows,
        "totals": {
            "parameters": total_params,
            "parameter_bytes": total_params * width,
            "forward_macs": total_macs,
            "forward_flops": total_macs * FLOPS_PER_MAC,
            "reported_compute": compute,
            "activation_elements_per_example": total_activations,
            "activation_bytes_per_example": total_activations * width,
        },
        "notes": [
            "Shapes and costs are per example; the batch dimension is excluded.",
            "A training step costs roughly 3x the forward FLOPs (forward + backward).",
            "Activation memory is the training-time cost of depth (ch06). Gradient "
            "checkpointing trades compute for it.",
            "Optimizer state is extra: Adam/AdamW holds two moments per parameter, so "
            "budget ~3x parameter bytes for weights plus state in fp32.",
            "Attention cost is quadratic in sequence length — visible in the mha row.",
        ],
    }


SAMPLE_SPEC = {
    "name": "small convnet, CIFAR-shaped",
    "layers": [
        {"type": "input", "shape": [3, 32, 32]},
        {"type": "conv2d", "filters": 32, "kernel": 3, "padding": "same"},
        {"type": "activation", "name": "relu"},
        {"type": "pool2d", "size": 2},
        {"type": "conv2d", "filters": 64, "kernel": 3, "padding": "same"},
        {"type": "activation", "name": "relu"},
        {"type": "pool2d", "size": 2},
        {"type": "flatten"},
        {"type": "linear", "units": 128},
        {"type": "activation", "name": "relu"},
        {"type": "dropout"},
        {"type": "linear", "units": 10},
    ],
}


def human(value: int) -> str:
    for unit, scale in (("G", 1e9), ("M", 1e6), ("K", 1e3)):
        if value >= scale:
            return f"{value / scale:.2f}{unit}"
    return str(value)


def render(result: dict) -> str:
    lines = [
        "MODEL ARITHMETIC",
        "=" * 78,
        f"{'#':>2}  {'layer':<12} {'output shape':<18} {'params':>12} "
        f"{'MFLOPs':>10} {'act.elts':>10}",
        "-" * 78,
    ]
    for row in result["layers"]:
        shape = "x".join(str(dim) for dim in row["output_shape"])
        lines.append(
            f"{row['index']:>2}  {row['type']:<12} {shape:<18} "
            f"{row['parameters']:>12,} {row['flops'] / 1e6:>10.2f} "
            f"{row['activation_elements']:>10,}"
        )
    totals = result["totals"]
    lines += [
        "-" * 78,
        f"Parameters          : {totals['parameters']:,} "
        f"({human(totals['parameter_bytes'])}B at {result['dtype']})",
        f"Forward FLOPs/ex    : {human(totals['forward_flops'])} "
        f"({human(totals['forward_macs'])} MACs)",
        f"Training step (~3x) : {human(totals['forward_flops'] * 3)} FLOPs/ex",
        f"Activations/ex      : {totals['activation_elements_per_example']:,} elements "
        f"({human(totals['activation_bytes_per_example'])}B at {result['dtype']})",
        "",
    ]
    lines.append(f"At batch 128: activations ≈ "
                 f"{human(totals['activation_bytes_per_example'] * 128)}B")
    lines.append("")
    for note in result["notes"]:
        lines.append(f"· {note}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compute parameters, FLOPs and activation memory for a layer stack.",
        epilog="Exit codes: 0 ok · 4 bad spec · 5 shape mismatch.",
    )
    parser.add_argument("--spec", help="path to a JSON layer spec")
    parser.add_argument("--spec-sample", action="store_true",
                        help="print the built-in sample spec and exit")
    parser.add_argument("--dtype", choices=sorted(BYTES_PER_ELEMENT), default="fp32")
    parser.add_argument("--convention", choices=("flop", "mac"), default="flop",
                        help="report FLOPs (1 MAC = 2 FLOPs) or raw MACs")
    parser.add_argument("--output", choices=("text", "json"), default="text")
    parser.add_argument("--sample", action="store_true",
                        help="analyse the built-in sample spec")
    args = parser.parse_args(argv)

    if args.spec_sample:
        print(json.dumps(SAMPLE_SPEC, indent=2))
        return 0

    if args.sample:
        spec = SAMPLE_SPEC
    elif args.spec:
        try:
            with open(args.spec, encoding="utf-8") as handle:
                spec = json.load(handle)
        except OSError as error:
            print(f"cannot read spec: {error}", file=sys.stderr)
            return 4
        except json.JSONDecodeError as error:
            print(f"spec is not valid JSON: {error}", file=sys.stderr)
            return 4
    else:
        parser.error("--spec is required (or use --sample / --spec-sample)")

    try:
        result = analyse(spec, args.dtype, args.convention)
    except ShapeError as error:
        print(f"SHAPE MISMATCH — {error}", file=sys.stderr)
        print("A shape mismatch is a modelling error, not a typing error (ch02).",
              file=sys.stderr)
        return 5
    except SpecError as error:
        print(f"BAD SPEC — {error}", file=sys.stderr)
        return 4

    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        print(render(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
