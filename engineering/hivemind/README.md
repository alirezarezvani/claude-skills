# hivemind

Opt-in plugin that lets Claude Code orchestrate [opencode](https://opencode.ai) workers
(single worker or a scout/coder/tester swarm) on cheaper or open models. It ships
outside every domain bundle; install it only if you want it.

## Data flow

**By default your code leaves your machine.** The default worker model,
`opencode/mimo-v2.5-free`, runs on opencode's hosted service, so every prompt, file and
diff a worker receives is sent to opencode's endpoints. Nothing on the worker side
calls the Anthropic API.

To keep code on your machine, pass `--model` pointing at a locally served model (for
example an Ollama or LM Studio provider configured in your opencode config). With any
hosted model, delegate only code you are allowed to send to that provider, and never
delegate secrets.

## Install and use

See [SKILL.md](SKILL.md) for prerequisites, setup, the invocation contract and the
swarm flow. License: MIT (see [LICENSE.txt](LICENSE.txt)).
