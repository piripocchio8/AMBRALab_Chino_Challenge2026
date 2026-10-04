#!/usr/bin/env python3
"""Build a ranked submission CSV for one size band of the challenge.

The script reads a JSON file of candidate records and writes a CSV whose rows are
ordered best-first, because the challenge reads the ranking from the top row down.

Usage
-----
    python3 scripts/make_submission_csv.py --input Target_1/micro/example_candidates.json

    python3 scripts/make_submission_csv.py \
        --input  Target_1/micro/candidates.json \
        --output Target_1/micro/submission_micro.csv \
        --limit  8

Input format
------------
Either a JSON list of record objects, or a JSON object with a "candidates" key
holding that list:

    [{"name": "...", "sequence": "...", "rank": 1, ...}, ...]
    {"candidates": [{...}, ...]}

Each record needs at least "name" and "sequence". Everything else is optional and
is written only if at least one record supplies it; see OPTIONAL_COLUMNS for the
recognised keys and the order they are written in. Unrecognised keys are ignored,
so a record may carry internal bookkeeping without it reaching the CSV.

"molecule_class" is always written as the literal "protein" and is not taken from
the input.

Output format
-------------
The three required columns come first and in this order:

    name, sequence, molecule_class

followed by whichever of the optional metric columns the input supplies, in the
fixed order given by OPTIONAL_COLUMNS. A record missing a column that another
record supplies is written with an empty field.

Refusals
--------
The script validates every record before it writes anything, so a rejected input
never leaves a partial CSV behind. It refuses to write:

  * a record whose "sequence" contains anything other than the 20 standard
    one-letter amino acid codes. Non-canonical chemistry cannot be expressed in a
    one-letter submission sequence, and silently passing it through would submit a
    molecule different from the one that was designed. Lower-case letters, gaps,
    whitespace, "X", and chemical-component blocks such as "(MEN)" are all refused.
  * a record with a missing or empty "name" or "sequence".
  * more candidates than the band allows. The challenge permits 8 designs in the
    micro band, which is the default for --limit.

Standard library only; no third-party dependencies.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

#: The 20 standard amino acids, one-letter. The only alphabet a submission
#: sequence may use.
STANDARD_AA = frozenset("ACDEFGHIKLMNPQRSTVWY")

#: Always written verbatim; never read from the input.
MOLECULE_CLASS = "protein"

#: Required, first, and in this order.
REQUIRED_COLUMNS = ("name", "sequence", "molecule_class")

#: Written after the required columns, in this order, and only when at least one
#: input record supplies the key.
OPTIONAL_COLUMNS = (
    "rank",
    "binder_length",
    "interface_iptm",
    "ipsae",
    "binder_ptm",
    "plddt_binder",
    "shape_complementarity",
    "buried_surface_area_A2",
    "interface_contacts",
    "his_hbond_count",
    "his_hbond_bidentate",
    "nd1_donor",
    "nd1_distance_A",
    "nd1_angle_deg",
    "ne2_donor",
    "ne2_distance_A",
    "ne2_angle_deg",
    "design_strategy",
    "validation_protocol",
    "notes",
)

#: Default band and output, matching the challenge's micro band.
DEFAULT_LIMIT = 8
DEFAULT_OUTPUT = Path("Target_1/micro/submission_micro.csv")


class SubmissionError(Exception):
    """A refusal: the input is not something we are willing to submit."""


def load_records(path: Path) -> list[dict]:
    """Read the candidate records from a JSON file.

    Accepts a bare list of records or an object with a "candidates" key.
    """
    try:
        with path.open(encoding="utf-8") as handle:
            payload = json.load(handle)
    except FileNotFoundError:
        raise SubmissionError(f"input file not found: {path}") from None
    except json.JSONDecodeError as exc:
        raise SubmissionError(f"{path} is not valid JSON: {exc}") from None

    if isinstance(payload, dict):
        if "candidates" not in payload:
            raise SubmissionError(
                f"{path}: a JSON object input must have a 'candidates' key "
                f"holding the list of records (found keys: "
                f"{', '.join(sorted(payload)) or 'none'})"
            )
        payload = payload["candidates"]

    if not isinstance(payload, list):
        raise SubmissionError(
            f"{path}: expected a list of candidate records, found "
            f"{type(payload).__name__}"
        )
    for index, record in enumerate(payload):
        if not isinstance(record, dict):
            raise SubmissionError(
                f"{path}: record {index} is {type(record).__name__}, "
                f"expected an object"
            )
    if not payload:
        raise SubmissionError(f"{path}: no candidate records")
    return payload


def validate_sequence(sequence: object, label: str) -> str:
    """Return the sequence, or raise if it is not 20-letter canonical protein."""
    if not isinstance(sequence, str) or not sequence:
        raise SubmissionError(f"{label}: missing or empty 'sequence'")
    bad = sorted({char for char in sequence if char not in STANDARD_AA})
    if bad:
        shown = ", ".join(repr(char) for char in bad)
        raise SubmissionError(
            f"{label}: sequence contains {len(bad)} character(s) that are not "
            f"one of the 20 standard amino acids: {shown}. A submission "
            f"sequence must be plain upper-case canonical protein, with no "
            f"gaps, whitespace, 'X', lower-case codes or chemical-component "
            f"blocks."
        )
    return sequence


def validate(records: list[dict], limit: int) -> list[dict]:
    """Validate every record and refuse the whole input if any is unacceptable."""
    if limit < 1:
        raise SubmissionError(f"--limit must be at least 1, got {limit}")
    if len(records) > limit:
        raise SubmissionError(
            f"{len(records)} candidate records, but this band allows at most "
            f"{limit}. Select the designs to submit before building the CSV, "
            f"or raise --limit if you are building a different band."
        )

    seen: set[str] = set()
    for index, record in enumerate(records):
        label = f"record {index}"
        name = record.get("name")
        if not isinstance(name, str) or not name.strip():
            raise SubmissionError(f"{label}: missing or empty 'name'")
        label = f"record {index} ({name})"
        if name in seen:
            raise SubmissionError(f"{label}: duplicate 'name'")
        seen.add(name)
        validate_sequence(record.get("sequence"), label)
    return records


def rank_key(record: dict, fallback: int) -> tuple[int, float, int]:
    """Sort key putting the best-ranked record first.

    Records carrying a numeric "rank" sort ahead of records without one, lowest
    rank first. Records without a rank keep their input order behind them.
    """
    raw = record.get("rank")
    try:
        return (0, float(raw), fallback)
    except (TypeError, ValueError):
        return (1, 0.0, fallback)


def order_records(records: list[dict]) -> list[dict]:
    """Return the records best-first, by their declared rank.

    The input index is carried into the sort key so that ties, and records with
    no rank at all, keep their original relative order.
    """
    indexed = sorted(
        enumerate(records), key=lambda pair: rank_key(pair[1], pair[0])
    )
    return [record for _, record in indexed]


def active_columns(records: list[dict]) -> list[str]:
    """Required columns, plus the optional ones some record actually supplies."""
    supplied = [
        column
        for column in OPTIONAL_COLUMNS
        if any(record.get(column) is not None for record in records)
    ]
    return list(REQUIRED_COLUMNS) + supplied


def cell(record: dict, column: str) -> str:
    """Render one field. 'molecule_class' is fixed; absent values are empty."""
    if column == "molecule_class":
        return MOLECULE_CLASS
    value = record.get(column)
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def write_csv(records: list[dict], output: Path) -> list[str]:
    """Write the ranked CSV and return the header that was written."""
    columns = active_columns(records)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        for record in records:
            writer.writerow([cell(record, column) for column in columns])
    return columns


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a ranked submission CSV for one size band from a JSON file "
            "of candidate records."
        )
    )
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="JSON file of candidate records (a list, or an object with a "
        "'candidates' key).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help=f"CSV to write. Default: {DEFAULT_OUTPUT} relative to the "
        f"repository root.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"Maximum number of designs this band accepts "
        f"(default: {DEFAULT_LIMIT}, the micro band's allowance).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output = args.output
    if output is None:
        output = Path(__file__).resolve().parent.parent / DEFAULT_OUTPUT

    try:
        records = order_records(validate(load_records(args.input), args.limit))
        columns = write_csv(records, output)
    except SubmissionError as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 1

    print(f"wrote {len(records)} row(s) to {output}")
    print(f"columns: {', '.join(columns)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
