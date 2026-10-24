# What each column of `metrics_full.csv` means

> `submission.csv` is the file submitted to the challenge and carries **only** the three columns
> the template defines — `name`, `sequence`, `molecule_class` — with `molecule_class` =
> `single_chain` for every design. Everything measured lives beside it in `metrics_full.csv`,
> keyed by the same `name`, so the submission stays in the required format while nothing is lost.
> The same fields, per design, are in `micro/<name>/metrics.json`.
>
> Both files are built by `scripts/make_target2_submission.py` from `docs/ranking.json`. The script
> refuses to write a row carrying a `[[PENDING: … ]]` marker, because a marker that reaches a
> deposited file is indistinguishable from a result.

Not every column is filled for every row. A blank means **not measured**, never *measured as zero*.
Three blanks are deliberate and are explained where they occur: `selection_score` on a design that
is a family original rather than a repack, `n_interface_his_seed` on the same, and
`approach_K104_human_A` has **no mouse counterpart at all** because mouse position 104 is a proline.

> **Nothing in this table measures protonation.** No protonation state was varied anywhere in this
> campaign; the oracles are heavy-atom only. The `dpka_*` columns are a predicted pKa *shift between
> two coordinate sets*, and the human-minus-mouse columns are a difference between two orthologs
> that differ in sequence and length. Neither is a pH measurement.

## What was measured, and what was not

Said once, in front of the table, because a column list is a poor place to discover an absence.

| planned for this target | status on the delivered band |
|---|---|
| binder approach to Lys57, per ortholog | **measured**, 5 models per design per ortholog |
| binder approach to Lys104 | **measured** on human; **does not exist** on mouse (Pro104) |
| count of binder histidines at the interface, per ortholog | **measured** |
| binder pLDDT, binder pTM, interface ipTM, per ortholog, three oracles | **measured** |
| symmetry-aware binder pose spread | **measured** on the primary oracle's human arm |
| predicted pKa drift | **measured** on the primary oracle's human arm only |
| **seating fraction** — both designed histidines within 7 Å of the epitope on one protomer | **not computed for this band.** It was the previous round's instrument; this round measured the three geometric quantities above instead. The column is absent rather than filled from another arm |
| **restraint-free approach to Lys57** | **not measured on this band.** Every fold it was cut on carries the 8 Å pocket. The previous round's restraint-free numbers are quoted in `methods_micro.md` §5 and are not per-design columns here |
| **hydrogen-bond partner of each histidine** | **not computed for this band** |
| **ipSAE** | **measured** for all three oracles, both orthologs, all 325 designs, on the canonical Dunbrack scale (raw per-token PAE, 10 Å cutoff, maximum over the three (protomer, binder) pairs and both directions, median over models). **It is not a second axis on this target:** within oracle, ρ(ipSAE, interface ipTM) is +0.867 (primary), +0.879 (Protenix) and +0.972 (Boltz-2), and 60.6 % of primary-oracle and 62.8 % of Protenix designs sit at or below the metric's own floor of 1/(1 + 10²) = 0.0099, with 51 % of Protenix designs exactly 0. "ipSAE + ipTM" here is close to 2 × ipTM. **Read the deposited values against the population, not instead of it:** over the 30 deposited designs `ipsae_human` averages **0.139** and none sits at the floor, against a population mean of 0.0355 with 60.6 % at or below it — the deposited designs are selected for fold and interface confidence, and ipSAE tracks those, which is the same fact stated from the other side. The separate observation that the primary oracle returned exactly 0.000 on all 540 **restrained** models of the **previous** round remains true of that round and is in the methods; it is no longer the reason this column is or is not carried |

## Identity and provenance

