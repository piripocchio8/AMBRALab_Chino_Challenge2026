#!/usr/bin/env python3
"""Copy the predicted structures for the twenty deposited designs into the repository.

One directory per design, named by its deposited identifier, holding the models
the numbers in ``metrics_full.csv`` were read off and nothing else. Anything
quoted in the deposition can then be recomputed from what is here.

What lands in each directory
----------------------------
**micro** -- three oracles, all in the **disulfide-only** condition, because that
is the condition the band is ranked in. The pocket restraint used during the
search is deliberately absent: with the pocket declared, "it binds the pocket" is
partly an instruction rather than a prediction, and refolding without it reorders
the band.

    chai_ssonly_model_{0..4}.cif        chai, disulfide restraint only
    chai_scores_model_{0..4}.npz        the ipTM/pTM arrays those models scored
    boltz_msa_model_{0..4}.cif          Boltz-2, disulfide bond constraint, with MSA
    boltz_confidence_model_{0..4}.json
    protenix_sample_{0..4}.cif          Protenix-v2, UNRESTRAINED, with MSA
    protenix_confidence_sample_{0..4}.json
    restraints.csv                      what chai was actually given
    sequence.fasta
    metrics.json                        every number this repository quotes for the design

**Protenix is unrestrained and is labelled so in its own filenames and in
metrics.json.** Protenix-v2's constraint embedders are disabled in the released
configuration and the checkpoint carries no constraint tensors, so it cannot be
given the disulfide. Its numbers are therefore not measured in the same condition
as the other two and must not be averaged with them.

**mini** -- the three predictions the collaborating pipeline made for each design,
copied verbatim from the campaign package:

    complex.pdb      the design bound to the receptor
    alone.pdb        the design by itself
    self_pair.pdb    the design against a copy of itself (a self-association check:
                     a LOW interface score here is the good outcome)
    sequence.fasta
    metrics.json

Nothing in ``mini/`` was folded or re-scored in this repository.

Usage
-----
    python3 scripts/pack_target3_structures.py \
        --ranking Target_3/docs/ranking.json \
        --chai-roots <dir> [<dir> ...] --boltz <dir> --protenix <dir> \
        --mini-src <dir containing b_complex_a.json ...> \
        --micro-index <ranking_computed.json> --mini-index <mini_top10.json>

Standard library only.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

#: The per-design file the source package keys its coordinates by, and the name
#: it is deposited under.
MINI_BUNDLES = {
    "complex.pdb": ("b_complex_a.json", "b_complex_b.json"),
    "alone.pdb": ("b_alone.json",),
    "self_pair.pdb": ("b_pair.json",),
}


def load(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def find_fold(roots: list[Path], dirname: str) -> Path | None:
    """Resolve a fold directory by name.

    The ``out_dir`` recorded in a result shard is the path *inside the container*
    (a container mount point), which does not exist on this filesystem. Only
    the leaf name is portable, so the search is by name across the known roots.
    """
    for root in roots:
        if (root / dirname / "chai_out").is_dir():
            return root / dirname
    return None


def copy_numbered(sources: list[Path], dest: Path, pattern: str) -> int:
    """Copy an ordered set of files to ``dest`` as ``pattern`` % index."""
    for index, src in enumerate(sources):
        shutil.copyfile(src, dest / (pattern % index))
    return len(sources)


def pack_micro(record: dict, source: dict, args, dest: Path) -> dict:
    """One micro design. Returns what was copied, for the report."""
    counts = {}
    dest.mkdir(parents=True, exist_ok=True)
    internal = source["name"]

    fold = find_fold(args.chai_roots, Path(source["ss_only_dir"]).name)
    if fold:
        chai = fold / "chai_out"
        cifs = sorted(chai.glob("pred.model_idx_*.cif"),
                      key=lambda p: int(p.stem.rsplit("_", 1)[-1]))
        npz = sorted(chai.glob("scores.model_idx_*.npz"),
                     key=lambda p: int(p.stem.rsplit("_", 1)[-1]))
        counts["chai_cif"] = copy_numbered(cifs, dest, "chai_ssonly_model_%d.cif")
        counts["chai_npz"] = copy_numbered(npz, dest, "chai_scores_model_%d.npz")
        restraints = fold / "restraints.csv"
        if restraints.is_file():
            shutil.copyfile(restraints, dest / "restraints.csv")
            counts["restraints"] = 1

    boltz = args.boltz / internal / f"boltz_results_{internal}" / "predictions" / internal
    if boltz.is_dir():
        cifs = sorted(boltz.glob(f"{internal}_model_*.cif"),
                      key=lambda p: int(p.stem.rsplit("_", 1)[-1]))
        conf = sorted(boltz.glob(f"confidence_{internal}_model_*.json"),
                      key=lambda p: int(p.stem.rsplit("_", 1)[-1]))
        counts["boltz_cif"] = copy_numbered(cifs, dest, "boltz_msa_model_%d.cif")
        counts["boltz_conf"] = copy_numbered(conf, dest, "boltz_confidence_model_%d.json")

    prot = args.protenix / internal
    predictions = sorted(prot.glob("seed_*/predictions")) if prot.is_dir() else []
    if predictions:
        pred = predictions[0]
        cifs = sorted(pred.glob(f"{internal}_sample_*.cif"),
                      key=lambda p: int(p.stem.rsplit("_", 1)[-1]))
        conf = sorted(pred.glob(f"{internal}_summary_confidence_sample_*.json"),
                      key=lambda p: int(p.stem.rsplit("_", 1)[-1]))
        counts["protenix_cif"] = copy_numbered(cifs, dest, "protenix_sample_%d.cif")
        counts["protenix_conf"] = copy_numbered(
            conf, dest, "protenix_confidence_sample_%d.json")

    (dest / "sequence.fasta").write_text(
        f">{record['name']} | {record.get('cyclisation', 'linear')} | "
        f"internal {internal}\n{record['sequence']}\n", encoding="utf-8")
    (dest / "metrics.json").write_text(
        json.dumps({**record, "_internal_name": internal,
                    "_chai_condition": "disulfide restraint only; no pocket restraint",
                    "_protenix_condition": "UNRESTRAINED (the model cannot take a constraint)"},
                   indent=1) + "\n", encoding="utf-8")
    return counts


def pack_mini(record: dict, tag: str, bundles: dict, dest: Path) -> dict:
    counts = {}
    dest.mkdir(parents=True, exist_ok=True)
    for filename, store in bundles.items():
        text = store.get(tag)
        if text:
            (dest / filename).write_text(text, encoding="utf-8")
            counts[filename] = len(text.splitlines())
    (dest / "sequence.fasta").write_text(
        f">{record['name']} | 140 aa miniprotein | source tag {tag}\n"
        f"{record['sequence']}\n", encoding="utf-8")
    (dest / "metrics.json").write_text(
        json.dumps({**record, "_source_tag": tag,
                    "_provenance": "folded and scored by the collaborating "
                                   "RFdiffusion3 + ProteinMPNN pipeline, outside this "
                                   "repository; copied verbatim, not re-measured"},
                   indent=1) + "\n", encoding="utf-8")
    return counts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--ranking", required=True, type=Path)
    parser.add_argument("--chai-roots", nargs="+", type=Path, default=[])
    parser.add_argument("--boltz", type=Path)
    parser.add_argument("--protenix", type=Path)
    parser.add_argument("--mini-src", type=Path)
    parser.add_argument("--micro-index", required=True, type=Path)
    parser.add_argument("--mini-index", required=True, type=Path,
                        help="the collaborating pipeline's FULL design pool. The join is "
                             "by sequence, so a file holding only a previous selection "
                             "silently skips every design that selection did not contain.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args(argv)

    ranking = load(args.ranking)["candidates"]
    submitted = [r for r in ranking if r.get("submission_rank") is not None]

    # the deposited record carries the renamed identity; the campaign file carries
    # the paths. Join them on the sequence, which is the one key both agree on.
    micro_by_seq = {c["sequence"]: c
                    for c in load(args.micro_index)["candidates"]}
    mini_by_seq = {d["seq"]: d for d in load(args.mini_index)["designs"]}

    bundles = {}
    if args.mini_src:
        for filename, names in MINI_BUNDLES.items():
            store = {}
            for name in names:
                path = args.mini_src / name
                if path.is_file():
                    store.update(load(path))
            bundles[filename] = store

    total = {}
    for record in sorted(submitted, key=lambda r: r["submission_rank"]):
        name = record["name"]
        if record.get("series") == "micro":
            source = micro_by_seq.get(record["sequence"])
            if source is None:
                print(f"  {name}: no campaign record for this sequence -- skipped")
                continue
            counts = pack_micro(record, source, args, args.root / "Target_3/micro" / name)
        else:
            tag = mini_by_seq.get(record["sequence"], {}).get("tag")
            if tag is None:
                print(f"  {name}: no source record for this sequence -- skipped")
                continue
            counts = pack_mini(record, tag, bundles, args.root / "Target_3/mini" / name)
        print(f"  {name}: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
        for key, value in counts.items():
            total[key] = total.get(key, 0) + (1 if key in MINI_BUNDLES else value)
    print("\ntotals: " + ", ".join(f"{k}={v}" for k, v in sorted(total.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
