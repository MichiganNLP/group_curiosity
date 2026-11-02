import argparse
import csv
import json
from pathlib import Path

COUNTRIES = ["India", "Nigeria", "Romania", "United States"]


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def agent_prompt(row, agent, curious, culture, history):
    country = COUNTRIES[agent % len(COUNTRIES)] if culture else None
    role = f"Scientist grounded in {country}." if country else "Scientist."
    question = "Ask one evidence-seeking question before proposing a hypothesis." if curious else "Propose directly."
    context = row.get("context") or row.get("input") or row.get("premise") or row.get("problem") or ""
    return f"{role}\nProblem: {context}\nDiscussion: {' '.join(history)}\n{question}\nReturn one testable hypothesis."


def summarizer(history):
    return "Synthesize these hypotheses into one concise final hypothesis:\n" + "\n".join(history)


def run(input_path, output_path, agents, mode, culture):
    records = []
    for i, row in enumerate(load(input_path)):
        history = []
        for agent in range(agents):
            curious = mode == "all" or (mode == "one" and agent == 0)
            history.append(agent_prompt(row, agent, curious, culture, history))
        records.append({"id": row.get("id", i), "final_prompt": summarizer(history)})
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
