import argparse
import csv
import json
from pathlib import Path

COUNTRIES = ["India", "Nigeria", "Romania", "United States"]


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def prompt(row, agent, curious, culture, history):
    country = COUNTRIES[agent % len(COUNTRIES)] if culture else None
    role = f"You are a writer from {country}." if country else "You are a writer."
    ask = "End with one question for the next writer." if curious else "Do not ask questions."
    title = row.get("title") or row.get("prompt") or row.get("story_title") or ""
    text = "\n".join(history)
    return f"{role}\nTitle: {title}\nPrior text:\n{text}\nWrite the next story segment. {ask}"


def make(input_path, output_path, agents, mode, culture):
    out = []
    for i, row in enumerate(rows(input_path)):
        history = []
        for agent in range(agents):
            curious = mode == "all" or (mode == "one" and agent == 0)
            history.append(prompt(row, agent, curious, culture, history))
        out.append({"id": row.get("id", i), "story": "\n\n".join(history)})
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--agents", type=int, default=3)
    p.add_argument("--mode", choices=["all", "one", "none"], default="all")
    p.add_argument("--culture", action="store_true")
    a = p.parse_args()
    make(a.input, a.output, a.agents, a.mode, a.culture)


if __name__ == "__main__":
    main()
