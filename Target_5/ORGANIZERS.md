# Information for the selection process

This file answers, point by point, what the selection process asks of a submission. Everything in
it is recomputable from the files in this directory; `_selftest/selftest.py` re-derives the checks
and prints its output to `_selftest/run_ok.log`.

## 1. Submission basics

| | |
|---|---|
| Track | **2** |
| Accounts | one; no shared team, nothing to merge |
| Designs submitted | 20, in `submission.csv` |
| **Ranking** | **the row order of `submission.csv`**, rank 1 first. `metrics_full.csv` carries the same order in `submission_rank`. The order is the four-criteria rule of `DESIGN_STRATEGY.md` §6 plus two adjustments to the first ten, both stated there: a cap of five designs from any one lineage, and two designs promoted for reaching the salt bridge 5 of 5 under a single declared contact |
| Chains per design | 1 |
| Length range | 25–62 residues, all within 10–250 |
| Alphabet | the standard twenty L-amino acids only |
| Classes | **miniprotein** ×19, **peptide** ×1 (`AMBRA_T5_19`, 25 residues) |
| `molecule_class` in the CSV | `single_chain` for all twenty, per the submission template |

## 2. De novo and zero-shot — what was and was not used

**No design in this submission is derived from, seeded with, templated on, or initialised from any
existing binder of this or any other target.** Every sequence was generated from scratch by the
design process described in `DESIGN_STRATEGY.md`. No known binder was used for training or
calibration either.

Two published entities appear in this work, and both appear **only as controls that were predicted
and measured, never as design input**:

- the therapeutic T-cell receptor of PDB **7OW6**, used as the positive control for the Asp6–Arg114
  measurement (42 of 50 models IN) and as the source of the 2.95 Å reference distance;
- a published de novo minibinder of a *different* pMHC, transplanted onto this groove as a
  specificity control (0 of 25 models IN).

Neither sequence contributed a residue, a fragment, or a starting point to any submitted design.
This is checkable: no submitted sequence has detectable similarity to either, and the controls are
reported with their own identifiers in `DESIGN_STRATEGY.md` §5.

**No tags, linkers, padding, or extra domains.** The submitted sequence is the binder chain alone —
exactly the chain that was folded, scored and deposited in `binder_alone.pdb`. Nothing was appended
to dilute a similarity score, and nothing in the design targets a construct tag: the restraint
tables and the scored contacts address the peptide and the HLA α1/α2 groove only.

## 3. Epitope — stated, not left to be predicted

The epitope is the peptide itself and the groove immediately around it, centred on **peptide
position 6**, the one residue that differs between the two peptide targets. The designed
interaction is specifically that the **Asp6 carboxylate engages HLA Arg114**.

`docs/epitope_contacts.json` lists, for each design, every peptide and HLA residue its deposited
G12D model contacts within 4.5 Å. Summary:

- **All 20** contact the decamer directly; **15 of 20** contact **Asp6** itself in the deposited
  model. The fewest decamer contacts are `AMBRA_T5_10` with two and `AMBRA_T5_18` with three.
  `AMBRA_T5_10` is the one design promoted on the restrained arm, and its
  `complex_G12D_Ile97_restrained.pdb` — the only such file in the deposit — holds the pose it was
  promoted for. For every other design the unrestrained complex is the evidence the ranking used.
- HLA contacts are 10–26 residues per design, **mostly** on the α1/α2 helices (57–84 and
  138–180); seven designs also touch residues outside those ranges, and the criterion is defined
  on the majority of contacts, not all of them (`docs/metrics.md`).
- Contacts are read from the deposited model, which is the **median** model of each ensemble on the
  Asp6–Arg114 axis, not the best one.

## 4. The three screens

Recorded for all twenty, same method for each.

| screen | where | note |
|---|---|---|
| **pLDDT** | `binder_plddt` (binder chain in the G12D complex) and `alone_plddt` (binder predicted with no target) in `metrics_full.csv` | ours, from the co-folding oracle; a ProteinTyper value is the organizers' to compute |
| **mean Kyte–Doolittle hydropathy** | `mean_kd_hydropathy` in `metrics_full.csv` | Kyte & Doolittle 1982 scale, unweighted mean over the whole chain. All twenty are hydrophilic (−1.23 to +0.25), consistent with cell-free expression and solubility |
| **ipSAE** | `ipsae_binder_target`, `ipsae_binder_peptide`, `ipsae_binder_hla` and `apo_ipsae_binder_target` in `metrics_full.csv`; `ipsae_method` in each `metrics.json` names every parameter | our own, from a **dedicated 5-model PAE ensemble folded for this purpose** — the campaign's earlier waves did not store PAE. Not pooled with the ranking ensembles. Median 0.583 against the whole target, range 0.014–0.813; `docs/metrics.md` has the parameters and the three designs that score ≈0 |
| **interface confidence** | `iptm_G12D` (binder↔decamer) and `iptm_restrained` in `metrics_full.csv`; per-chain-pair ipTM in each `metrics.json` | reported alongside ipSAE rather than in place of it |

Self-reported numbers are comparable within this submission only; they all come from one oracle
with one set of settings, and the per-model values behind every summary are in each `metrics.json`.

