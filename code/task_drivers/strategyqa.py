import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def load(path):
    if path.endswith(".jsonl"):
        with open(path, encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def prompt(row, agent, curious, history):
    question = row.get("question") or row.get("input") or ""
    ask = "Ask one missing-fact question before deciding yes or no." if curious else "Decide yes or no directly."
    return f"Question: {question}\nPrior: {' '.join(history)}\n{ask}"


def vote(outputs):
    labels = []
    for output in outputs:
        text = output.lower()
        labels.append("yes" if " yes" in f" {text}" else "no" if " no" in f" {text}" else "")
    labels = [x for x in labels if x]
    return Counter(labels).most_common(1)[0][0] if labels else ""


def run(input_path, output_path, agents, mode):
    records = []
    for i, row in enumerate(load(input_path)):
        history = []
        for agent in range(agents):
            curious = mode == "all" or (mode == "one" and agent == 0)
            history.append(prompt(row, agent, curious, history))
        records.append({"id": row.get("id", i), "prediction": vote(history), "agent_outputs": history})
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--agents", type=int, default=3)
    p.add_argument("--mode", choices=["all", "one", "none"], default="one")
    a = p.parse_args()
    run(a.input, a.output, a.agents, a.mode)


if __name__ == "__main__":
    main()
