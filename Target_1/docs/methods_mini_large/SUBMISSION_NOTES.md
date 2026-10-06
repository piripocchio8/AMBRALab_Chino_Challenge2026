# Submission notes

**Challenge:** EGFR Challenge 01, Anthropic x Adaptyv 2026.
**Deadline:** 6 October 2026, 23:59 AoE (UTC-12).
**Track:** Track 1 (cap 40).

## File to upload

`SUBMISSION.csv` — **23 designs**, ordered by ranking preference (row 1 = most preferred).
Nine carry their original sequence, five a surface/core polarity-optimised sequence, and
9 a round-5 alanine-biased sequence; the `sequence_origin` column records which and
`optimised_mutations` lists substitutions where applicable.

Required columns are present and first, exactly as the brief specifies:

| column | value |
|---|---|
| `name` | `pHsel-01` … `pHsel-23` |
| `sequence` | single-chain amino-acid sequence, 60–140 aa (brief allows 10–250) |
| `molecule_class` | `protein` for all 23 (single-chain, not nanobody/scFv/Fab) |

81 further columns carry the metrics, so the file can be submitted as-is without stripping. These
include eight PROPKA columns (`propka_*`) giving structural-pKa charge at pH 6.5 and 7.4 and the
best-histidine switching figures, populated for **all 23** designs.

## Design-count caps

| track | cap | our submission |
|---|---|---|
| Track 1 (labs/companies) | up to 40 | **23 — under the cap** |
| Track 2 (individuals/small teams) | up to 20 | 23 — over the cap by 3 |
| Track 3 (open) | up to 20 | 23 — over the cap by 3 |

**This file is sized for Track 1.** For Track 2 or 3, take the first 20 rows — they are already in
preference order, so `head -21 SUBMISSION.csv` is a valid 20-design submission and drops the three
lowest-ranked designs, all of which are round-3/4 composition-envelope violators or the two weakest
binders in the set.

## Two accepted designs are not in this file

Round 5 accepted 11 designs; 9 are submitted. The two held back, both for reasons outside the
acceptance gate:

| design | why not submitted |
|---|---|
| `R5_01` (187 aa, ipSAE 0.891) | **Length.** Would have ranked 3rd. Our cell-free expression evidence covers only 60–134 aa, and 187 aa is outside it. This trades against the length signal in `README.md` section 4, which points the other way — a deliberate choice, explained there. |
| `R5_11` (110 aa, ipSAE 0.602) | **Cross-species.** Passed both human folds but collapsed on the mouse ortholog (ipSAE 0.094, mouse bridge 10.8 Å); also the weakest human binder of the accepted set. |

Both are retained in `metrics/round5_all_metrics.csv` and `metrics/round5_ph_selectivity.csv`, which
carry all 11 accepted designs with a `submitted` flag and an `exclusion_reason`, so the full accepted
set stays recoverable from this repository alone.

## Names were reassigned in this round

`name` is assigned by cumulative rank, so **the `pHsel-NN` labels do not match the earlier 14-design
submission.** Use `local_id` (stable, round-internal, and the `designs/` directory name) or
`legacy_name` (the label this design carried in the 14-design file) to map between them. Round-5
`local_id`s are assigned over the full accepted set, which is why `R5_01` and `R5_11` are absent.
Nine designs were additionally re-ranked after their cysteines were replaced (METHODS 7c), which
moved names again; `local_id` and `legacy_name` were unaffected.

