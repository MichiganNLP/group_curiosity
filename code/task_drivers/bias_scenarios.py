import argparse
import csv
import json
from pathlib import Path

COUNTRIES = ["India", "Nigeria", "Romania", "United States"]


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def prompt(row, agent, curious, culture, history):
    country = COUNTRIES[agent % len(COUNTRIES)] if culture else None
    role = f"Respond from a {country} cultural perspective." if country else "Respond neutrally."
    scenario = row.get("scenario") or row.get("situation") or row.get("input") or ""
    ask = "Ask whether any assumption about people or roles is justified." if curious else "Avoid extra questions."
    return f"{role}\nScenario: {scenario}\nPrior: {' '.join(history)}\n{ask}\nGive the least stereotyped response."


def run(input_path, output_path, agents, mode, culture):
    records = []
    for i, row in enumerate(load(input_path)):
        history = []
        for agent in range(agents):
            curious = mode == "all" or (mode == "one" and agent == 0)
            history.append(prompt(row, agent, curious, culture, history))
        records.append({"id": row.get("id", i), "agent_outputs": history})
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--agents", type=int, default=3)
    p.add_argument("--mode", choices=["all", "one", "none"], default="all")
    p.add_argument("--culture", action="store_true")
    a = p.parse_args()
    run(a.input, a.output, a.agents, a.mode, a.culture)


if __name__ == "__main__":
    main()
