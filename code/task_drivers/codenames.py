import argparse
import json
from collections import Counter
from pathlib import Path


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def prompt(item, agent, curious, history):
    clue = item.get("clue", "")
    board = ", ".join(item.get("board", item.get("words", [])))
    ask = "Ask whether another meaning of the clue is useful." if curious else "Do not ask a question."
    return f"Clue: {clue}\nBoard: {board}\nPrior: {' '.join(history)}\nChoose target words. {ask}"


def vote(outputs):
    words = []
    for output in outputs:
        words.extend([w.strip().lower() for w in output.replace("\n", ",").split(",") if w.strip()])
    return [w for w, _ in Counter(words).most_common(4)]


def run(input_path, output_path, agents, mode):
    results = []
    for i, item in enumerate(load(input_path)):
        history = []
        for agent in range(agents):
            curious = mode == "all" or (mode == "one" and agent == 0)
            history.append(prompt(item, agent, curious, history))
        results.append({"id": item.get("id", i), "prediction": vote(history), "agent_outputs": history})
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)


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
