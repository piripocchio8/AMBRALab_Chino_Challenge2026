# pH-selective de novo binders to EGFR domain III

Submission to the **Anthropic × Adaptyv 2026 protein design competition, EGFR Challenge 01**
(`proteinbase.com/competitions/anthropic-adaptyv-2026/challenges/egfr`).

All designs are **de novo**: no existing binder, antibody framework or natural EGFR ligand was used
as a starting point. Backbones come from motif-scaffolded RFdiffusion3, sequences from soluble
ProteinMPNN, validation from Boltz-2 co-folding plus ipSAE.

---

## 1. Objective

The design objective is not affinity alone but **pH-selective binding**: tighter at the acidic pH of
the tumour microenvironment and of the endosome (~6.5) than at blood pH (~7.4). The mechanism is a
**two-point salt-bridge motif** built on a histidine of the target itself:

| role | mature EGFR | **UniProt P00533** | partner on the binder |
|---|---|---|---|
| protonation switch | His409 | **His433** | an engineered Asp/Glu |
| fixed anchor | Asp436 | **Asp460** | an engineered His |

At pH 6.5 the target His433 is protonated and forms a salt bridge to the binder's carboxylate; by
pH 7.4 it deprotonates and that bridge is lost. His433 sits in the domain III ligand pocket, the
epitope the competition brief recommends, and is one of the two histidines independently identified
as pH-relevant for EGF binding in the published Adaptyv EGFR analysis.

> Every file in this repository uses
> **mature EGFR numbering (1–621)**, which is the competition construct UniProt **25–645**.
> Mature *m* = UniProt *m + 24*. Domain III is mature 311–480 = **UniProt 335–504**.
> The anchors are mature His409/Asp436 = **UniProt His433/Asp460**.

## 2. What is in this repository

```
SUBMISSION.csv          the ranked submission (name, sequence, molecule_class + all metrics)
METHODS.md              full protocol, every stage and its parameters
designs/                per-design structures: 3 independent folds, confidence, PAE/pLDDT, ipSAE
metrics/                metric tables for the designs AS SUBMITTED (PROPKA pKa and charge for all
                        23 + raw .pka, pH selectivity, cumulative ranking inputs) plus the
                        per-round campaign records, which carry a `disposition` column
protocol/DESIGN_PIPELINE_PROCEDURE.md  how the pipeline works and how to run it
protocol/scripts/       the pipeline as run (round5/ holds the round-5 scripts and SLURM jobs)
protocol/envs/          conda environment exports (exact pins)
protocol/inputs/        target structure, FASTA, MSA, motif definitions
analysis/               what predicts binding, the pKa analysis, and the provenance and
                        limits of the composition envelope
```

## 3. Results summary

**23 de novo designs** from three design rounds, each validated by **three independent
unconstrained co-folds** (two human replicates at different seeds, one mouse-ortholog
cross-species fold). **All 23 clear the acceptance gate in every fold**: binder pLDDT >= 0.80,
self-consistency RMSD < 2.0 A, ipSAE >= 0.50 — including the mouse arm.

| | across the 23 | median |
|---|---|---|
| ipSAE (worst of all 3 folds) | 0.660 - 0.890 | 0.836 |
| ipSAE (worst human fold) | 0.660 - 0.897 | 0.851 |
| pDockQ | 0.376 - 0.614 | 0.539 |
| ipTM | 0.813 - 0.936 | 0.905 |
| binder pLDDT (mean of 3) | 0.900 - 0.967 | 0.941 |
| self-consistency RMSD (worst of 3) | 0.54 - 1.31 A | 0.94 A |
| interface contacts < 5 A | 419 - 667 | 552 |
| binder length | 60 - 140 aa | 117 aa |

**The designed salt-bridge motif survives unconstrained folding in every design.** Both anchor
bridges are <= 4.0 A in **23/23 designs in the human arm** and 22/23 in the mouse arm, and the
bridge geometry is indistinguishable from native in 22/23 (`realism_dev` <= 3.39, the
95th-percentile self-deviation of 39 native His-carboxylate contacts; our median is 1.66). This is
the evidence that matters for the mechanism, because these folds carry no contact restraints -- a
restrained fold would only echo the restraint back.

**Every design is predicted to engage the mouse ortholog** (mouse ipSAE 0.695-0.924, all >= 0.50).
Both anchor residues are identical in mouse and domain III is 87.6% identical, so cross-reactivity
is the expected outcome rather than a surprise; it is reported because it permits mouse PK and
efficacy work without a surrogate reagent.

