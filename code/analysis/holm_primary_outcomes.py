#!/usr/bin/env python3
"""Apply Holm correction to the eight primary comparisons in Appendix D.1.

The input values are transcribed from Table 2 and Appendix D.1 of the current
manuscript. Entries reported as p < x are conservatively represented by x, so
their adjusted values are upper bounds rather than exact adjusted p-values.
"""

import csv
from pathlib import Path


OUT_DIR = Path(__file__).resolve().parent

ROWS = [
    {
        "task": "Story",
        "metric": "Novelty",
        "curiosity": 0.647,
        "no_curiosity": 0.600,
        "effect": 0.047,
        "effect_unit": "raw difference",
        "p": 0.030,
        "p_is_upper_bound": False,
    },
    {
        "task": "Hypothesis",
        "metric": "IA score",
        "curiosity": 0.595,
        "no_curiosity": 0.542,
        "effect": 0.053,
        "effect_unit": "raw difference",
        "p": 1e-7,
        "p_is_upper_bound": True,
    },
    {
        "task": "Codenames",
        "metric": "ROUGE-L",
        "curiosity": 0.261,
        "no_curiosity": 0.177,
        "effect": 0.084,
        "effect_unit": "raw difference",
        "p": 0.001,
        "p_is_upper_bound": True,
    },
    {
        "task": "CSQA",
        "metric": "Accuracy",
        "curiosity": 73.77,
        "no_curiosity": 72.81,
        "effect": 0.96,
        "effect_unit": "percentage points",
        "p": 0.063,
        "p_is_upper_bound": False,
    },
    {
        "task": "StrategyQA",
        "metric": "Accuracy",
        "curiosity": 69.56,
        "no_curiosity": 70.33,
        "effect": -0.77,
        "effect_unit": "percentage points",
        "p": 0.071,
        "p_is_upper_bound": False,
    },
    {
        "task": "Novel Concepts",
        "metric": "Accuracy",
        "curiosity": 34.33,
        "no_curiosity": 30.21,
        "effect": 4.12,
        "effect_unit": "percentage points",
        "p": 0.049,
        "p_is_upper_bound": False,
    },
    {
        "task": "Bias scenarios",
        "metric": "1 - stereotype rate",
        "curiosity": 75.36,
        "no_curiosity": 60.46,
        "effect": 14.90,
        "effect_unit": "percentage points",
        "p": 1e-6,
        "p_is_upper_bound": True,
    },
    {
        "task": "ETHICS",
        "metric": "Accuracy",
        "curiosity": 49.39,
        "no_curiosity": 48.97,
        "effect": 0.42,
        "effect_unit": "percentage points",
        "p": 0.085,
        "p_is_upper_bound": False,
    },
]


def holm_adjust(rows):
    ordered = sorted(enumerate(rows), key=lambda item: item[1]["p"])
    running_max = 0.0
    adjusted = [None] * len(rows)
    total = len(rows)
    for rank, (original_index, row) in enumerate(ordered):
        candidate = min(1.0, (total - rank) * row["p"])
        running_max = max(running_max, candidate)
        adjusted[original_index] = running_max
    return adjusted


def p_text(value, upper_bound=False):
    prefix = "<" if upper_bound else ""
    if value < 0.001:
        return f"{prefix}{value:.1e}"
    return f"{prefix}{value:.3f}"


def p_text_tex(value, upper_bound=False):
    relation = "<" if upper_bound else "="
    if value < 0.001:
        coefficient, exponent = f"{value:.1e}".split("e")
        return rf"${relation}{coefficient}\times10^{{{int(exponent)}}}$"
    return rf"${relation}{value:.3f}$"


def main():
    adjusted = holm_adjust(ROWS)
    output_rows = []
    for row, adjusted_p in zip(ROWS, adjusted):
        result = dict(row)
        result["holm_p"] = adjusted_p
        result["holm_significant_0.05"] = adjusted_p < 0.05
        output_rows.append(result)

    csv_path = OUT_DIR / "holm_primary_outcomes.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=output_rows[0].keys())
        writer.writeheader()
        writer.writerows(output_rows)

    md_lines = [
        "| Task | Primary metric | Curiosity | No curiosity | Effect | Raw p | Holm p | Reliable after Holm? |",
        "|---|---|---:|---:|---:|---:|---:|:---:|",
    ]
    tex_lines = []
    for row in output_rows:
        effect = f"{row['effect']:+.3f}" if row["effect_unit"] == "raw difference" else f"{row['effect']:+.2f} pp"
        raw_p = p_text(row["p"], row["p_is_upper_bound"])
        holm_p = p_text(row["holm_p"], row["p_is_upper_bound"])
        raw_p_tex = p_text_tex(row["p"], row["p_is_upper_bound"])
        holm_p_tex = p_text_tex(row["holm_p"], row["p_is_upper_bound"])
        reliable = "Yes" if row["holm_significant_0.05"] else "No"
        md_lines.append(
            f"| {row['task']} | {row['metric']} | {row['curiosity']:.3f} | "
            f"{row['no_curiosity']:.3f} | {effect} | {raw_p} | {holm_p} | {reliable} |"
        )
        tex_lines.append(
            f"{row['task']} & {row['metric']} & {row['curiosity']:.3f} & "
            f"{row['no_curiosity']:.3f} & {effect} & {raw_p_tex} & "
            f"{holm_p_tex} & {reliable} \\\\"
        )

    note = (
        "\n\nValues are from Table 2 and Appendix D.1. Holm correction is across "
        "the eight task-level primary comparisons. For entries originally reported "
        "as p < x, x is used conservatively, so the corresponding adjusted p-value "
        "is an upper bound. These tests do not estimate run-to-run seed variance.\n"
    )
    (OUT_DIR / "holm_primary_outcomes.md").write_text(
        "\n".join(md_lines) + note, encoding="utf-8"
    )
    (OUT_DIR / "holm_primary_outcomes_rows.tex").write_text(
        "\n".join(tex_lines) + "\n", encoding="utf-8"
    )
    table = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\small",
        r"\setlength{\tabcolsep}{4pt}",
        r"\begin{tabular}{llrrrrrc}",
        r"\toprule",
        r"Task & Primary metric & Curious & No-curious & $\Delta$ & $p$ & $p_{\mathrm{Holm}}$ & Reliable? \\",
        r"\midrule",
        *tex_lines,
        r"\bottomrule",
        r"\end{tabular}",
        r"\caption{Curiosity versus no-curiosity for one primary outcome per task. "
        r"Effects are raw differences; accuracy effects are percentage-point differences. "
        r"Holm correction is applied across the eight task-level comparisons. Values "
        r"reported as inequalities use the manuscript's conservative upper bound.}",
        r"\label{tab:holm-primary}",
        r"\end{table*}",
    ]
    (OUT_DIR / "holm_primary_outcomes_table.tex").write_text(
        "\n".join(table) + "\n", encoding="utf-8"
    )

    print("\n".join(md_lines))
    print(note.strip())


if __name__ == "__main__":
    main()
