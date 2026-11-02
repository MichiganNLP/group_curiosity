from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from typing import Any, Iterable

from .backends import GenerationBackend
from .tasks import COUNTRIES, TASKS, Record, extract_answer


@dataclass
class AgentTurn:
    agent: int
    curious: bool
    country: str | None
    prompt: str
    response: str


def curiosity_for(agent_index: int, mode: str) -> bool:
    if mode == "all":
        return True
    if mode == "one":
        return agent_index == 0
    if mode == "none":
        return False
    raise ValueError(f"Unknown curiosity mode: {mode}")


def aggregate(responses: list[str], strategy: str, backend: GenerationBackend) -> Any:
    if strategy == "concatenate":
        return "\n\n".join(responses)
    if strategy == "individual":
        return responses
    if strategy == "synthesize":
        joined = "\n\n".join(f"Candidate {i + 1}: {text}" for i, text in enumerate(responses))
        return backend.generate(
            "Synthesize the candidate hypotheses into one concise, testable final hypothesis.\n"
            + joined
        )
    answers = [extract_answer(response) for response in responses]
    answers = [answer for answer in answers if answer]
    return Counter(answers).most_common(1)[0][0] if answers else ""


def run_record(
    record: Record,
    task_name: str,
    backend: GenerationBackend,
    agents: int = 3,
    curiosity: str = "one",
    culture: bool = False,
) -> dict[str, Any]:
    if task_name not in TASKS:
        raise KeyError(f"Unknown task: {task_name}")
    if agents < 1:
        raise ValueError("agents must be at least 1")

    adapter = TASKS[task_name]
    turns: list[AgentTurn] = []
    history: list[str] = []
    for agent_index in range(agents):
        is_curious = curiosity_for(agent_index, curiosity)
        country = COUNTRIES[agent_index % len(COUNTRIES)] if culture else None
        prompt = adapter.build_prompt(record, is_curious, country, history)
        response = backend.generate(prompt)
        turns.append(AgentTurn(agent_index + 1, is_curious, country, prompt, response))
        history.append(response)

    return {
        "id": record.get("id"),
        "task": task_name,
        "dimension": adapter.dimension,
        "curiosity": curiosity,
        "culture": culture,
        "agents": agents,
        "final_output": aggregate(history, adapter.aggregate, backend),
        "trace": [asdict(turn) for turn in turns],
    }


def run_dataset(
    records: Iterable[Record],
    task_name: str,
    backend: GenerationBackend,
    agents: int = 3,
    curiosity: str = "one",
    culture: bool = False,
) -> list[dict[str, Any]]:
    return [
        run_record(record, task_name, backend, agents, curiosity, culture)
        for record in records
    ]