| submitted name | previous name | local_id | round |
|---|---|---|---|
| `pHsel-01` | `pHsel-01` | `R3_01` | 3 |
| `pHsel-02` | `pHsel-02` | `R4_03` | 4 |
| `pHsel-03` | — (new) | `R5_02` | 5 |
| `pHsel-04` | `pHsel-05` | `R4_04` | 4 |
| `pHsel-05` | — (new) | `R5_03` | 5 |
| `pHsel-06` | — (new) | `R5_04` | 5 |
| `pHsel-07` | — (new) | `R5_05` | 5 |
| `pHsel-08` | — (new) | `R5_08` | 5 |
| `pHsel-09` | — (new) | `R5_07` | 5 |
| `pHsel-10` | `pHsel-07` | `R4_07` | 4 |
| `pHsel-11` | — (new) | `R5_06` | 5 |
| `pHsel-12` | `pHsel-09` | `R3_07` | 3 |
| `pHsel-13` | `pHsel-03` | `R3_05` | 3 |
| `pHsel-14` | — (new) | `R5_09` | 5 |
| `pHsel-15` | `pHsel-04` | `R3_04` | 3 |
| `pHsel-16` | `pHsel-06` | `R3_03` | 3 |
| `pHsel-17` | — (new) | `R5_10` | 5 |
| `pHsel-18` | `pHsel-08` | `R3_06` | 3 |
| `pHsel-19` | `pHsel-11` | `R3_02` | 3 |
| `pHsel-20` | `pHsel-10` | `R4_05` | 4 |
| `pHsel-21` | `pHsel-12` | `R4_02` | 4 |
| `pHsel-22` | `pHsel-13` | `R4_01` | 4 |
| `pHsel-23` | `pHsel-14` | `R4_06` | 4 |

## Eligibility checks against the brief

- **de novo:** yes. Backbones are motif-scaffolded RFdiffusion3 from a geometric His–carboxylate
  motif; no existing binder, antibody framework or natural EGFR ligand was used as a starting point.
- **epitope:** domain III, the recommended epitope. The motif is built on target His433 and Asp460
  (UniProt P00533), both inside domain III.
- **length:** 60–140 aa, inside the 10–250 range.
- **molecule class:** single-chain protein, all 23.
- **metrics, structures, methodology:** included (`metrics/`, `designs/`, `METHODS.md`) — these are
  encouraged rather than required.
- **repository link:** this repository.

## Ranking basis

**ipSAE of the worst of the two human unconstrained folds, minus 0.030 per composition-envelope axis
violated.** Rationale and the two deliberate departures from the earlier basis (worst rather than
best fold; human folds only rather than all three) are in `README.md` section 3. The penalty is the
only non-mechanical term; `metrics/cumulative_ranking_inputs.csv` carries the inputs so the ranking
can be reproduced or re-weighted.

## Known weaknesses, stated plainly

- **Length.** 60–140 aa, median 117. The Adaptyv data associates higher hit rates with >= 200 aa
  (26.9% vs 9.8% at 100–200 aa, p = 0.00086). **No design here reaches 150 aa**, and the one that came
  closest (187 aa) was excluded on expression grounds. This is the clearest known weakness.
- **8 of 23 designs sit outside the confirmed-binder composition envelope**, all from rounds 3-4;
  `in_composition_envelope` and `risk_flags` mark them. All 9 round-5 designs are inside.
- **pH selectivity coverage is uneven.** PROPKA pKa and pH-dependent charge are computed for all 23
  designs; pH-dependent *binding* free energy (`ddG_bind_pH_REU`) exists for the 9 round-5 designs
  only. All of it is estimation, and Rosetta and PROPKA disagree by >1 pKa unit on the key anchor, so
  the magnitude is uncertain. 4 of 23 designs have no histidine in the switching window.
- **`predicted_cellfree_expression` is blank for the round-5 designs** — the rounds-3/4 model was not
  re-run, and a differently-derived number would not be comparable.
- **Unpaired cysteines reduced from 18 to 5.** 9 of the 12 affected designs were redesigned at the
  cysteine positions only (METHODS 7c); `pHsel-14`, `-16` and `-22` keep theirs because no
  substitution held the interface, and stay flagged `free-cys:N`. All were buried, which lowers the
  liability. `pHsel-02`'s two remaining cysteines form a genuine disulfide. Reported as
  `n_free_thiols` / `n_disulfides`.
- **No computational metric here strongly predicts binding** (see `analysis/what_predicts_binding.md`).
  The order is a preference, not a prediction.