## 5. The three goals, each with the measurement that bears on it

Goals as stated for this run, hardest first.

**(a) No binding to the wild-type peptide VVVGAGGVGK on the same HLA.** Every design was predicted
on the wild-type complex under identical conditions. `margin_unrestrained` = ipTM(G12D) −
ipTM(WT); 15 of 20 are positive by the pre-set threshold, and the within-design standard deviation
of that margin is 0.0295, which is printed in `docs/metrics.md` so a small margin is not read as a
large one. The *structural* discriminator is stronger than the ipTM margin: the Asp6–Arg114 contact
that eleven of the twenty reproduce **cannot exist** on the wild-type peptide, which has glycine at
that position.

**(b) No binding to HLA + β2-microglobulin with no peptide.** Measured directly for this
submission: every design re-predicted as **three chains — binder, HLA heavy chain,
β2-microglobulin, no peptide record, no restraints** — five models each, through the same code
path and seed as every other unrestrained fold. `docs/peptide_free_control.md` has the full
result; the `apo_*` columns of `metrics_full.csv` carry it per design.

Every confidence measure falls: binder↔HLA ipTM in **20 of 20** designs by a median of **−0.265**,
the binder's own pLDDT in **20 of 20** by a median of **−8.2**, and ipSAE in **18 of 20**.
Structurally, however, **19 of 20 occupy the
seat the peptide vacated** (median 42.5 binder heavy atoms within 4 Å of the decamer's position), so
we do not claim peptide-free non-binding. `AMBRA_T5_12` is the exception and the one design with
positive evidence here. Two qualifications we state rather than leave to be found: goal (b) was
never an objective of the search, and the apo pose is not a realizable state — a peptide-free
class I heavy chain does not hold its fold, so this arm is a screen on what the oracle does with
an empty channel, not a verdict on an interaction that could be measured at the bench.

**(c) Strong binding to the G12D complex.** Twelve of the twenty reproduce the Asp6–Arg114 salt
bridge with nothing declared at all — `AMBRA_T5_05` in 14 of 20 models, with the largest
G12D-versus-wild-type margin in the campaign (+0.370) — and four more reproduce it under a single
declared contact (Asp6 to HLA Ile97, 6.5 Å — a condition that does not name Arg114), three of those
in 5 of 5 models.
Sixteen of the twenty therefore produce the discriminating interaction under one condition or the
other; `IN_unrestrained` and `IN_restrained` are kept as separate columns so the two are never
conflated. Beyond that: `iptm_G12D`, `on_groove` (20 of 20 designs place the
binder on the α1/α2 groove in ≥60% of unrestrained models), `engaged`, and the IN counts.

## 6. Method family, and what is not disclosed

**Family:** forward-folding sequence design against a structure-prediction oracle — the
hallucination family, in which the oracle is queried, not differentiated through — with
**ProteinMPNN** redesign of delivered sequences inside their own predicted complexes, and terminal
elongation followed by redesign. The co-folding oracle throughout is **Chai-1**. If families are
bucketed, this submission belongs with forward-folding/hallucination methods, not with diffusion
backbone generation (no RFdiffusion, no backbone diffusion of any kind was used) and not with
inverse folding alone.

**Declared AI tools:** Claude (Claude Code) for orchestration, analysis and documentation; Chai-1
as the structure oracle; ProteinMPNN for sequence redesign.

**Not disclosed:** the internals of the sequence-search engine, which is the subject of a
manuscript in preparation. Nothing needed to *evaluate* these designs is withheld — sequences,
structures, per-model measurements, the selection rule, the controls, and what the restraint
tables did and did not declare are all here. What is held back is how candidates were *generated*,
not how they were *judged*. We will release the engine with the publication and are glad to
discuss it in confidence with the organizers.

## 7. Where this submission is weak

Stated by us rather than left to be found:

- **Eight of the twenty do not clear the IN criterion.** They are deposited on the other three
  criteria and their IN counts are reported with denominators and intervals.
- **`AMBRA_T5_10` contacts only two decamer residues in its deposited model.** It is the design
  promoted for reaching the salt bridge 5 of 5 under the single Ile97 contact; in the fully
  unrestrained pose its grip is on the HLA rather than on the decamer, and the promotion and its
  reason are recorded in `DESIGN_STRATEGY.md` §6 rather than hidden in the ranking.
- **`peptide_register_rmsd_A` is blank for `AMBRA_T5_05`.** That design was folded after the
  register audit ran and the column was not recomputed for it before the deadline. It is a
  reported-not-ranked column; the other nineteen sit between 0.72 and 1.99 Å.
- **Two designs stand at five models** rather than twenty (`AMBRA_T5_18`, `AMBRA_T5_19`); their
  intervals are correspondingly wide.
- **Five of the top ten share one lineage**, which is the cap we set. The set as a whole spans
  nine lineages and the first ten span six, but a screen limited to the first few still tests
  fewer independent hypotheses than the count of designs suggests.
- **Everything is predicted structure.** No experiment was performed, and three systematic
  behaviours of the oracle that bear on reading these numbers are quantified in `docs/metrics.md`.