### What round 5 added

Round 5 (9 of the 23, `design_round = 5`, `local_id` `R5_*`) targeted the single clearest weakness
of the earlier set: **amino-acid composition outside the envelope of experimentally confirmed
sub-uM all-alpha EGFR binders** (bounds, provenance and limits in
`analysis/composition_envelope.md`). It enforced that envelope *before* folding, by biasing ProteinMPNN
against alanine at sampling time rather than resurfacing sequences afterwards.

| | rounds 3-4 (14) | round 5 (9) | cumulative (23) | all-alpha ideal |
|---|---|---|---|---|
| alanine fraction | 0.102 | **0.072** | 0.079 | 0.085 |
| hydrophobic AVILMFWY | 0.409 | **0.367** | **0.376** | 0.376 |
| **outside the envelope** | **8/14** | **0/9** | 8/23 | — |

Round 5 also used a stricter acceptance rule than rounds 3-4: every mechanism criterion had to hold
in **both** independent unconstrained folds, not on average, because the designed salt bridge
replicates poorly across folds (Spearman rho +0.36 between folds). 2370 constrained folds produced
98 founders, of which 11 were accepted and 9 are submitted here.

**pH selectivity is now measured per design** for all 9 (PyRosetta pH mode, whole-pose, 8
replicates): ddG_bind median **+3.12 REU** favouring pH 6.5, range +0.47 to +5.98, with 5 of 9 above
twice the combined standard error. The mechanism is confirmed through the anchor's own protonation:
target His409 is 0.50-1.00 protonated at pH 6.5 and 0.00-0.25 at pH 7.4. The two strongest switches
in the whole programme, **+5.98** (`pHsel-07`) and **+5.34** (`pHsel-08`), are round-5 designs.

