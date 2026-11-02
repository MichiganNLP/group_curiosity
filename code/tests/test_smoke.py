from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, os.fspath(ROOT / "src"))

from curioustogether.backends import DryRunBackend
from curioustogether.experiment import curiosity_for, run_record
from curioustogether.tasks import TASKS


class ExperimentSmokeTest(unittest.TestCase):
    def test_all_task_adapters_build_three_turns(self) -> None:
        examples = {
            "story": {"id": "s", "title": "A lighthouse"},
            "hypothesis": {"id": "h", "context": "A measured effect changes."},
            "codenames": {"id": "c", "clue": "bank", "board": ["river", "money"]},
            "csqa": {"id": "q", "question": "Where?", "choices": ["A", "B"]},
            "strategyqa": {"id": "sq", "question": "Is it possible?"},
            "novel-concepts": {"id": "n", "links": ["fire", "rust"]},
            "bias": {"id": "b", "scenario": "Assign two tasks fairly."},
            "ethics": {"id": "e", "scenario": "Someone takes a shared item."},
        }
        self.assertEqual(set(examples), set(TASKS))
        for task, record in examples.items():
            with self.subTest(task=task):
                result = run_record(
                    record,
                    task_name=task,
                    backend=DryRunBackend(),
                    agents=3,
                    curiosity="one",
                    culture=True,
                )
                self.assertEqual(len(result["trace"]), 3)
                self.assertTrue(result["trace"][0]["curious"])
                self.assertFalse(result["trace"][1]["curious"])
                self.assertIsNotNone(result["final_output"])

    def test_curiosity_allocation(self) -> None:
        self.assertEqual([curiosity_for(i, "all") for i in range(3)], [True, True, True])
        self.assertEqual([curiosity_for(i, "one") for i in range(3)], [True, False, False])
        self.assertEqual([curiosity_for(i, "none") for i in range(3)], [False, False, False])


if __name__ == "__main__":
    unittest.main()
