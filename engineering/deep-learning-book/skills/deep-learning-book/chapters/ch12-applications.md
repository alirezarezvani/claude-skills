# Chapter 12: Applications

**Source chapter (free, official):** https://www.deeplearningbook.org/contents/applications.html

## Core Idea

How deep learning was actually deployed circa 2016: large-scale implementation (GPUs,
distributed training, model compression), then computer vision, speech recognition, and NLP.
This is the most time-dated chapter in the book — read the *systems* half, discount the
*state-of-the-art* half.

## Frameworks Introduced

- **Large-scale implementation**: GPU data parallelism, model parallelism, asynchronous SGD
  (Hogwild-style), parameter servers.
- **Model compression**: distillation, quantization, pruning — for inference cost.
- **Dynamic structure / conditional computation**: cascades and gating so that not every input
  pays the full cost.
- **Preprocessing in vision**: contrast normalization, whitening, dataset augmentation.
- **Speech**: the acoustic-model pipeline and its shift from GMM-HMM to deep networks.
- **NLP**: n-gram models, word embeddings and the curse of dimensionality over vocabularies,
  hierarchical softmax and sampling-based approximations for large output vocabularies,
  neural machine translation.
- **Recommender systems** and the exploration/exploitation problem.
- **Knowledge representation and relational reasoning.**

## Mental Models

- Separate **capability claims** (perishable) from **systems constraints** (durable). Memory
  bandwidth, batch efficiency, and inference cost still shape architecture choices.
- Read the large-vocabulary softmax section as an instance of the general pattern: **when the
  normalizing sum is expensive, approximate it** — the same problem Ch 18 attacks head-on.
- Treat conditional computation as the ancestor of **Mixture-of-Experts** routing.

## Anti-patterns

- **Citing this chapter's benchmark numbers or SOTA claims** — they are a decade old.
- **Copying its NLP pipeline**: subword tokenization (BPE/SentencePiece) and pretrained
  transformers replaced nearly all of it.

## What changed after 2016

Almost everything at the application layer. Speech moved to end-to-end CTC/attention models and
then to large self-supervised encoders. NLP moved to pretrained transformers (BERT 2018, GPT
family), with subword tokenization and full-softmax over ~30k–200k subwords making hierarchical
softmax largely unnecessary. Vision moved to self-supervised pretraining and ViTs. Distillation,
quantization and pruning grew into a mature inference-optimization discipline. Conditional
computation matured into sparse MoE. **Confidence: high.**

## Key Takeaways

1. Read this chapter for the systems reasoning and the approximation techniques, not for what is
   state of the art.
2. When your output vocabulary or normalizing constant is huge, recognize it as the recurring
   partition-function problem.
3. Plan inference cost as an architecture constraint from the start.

## Connects To

- **Ch 18**: the partition-function problem in its general form.
- **Ch 9 / Ch 10**: the architectures being applied here.
- **references/book_to_2026_delta.md**: what replaced each application pipeline.
