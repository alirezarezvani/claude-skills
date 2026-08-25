# Chapter 11: Key Papers in Deep RL

## Core Idea
A curated, explicitly non-comprehensive reading list of roughly 100 papers organized into
13 topic areas — designed as a starting point for someone looking to do research, and as
the map you use to pick a research topic in ch10's "explore the literature" step.

## Frameworks Introduced
- **Use the list as a topic map, not a queue.** The intended workflow (from ch10): scan the
  sections to become aware of what topics exist, find a paper on one that inspires you, read
  it thoroughly, then use its related-work section and citations to do a deep dive. You will
  start to see where the unsolved problems are.
- **Each entry is annotated with what it contributes** — either **Algorithm: X** (this paper
  introduced X) or **Contribution: ...** (this paper established a result, a critique or a
  codebase). Scan the annotations, not the titles.

## Reference Tables

The 13 sections, with the subsections that reveal the field's internal structure:

| # | Section | Subsections / notable entries |
|---|---------|------------------------------|
| 1 | **Model-Free RL** | a. Deep Q-Learning (DQN, Deep Recurrent Q-Learning, Dueling DQN, Double DQN, Prioritized Experience Replay, Rainbow) · b. Policy Gradients (A3C, TRPO, GAE, PPO, ACKTR, ACER, SAC) · c. Deterministic Policy Gradients (DPG, DDPG, TD3) · d. Distributional RL (C51, QR-DQN, IQN, Dopamine) · e. Policy Gradients with Action-Dependent Baselines (Q-Prop, Stein Control Variates, and Tucker et al's critique) · f. Path-Consistency Learning (PCL, Trust-PCL) · g. Other Ways of Combining Policy-Learning and Q-Learning (PGQL, Reactor, IPG, the policy-gradient/soft-Q-learning equivalence) · h. Evolutionary Algorithms (ES) |
| 2 | **Exploration** | a. Intrinsic Motivation (VIME, count-based pseudocounts, hash-based counts, EX2, ICM, RND) · b. Unsupervised RL (VIC, DIAYN, VALOR) |
| 3 | **Transfer and Multitask RL** | Progressive Networks, UVFA, UNREAL, PathNet, MATL, HER |
| 4 | **Hierarchy** | STRAW, Feudal Networks, HIRO |
| 5 | **Memory** | MFEC, NEC, Neural Map, MERLIN, RMC |
| 6 | **Model-Based RL** | a. Model is Learned (I2A, MBMF, MVE) · b. Model is Given (AlphaZero and relatives) |
| 7 | **Meta-RL** | |
| 8 | **Scaling RL** | |
| 9 | **RL in the Real World** | |
| 10 | **Safety** | |
| 11 | **Imitation Learning and Inverse Reinforcement Learning** | |
| 12 | **Reproducibility, Analysis, and Critique** | |
| 13 | **Bonus: Classic Papers in RL Theory or Review** | |

## Mental Models
- **Section 1's shape mirrors ch8's taxonomy**: Q-learning, policy gradients, and the
  deterministic and interpolating methods between them. If you understood ch8, section 1
  is already organized in your head.
- **Section 12 is the one people skip and shouldn't.** "Reproducibility, Analysis, and
  Critique" is where ch10's rigor standards come from, and where you learn that published
  gains sometimes do not survive re-examination — the Tucker et al entry in section 1e is a
  worked example: it critiques and re-evaluates claims from earlier papers (including Q-Prop
  and Stein control variates) and finds important methodological errors in them.
- **A reading list is a topic-awareness tool.** The list explicitly does not claim
  completeness; its job is to prevent you from picking a research problem while unaware that
  a whole subfield already works on it.

## Anti-patterns
- **Reading it front to back.** It is far from comprehensive and is not a curriculum; the
  intended use is targeted depth after topic selection.
- **Treating an entry as endorsement of the result.** Several entries exist precisely because
  they critique other entries.
- **Skipping the related-work walk.** The list is the entry point; the citations are the
  actual literature review.

## Key Takeaways
1. 13 topic sections; section 1 (Model-Free RL) alone has eight subsections and mirrors ch8.
2. Every entry is annotated with the algorithm it introduced or the contribution it made.
3. The list is a topic map for choosing a research direction, not a reading queue.
4. Sections 7-13 (meta-RL, scaling, real world, safety, imitation/IRL, critique, classics)
   are where the topics ch10 suggests for project ideas actually live.

## Connects To
- **Ch 8**: the taxonomy that section 1's structure reproduces.
- **Ch 10**: "start by exploring the literature to become aware of topics in the field" —
  this chapter is that step's tool.
- **Ch 14-19**: every implemented algorithm's own "Why These Papers?" section is a
  three-paper version of this list, scoped to one algorithm.
