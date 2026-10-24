#!/usr/bin/env python3
"""Build Target 3's submission CSV and its full metric table from a ranking file.

Target 3 is the GLP-1R agonist target, deposited as two bands under one ranking:
a **micro** band of disulfide-cyclised peptides of 12 to 39 residues designed in
this group, and a **mini** band of 140-residue de novo miniproteins. Both are
submitted as ``molecule_class = single_chain``, which is what the upload form
offers; the distinction between the bands lives in the ``series`` column and in
``Target_3/docs/``.

Adapted from ``scripts/make_target2_submission.py``. The two default output
paths, this docstring, the ``OPTIONAL_COLUMNS`` set and the cyclisation check
differ; the rest of the validation, the ordering and the two-file output are that
script's, unchanged.

The script reads a JSON file of ranked candidate records and writes two files:

  * ``Target_3/submission.csv``   -- the file submitted to the challenge. Exactly
    the three columns the template defines, ``name,sequence,molecule_class``, and
    only the rows that are actually being submitted, ordered best-first because
    the challenge reads the ranking from the top row down.
  * ``Target_3/metrics_full.csv`` -- every row the ranking produced, submitted or
    not, with every metric the input supplies, keyed by the same ``name``.

Usage
-----
    python3 scripts/make_target3_submission.py \
        --input Target_3/docs/ranking.json \
        --limit <the number of designs this target accepts>

``--limit`` has **no default**. Target 1's script defaults to 8 because the micro
band's allowance is known; this target's allowance was not established when this
script was written, and a guessed default would silently truncate or silently
admit. Pass the number the competition states.

**No band has been built with this script yet**, so there is no limit here that a
previous run can be said to have used. When the band is cut, set ``--limit`` to
the number the competition states, or, failing that, to the size of the band
being delivered so that the script refuses one row more rather than silently
admitting it -- and say in ``Target_3/README.md`` which of the two the number is.
The script refuses rather than truncates, so choosing the designs to drop stays a
decision for a person.

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
``Target_3/docs/metrics.md``; keep the two in step. Unrecognised keys are
ignored, so a record may carry internal bookkeeping without it reaching the CSV.

A record that documents a design which is **not** being submitted carries a
``status`` saying so in a sentence, and carries **no** ``submission_rank`` -- a
design has no rank in a submission it is not part of.

What changed from the Target 2 script
-------------------------------------
  * The two default output paths point at ``Target_3/`` instead of ``Target_2/``.
  * ``OPTIONAL_COLUMNS`` carries Target 3's measurements. Target 2's ortholog
    pair and its histidine-proximity bar have no counterpart here and are gone
    entirely; in their place are this target's fold-confidence block (measured
    without the pocket restraint, with the restrained arm kept beside it), the
    pose-agreement and interface-contact blocks, the TM6 two-state
    receptor-activation readout, the ECL2+TM5 engagement-family readout, the
    Boltz-2 and Protenix-v2 blocks measured with an alignment, the disulfide
    ring-closure block, the terminal-tail block the trimming question is decided
    on, and a separate block for the mini band's own metrics.
  * ``validate_consistency`` checks a declared disulfide against
    ``cys_positions`` rather than against the two terminal residues. Target 2's
    band was entirely Cys1-CysN macrocycles; this one is not, and the terminal
    test would refuse a correctly declared ring sitting at, say, 28-39.
  * Nothing else. The remaining validation, the refusals, the rank check, the ordering,
    ``active_columns``/``cell``/``write_csv`` and
    ``SUBMISSION_COLUMNS`` are the Target 2 script's, unchanged -- including
    ``molecule_class`` being validated against the upload form's own enumeration
    (``single_chain, nanobody, scfv, fab_kappa, fab_lambda``) rather than the
    "protein" that prose elsewhere on the competition site says, and ``--limit``
    being required rather than defaulted.

Two cautions about the columns, carried here from the column notes below so that
a reader of the CSV does not have to infer them:

  * The TM6 and ECL2 blocks read a **binding mode**, not validated pharmacology.
    An "active-like" TM6 separation or a canonical ECL2 family says the peptide
    sits where an agonist sits in the models; it is not evidence of agonism.
  * The design search's own objective values are deliberately NOT deposited. They
    are not measurements of the delivered fold, they are not comparable between
    the two bands, and nothing in this deposition is argued from them.

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
    cyclisation whose ``cys_positions`` do not name two distinct cysteines of
    that sequence.
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
#: meanings are in Target_3/docs/metrics.md.
OPTIONAL_COLUMNS = (
    # identity and provenance
    "binder_length",
    "series",
    "cyclisation",
    "mechanism",
    "parent_family",
    "wave",
    "arm",
    "direction",
    "design_origin",
    "design_round",
    "cys_positions",
    "trimmed",
    "trimmed_from",
    # fold confidence -- the primary oracle for the micro band.
    # Measured WITHOUT the pocket restraint: see the note below.
    "selected_iptm",
    "selected_ptm",
    "binder_plddt",
    "state",
    "score_source",
    # the restrained arm, and the difference. Kept because the two arms are not
    # interchangeable: ranking on the restrained numbers reorders the band
    # (rho = +0.538 over 48 designs), so the condition has to travel with the score.
    "chai_iptm_restrained",
    "restraint_delta",
    "chai_iptm_spread",
    "chai_n_folds",
    # pose agreement across the five diffusion samples, reference-free
    "pose_disp_mean",
    "pose_disp_max",
    # interface polar contacts
    "hb_mean",
    "hb_conserved",
    "hb_partners",
    # receptor activation conformation (TM6 two-state), reported -- near-universal,
    # NOT a ranker
    "tm6_primary_mean",
    "tm6_k_active",
    "tm6_n",
    "consensus_active_frac",
    # ECL2+TM5 engagement family -- the real discriminant; fam0 = canonical/
    # agonist-like. Report it AND state it reads binding mode, not validated
    # pharmacology (docs/metrics.md).
    "ecl2_fam0_k",
    "ecl2_family_n",
    "ecl2_canonical",
    "ecl2_d_fam0",
    "ecl2_d_fam1",
    "ecl2_tm5_mix",
    # the SECOND AND THIRD ORACLES. Reported, never ranked on. Every number in
    # these two blocks was produced WITH an alignment, so that the two models
    # that need one are not being compared against chai with it switched off;
    # the single-sequence arm is a separate experiment and is not deposited here.
    # chai and Boltz-2 disagree on this target while each reproduces itself, so
    # the disagreement is real rather than noise, and a blended score would
    # average it away. See Target_3/docs/metrics.md.
    "boltz_msa_iptm_max",
    "boltz_msa_iptm_mean",
    "boltz_msa_iptm_spread",
    "boltz_msa_ptm_mean",
    "boltz_msa_ipsae_max",
    "boltz_msa_ipsae_mean",
    "boltz_msa_binder_plddt",
    "boltz_condition",
    "protenix_msa_iptm_max",
    "protenix_msa_iptm_mean",
    "protenix_msa_iptm_spread",
    "protenix_msa_ptm_mean",
    "protenix_msa_ipsae_max",
    "protenix_msa_ipsae_mean",
    "protenix_msa_binder_plddt",
    "protenix_condition",
    "receptor_msa_depth",
    "binder_msa_depth",
    # ring closure
    "ss_distance_median",
    "ss_bonded_k",
    "ss_n",
    # tail order (the trim question)
    "ring_plddt",
    "tail_plddt",
    "tail_lt70",
    "nterm_run_lt70",
    "cterm_run_lt70",
    # ---- the mini band ----------------------------------------------------
    # Separate columns, deliberately. The mini designs were produced and scored
    # by a different pipeline and a different oracle from the micro band; a
    # shared `selected_iptm` column would put two numbers that were never
    # measured the same way under one heading. A blank here means the design was
    # not measured on that axis, which for a cross-band column is always true.
    "anchor_seq",
    "n_hotspots",
    "hotspot_positions",
    "motif_rmsd_A",
    "receptor_rmsd_A",
    "rmsd_domain_A",
    "rmsd_all_A",
    "min_dist_A",
    "mini_iptm",
    "mini_ipsae",
    "mini_ipsae_consensus",
    "mini_plddt_binder",
    "mini_plddt_design",
    "mini_iplddt",
    "mini_pdockq",
    "mono_plddt",
    "mono_plddt_designed",
    "self_iptm",
    "self_contacts",
    "mini_score",
    # flags
    "risk_flags",
    "notes",
)

DEFAULT_SUBMISSION = Path("Target_3/submission.csv")
DEFAULT_METRICS = Path("Target_3/metrics_full.csv")


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
        # Target 2's rule was "begins and ends with cysteine", because every
        # design in that band was a Cys1-CysN macrocycle. It does not hold here:
        # six of the ten Target-3 micro designs are a 12-mer macrocycle extended
        # by a tail, so the ring sits at positions like 28-39 and the terminal
        # test would refuse a correctly declared design. What has to be true is
        # the weaker, exact statement: the two residues the declaration names
        # are cysteines of this sequence.
        positions = record.get("cys_positions")
        if isinstance(positions, str):
            positions = positions.replace(",", " ").split()
        if not isinstance(positions, (list, tuple)) or len(positions) != 2:
            raise SubmissionError(
                f"{label}: cyclisation is declared as {cyclisation!r} but "
                f"cys_positions is {positions!r}. A declared disulfide names "
                f"exactly two residues, 1-based, or it is not a declaration."
            )
        try:
            first, second = (int(p) for p in positions)
        except (TypeError, ValueError):
            raise SubmissionError(
                f"{label}: cys_positions {positions!r} are not two integers"
            ) from None
        for position in (first, second):
            if not 1 <= position <= len(sequence):
                raise SubmissionError(
                    f"{label}: cys_positions names residue {position}, outside "
                    f"a {len(sequence)}-residue sequence."
                )
            if sequence[position - 1] != "C":
                raise SubmissionError(
                    f"{label}: cyclisation is declared as {cyclisation!r}, but "
                    f"residue {position} of the sequence is "
                    f"{sequence[position - 1]!r}, not cysteine, so the bond "
                    f"that is said to close it cannot form."
                )
        if first == second:
            raise SubmissionError(
                f"{label}: cys_positions names residue {first} twice; a "
                f"disulfide joins two different cysteines."
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
            "Build Target 3's submission CSV and its full metric table from a "
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
