# Code release

This folder contains the cleaned, portable multi-agent curiosity implementation.

- `task_drivers/` preserves the eight clean task scripts from the research working directory.
- `src/curioustogether/` provides a consistent command-line interface and optional local Transformers backend.
- `analysis/` contains the statistical-robustness analysis used for the released summary table.

## Quick start

Use Python 3.10 or newer from the repository root:

```bash
python3 -m unittest discover -s code/tests -v

PYTHONPATH=code/src python3 -m curioustogether.cli \
  --task strategyqa \
  --input code/examples/strategyqa.jsonl \
  --output outputs/strategyqa.jsonl \
  --backend dry-run \
  --curiosity one
```

For a real local model:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e 'code[models]'

curioustogether \
  --task strategyqa \
  --input code/examples/strategyqa.jsonl \
  --output outputs/strategyqa.jsonl \
  --backend transformers \
  --model Qwen/Qwen2.5-7B-Instruct \
  --curiosity one
```

The eight supported task identifiers are `story`, `hypothesis`, `codenames`, `csqa`, `strategyqa`, `novel-concepts`, `bias`, and `ethics`. Every run supports `all`, `one`, or `none` curiosity allocation and optional `--culture` prompting.

Toy examples validate the schemas and pipeline; they are not replacements for the licensed benchmarks. See `../data/README.md` for release scope.