| column | meaning |
|---|---|
| `name` | the deposited identifier, `AMBRA_T2_micro_01` … `_20` for the submitted band and `_21` … `_30` for the ten documented designs that are not submitted |
| `sequence` | the binder sequence, as submitted; 39 residues, the twenty standard amino acids |
| `molecule_class` | `single_chain` for every row — the upload form enumerates `single_chain`, `nanobody`, `scfv`, `fab_kappa`, `fab_lambda`, and the build refuses anything outside that list |
| `status` | `submitted`, or a sentence saying why a documented design is not part of the submission. Twenty rows are `submitted`; `AMBRA_T2_micro_21` … `_30` carry the sentence |
| `submission_rank` | the position the upload form reads, 1 first. It is the design's position on **`worse_ortholog_iptm`**, the lower of the two orthologs' interface ipTM, descending — never the mean, never the maximum, never the difference. **The order is not supported by the data** — see the band note below. Absent on a row that is not submitted, and the build refuses a submitted row without it |
| `binder_length`, `series` | 39 and `micro` for every row |
| `cyclisation` | `disulfide_1_39` — a real Cys1–Cys39 bond, not a head-to-tail amide |
| `target_epitope`, `mechanism` | the epitope the design was aimed at and how it was meant to engage it. **Objective, not observation** |
| `parent_family` | designs sharing a backbone carry the same family tag. **10** families over the 20, with at most **4** designs in any one — reported, not capped |
| `design_origin` | `parent` for a family original, `repack` for an inverse-folding rebuild of one. **0 and 20**: no family original cleared the fold floor on both orthologs |
| `design_round` | which round of the campaign produced the sequence |

**Campaign identifiers are deliberately not carried into this directory.** The deposited names and
the family tags are the only provenance here, for the same reason the design engine is described in
principle rather than in detail: the method is the subject of a manuscript in preparation. Nothing
needed to *evaluate* these designs is withheld.

## The membership bar

| column | meaning |
|---|---|
| `n_interface_his_seed` | histidines at interfacial binder positions in that design's own seed structure, which is where the bar was applied. Blank on a family original, because the bar selected repacks |
| `interface_cutoff_A` | 8.0 — a binder position is interfacial when any of its heavy atoms lies within 8.0 Å of any target heavy atom |
| `n_interface_his_human`, `n_interface_his_mouse` | the same count re-measured **in the folded complex**, median over the five models. This is a count of histidines touching the target; it is **not** a statement that they touch the lysines |
| `his_positions` | every histidine position in the binder, 1-based |
| `n_his` | how many there are. **2 for 17 designs and 3 for 3** in this band |
| `selection_score` | the inverse-folding model's own score for a repacked sequence. Used to **order** qualifiers, never to filter them — the two are essentially unrelated (pooled Spearman −0.078 over 3,960 variants) and the score-best decile is *depleted* in interfacial histidines. Blank on a family original, which was never scored by it |

## Where the binder sits relative to the epitope

Every value is a **median over all five models** of that design and ortholog, never a best model:
the primary oracle is nondeterministic here — the same sequence and seed can give poses about 9 Å
apart — so the best of *n* draws is a property of *n*.

| column | meaning |
|---|---|
| `approach_K57_human_A`, `approach_K57_mouse_A` | minimum distance from **any** binder heavy atom to the NZ of Lys57, minimised over the three protomers. **Read it with the restraint in front of it:** every fold carries an 8 Å pocket on Lys57, and on this arm that pulled nine deciles of the 325 to 2.4–3.7 Å, which made the 5.0 Å gate inert at 99.1 % |
| `approach_K104_human_A` | the same quantity for Lys104, the **unrestrained** half of the designed pair. Over the band it runs 3.53–11.10 Å with a median of 7.81 Å and **7 of 20 within 7 Å**. There is no mouse counterpart: mouse 104 is a proline, the equivalent lysine is 103, and the two were never differenced |
| `n_models_human`, `n_models_mouse` | how many independent models the figures above are computed from. Read these first: a median over five models is a median over five models. 5 and 5 for every row, counted from the deposited files |

## Pose: is it the same place every time?

