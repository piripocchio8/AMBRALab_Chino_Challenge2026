# Target 4 — what every column in `metrics_full.csv` means

Target 4 is a de novo binder deposition against a 189-residue target window in two orthologues,
**H** and **M**. `submission.csv` carries only the three columns the upload form defines
(`name`, `sequence`, `molecule_class`); everything below is the companion metric table, one row per
deposited design.

Every number comes from **one** oracle configuration, stated in the `oracle` column: boltz-2, the
189-residue window, the design's own declared pocket, `msa: empty`, seed 2000, five diffusion
samples. That configuration is the only one of all those tried that reproduced a deposited
co-crystal structure (2.86 Å on B1). A blank cell means **not measured**, never zero.

---

| column | meaning |
|---|---|
| `sequence` | the designed peptide, one letter per residue |
| `name` | deposition id, `AMBRA_T4_<band>_<nn>` |
| `band` | `h_anchored` or `dual_lean` — see below |
| `submission_rank` | 1–20, `h_anchored` first then `dual_lean`, each band ordered by its own band criterion |
| `run_id` | the design's run identifier in the campaign; the family prefix is the only surviving record of its declared pocket |
| `design_family` | which wave produced it, with that wave's pocket |
| `design_stage` | 1 or 2; stage 2 is a re-search in which M was visible |
| `binder_length` | residues |
| `cys_count` | cysteines in the sequence |
| `pocket_H`, `pocket_M` | the declared pocket columns, **fragment-local** in the 189-residue window, 1-based. These differ between orthologues only for the stage-1 family (17 vs 18). |

## The confidence columns

| column | meaning |
|---|---|
| `boltz_iptm_H_mean`, `boltz_iptm_M_mean` | ipTM averaged over the five models. **This is the ranking quantity.** |
| `boltz_iptm_H_best`, `boltz_iptm_M_best` | the single best of five, carried so the mean can be read against its own spread |
| `boltz_plddt_H`, `boltz_plddt_M` | complex pLDDT, mean over five models, 0–1 |
| `n_models_H`, `n_models_M` | always 5 |
| `threshold` | 0.6428, the same for every row |
| `clears_threshold_H`, `clears_threshold_M` | whether `*_mean` ≥ threshold |

**`clears_threshold_M` is `false` on every row in this deposit.** That is the result, not an
omission; see `README.md`.

### What ipTM here is and is not

T = 0.6428 is the ipTM this oracle assigned to the one deposited complex it reproduced below 5 Å.
A design clearing T has earned the statement *the oracle is as confident about this as it was about
the complex it got right* — and no more. On the same five controls, the same oracle reports 0.85
ipTM on a pose 17.6 Å from the crystal structure, so a high ipTM is compatible with the wrong
answer. Do not read these as probabilities of binding.

**The M columns have no calibration at all.** The threshold is derived from H-side controls. The
deposited binders are not known to bind the paralogue, so there is no molecule whose M complex the
oracle could be checked against, and an M ipTM is a measured number with no positive control behind
it. It cannot distinguish a weak binder from the oracle's ceiling on that surface.

## The pose column

| column | meaning |
|---|---|
| `pose_disp_H_A`, `pose_disp_M_A` | binder CA RMSD about the medoid pose over the five models, after superposing on the target, in Å |

**Reported for every design, used to include or exclude none of them.** The campaign's
pre-registered 6.0 Å dispersion gate was calibrated on Chai-1; on this oracle it rejects 4 of the 5
molecules that have deposited co-crystal structures, so enforcing it here would carry that
miscalibration into the deposit. Read it as the spread of five samples: a small number means the
five models agree, which is not the same as agreeing with reality.

## The provenance column

| column | meaning |
|---|---|
| `search_iptm` | the Chai-1 interface ipTM recorded by the design search that produced the sequence |

Kept for provenance only. It comes from a different oracle under different conditions and is **not**
comparable to the `boltz_iptm_*` columns; it played no part in the ranking, and was used only to
pick the survivor when the same sequence was delivered by more than one run.

## The two bands

| band | n | selection |
|---|---|---|
| `h_anchored` | 15 | highest `boltz_iptm_H_mean` among designs clearing T on H |
| `dual_lean` | 5 | highest `boltz_iptm_M_mean` among the designs not already taken; none clears T on H |

The bands are not two halves of one ranking. `h_anchored` is ordered on the axis where the oracle
has a verified true positive; `dual_lean` is ordered on an axis with no control at all, and exists
because the brief asks for a dual binder. Comparing a rank in one band with a rank in the other is
arithmetic on two different scales.

## Population

The twenty were drawn from 70 unique designs recovered from 129 runs across every wave and host,
deduplicated by sequence. The full ranked population, with both orthologues' numbers for all 70, is
in `docs/ranking_all.json`.
