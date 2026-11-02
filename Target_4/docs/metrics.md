# What every column in `metrics_full.csv` means

One row per deposited design. `submission.csv` carries only the three columns the upload form needs
(`name`, `sequence`, `molecule_class`); this file is the companion table.

**H** and **M** are the two orthologues of the target — the same protein from two species, 640 and
641 residues. Every number comes from one prediction setup: **boltz-2, full-length target,
evolutionary alignments (MSAs) supplied for both chains, the design's own target site declared as a
soft 8 Å restraint, 5 predicted models, seed 2000.** That setup is the only one, out of everything
we tested, that reproduced a published experimental structure of a real binder of this target
(2.8 ± 0.3 Å, 5 of 5 models). A blank cell means *not measured*, never zero.

## Identity

| column | meaning |
|---|---|
| `name` | deposition id, `AMBRA_T4_01` … `_20` |
| `sequence` | the designed peptide |
| `submission_rank` | 1–20; see "How the order is set" below |
| `run_id` | internal identifier of the design run that produced it |
| `design_family` | which design round it came from |
| `designed_against` | which orthologue that round optimised against |
| `binder_length` | residues |
| `cys_count` | cysteines in the sequence |
| `pocket_H`, `pocket_M` | the target site this design was aimed at, as residue positions **within a 189-residue region** of the target. Different rounds aimed at different sites, so this differs between designs. |
| `search_iptm` | the score recorded by the design engine when it produced the sequence. **Provenance only** — a different program under different conditions, not comparable with the `boltz_*` columns, and it played no part in the ranking. |

## Prediction confidence

| column | meaning |
|---|---|
| `boltz_iptm_H_mean`, `boltz_iptm_M_mean` | interface confidence, 0–1, averaged over the 5 predicted models. **This is what the ranking uses.** |
| `boltz_iptm_H_best`, `boltz_iptm_M_best` | the single best of the 5, so the mean can be read against its spread |
| `mean_iptm` | mean of the H and M values — the ordering quantity |
| `target_plddt_H`, `target_plddt_M` | how confidently the program folded the **target** itself (0–100); here 93–95. This matters: a program that fails to fold the target still emits a confident-looking interface score, so this is the check that the interface numbers mean anything. |
| `n_models_H`, `n_models_M` | always 5 |
| `threshold_T_full` | 0.6278 — the confidence the method assigned to the one published binder it predicts correctly |
| `clears_T_full_H`, `clears_T_full_M` | whether this design reaches that confidence |

**`clears_T_full_*` is `False` on every row.** That is the result, not an omission: no design among
103 candidates reaches the confidence of the one real binder the method gets right (0.628; our best
≈ 0.52).

**High confidence does not mean a correct answer.** In this same setup one published binder scores
0.714 — higher than the binder the method predicts correctly — on a prediction 19 Å from its
experimental structure. Treat these as an ordering, not a probability of binding.

## Whether the peptide reaches its site

| column | meaning |
|---|---|
| `epitope_models_H`, `epitope_models_M` | in how many of the 5 models the peptide comes within 8 Å of its declared site |
| `min_dist_to_pocket_H_A`, `min_dist_to_pocket_M_A` | median closest approach to that site, in ångströms |

**Reported, and deliberately NOT used to select.** With the site declared, all three published
control binders reach it in 5 of 5 models — *including the two whose predictions are 17–19 Å
wrong*. With it not declared, all three fail 5 of 5 — *including the one that is right*. The
restraint steers the peptide to the site; it does not judge whether it belongs there. All 103
designs score 5/5, so this column separates nothing.

## The artefact column

| column | meaning |
|---|---|
| `sinkfrac_fulllength_H`, `sinkfrac_fulllength_M` | fraction of the peptide's contacts landing on one particular hydrophobic patch of the target |

Earlier work evaluated designs against a 189-residue fragment cut from the target. Cutting exposes
a surface normally buried inside the intact protein, and predicted peptides are strongly drawn to
it — a design can score well while sitting in the scar of the cut rather than on its intended site.
On the fragment this reached **0.78**; on the full-length protein used here it is **0.00–0.07**,
confirming the artefact is absent.

## The selection columns

| column | meaning |
|---|---|
| `scramble_iptm_H`, `scramble_iptm_M` | confidence for the **same peptide with its residues shuffled into random order** — same composition, same length, same target, same site, same MSAs |
| `gap_vs_scramble_H`, `gap_vs_scramble_M` | design minus shuffle; positive means the design outscores its own shuffle |
| `beats_own_scramble_both` | `True` on every deposited row — **this is the selection criterion** |
| `scramble_tested` | `True`; all 103 candidates were tested |

A design that does not beat its own shuffle has a score explained by what it is *made of* rather
than how it is *arranged*. Across all 103 candidates the design beats its shuffle on M in 80/103
(sign test p = 7.3 × 10⁻⁹) and on H in 63/103 (p = 0.015). A control for a possible confound — that
supplying an MSA for the peptide itself inflates its score, which shuffles never receive —
measured **+0.010**, well below the median advantage of +0.035. Read any gap smaller than ~0.01 as
uninformative.

## How the order is set

1. Keep only designs that beat their own shuffle on **both** orthologues (54 of 103).
2. Order those by `mean_iptm`.
3. Take the top 20.

It is **not** the worse of the two scores and **not** an average over designs. Both per-orthologue
numbers ship here so any other rule can be recomputed. `docs/ranking_all.json` holds all 103
candidates, including those that failed the shuffle control.