| column | meaning |
|---|---|
| `pose_sym_lrmsd_human_A` | **symmetry-aware** mean binder Cα RMSD over every *pair* of the five models. For each pair, the target trimers are superposed under each of the six protomer relabellings; a relabelling is admissible when the target Cα RMSD falls under 3.0 Å; the reported value is the **minimum binder RMSD over the admissible relabellings**. Reference-free: no model is privileged, because a scattered set's own best pose sits in the middle of the scatter |
| `pose_sym_converged_human` | true when that mean is under 8 Å. **14 of 20** |
| `pose_cross_redraw_lrmsd_A` | the same statistic between this design's five models and five more from an **independent re-draw** of the primary oracle at a different seed. Measured on the 50-design replicate pool only, so it is **blank for the three delivered designs outside it** — blank meaning not measured, never zero |

**Why the relabelling is not optional.** The target is a C3 homotrimer with three chemically
identical sites, and nothing forces a predictor to give the same physical copy the same letter
twice. Measured over 3,250 model pairs per oracle: exactly 3 of the 6 relabellings are admissible in
100 % of pairs, the admissibility distribution is bimodal with an entirely empty gap between 1 Å and
15 Å, and the primary oracle happens to label consistently (0 of 3,250 pairs mis-register) while the
second oracle does not (38.3 %). A metric that assumes the identity labelling therefore reports the
second oracle's within-oracle spread as **22.1 Å with 7.1 % of designs converged** when the correct
figures are **14.1 Å and 21.5 %**. Any pose number anywhere in this repository is the symmetry-aware
one; the confounded figures are not used and should not be reproduced.

**A warning that belongs with this column.** ρ(primary-oracle interface ipTM, within-oracle pose
spread) = **−0.661** over all 325 designs, and ρ(interface ipTM, cross-redraw pose spread) =
**−0.600** over the delivered 50. The axis the band was ordered on and the pose-convergence label
are largely the same label.

## Fold confidence

| column | meaning |
|---|---|
| `binder_plddt_human`, `binder_plddt_mouse` | mean **per-token** pLDDT over the binder's 39 tokens, 0–1, median over models. The per-atom route from the model's own B-factor column differs from it by 0.0034 ± 0.0023 (maximum absolute difference 0.0137, n = 1,625 models) and is not the route used. **This is the gate that does the work**: at ≥ 0.50 it passes 53.2 % of the 325 |
| `binder_ptm_human` | the binder chain's own pTM. On a 39-mer it sits near a short-chain floor and moves little with binding; it is reported, not ranked on |

**On the pLDDT cutoff, and the floor that was added above it.** The G2 gate is at 0.50, a
precondition ("the binder has a predicted structure") rather than a disguised ranking. **A separate
floor at 0.65, applied to `binder_plddt_human` AND `binder_plddt_mouse`, is what decides membership
of the delivered band**, and it was added after the ordering had been computed, as a project
decision. It leaves **34 of 325**, of which **30** also clear every primary-oracle gate; the band of
20 is the top of those 30 on the ranking key, and the other ten are documented with a `status`.

**Why 0.65 and not higher.** Applied to both arms, 0.70 leaves 10 designs from 4 backbone families
and 0.68 leaves 18 from 6 — neither can fill a band of 20. 0.65 leaves 30 from 10. 0.62 would leave
42 and move the worse-ortholog ipTM at pool rank 20 from 0.2008 to 0.2014. The previous round
reported a 0.70 figure as a caution — nothing in 900 of its restraint-free models reached it
(maximum 0.658) while the same designs' restrained refolds on the smaller design-time construct ran
0.703–0.779 — but the restraints and the assembly both differ there, so that figure does not
transfer to this round's instrument and construct.

**The floor sits on an axis that reproduces.** All 17 delivered designs with an independent re-draw
still clear 0.65 on both orthologs at a different seed, the per-design change being −0.0002 ± 0.0054
on human and −0.0002 ± 0.0067 on mouse (n = 17). Two designs nevertheless sit closer to the floor
than that spread — `AMBRA_T2_micro_04` is 0.0011 above it on mouse and `AMBRA_T2_micro_12` is 0.0016
above it on human — and for those two the gate is met **within the instrument's own error**.

## Interface confidence: the axis this band was ranked on