**Structural pKa and pH-dependent charge are now reported for all 23 designs** (PROPKA 3.5.1 on each
design's unconstrained co-fold, free binder and complex). Every design is more negative at pH 7.4
than at 6.5 (dq median -0.90 e), which is the intended direction; **19 of 23 carry a histidine inside
the 6.5/7.4 switching window**, seven of them at >= 90% of the theoretical ceiling, with
`pHsel-18`'s HIS20 (pKa 6.94) and `pHsel-04`'s HIS55 (pKa 6.99) essentially perfectly centred on
the window midpoint. Round 5 is modestly ahead of rounds 3-4 here too
(8/9 vs 11/14 in-window). Details, including the four designs with no in-window histidine and the three
that are over-shifted, are in `analysis/pka.md`; per-design numbers in
`metrics/propka_all_designs.csv`, pH selectivity in `metrics/ph_selectivity_submitted.csv`, and
eight summary columns in `SUBMISSION.csv`.

### Cysteine removal

All 23 designs were audited for unpaired cysteines on their shipped structures; 18 free thiols were
found across 12 designs, every one of them buried. Only the cysteine positions were redesigned --
ProteinMPNN was given those positions alone as designable and the parent sequence is reproduced at
every other position -- then each candidate was refolded unconstrained in all three arms and
accepted only if it cost nothing measurable: ipSAE within 0.05 of the parent in every fold, the fold
kept within 2 A, both designed bridges still <= 4.0 A, and the composition envelope not worsened.

**9 of 12 designs were fixed, taking free thiols from 18 to 5**, and the interface is flat or better
in 7 of the 9. Where a buried position had an apolar option that was equal or better on every
measured axis it was taken, so 5 of the 9 substitute only into A/V/I/L/M/F; the remaining 4 keep a
serine or asparagine either because no apolar candidate held the interface (`pHsel-10`) or because
the polar residue is load-bearing for the pH switch (below). Every introduced polar side chain was
checked for an H-bond partner in the predicted structure and all are satisfied at 2.4-3.4 A, mostly
to a local backbone carbonyl. For the round-5 designs, where pH selectivity is measured per design, it was also
required that the fix not cost more than 0.5 REU of switch -- and that criterion mattered: at the
same positions, different residues swing ddG by up to **3.7 REU**, so the buried cysteines are
coupled to the His switch in a way ipSAE cannot see. Choosing on selectivity as well as interface
turned `pHsel-07` from a 1.66 REU loss into a **+3.65 REU gain**, giving it the strongest switch in
the programme (5.98 REU). Candidate-level data is in `metrics/cysteine_removal_all_candidates.csv`.

### Two designs were accepted but deliberately not submitted

Both were round-5 designs that passed every acceptance criterion, and both are excluded on grounds
outside the acceptance gate. They are named here so the 11-accepted / 9-submitted gap is not silent:

- **`R5_01`, 187 aa, ipSAE 0.891** — the highest-scoring round-5 design, and it would have ranked 3rd
  overall. Excluded on **length**: our cell-free expression evidence was derived entirely within a
  60-134 aa band (143/144 expressed), and 187 aa sits far outside the range where that holds. This
  is a deliberate trade against the length signal in section 4, which points the other way; we chose
  validated expression over an extrapolated hit-rate gain. In fairness the band is not a cliff and
  this submission is not wholly inside it either -- `pHsel-17` is 140 aa, six residues beyond. The
  judgement was one of degree: 6 aa of extrapolation is a different proposition from 53.
- **`R5_11`, 110 aa, ipSAE 0.602** — passed both human folds but collapsed on the mouse ortholog
  (ipSAE 0.094, mouse bridge 10.8 A). It was also the weakest human binder of the accepted set.

Both remain in `metrics/round5_all_metrics.csv` and `metrics/round5_ph_selectivity.csv`, flagged with
`submitted = 0` and an `exclusion_reason`, so the full accepted set of 11 is recoverable here.

### Ranking basis

Designs are ranked by **ipSAE of the worst of the two human unconstrained folds**, minus an explicit
penalty of 0.030 per composition-envelope axis violated.

Two deliberate choices worth stating:

1. **Worst fold, not best.** In our own earlier work a design scored ipSAE 0.79 while docking to a
   completely different face, so peak confidence on one fold is not evidence.
2. **Human folds only** (rounds 3-4 ranked on the worst of all three folds, mouse included). The
   competition measures binding to *human* EGFR, so penalising a design for weak mouse
   cross-reactivity confuses a bonus with the objective. Mouse ipSAE is reported separately in
   `SUBMISSION.csv`, and `ipsae_min_of_3_folds` is retained there for continuity. With the 23 designs
   submitted the two keys coincide anyway -- the human fold is the worst fold for every design.

The composition penalty is a judgement call and is the only non-mechanical term in the ranking. It
moves three high-ipSAE but non-compliant round-3 designs (`pHsel-13`, `-15`, `-17`) out of the
top ten. Set the penalty to zero and they return; `metrics/cumulative_ranking_inputs.csv` carries the
inputs so any reader can re-rank.

Nine designs carry their original sequence, five a surface/core polarity-optimised sequence
(METHODS section 3b), and nine a round-5 alanine-biased sequence; the `sequence_origin` column
records which.

## 4. Honest limitations

These are stated because they affect how the ranking should be read.

- **Some comparison figures below are external and cannot be checked from this repository.** The
  all-alpha reference values -- median binder length 228 aa against ~100 aa for non-binders, 8.5%
  alanine and 0.376 hydrophobic for the eleven confirmed binders of that class, and 15.8% alanine as
  the highest value in any observed binder -- come from an analysis of the previous round's published
  cohort that is **not** included here. They shaped real design decisions, so they are reported, but
  a reader cannot verify them against anything shipped. Everything attributed to
  `analysis/what_predicts_binding.md` is computed on data we assembled and is checkable; the
  composition envelope's provenance and limits are set out in `analysis/composition_envelope.md`.
- **No computational metric here strongly predicts binding.** On a 3027-design, 32-target
  experimental benchmark we assembled, every sequence feature explained <1.4% of binding outcome
  and target identity dominated (eta^2 = 0.21). Ranking by PAE-interaction on the EGFR cohort lifts
  hit rate only 14% -> 26%. The ranking is a preference order, not a prediction.
- **Length is the largest known gap, and this submission widens it.** Designs are 60-140 aa
  (median 117). In three independent cuts of the Adaptyv EGFR data the productive regime is longer:
  all-alpha binders had median 228 aa against ~100 aa for non-binders, and within a single method
  group designs >= 200 aa bound at 26.9% versus 9.8% at 100-200 aa (Fisher p = 0.00086).
  **No design here reaches 150 aa.** Round 5 did produce a 187 aa design, the closest we have come to
  that regime and the highest-scoring round-5 design, and it was **deliberately excluded** because
  our cell-free expression evidence only covers 60-134 aa, which one shipped design (`pHsel-17`,
  140 aa) also marginally exceeds (see section 3). That is a real trade, made
  knowingly: the length signal is an extrapolation from another group's cohort, the expression
  evidence is from our own, and we preferred the latter. A reader who weights the length signal more
  heavily should recover `R5_01` from `metrics/round5_all_metrics.csv`.
  Round 5 also showed the long regime is simply *low-yield*, not low-ceiling: 179-245 aa gave a 1.45%
  founder rate against 5.58% at 86-146 aa, yet its one survivor outscored everything else in the
  round. Future rounds should spend proportionally more compute there rather than fewer samples.
- **Alanine and apolarity: much improved, not eliminated.** Cumulative median alanine is 7.9% and
  median hydrophobic fraction 0.376, against 8.5% / 0.376 for the confirmed sub-uM all-alpha class --
  i.e. the set now sits on that envelope at the median. But **8 of 23 designs still fall outside it**,
  all from rounds 3-4: five exceed 15.8% alanine (the highest value in any observed binder) and two
  exceed 32%. All 9 round-5 designs are inside on every axis. Alanine does **not** affect expression
  (p = 0.47 on our data) and does not discriminate within our length band (p = 1.00, underpowered),
  so this is an argument from sitting outside the observed envelope rather than from a demonstrated
  effect. It is flagged per design in `risk_flags`, and `in_composition_envelope` marks compliance.
- **pH selectivity is computational throughout, and unevenly covered.** The two-point motif is
  geometrically satisfied and the salt bridges reproduce across unconstrained folds in all 23.
  Coverage differs by quantity:
  **pKa and pH-dependent charge are now computed for all 23** (PROPKA, free binder and complex);
  **pH-dependent binding free energy `ddG_bind` exists for only the 9 round-5 designs** (median
  +2.33 REU favouring pH 6.5, 5 of 9 above twice the combined standard error), so that column is
  empty for the 14 round-3/4 designs. All of it is PyRosetta/PROPKA estimation, and Rosetta and
  PROPKA disagree by >1 pKa unit on the key anchor (6.75 vs 7.95), so the *magnitude* of selectivity
  is genuinely uncertain even where measured. A sequence-only charge calculation understates the
  histidine contribution by ~2.3x relative to the structural one, and the two disagree about which
  designs sit outside the charge envelope — both are shown in `analysis/pka.md` rather than one being
  presented as settled.
- **4 of 23 designs have no histidine inside the switching window** (`pHsel-10`, `-16`, `-17`, `-20`),
  so their intrinsic charge switch is weak regardless of interface geometry; and 8 of 23 carry a
  carboxylate above pKa 5.5 that co-titrates and partially short-circuits the switch. Both are
  reported per design in `metrics/propka_all_designs.csv`.
- **`predicted_cellfree_expression` is empty for the 9 round-5 designs.** It came from a
  cohort-fitted model used in rounds 3-4 that was not re-run for round 5; the cells are left blank
  rather than filled with a differently-derived number. Note this is the same evidence base invoked
  to exclude the 187 aa design, so that exclusion rests on the model's *input domain* (60-134 aa),
  not on a score computed for that design.
- **Unpaired cysteines: reduced from 18 to 5, three designs still carry one.** Measured on the
  shipped structures (SG-SG < 2.5 A counts as a disulfide). All 18 were fully **buried**
  (relSASA 0.00-0.12), which materially lowers the liability -- intermolecular crosslinking and
  thiol-driven aggregation need solvent access -- but cysteine was never excluded at ProteinMPNN
  sampling time, which is an omission for a de novo single-chain binder. 9 of the 12 affected designs
  were redesigned at the cysteine positions only (see METHODS section 7c); `pHsel-14`, `-16` and
  `-22` keep theirs because no substitution preserved the interface, and are flagged `free-cys:N` in
  `risk_flags`. `pHsel-02` retains two cysteines that form a genuine disulfide, which is a
  stabiliser rather than a liability. Reported per design as `n_free_thiols` / `n_disulfides`.
- **The co-folding target was truncated** to domain III (mature 311-480) rather than the full
  621-residue ectodomain, for tractability. The epitope is inside domain III so this is expected to
  be conservative, but it is not the competition construct.

## 5. Licence

Sequences released under **ODC-BY**, consistent with the competition terms.
