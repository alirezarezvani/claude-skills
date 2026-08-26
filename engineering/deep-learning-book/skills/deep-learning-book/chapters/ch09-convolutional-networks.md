# Chapter 9: Convolutional Networks

**Source chapter (free, official):** https://www.deeplearningbook.org/contents/convnets.html

## Core Idea

Convolution is three ideas at once — sparse interactions, parameter sharing, and equivariance to
translation — and each is a prior about grid-structured data. Pooling adds approximate invariance
to small translations. The architecture is a statement about the data, not a trick.

## Frameworks Introduced

- **Sparse interactions**: each output depends on a small receptive field, so cost drops from
  O(m·n) to O(k·n).
- **Parameter sharing**: one kernel is reused at every position — the strongest regularizer in
  Ch 7's catalogue, applied structurally.
- **Equivariance to translation**: shift the input, the feature map shifts. Convolution is *not*
  equivariant to rotation or scale — a fact that motivates augmentation.
- **Pooling**: max/average pooling gives local invariance and downsampling; it is a prior that
  small position changes should not matter.
- **Variants**: valid/same/full padding, strided convolution, dilated convolution, tiled
  convolution, locally-connected layers (no sharing), transposed convolution for upsampling.
- **Convolution as an infinitely strong prior**: the chapter's sharpest framing — a conv layer is
  a fully-connected layer with hard constraints on its weights.
- **Structured outputs**: dense prediction (segmentation) rather than one label per image.
- **Efficiency**: FFT-based and separable convolutions.

## Mental Models

- Ask "**is the statistic I need position-invariant?**" If yes, convolve. If not (a face-aligned
  dataset, a tabular grid with meaningful coordinates), the prior is wrong and locally-connected
  or attention layers may fit better.
- Compute **receptive field** deliberately: it must cover the evidence needed for the decision.
  Depth, stride and dilation are three ways to buy it, with different costs.
- Treat pooling as **throwing away location on purpose**; when location is the answer
  (segmentation, detection), pool less and use dilation or skip connections.

## Anti-patterns

- **Using convolution on data with no spatial/temporal locality** (arbitrary tabular columns) —
  the sharing prior is simply false there.
- **Ignoring receptive field** and then adding parameters to fix an underfitting model.
- **Aggressive pooling in a dense-prediction task.**

## What changed after 2016

Residual networks (2015) are treated only briefly here but became the default. Since then:
depthwise-separable convolutions (MobileNet/Xception), EfficientNet-style compound scaling,
and — most importantly — **Vision Transformers** (Dosovitskiy et al. 2020), which discard the
convolutional prior in favour of data plus attention, and win at scale while ConvNets remain
competitive at smaller data sizes (ConvNeXt, 2022, closed much of the gap). The chapter's
argument that the conv prior is a *bet on the data* is exactly what ViT's data-hunger confirms.
**Confidence: high.**

## Key Takeaways

1. Justify convolution by the invariance you actually believe in.
2. Size the receptive field before adding depth for its own sake.
3. Expect the conv prior to pay off most when data is limited — this is the modern boundary
   between ConvNets and ViTs.

## Connects To

- **Ch 7**: parameter sharing as structural regularization.
- **Ch 12**: computer-vision applications built on this.
- **references/book_to_2026_delta.md**: the ViT/ConvNeXt line.