| column | meaning |
|---|---|
| `interface_iptm_human`, `interface_iptm_mouse` | the maximum of the protomer-binder entries of the per-chain-pair ipTM matrix, both orientations, median over the five models, with `_sd` beside it. Maximum rather than mean over the three protomers: the binder engages one, and averaging over three dilutes a real interface by a factor of three |
| `interface_iptm_human_redraw8300`, `interface_iptm_human_redraw9300`, `interface_iptm_mouse_redraw8300` | the same quantity from independent re-draws of the primary oracle at different seeds. They are **evidence about the measurement**, not better estimates, and are never averaged into the first draw |
| `iptm_H_minus_M`, `iptm_H_minus_M_redraw` | the human-minus-mouse difference. **Reported, and not a selection criterion**: it gates nothing and orders nothing, and **no ortholog preference is claimed for this band**, whose objective is that *both* orthologs are bound. Over the 20 it runs −0.3404 to +0.3836, positive for 8 and negative for 12. The reason it is not used is measured: it is reproducible within this oracle (**ρ = +0.948 [+0.926, +0.964], n = 325**, both orthologs independently re-drawn) and **shared with no other** (ρ = **+0.0533 [−0.0569, +0.1580]** with the second oracle and **+0.0566 [−0.0582, +0.1713]** with the third, **every interval containing zero**; the second-oracle figure is **8.3 %** of what their two reliabilities make attainable), so it is a property of *(design, oracle)*, not of *design*. It is **not** a pH measurement |
| `worse_ortholog_iptm`, `worse_ortholog_which` | the lower of the two, and which ortholog it was. **`worse_ortholog_iptm` is this band's ranking key** — `submission_rank` is its descending order. **Never an average**: a design that works on one ortholog and not the other is not cross-reactive, an average hides exactly that, and ranking on the worse arm makes such a design rank low by construction. The worse arm is mouse for 8 of 20 and human for 12. **For five designs the two arms are closer together than the measurement's own draw-to-draw spread (0.0134), so the letter is a tie and not a result**: `_01`, `_03`, `_10`, `_14`, `_15` |

**This column ordered the band, and the evidence against ordering on it was not withdrawn.** Over
100 design-species pairs of the previous round the binder's pair-interface pTM tracks **how
confidently the binder folded** (r = +0.634) and not the engagement it is supposed to stand for; its
partial correlation with the measured histidine distance, controlling for binder pTM, moved from
**+0.048 at n = 78 to −0.155 at n = 100**. On this round's 325 designs ρ(interface ipTM, binder
pLDDT) = **+0.714**. The band is ordered on a quantity that is largely about foldedness and pose
rigidity, and should be read that way.

A second warning about the same family of numbers: the second oracle's largest interface score in
its pocket arm belongs to the design with the **worst** binder confidence and the **largest**
histidine distance. Read interface confidence beside a measured distance or not at all.

## The second and third oracles

Every design in this round was folded by the primary oracle and by **Boltz-2**, each given the same
single statement: an 8 Å pocket on Lys57 of one protomer, with **no** histidine-to-lysine contact
row and **no** disulfide row. The top 50 were additionally folded by **Protenix**, which carried
**no restraint at all** — its input JSON holds only the sequences, verified by reading the file. The
column names say so.

| column | meaning |
|---|---|
| `boltz_interface_iptm_human`, `_sd`, `boltz_interface_iptm_mouse`, `boltz_iptm_H_minus_M`, `boltz_binder_plddt_human`, `boltz_worse_ortholog_iptm` | the measures above recomputed on the second oracle's own five models per arm |
| `protenix_unrestrained_*` | the same on the third oracle. The `unrestrained` in every name is load-bearing: this arm is a reading of a different experiment |
| `boltz_in_own_top20`, `protenix_in_own_top20` | true when that oracle places this design in **its own** top 20 of the same 50, by its own human-arm interface ipTM. The rule was stated before it was computed |
| `oracles_placing_it_in_their_own_top20` | 1, 2 or 3. The primary oracle counts for 1 by construction, since the 20 are its own top 20 |

