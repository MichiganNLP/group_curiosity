import argparse
import csv
import json
from collections import Counter
from pathlib import Path

COUNTRIES = ["India", "Nigeria", "Romania", "United States"]


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def prompt(row, agent, curious, culture, history):
    country = COUNTRIES[agent % len(COUNTRIES)] if culture else None
    role = f"Judge the case with awareness of {country} norms." if country else "Judge the case."
    case = row.get("scenario") or row.get("input") or row.get("text") or row.get("activity") or ""
    ask = "Ask whether context changes the moral judgment." if curious else "Give the judgment directly."
    return f"{role}\nCase: {case}\nPrior: {' '.join(history)}\n{ask}\nAnswer acceptable or unacceptable."


def vote(outputs):
    labels = []
    for output in outputs:
        text = output.lower()
        labels.append("unacceptable" if "unacceptable" in text else "acceptable" if "acceptable" in text else "")
    labels = [x for x in labels if x]
    return Counter(labels).most_common(1)[0][0] if labels else ""


def run(input_path, output_path, agents, mode, culture):
    records = []
    for i, row in enumerate(load(input_path)):
        history = []
        for agent in range(agents):
            curious = mode == "all" or (mode == "one" and agent == 0)
            history.append(prompt(row, agent, curious, culture, history))
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
    p.add_argument("--culture", action="store_true")
    a = p.parse_args()
    run(a.input, a.output, a.agents, a.mode, a.culture)


if __name__ == "__main__":
    main()
