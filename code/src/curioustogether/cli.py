from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from .backends import DryRunBackend, TransformersBackend
from .experiment import run_dataset
from .tasks import TASKS


def load_records(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".jsonl":
        with path.open(encoding="utf-8") as handle:
            return [json.loads(line) for line in handle if line.strip()]
    if suffix == ".json":
        with path.open(encoding="utf-8") as handle:
            value = json.load(handle)
        return value if isinstance(value, list) else value.get("records", [value])
    if suffix == ".csv":
        with path.open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))
    raise ValueError("Input must use .jsonl, .json, or .csv")


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a multi-agent curiosity condition")
    parser.add_argument("--task", choices=sorted(TASKS), required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--agents", type=int, default=3)
    parser.add_argument("--curiosity", choices=("all", "one", "none"), default="one")
    parser.add_argument("--culture", action="store_true")
    parser.add_argument("--backend", choices=("dry-run", "transformers"), default="dry-run")
    parser.add_argument("--model")
    parser.add_argument("--max-new-tokens", type=int, default=192)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--device-map", default="auto")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.backend == "transformers":
        if not args.model:
            raise SystemExit("--model is required with --backend transformers")
        backend = TransformersBackend(
            model_name=args.model,
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
            seed=args.seed,
            device_map=args.device_map,
        )
    else:
        backend = DryRunBackend()

    records = load_records(args.input)
    outputs = run_dataset(
        records,
        task_name=args.task,
        backend=backend,
        agents=args.agents,
        curiosity=args.curiosity,
        culture=args.culture,
    )
    write_jsonl(args.output, outputs)
    print(f"Wrote {len(outputs)} records to {args.output}")


if __name__ == "__main__":
    main()
