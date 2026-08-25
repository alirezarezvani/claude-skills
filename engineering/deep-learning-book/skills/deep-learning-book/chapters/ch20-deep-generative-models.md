# Chapter 20: Deep Generative Models

**Source chapter (free, official):** https://www.deeplearningbook.org/contents/generative_models.html

## Core Idea

The book's capstone: every generative model family circa 2016, organized by how it handles the
intractable quantity. Boltzmann machines and their deep variants pay for the partition function;
VAEs bound the likelihood; GANs avoid likelihood entirely; autoregressive models factor it away.
That taxonomy — **not** the specific models — is what still holds.

## Frameworks Introduced

- **Boltzmann machines, RBMs, deep belief networks, deep Boltzmann machines**: energy-based
  models trained with the Ch 18 machinery. Historically pivotal; now largely superseded.
- **Variational autoencoder (VAE)**: an encoder produces q(h|x), a decoder produces p(x|h), and
  the **reparameterization trick** makes the sampling step differentiable so the ELBO can be
  optimized by backprop. Blurry samples are the predictable consequence of the likelihood
  objective plus a limited posterior family.
- **Generative adversarial networks (GANs)**: a generator and a discriminator in a minimax game;
  no explicit likelihood, sharp samples, unstable training, and mode collapse as the
  characteristic failure.
- **Autoregressive / fully-visible belief networks**: factor p(x) by the chain rule and model each
  conditional. Exact likelihood, sequential sampling. (NADE, PixelRNN/PixelCNN, WaveNet era.)
- **Generative stochastic networks; denoising-based generation**: learning a transition operator
  rather than a distribution — the direct ancestor of diffusion.
- **Evaluating generative models**: the chapter's warning that likelihood, sample quality and
  downstream usefulness are **three different axes** that routinely disagree.

## Mental Models

- Classify any new generative model by **what it does about the intractable term**: bound it,
  avoid it, factor it away, or learn a sampler directly. New families are new answers to that one
  question.
- Read blurriness vs mode collapse as **the KL asymmetry from Ch 3 made visible**: likelihood-based
  models cover modes and blur; adversarial models sharpen and drop modes.
- Never accept a **single** evaluation number for a generative model.

## Anti-patterns

- **Comparing FID across papers with different preprocessing** — the metric is not portable.
- **Treating sample quality as evidence of density estimation quality**, or vice versa.
- **Starting a new project with a Boltzmann machine.**

## What changed after 2016

The most-superseded chapter in the book, and worth reading anyway for its taxonomy.
**Diffusion models** (Ho et al. 2020, built on Ch 18's denoising score matching and Ch 14's
denoising autoencoders) displaced GANs for image, audio and video generation. **Autoregressive
transformers** became the dominant generative model overall — the chain-rule factorization
described here, scaled. VAEs persist mainly as latent-space compressors inside latent diffusion
pipelines rather than as end-user generators. GANs remain useful for fast, low-step generation.
Boltzmann machines are history. Evaluation remains unsolved, exactly as the chapter warned.
**Confidence: high.**

## Key Takeaways

1. Use the taxonomy, not the model list — it classifies architectures invented since.
2. Expect blurring from likelihood objectives and mode-dropping from adversarial ones; pick your
   failure mode deliberately.
3. Evaluate generative models on at least likelihood, sample quality, and downstream use.

## Connects To

- **Ch 18**: score matching, whose descendants replaced most of this chapter.
- **Ch 19**: the ELBO the VAE optimizes.
- **references/book_to_2026_delta.md**: the diffusion and autoregressive-transformer lines.
