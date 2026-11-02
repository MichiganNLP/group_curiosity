# CuriousTogether

**CuriousTogether** studies how curiosity changes collaboration among language-model agents. Instead of treating curiosity as a human-like internal trait, we operationalize it as an interaction mechanism: selected agents are instructed to ask questions, probe missing information, challenge assumptions, and consider other perspectives before the group produces an answer.

The project examines two related design choices:

1. **Who should be curious?** We compare groups in which all agents, one agent, or no agents are prompted to ask curiosity-driven questions.
2. **When does cultural grounding help?** We compare agents with and without country-conditioned context to test when heterogeneous starting perspectives improve collective outcomes.

## Research framework

We organize group curiosity into three functional dimensions and evaluate eight tasks:

| Dimension | Role in interaction | Tasks |
| --- | --- | --- |
| **Novelty-seeking** | Opens unexpected directions and encourages exploration | Story Generation, Hypothesis Generation, Codenames |
| **Epistemic** | Identifies missing knowledge and asks clarifying questions | CommonsenseQA, StrategyQA, Novel Concepts |
| **Social** | Probes assumptions and invites perspective-taking | Implicit Bias Scenarios, ETHICS |

For each task instance, three agents contribute sequentially through a shared interaction history. Depending on the experimental condition, an agent may ask a task-specific question before responding. The final output is produced through task-appropriate aggregation, such as majority vote, concatenation, or synthesis.

The study evaluates six publicly available instruction-tuned model families across curiosity and cultural-grounding conditions. The main findings are:

- curiosity-guided multi-agent settings improve over non-curious settings on **seven of eight tasks**;
- story-generation semantic diversity improves by up to **20.6%**;
- the anti-stereotype score improves by **14.9 percentage points**;
- all-curious groups work best for several divergent creative and social tasks;
- one-curious groups often provide a better coordination–exploration balance for convergent tasks;
- cultural grounding is most helpful when a task rewards diverse perspectives, but can hurt narrow precision-oriented reasoning;
- token efficiency remains task-dependent: multi-agent curiosity is most compelling when its quality gains outweigh interaction overhead.

These results suggest that curiosity should be allocated according to task structure—not added indiscriminately to every agent or every round.

## Repository contents

```text
.
├── src/curioustogether/     # task adapters, backends, runner, and CLI
├── data/
│   ├── examples/            # synthetic examples for all eight task schemas
│   └── results/             # aggregate main-table values
├── docs/                    # experiment design and interface documentation
├── tests/                   # smoke tests covering every task adapter
├── scripts/                 # anonymization and path scanner
└── website/                 # placeholder for the static project page
```

This is a compact, portable release. It does not include several gigabytes of generated outputs, model weights, or third-party benchmark files. See [data/README.md](data/README.md) for the data-release scope and [docs/EXPERIMENTS.md](docs/EXPERIMENTS.md) for the complete interface description.

## Installation

Python 3.10 or newer is recommended.

The dry-run backend uses only the Python standard library:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

To run a local Hugging Face model, install the optional model dependencies:

```bash
pip install -e '.[models]'
```

## Quick start

First, verify the installation:

```bash
python3 -m unittest discover -s tests -v
```

Then run a deterministic dry test. This validates data loading, prompt construction, curiosity allocation, interaction history, aggregation, and JSONL output without downloading model weights:

```bash
curioustogether \
  --task strategyqa \
  --input data/examples/strategyqa.jsonl \
  --output outputs/strategyqa.jsonl \
  --backend dry-run \
  --curiosity one
```

The same command can be run without installing the package:

```bash
PYTHONPATH=src python3 -m curioustogether.cli \
  --task strategyqa \
  --input data/examples/strategyqa.jsonl \
  --output outputs/strategyqa.jsonl \
  --backend dry-run \
  --curiosity one
```

## Run with a local language model

```bash
curioustogether \
  --task strategyqa \
  --input data/examples/strategyqa.jsonl \
  --output outputs/strategyqa_qwen.jsonl \
  --backend transformers \
  --model Qwen/Qwen2.5-7B-Instruct \
  --curiosity one \
  --agents 3 \
  --max-new-tokens 160 \
  --temperature 0.7 \
  --seed 0
```

Add `--culture` to enable country-conditioned context:

```bash
curioustogether \
  --task story \
  --input data/examples/story.jsonl \
  --output outputs/story_all_curious_culture.jsonl \
  --backend transformers \
  --model Qwen/Qwen2.5-7B-Instruct \
  --curiosity all \
  --culture
```

## Core options

| Option | Values | Purpose |
| --- | --- | --- |
| `--task` | `story`, `hypothesis`, `codenames`, `csqa`, `strategyqa`, `novel-concepts`, `bias`, `ethics` | Selects the task adapter and aggregation rule |
| `--curiosity` | `all`, `one`, `none` | Chooses which agents receive curiosity instructions |
| `--culture` | flag | Adds country-conditioned context to agent prompts |
| `--agents` | integer, default `3` | Sets the number of sequential agents |
| `--backend` | `dry-run`, `transformers` | Selects deterministic validation or local generation |
| `--model` | Hugging Face model ID | Required for the Transformers backend |
| `--max-new-tokens` | integer, default `192` | Limits each generated response |
| `--temperature` | float, default `0.7` | Controls sampling diversity |
| `--seed` | integer, default `0` | Sets the PyTorch random seed |

Input files may be JSONL, JSON, or CSV. The runner writes JSONL records containing the experimental condition, final output, and a full per-agent trace of prompts and responses. Exact schemas and aggregation behavior are documented in [docs/EXPERIMENTS.md](docs/EXPERIMENTS.md).

## Adding the project website

Place the static project-page files inside `website/`. The code and website can then live in the same GitHub repository while remaining cleanly separated.

## Anonymization check

Before uploading code or data, run:

```bash
python3 scripts/check_anonymity.py src
python3 scripts/check_anonymity.py data
```

The scanner checks for email addresses, absolute user or cluster paths, scheduler accounts, and ORCID-like identifiers. It is a conservative automated check and does not replace a manual review.

## Citation

Citation metadata can be added after the anonymous review period. The non-anonymous project website may include the complete paper citation separately.
