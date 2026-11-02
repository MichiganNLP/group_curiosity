# Data and results release

This folder contains compact, GitHub-safe result summaries from the CuriousTogether experiments:

- `results/main_table.csv`: aggregate values from the main results table;
- `results/holm_primary_outcomes.csv`: Holm-corrected primary-outcome tests;
- `results/matched_prompt_summary.csv`: matched-prompt control summary;
- `results/ensemble_baseline_summary.csv`: non-interacting ensemble baseline summary.

Synthetic task inputs are stored under `../code/examples/` so every adapter can be tested without redistributing benchmark records.

The working research directory contains approximately 3.6 GB of generated outputs plus 79 MB of evaluation data. Those files are deliberately not copied wholesale into this GitHub release because of repository size limits, benchmark redistribution requirements, caches, model artifacts, and legacy machine paths. Full outputs should be hosted as a versioned archive after a separate licensing and privacy review.
