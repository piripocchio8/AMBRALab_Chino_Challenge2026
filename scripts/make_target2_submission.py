#!/usr/bin/env python3
"""Build Target 2's submission CSV and its full metric table from a ranking file.

Adapted from ``scripts/make_submission_csv.py``, which builds one size band for
Target 1. The differences are deliberate and are listed under "What changed from
the Target 1 script" below; everything the Target 1 script refuses, this one
refuses too.

The script reads a JSON file of ranked candidate records and writes two files:

  * ``Target_2/submission.csv``   -- the file submitted to the challenge. Exactly
    the three columns the template defines, ``name,sequence,molecule_class``, and
    only the rows that are actually being submitted, ordered best-first because
    the challenge reads the ranking from the top row down.
  * ``Target_2/metrics_full.csv`` -- every row the ranking produced, submitted or
    not, with every metric the input supplies, keyed by the same ``name``.

Usage
-----
    python3 scripts/make_target2_submission.py \
        --input Target_2/docs/ranking.json \
        --limit <the number of designs this target accepts>

``--limit`` has **no default**. Target 1's script defaults to 8 because the micro
band's allowance is known; this target's allowance was not established when this
script was written, and a guessed default would silently truncate or silently
admit. Pass the number the competition states.

The band in this repository was built with ``--limit 20``. **20 is the size of
the band we deliver, not an allowance we verified**: the organisers' Target-2
count is still not established, and the limit was set to the band so that the
script would refuse a 21st row rather than silently admit one. If the stated
allowance turns out to be smaller, re-run with it -- the script refuses rather
than truncates, and the designs to drop are a decision for a person, because the
order inside this band is not supported by the data (``Target_2/README.md``).

Input format
------------
Either a JSON list of record objects, or a JSON object with a ``candidates`` key
holding that list:

    [{"name": "...", "sequence": "...", "submission_rank": 1, ...}, ...]
    {"candidates": [{...}, ...]}

Required of every record:

    name              the submitted identifier, non-empty and unique
    sequence          the binder sequence, upper-case, 20 standard amino acids

Required of every *submitted* record (``status`` absent or "submitted"):

    submission_rank   1 = the entry we would most like tested. The submitted rows
                      must carry exactly the ranks 1..n with no gaps and no ties.

Optional, written only if at least one record supplies it, in the fixed order
given by ``OPTIONAL_COLUMNS``. Those names and their meanings are
``Target_2/docs/metrics.md``; keep the two in step. Unrecognised keys are
ignored, so a record may carry internal bookkeeping without it reaching the CSV.

A record that documents a design which is **not** being submitted carries a
``status`` saying so in a sentence, and carries **no** ``submission_rank`` -- a
design has no rank in a submission it is not part of.

What changed from the Target 1 script
-------------------------------------
  * Two output files instead of one, because Target 2 follows Target 1's final
    shape (a three-column submission beside a full metric table) rather than the
    per-band CSV the Target 1 script was written for.
  * ``molecule_class`` is validated against the upload form's own enumeration and
    defaults to ``single_chain``. The Target 1 script writes the literal
    "protein"; the form enumerates ``single_chain, nanobody, scfv, fab_kappa,
    fab_lambda``, prose elsewhere on the site says "protein", and taking that
    prose over the form was an error already corrected once in this repository.
  * ``--limit`` is required rather than defaulted (see above).
  * Four further refusals, each for a mistake this repository has actually made:
    a pending-marker leaking into a deposited file, one sequence under two names,
    a declared length disagreeing with the sequence, and a declared cyclisation
    the sequence cannot form.

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
  * a duplicate "name", or the same sequence under two different names. A name
    that denotes two molecules, or a molecule that answers to two names, has
    already cost this submission real time.
  * any field whose text contains a pending marker. A marker that survives into a
    deposited file is indistinguishable from a result.
  * a ``molecule_class`` outside the upload form's list.
  * a submitted record with no rank, a non-submitted record with one, or a set of
    submitted ranks that is not exactly 1..n.
  * a ``binder_length`` that disagrees with the sequence, or a declared disulfide
    cyclisation whose sequence does not begin and end with cysteine.
  * more candidates than the band allows.

Standard library only; no third-party dependencies.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

#: The 20 standard amino acids, one-letter. The only alphabet a submission
#: sequence may use.
STANDARD_AA = frozenset("ACDEFGHIKLMNPQRSTVWY")

#: The values the upload form accepts. Prose elsewhere on the competition site
#: says "protein"; the form itself enumerates these, and the form wins.
MOLECULE_CLASSES = ("single_chain", "nanobody", "scfv", "fab_kappa", "fab_lambda")
DEFAULT_MOLECULE_CLASS = "single_chain"

#: A design is part of the submission unless its status says otherwise.
SUBMITTED = "submitted"

#: Markers left in the prose where a figure had not been measured yet. None of
#: them may reach a CSV. Matches "[[PENDING: ...]]" and a bare "PENDING".
PENDING_MARKER = re.compile(r"\[\[\s*PENDING|(?<![A-Za-z])PENDING(?![A-Za-z])")

#: submission.csv: required, first, and in this order.
SUBMISSION_COLUMNS = ("name", "sequence", "molecule_class")

#: metrics_full.csv: the same three, then `status` and `submission_rank`, which
#: are written even when every row is submitted. Without them a submitted row and
#: a documented-but-withdrawn row are indistinguishable and the table reads as a
#: larger submission than it is.
METRICS_BASE_COLUMNS = SUBMISSION_COLUMNS + ("status", "submission_rank")

#: Then the identity columns that make a row readable on its own, then the
#: measurements. Written only when at least one record supplies the key. The
#: meanings are in Target_2/docs/metrics.md.
OPTIONAL_COLUMNS = (
    # identity and provenance
    "binder_length",
    "series",
    "cyclisation",
    "target_epitope",
    "mechanism",
    "parent_family",
    "design_origin",
    "design_round",
    # the membership bar
    "n_interface_his_seed",
    "n_interface_his_human",
    "n_interface_his_mouse",
    "interface_cutoff_A",
    "his_positions",
    "n_his",
    "selection_score",
    # where the binder sits relative to the epitope
    "approach_K57_human_A",
    "approach_K57_mouse_A",
    "approach_K104_human_A",
    "n_models_human",
    "n_models_mouse",
    # pose, symmetry-aware (the target is a C3 homotrimer)
    "pose_sym_lrmsd_human_A",
    "pose_sym_converged_human",
    "pose_cross_redraw_lrmsd_A",
    # fold confidence
    "binder_plddt_human",
    "binder_plddt_mouse",
    "binder_ptm_human",
    # ipSAE, primary oracle. Shipped because Target 1 carries one; NOT a second
    # axis on this target -- see Target_2/docs/metrics.md.
    "ipsae_human",
    "ipsae_mouse",
    # interface confidence -- the axis this band was actually cut on
    "interface_iptm_human",
    "interface_iptm_human_sd",
    "interface_iptm_human_redraw8300",
    "interface_iptm_human_redraw9300",
    "interface_iptm_mouse",
    "interface_iptm_mouse_sd",
    "interface_iptm_mouse_redraw8300",
    "iptm_H_minus_M",
    "iptm_H_minus_M_redraw",
    "worse_ortholog_iptm",
    "worse_ortholog_which",
    # the second oracle, carrying the same 8 A pocket. `boltz_state` is its
    # quality-gate verdict. It is reported per design and does NOT exclude from
    # this band, so a reader has to be able to see which designs it demotes.
    "boltz_state",
    "boltz_interface_iptm_human",
    "boltz_interface_iptm_human_sd",
    "boltz_interface_iptm_mouse",
    "boltz_iptm_H_minus_M",
    "boltz_binder_plddt_human",
    "boltz_worse_ortholog_iptm",
    "boltz_in_own_top20",
    # the third oracle, which carried NO restraint -- the column names say so
    "protenix_unrestrained_interface_iptm_human",
    "protenix_unrestrained_interface_iptm_human_sd",
    "protenix_unrestrained_interface_iptm_mouse",
    "protenix_unrestrained_iptm_H_minus_M",
    "protenix_unrestrained_binder_plddt_human",
    "protenix_unrestrained_worse_ortholog_iptm",
    "protenix_in_own_top20",
    "oracles_placing_it_in_their_own_top20",
    # does the selection survive an independent draw
    "survives_redraw_seed8300",
    "survives_redraw_seed9300",
    # predicted pKa drift, human arm only
    "dpka_his_best_human",
    "dpka_his_human_spread",
    "dpka_his_human_n_models",
    # gates
    "gate_G1_approach_K57",
    "gate_G2_binder_plddt",
    "gate_G3_interface_his",
    "gate_pass_all",
    "gate_binder_plddt_human_0p65",
    "gate_binder_plddt_mouse_0p65",
    "gate_waived",
    # composition, reported and not optimised
    "n_cys",
    "n_lys_arg",
    "n_asp_glu",
    "frac_hydrophobic_AVILMFWY",
    "gravy",
    "risk_flags",
    "notes",
)

DEFAULT_SUBMISSION = Path("Target_2/submission.csv")
DEFAULT_METRICS = Path("Target_2/metrics_full.csv")


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


def validate_no_pending(record: dict, label: str) -> None:
    """Refuse a record carrying a marker left where a measurement belongs."""
    for key, value in record.items():
        if isinstance(value, str) and PENDING_MARKER.search(value):
            raise SubmissionError(
                f"{label}: field {key!r} still carries a pending marker "
                f"({value.strip()[:60]!r}). Those mark figures that were never "
                f"measured; a marker that reaches a deposited file is "
                f"indistinguishable from a result. Measure it or drop the field."
            )


def validate_molecule_class(record: dict, label: str) -> str:
    """Return the molecule class, defaulting to single_chain, or raise."""
    value = record.get("molecule_class", DEFAULT_MOLECULE_CLASS)
    if value not in MOLECULE_CLASSES:
        raise SubmissionError(
            f"{label}: molecule_class {value!r} is not one of the values the "
            f"upload form accepts ({', '.join(MOLECULE_CLASSES)}). Prose "
            f"elsewhere on the competition site says 'protein'; the form "
            f"itself does not, and the form is what the file is read by."
        )
    return value


def validate_consistency(record: dict, sequence: str, label: str) -> None:
    """Refuse a declared property the sequence contradicts."""
    length = record.get("binder_length")
    if length is not None and str(length) != str(len(sequence)):
        raise SubmissionError(
            f"{label}: binder_length says {length} and the sequence is "
            f"{len(sequence)} residues. One of the two is wrong, and a length "
            f"column that disagrees with its own sequence has already misread "
            f"a delivered design in this project."
        )
    cyclisation = record.get("cyclisation")
    if isinstance(cyclisation, str) and cyclisation.startswith("disulfide"):
        if not (sequence.startswith("C") and sequence.endswith("C")):
            raise SubmissionError(
                f"{label}: cyclisation is declared as {cyclisation!r} but the "
                f"sequence does not begin and end with cysteine, so the bond "
                f"that is said to close it cannot form."
            )


def is_submitted(record: dict) -> bool:
    """A record is part of the submission unless its status says otherwise."""
    status = record.get("status")
    return status is None or str(status).strip() == SUBMITTED


def validate_ranks(records: list[dict]) -> None:
    """The submitted rows must carry exactly the ranks 1..n, no gaps, no ties."""
    ranks: list[int] = []
    for index, record in enumerate(records):
        label = f"record {index} ({record.get('name')})"
        raw = record.get("submission_rank")
        if is_submitted(record):
            if raw is None or str(raw).strip() == "":
                raise SubmissionError(
                    f"{label}: submitted, but carries no 'submission_rank'. The "
                    f"challenge reads the ranking from the top row down, so an "
                    f"unranked submitted design has no defined position."
                )
            try:
                ranks.append(int(raw))
            except (TypeError, ValueError):
                raise SubmissionError(
                    f"{label}: 'submission_rank' is {raw!r}, not an integer"
                ) from None
        elif raw not in (None, ""):
            raise SubmissionError(
                f"{label}: not submitted (status {record.get('status')!r}) but "
                f"carries submission_rank {raw!r}. A design has no rank in a "
                f"submission it is not part of."
            )
    if not ranks:
        raise SubmissionError("no submitted records: every row carries a status")
    expected = list(range(1, len(ranks) + 1))
    if sorted(ranks) != expected:
        raise SubmissionError(
            f"the submitted designs carry ranks {sorted(ranks)}, which is not "
            f"1..{len(ranks)}. Ranks must be contiguous and unique, or the "
            f"column is a row counter rather than a ranking."
        )


def validate(records: list[dict], limit: int) -> list[dict]:
    """Validate every record and refuse the whole input if any is unacceptable."""
    if limit < 1:
        raise SubmissionError(f"--limit must be at least 1, got {limit}")

    seen_names: set[str] = set()
    seen_sequences: dict[str, str] = {}
    n_submitted = 0
    for index, record in enumerate(records):
        label = f"record {index}"
        name = record.get("name")
        if not isinstance(name, str) or not name.strip():
            raise SubmissionError(f"{label}: missing or empty 'name'")
        label = f"record {index} ({name})"
        if name in seen_names:
            raise SubmissionError(f"{label}: duplicate 'name'")
        seen_names.add(name)

        validate_no_pending(record, label)
        sequence = validate_sequence(record.get("sequence"), label)
        if sequence in seen_sequences:
            raise SubmissionError(
                f"{label}: the same sequence is already carried by "
                f"{seen_sequences[sequence]!r}. One molecule under two names "
                f"makes the ranking ambiguous and the metric table unreadable."
            )
        seen_sequences[sequence] = name
        validate_molecule_class(record, label)
        validate_consistency(record, sequence, label)
        if is_submitted(record):
            n_submitted += 1

    if n_submitted > limit:
        raise SubmissionError(
            f"{n_submitted} records are marked submitted, but this target "
            f"allows at most {limit}. Select the designs to submit before "
            f"building the CSVs, or pass the --limit the competition states."
        )
    validate_ranks(records)
    return records


def rank_key(record: dict, fallback: int) -> tuple[int, float, int]:
    """Sort key putting the best-ranked record first.

    Records carrying a numeric rank sort ahead of records without one, lowest
    rank first. Records without a rank keep their input order behind them.
    """
    raw = record.get("submission_rank")
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


def active_columns(records: list[dict], base: tuple[str, ...]) -> list[str]:
    """The base columns, plus the optional ones some record actually supplies."""
    supplied = [
        column
        for column in OPTIONAL_COLUMNS
        if any(record.get(column) is not None for record in records)
    ]
    return list(base) + supplied


def cell(record: dict, column: str) -> str:
    """Render one field.

    'molecule_class' and 'status' are defaulted rather than left blank, because a
    blank in this table means *not measured* and neither of those is ever
    unmeasured. Every other absent value is written empty.
    """
    if column == "molecule_class":
        return record.get("molecule_class", DEFAULT_MOLECULE_CLASS)
    if column == "status":
        return str(record.get("status") or SUBMITTED)
    value = record.get(column)
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (list, tuple)):
        return " ".join(str(item) for item in value)
    return str(value)


def write_csv(records: list[dict], columns: list[str], output: Path) -> None:
    """Write one CSV with the given columns, in the given row order."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        for record in records:
            writer.writerow([cell(record, column) for column in columns])


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build Target 2's submission CSV and its full metric table from a "
            "JSON file of ranked candidate records."
        )
    )
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="JSON file of ranked candidate records (a list, or an object with "
        "a 'candidates' key).",
    )
    parser.add_argument(
        "--submission",
        type=Path,
        default=None,
        help=f"The three-column file to submit. Default: {DEFAULT_SUBMISSION} "
        f"relative to the repository root.",
    )
    parser.add_argument(
        "--metrics",
        type=Path,
        default=None,
        help=f"The full metric table. Default: {DEFAULT_METRICS} relative to "
        f"the repository root.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        required=True,
        help="The number of designs this target accepts. Required, and "
        "deliberately not defaulted: the allowance was not established when "
        "this script was written, and a guessed default would silently "
        "truncate the band or silently admit too many.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(__file__).resolve().parent.parent
    submission_path = args.submission or root / DEFAULT_SUBMISSION
    metrics_path = args.metrics or root / DEFAULT_METRICS

    try:
        records = order_records(validate(load_records(args.input), args.limit))
        submitted = [record for record in records if is_submitted(record)]
        documented = [record for record in records if not is_submitted(record)]

        write_csv(submitted, list(SUBMISSION_COLUMNS), submission_path)
        metrics_columns = active_columns(records, METRICS_BASE_COLUMNS)
        write_csv(records, metrics_columns, metrics_path)
    except SubmissionError as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 1

    print(f"wrote {len(submitted)} submitted row(s) to {submission_path}")
    print(f"wrote {len(records)} row(s) to {metrics_path}")
    if documented:
        print(
            f"{len(documented)} documented but not submitted: "
            f"{', '.join(record['name'] for record in documented)}"
        )
    print(f"submission columns: {', '.join(SUBMISSION_COLUMNS)}")
    print(f"metric columns: {len(metrics_columns)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