**The confidence scores of the three oracles are not on a common scale and are never averaged into
one number**, and they do not agree about binding. At n = 50 the three pairwise Spearman
correlations on interface ipTM are +0.194, −0.195 and −0.026, **all with intervals containing
zero**, while the three on binder pLDDT are +0.694, +0.576 and +0.326, **all excluding it**. Over
the 20, the second oracle agrees on 7 and the third on 9, with 3 in both, against 8 and 3.2 expected
by chance. That disagreement is reported as a figure in its own right, because if the oracles
disagree about which designs are good, that changes what a ranked band means.

## Does the selection survive an independent draw?

| column | meaning |
|---|---|
| `survives_redraw_seed8300`, `survives_redraw_seed9300` | whether this design is still in the top 20 of the same 50 **by the primary oracle's human-arm interface ipTM** when it is re-run with only the **structure-prediction seed** changed (8300 and 9300, against 7300 for the first draw). The same seeds name the `interface_iptm_*_redraw*` columns. These are the predictor's own random seeds; nothing about how the sequences were generated differs between draws. **This tests a human-arm ordering, which is neither this band's gate nor its ranking key**, and it is defined on the 50-design replicate pool: 7 of the 17 delivered designs it is defined for survive at 8300 and 8 at 9300, and it is **blank** for the other three. The rule this band actually turns on reproduces: 17 of 17 still clear the 0.65 floor on both orthologs, and the worse-ortholog key returns at ρ = +0.9447 [+0.7970, +0.9897] with 17 of 17 inside the re-drawn top 20 |

The *selection* reproduces; the *order* and the *boundary* do not. Ranks 17–24 of the 50 span 0.045
interface ipTM and ranks 20 and 21 are 0.0073 apart. And reproducibility is not quality: see the
−0.600 against cross-redraw pose spread, above.

## Gates

| column | meaning |
|---|---|
| `gate_G1_approach_K57` | median approach to Lys57 NZ ≤ 5.0 Å. **Inert on this arm** (99.1 % of 325), because the 8 Å pocket produced contact |
| `gate_G2_binder_plddt` | median binder pLDDT ≥ 0.50. The informative gate, 53.2 % |
| `gate_G3_interface_his` | median interfacial binder histidines ≥ 2. 89.2 % |
| `gate_pass_all` | all gates including the two integrity checks (chain contract A=149 B=149 C=149 D=39 with ≥ 3 parsed models, and no inter-chain clash in more than half the models), both of which pass 100 % by design |
| `gate_binder_plddt_human_0p65`, `gate_binder_plddt_mouse_0p65` | the **binder-pLDDT floor at 0.65**, the criterion that decides membership of this band. It is applied to **both** orthologs, so both columns are true for every submitted row by construction |
| `boltz_state` | the second oracle's own quality-gate verdict, `pass` or `fail`. **Reported, not applied**: it does not exclude from this band, and three submitted designs carry `fail` |
| `gate_waived` | the bar a design missed and by how much, where a slot was filled by the best-scoring design missing exactly one. Blank for every row here: **no gate was waived**, and the gate is never loosened to admit a design |

Gates, not penalties: a weighted sum lets a design that fails badly on one axis be carried by the
others, so membership is decided by bars and order by the rule above.

**The gate columns above are the primary oracle's. The second oracle applied the same four gates to
its own models, and that built the top 50 — it does not gate this band.** Of the 148 designs
clearing the primary oracle's gates, **95** also clear Boltz-2's and **53** were demoted to a
reserve tier below them — 31 on Boltz-2's binder-pLDDT gate, 15 on its interfacial-histidine count,
4 on its Lys57 approach, 3 on two. The 50 that the three-oracle and mouse passes ran on is the top
50 of the **95**. **For the delivered band that gate is relaxed**: the band is cut from all 325 by
the pLDDT floor plus the primary oracle's gates, `boltz_state` is carried as a per-design column,
and three submitted designs are ones Boltz-2 demotes. Keeping the gate would have left 18
qualifying designs rather than 20; it was relaxed because the oracles disagree on the **binding**
axis, where the agreement is a single-digit percentage of attainable with an interval containing
zero, while the floor that now cuts the band is on the **foldedness** axis, where they agree. It
does not follow that the second oracle's opinion is worthless, which is why every Boltz-2 figure is
still carried per design.

