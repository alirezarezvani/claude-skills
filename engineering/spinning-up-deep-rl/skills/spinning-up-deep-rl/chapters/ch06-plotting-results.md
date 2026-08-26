# Chapter 6: Plotting Results

## Core Idea
The plotter reads a directory prefix, autocompletes every matching run beneath it, averages
across seeds by default, and resolves the pseudo-metric `Performance` to the *correct*
performance measure for each algorithm family — so a fair on-policy versus off-policy
comparison is one command.

## Frameworks Introduced
- **`Performance` as a family-aware alias**: `Performance` is not a real output of any
  algorithm. The plotter resolves it per logdir to `AverageEpRet` for on-policy algorithms
  and `AverageTestEpRet` for off-policy ones.
  - When to use: always, unless you specifically want one raw column. It is the default `-y`.
  - Why it matters: on-policy performance is the average return of the batch just collected;
    off-policy performance is measured by separate deterministic test rollouts. Plotting the
    same raw column for both would compare two different quantities.

- **Prefix autocompletion**: logdirs are searched recursively and prefixes expand. Give the
  plotter `data/bench_algo` and it finds `bench_algo1` and `bench_algo2` with all their seeds.
  - How: name experiments with a shared prefix at launch and comparison becomes free.

- **Average by default, `--count` to disaggregate**: by default, y-values are averaged across
  all results sharing an `exp_name` — typically identical experiments differing only in seed.
  `--count` shows each curve separately.

## Key Concepts
- **`--xaxis` / `-x`**: which column is the x-axis. Default `TotalEnvInteracts`, i.e. sample
  efficiency is the default framing, not wall-clock or epochs.
- **`--value` / `-y`**: which columns to graph; multiple values produce multiple graphs.
- **`--smooth S`**: average over a fixed window of width S. The book's own benchmark plots
  use a window of 11 epochs (ch13).
- **`--legend` / `-l`**: overrides the automatic legend, which uses `exp_name` from
  `config.json`. One string per *matched* directory, which may exceed the number of logdir
  arguments you passed.
- **`--select` / `--exclude`**: keep or drop curves whose logdir contains all of / any of
  these substrings. The way to narrow an over-eager autocomplete.

## Code Examples
```bash
python -m spinup.run plot [path/to/output_directory ...] [--legend [LEGEND ...]] \
    [--xaxis XAXIS] [--value [VALUE ...]] [--count] [--smooth S] \
    [--select [SEL ...]] [--exclude [EXC ...]]
```

Comparing two algorithms across all their seeds, relying on autocompletion:

```
data/
    bench_algo1/
        bench_algo1-seed0/
        bench_algo1-seed10/
    bench_algo2/
        bench_algo2-seed0/
        bench_algo2-seed10/
```

```bash
python spinup/utils/plot.py data/bench_algo
```

## Anti-patterns
- **Passing one legend string per logdir argument.** Autocompletion may match several
  directories per argument; you need one legend entry per match, unless you narrowed the
  set with `--select` / `--exclude`.
- **Plotting `AverageEpRet` for an off-policy algorithm** and calling it performance — that
  is the behavior policy with exploration noise, not the evaluated policy. Use `Performance`.
- **Heavy smoothing to make a result look clean.** Smoothing is a display parameter; it does
  not change what the seeds did, and ch10 asks you to show seed variance rather than hide it.

## Key Takeaways
1. `Performance` is the correct default because it is algorithm-family aware.
2. Prefix autocompletion plus shared `exp_name` prefixes is the intended comparison workflow.
3. Seed averaging is on by default; `--count` reveals the individual curves that average hides.
4. The default x-axis is environment interactions — sample efficiency is the default question.

## Connects To
- **Ch 5**: `progress.txt`, the plotter's input.
- **Ch 4**: the suffix rules that group seeds into one folder for averaging.
- **Ch 13**: the benchmark plots, produced with 10 seeds and an 11-epoch smoothing window.
