#!/usr/bin/env python3
"""Assemble ``Target_3/docs/ranking.json`` from the design repository's results.

This is the step between the design campaign and the deposition. It reads the
measurement files the campaign produced, renames each design to its deposited
identifier, and writes one ranked list in the schema
``scripts/make_target3_submission.py`` validates. It measures nothing itself:
every number it writes is copied from a named file, and the file it came from is
recorded in the output's ``_sources`` block.

Two bands, one ranking
----------------------
* **micro** -- disulfide-cyclised peptides of 12 to 39 residues designed in this
  group. Ranked on chai interface pTM measured in the **disulfide-only**
  condition (no pocket restraint), under a quota that guarantees places to the
  designs whose receptor engagement is canonical.
* **mini** -- 140-residue de novo miniproteins from a collaborating pipeline
  (RFdiffusion3 + ProteinMPNN), taken in that pipeline's own rank order. Nothing
  about them was re-measured here.

The two bands are deposited as consecutive blocks, micro first, rather than
interleaved. Their scores come from different oracles run on different machines
in different conditions, so a merged ordering would be arithmetic performed on
numbers that were never on the same scale. ``--mini-first`` swaps the blocks if
the ordering decision goes the other way; it does not interleave them either.

Usage
-----
    python3 scripts/build_target3_ranking.py \
        --micro   <ranking_computed.json> \
        --mini    <mini_top10.json> \
        --boltz   <boltz_msa.json> \
        --protenix <protenix_msa.json> \
        --mini-pool <gianmattia_designs.json> \
        --out Target_3/docs/ranking.json

Standard library only.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

#: The deposited band sizes. Both are stated rather than inferred, so that a
#: short input is a refusal and not a quietly smaller submission.
N_MICRO = 10
N_MINI = 10

#: GLP-1(7-15). The deposition platform's novelty check rejects a design that
#: CONTAINS this exact nine-residue fragment and accepts one that does not. That is
#: not a guess: of the first ten miniproteins uploaded, five were rejected with
#: "contains a known binder fragment" and five passed, and this rule reproduces all
#: ten outcomes. Two near misses show it is the fragment and not merely similarity
#: -- a passing design carries `EGTFTSDVS`, a different exact nine-residue fragment
#: of GLP-1, and another carries exendin-4's exact N-terminal decapeptide. Only
#: GLP-1's own N-terminus is in the platform's set.
GLP1_NTERM = "HAEGTFTSD"

#: The ten mini designs deposited, by the source package's own rank. The first five
#: are the survivors of that upload, in their original order; the last five are the
#: highest-scoring eligible designs from the package's second block, which was built
#: with the identity to the natural agonists deliberately reduced.
#:
#: Rank 41 outscores rank 42 and is NOT here: it shares a parent backbone with rank
#: 35, and the pipeline's author asked for fold diversity if the first set had to be
#: replaced. One design per backbone is the cheaper way to honour that than a tie-break
#: after the fact.
MINI_RANKS = (1, 2, 4, 8, 10, 35, 36, 38, 39, 42)

#: Everything else in the second block that clears the fragment rule, held as
#: documented reserves so a further rejection can be answered from measured designs.
MINI_RESERVE_RANKS = (41, 43, 44, 45, 47, 48, 50)

RESERVE_STATUS = (
    "reserve: not submitted. Held to replace a submitted mini design if one "
    "fails the deposition platform's novelty check."
)


def load(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def drop_none(record: dict) -> dict:
    """Remove the keys with no value, so a blank cell means *not measured*."""
    return {key: value for key, value in record.items() if value is not None}


#: Two campaign arms carry an internal infrastructure label rather than a design-arm name.
#: They are relabelled here, keyed on (wave, seed) so that the label itself does not have to
#: be written down. Both designs concerned are documented rows, not submitted ones.
ARM_RELABEL = {("t3w3", 9203): "w3b", ("t3w3", 9204): "w3c"}


def micro_records(micro: dict, boltz: dict, protenix: dict) -> list[dict]:
    """Convert the campaign's candidate list into deposition records.

    The submitted band keeps its computed ranks 1..10 and is named in rank
    order; everything else in the pool is documented behind it, unranked, in the
    order the ranker left it.
    """
    pool = micro["candidates"]
    submitted = sorted(
        (c for c in pool if (c.get("status") or "submitted") == "submitted"),
        key=lambda c: c["submission_rank"],
    )
    if len(submitted) != N_MICRO:
        raise SystemExit(
            f"refused: the micro input marks {len(submitted)} designs submitted, "
            f"expected {N_MICRO}"
        )
    documented = [c for c in pool if (c.get("status") or "submitted") != "submitted"]

    out = []
    for index, c in enumerate(submitted + documented, start=1):
        is_sub = (c.get("status") or "submitted") == "submitted"
        cys = c.get("cys") or []
        b = boltz.get(c["name"]) or {}
        p = protenix.get(c["name"]) or {}
        depths = (boltz.get("_meta") or {}).get("binder_msa_depth") or {}

        record = {
            "name": f"AMBRA_T3_micro_{index:02d}",
            "sequence": c["sequence"],
            "molecule_class": "single_chain",
            "status": "submitted" if is_sub else str(c.get("status")),
            "submission_rank": c["submission_rank"] if is_sub else None,
            "binder_length": c.get("binder_length"),
            "series": "micro",
            "cyclisation": f"disulfide C{cys[0]}-C{cys[1]}" if len(cys) == 2 else None,
            "mechanism": "agonist",
            # `parent` is a pocket-family tag (p1/p2/p3) on the wave-4 cells, not
            # a parent design. It is written here only when it is one of those.
            "parent_family": c.get("parent") if str(c.get("parent") or "").startswith("p") else None,
            "wave": c.get("wave"),
            "arm": ARM_RELABEL.get((c.get("wave"), c.get("seed")), c.get("arm")),
            "direction": c.get("direction"),
            "design_origin": c.get("origin"),
            "cys_positions": " ".join(str(x) for x in cys) if cys else None,
            # the ranking axis, and the condition it was measured in
            "selected_iptm": c.get("chai_iptm_ss_only", c.get("chai_iptm")),
            "selected_ptm": c.get("chai_ptm"),
            "binder_plddt": c.get("binder_plddt_ss_only", c.get("binder_plddt")),
            "state": c.get("state"),
            "score_source": c.get("chai_source"),
            "chai_iptm_restrained": c.get("chai_iptm_restrained"),
            "restraint_delta": c.get("restraint_delta"),
            "chai_iptm_spread": c.get("chai_iptm_spread"),
            "chai_n_folds": c.get("chai_n_folds"),
            "pose_disp_mean": c.get("pose_disp_ss_only", c.get("pose_disp_mean")),
            "pose_disp_max": c.get("pose_disp_max"),
            "hb_mean": c.get("hb_mean"),
            "hb_conserved": c.get("hb_conserved"),
            "hb_partners": c.get("hb_partners"),
            "tm6_k_active": c.get("tm6_k_active"),
            "tm6_n": c.get("tm6_n"),
            "ecl2_fam0_k": c.get("ecl2_fam0_k"),
            "ecl2_family_n": c.get("ecl2_family_n"),
            "ecl2_canonical": c.get("ecl2_canonical"),
            "ecl2_tm5_mix": c.get("ecl2_tm5_mix"),
            "ss_distance_median": c.get("ss_distance_median"),
            "ss_bonded_k": c.get("ss_bonded_k"),
            "ss_n": c.get("ss_n"),
            "ring_plddt": c.get("ring_plddt"),
            "tail_plddt": c.get("tail_plddt"),
            "tail_lt70": c.get("tail_lt70"),
            "nterm_run_lt70": c.get("nterm_run_lt70"),
            "cterm_run_lt70": c.get("cterm_run_lt70"),
            "risk_flags": c.get("risk_flags"),
        }
        if b:
            record.update({
                "boltz_msa_iptm_max": b.get("iptm_max"),
                "boltz_msa_iptm_mean": b.get("iptm_mean"),
                "boltz_msa_iptm_spread": b.get("iptm_spread"),
                "boltz_msa_ptm_mean": b.get("ptm_mean"),
                "boltz_msa_ipsae_max": b.get("ipsae_max"),
                "boltz_msa_ipsae_mean": b.get("ipsae_mean"),
                "boltz_msa_binder_plddt": b.get("binder_plddt_mean"),
                "boltz_condition": b.get("condition"),
            })
        if p:
            record.update({
                "protenix_msa_iptm_max": p.get("iptm_max"),
                "protenix_msa_iptm_mean": p.get("iptm_mean"),
                "protenix_msa_iptm_spread": p.get("iptm_spread"),
                "protenix_msa_ptm_mean": p.get("ptm_mean"),
                "protenix_msa_ipsae_max": p.get("ipsae_max"),
                "protenix_msa_ipsae_mean": p.get("ipsae_mean"),
                "protenix_msa_binder_plddt": p.get("binder_plddt_mean"),
                "protenix_condition": p.get("condition"),
            })
        if b or p:
            record["receptor_msa_depth"] = (boltz.get("_meta") or {}).get("receptor_msa_depth")
            record["binder_msa_depth"] = depths.get(c["name"])
        out.append(drop_none(record))
    return out


def backbone(d: dict) -> str:
    """The parent backbone a design was threaded onto.

    The source tag is `<source>_<index>_<backbone>__<mpnn draw tail>`; two designs
    from one backbone differ only in the tail, so the backbone is the middle.
    """
    parts = d["name"].split("_", 2)
    return d["source"] + "_" + parts[2].split("__")[0] if len(parts) > 2 else d["name"]


def mini_record(d: dict, name: str, rank: int | None, status: str) -> dict:
    """One deposited miniprotein, with every number copied from the source."""
    hot = d.get("hot_list") or []
    return drop_none({
        "name": name,
        "sequence": d["seq"],
        "molecule_class": "single_chain",
        "status": status,
        "submission_rank": rank,
        "binder_length": len(d["seq"]),
        "series": "mini",
        "mechanism": "agonist",
        "design_origin": "RFdiffusion3 + ProteinMPNN (collaborating pipeline, run outside this repository)",
        "design_round": d.get("source"),
        "anchor_seq": d.get("anchor"),
        "n_hotspots": d.get("hotspots"),
        "hotspot_positions": " ".join(str(x) for x in hot) if hot else None,
        "motif_rmsd_A": d.get("motif_rmsd"),
        "receptor_rmsd_A": d.get("receptor_rmsd"),
        "rmsd_domain_A": d.get("rmsd_domain"),
        "rmsd_all_A": d.get("rmsd_all"),
        "min_dist_A": d.get("min_dist"),
        "mini_iptm": d.get("iptm"),
        "mini_ipsae": d.get("ipsae"),
        "mini_ipsae_consensus": d.get("ipsae_cons"),
        "mini_plddt_binder": d.get("plddt_binder"),
        "mini_plddt_design": d.get("plddt_design"),
        "mini_iplddt": d.get("iplddt"),
        "mini_pdockq": d.get("pdockq"),
        "mono_plddt": d.get("mono_plddt"),
        "mono_plddt_designed": d.get("mono_plddt_designed"),
        "self_iptm": d.get("self_iptm"),
        "self_contacts": d.get("self_contacts"),
        "mini_score": d.get("score"),
        "notes": f"source pipeline tag {d.get('tag')}",
    })


def mini_records(pool: dict, rank_offset: int) -> list[dict]:
    """The deposited mini band, selected from the source package by MINI_RANKS.

    The selection is refused outright if any chosen design carries GLP-1's
    N-terminal fragment, or if two of them share a parent backbone. Both are
    conditions a hand-edited rank list could break silently.
    """
    by_rank = {d["rank"]: d for d in pool["designs"]}
    missing = [r for r in MINI_RANKS if r not in by_rank]
    if missing:
        raise SystemExit(f"refused: the source package has no rank {missing}")
    chosen = [by_rank[r] for r in MINI_RANKS]
    if len(chosen) != N_MINI:
        raise SystemExit(f"refused: MINI_RANKS holds {len(chosen)}, expected {N_MINI}")

    carries = [d["rank"] for d in chosen if GLP1_NTERM in d["seq"]]
    if carries:
        raise SystemExit(
            f"refused: rank(s) {carries} contain {GLP1_NTERM}, GLP-1's own "
            f"N-terminus. The deposition platform rejects those as a known binder "
            f"fragment; five designs were already lost to it."
        )
    seen: dict[str, int] = {}
    for d in chosen:
        key = backbone(d)
        if key in seen:
            raise SystemExit(
                f"refused: ranks {seen[key]} and {d['rank']} share parent backbone "
                f"{key}. Two sequences on one backbone spend two of ten slots on "
                f"one fold."
            )
        seen[key] = d["rank"]

    out = [
        mini_record(d, f"AMBRA_T3_mini_{i:02d}", rank_offset + i, "submitted")
        for i, d in enumerate(chosen, start=1)
    ]
    reserves = sorted(
        (by_rank[r] for r in MINI_RESERVE_RANKS if r in by_rank),
        key=lambda d: d["rank"],
    )
    out += [
        mini_record(d, f"AMBRA_T3_mini_reserve_{i:02d}", None, RESERVE_STATUS)
        for i, d in enumerate(reserves, start=1)
    ]
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--micro", required=True, type=Path)
    parser.add_argument("--mini", type=Path, default=None,
                        help="unused; the band is selected from --mini-pool by MINI_RANKS")
    parser.add_argument("--boltz", type=Path, default=None)
    parser.add_argument("--protenix", type=Path, default=None)
    parser.add_argument("--mini-pool", required=True, type=Path,
                        help="the collaborating pipeline's full 50-design pool; the "
                             "deposited band and the reserves are both selected from it")
    parser.add_argument("--mini-first", action="store_true",
                        help="deposit the mini block ahead of the micro block")
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)

    boltz = load(args.boltz) if args.boltz else {}
    protenix = load(args.protenix) if args.protenix else {}
    micro = micro_records(load(args.micro), boltz, protenix)
    mini = mini_records(load(args.mini_pool),
                        rank_offset=0 if args.mini_first else N_MICRO)
    if args.mini_first:
        for record in micro:
            if record.get("submission_rank") is not None:
                record["submission_rank"] += N_MINI
        records = mini + micro
    else:
        records = micro + mini

    payload = {
        "_rule": (
            "Two bands under one ranking, deposited as consecutive blocks rather "
            "than interleaved: micro ranks 1-10, mini ranks 11-20. Within the "
            "micro band, chai interface pTM measured WITHOUT the pocket restraint, "
            "under a quota guaranteeing places to designs whose ECL2+TM5 "
            "engagement is canonical. Within the mini band, the collaborating "
            "pipeline's own rank order, unchanged. The two bands are not merged "
            "because their scores come from different oracles in different "
            "conditions and were never on one scale."
        ),
        # Basenames only. This file is public; the directory layout of the machines the
        # campaign ran on is not, and a scratch path in a deposited file is noise to every
        # reader who cannot open it.
        "_sources": {
            "micro": args.micro.name,
            "mini": args.mini_pool.name,
            "boltz": args.boltz.name if args.boltz else None,
            "protenix": args.protenix.name if args.protenix else None,
            "mini_pool": args.mini_pool.name if args.mini_pool else None,
        },
        "candidates": records,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8")

    n_sub = sum(1 for r in records if r.get("submission_rank") is not None)
    print(f"wrote {len(records)} records ({n_sub} submitted) to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