## Predicted pKa drift

| column | meaning |
|---|---|
| `dpka_his_best_human` | propka run **twice on the same coordinates**, once on the complex and once on the binder alone, so nothing but the target's presence differs. For each binder histidine, `pKa(complex) − pKa(free)`; per model the **maximum** over the binder's *surface* histidines (propka buried fraction below 50 % **in the free binder**, measured free on purpose, because measuring burial in the complex would disqualify exactly the histidines that engage); per design the median over models |
| `dpka_his_human_spread`, `dpka_his_human_n_models` | how far the value moves between models of the same design, and the denominator. A shift that varies by several pH units between models is not a measurement of that design |

Computed on the primary oracle's human arm only. A tiebreak computed on a partial, shard-ordered
subset of another arm would be a different tiebreak for different designs, so the other arms are
named as not computed rather than proxied.

**Read this axis with its limitation in front of it, and then read the number.** propka is additive
and has no term for a geometry that *requires* a charged ring: burying a histidine against the
target moves its desolvation penalty strongly negative, so an engaged, buried histidine can read as
a negative shift, and the axis tends to reward histidines that stay solvent-exposed. Over the
delivered 20 it runs **−1.39 to +0.68 with a median of −0.27 and only 2 of 20 positive**; over all
325 designs the median is −0.01 and only 22 % are positive, and ρ(interface ipTM, pKa drift) =
−0.155. **This arm shows no protonation-driven selectivity signal** — the histidines that engage are
the ones propka penalises, and the ones it rewards stay in solvent. In the previous round the axis
was also orthogonal to everything preceding it (Spearman +0.12 to +0.15 against interface
confidence, binder pLDDT and pose spread) and could not separate the top four designs.

**One conclusion drawn from this axis has already been withdrawn.** An earlier reading — that the
histidines which titrate are not the designed ones — was an artefact of the **restrained** folds it
was computed on: the restraint buries the designed histidines against their lysines. On
restraint-free coordinates they come back into the window (2.10 → 6.55 and 4.27 → 6.16 on one
design's mouse fold). The column is reported with the arm it was computed on.

## Composition

`n_cys`, `n_lys_arg`, `n_asp_glu`, `frac_hydrophobic_AVILMFWY`, `gravy` and `risk_flags` are
computed from the sequence alone and are **reported, not optimised**. A convincing design is allowed
to be awkward to make. `gravy` is the mean Kyte-Doolittle hydropathy over the 39 residues.

**Charge is given as counts rather than as a net charge at a stated pH, on purpose.** The mechanism
is about the binder's own histidines, and a single net-charge number absorbs exactly those into a
titration model that this campaign never tested. `n_his` and `his_positions` are the columns that
matter for the mechanism; `n_lys_arg` and `n_asp_glu` give the permanent charges either side of it.

`risk_flags` carries anything a reader would otherwise have to find by eye: a design with more than
two cysteines, so that the Cys1–Cys39 pair is not its only possible disulfide; a pose flag; and the
note on the three designs the second oracle demotes. One design, **`AMBRA_T2_micro_09`**, carries
three cysteines and is flagged rather than excluded.

## The honest reading

Every number here describes a **prediction**. None of these designs has been measured, and nothing
here varies pH. What the measurements support is that these binders reach the **Lys57** face of the
trimer under a restraint that asks them to, that 14 of the 20 reproduce their own pose within 8 Å
across five models, and that the rule they were selected by — a binder pLDDT of at least 0.65 in
**both** complexes, ranked on the worse of the two orthologs' interface confidence — is a property
of the designs rather than of one prediction seed, holding on 17 of 17 delivered designs that have
an independent re-draw and returning at ρ = +0.9447 on the ranking key. What they do not support is
engagement of the **second** designed lysine, unaided reproduction of the designed two-histidine
arrangement, agreement between oracles about which of these bind, an ordering of the band, **any
claim of ortholog preference in either direction**, or any statement about pH.
