# pH-selective de novo binders to EGFR domain III

Submission to the **Anthropic × Adaptyv 2026 protein design competition, EGFR Challenge 01**
(`proteinbase.com/competitions/anthropic-adaptyv-2026/challenges/egfr`).

All designs are **de novo**: no existing binder, antibody framework or natural EGFR ligand was used
as a starting point. Backbones come from motif-scaffolded RFdiffusion3, sequences from soluble
ProteinMPNN, validation from Boltz-2 co-folding plus ipSAE.

---

## 1. What is being attempted, and why it is unusual

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

> **Numbering is the single easiest thing to get wrong here.** Every file in this repository uses
> **mature EGFR numbering (1–621)**, which is the competition construct UniProt **25–645**.
> Mature *m* = UniProt *m + 24*. Domain III is mature 311–480 = **UniProt 335–504**.
> The anchors are mature His409/Asp436 = **UniProt His433/Asp460**.

## 2. What is in this repository

```
SUBMISSION.csv          the ranked submission (name, sequence, molecule_class + all metrics)
METHODS.md              full protocol, every stage and its parameters
designs/                per-design structures: 3 independent folds, confidence, PAE/pLDDT, ipSAE
metrics/                the complete metric tables, including the pH-switch scan
protocol/scripts/       the pipeline as run
protocol/envs/          conda environment exports (exact pins)
protocol/inputs/        target structure, FASTA, MSA, motif definitions
analysis/               what we learned about what predicts binding, and the pKa analysis
```

## 3. Results summary

14 de novo designs, each validated by **three independent unconstrained co-folds** (two human
replicates at different seeds, one mouse-ortholog cross-species fold). **All 14 pass the acceptance
gate in every fold**: binder pLDDT >= 0.80, self-consistency RMSD < 2.0 A, ipSAE >= 0.50.

| | across the 14 | median |
|---|---|---|
| ipSAE (worst of 3 folds) | 0.660 - 0.898 | 0.832 |
| pDockQ | 0.376 - 0.606 | 0.535 |
| ipTM | 0.813 - 0.936 | 0.905 |
| binder pLDDT (mean of 3) | 0.900 - 0.966 | 0.942 |
| self-consistency RMSD (worst of 3) | 0.48 - 1.21 A | 0.90 A |
| interface contacts < 5 A | 419 - 667 | 540 |
| binder length | 60 - 134 aa | 116 aa |

**The designed salt-bridge motif survives unconstrained folding in every design.** Both anchor
bridges are <= 4.0 A in **14/14 designs in BOTH species arms**, and the bridge geometry is
indistinguishable from native in 13/14 (`realism_dev` <= 3.39, the 95th-percentile self-deviation of
39 native His-carboxylate contacts; our median is 1.69). This is the evidence that matters for the
mechanism, because these folds carry no contact restraints -- a restrained fold would only echo the
restraint back.

Nine designs carry their original sequence; five carry a sequence optimised for surface/core
polarity (see METHODS section 3b), marked `polarity_optimised` in the `sequence_origin` column.

Designs are ranked by **ipSAE of the worst of the three folds**, not the best. That choice is
deliberate: in our own earlier work a design scored ipSAE 0.79 while docking to a completely
different face, so peak confidence on one fold is not evidence. Ranking on the worst fold rewards
reproducibility instead.

## 4. Honest limitations

These are stated because they affect how the ranking should be read.

- **No computational metric here strongly predicts binding.** On a 3027-design, 32-target
  experimental benchmark we assembled, every sequence feature explained <1.4% of binding outcome
  and target identity dominated (eta^2 = 0.21). Ranking by PAE-interaction on the EGFR cohort lifts
  hit rate only 14% -> 26%. The ranking is a preference order, not a prediction.
- **Length.** Our designs are 60–134 aa. In three independent cuts of the Adaptyv EGFR data the
  productive regime is longer: all-alpha binders had median 228 aa against ~100 aa for
  non-binders, and within a single method group designs >= 200 aa bound at 26.9% versus 9.8% at
  100–200 aa (Fisher p = 0.00086). **Every design here sits below that regime.** We report it rather
  than hide it.
- **Alanine and apolarity.** Median alanine is 9.7% and median hydrophobic fraction (AVILMFWY)
  is 0.404, against 8.4% and 0.407 for the all-alpha class of the Adaptyv EGFR round-2 data and
  8.5% / 0.376 for that class's 11 binders. Five designs still exceed 15.8% alanine, the highest
  value seen in any observed binder, and four exceed 20%, a bin in which 0/16 of that class and
  2/76 of our own 800-design EGFR cohort bound. Alanine does **not** affect expression (p = 0.47 on
  our data) and does not discriminate within our length band (p = 1.00, underpowered), so this is an
  argument from sitting outside the observed envelope rather than from a demonstrated effect. It is
  flagged per design in `SUBMISSION.csv`.
- **pH selectivity is computational only.** The two-point motif is geometrically satisfied and the
  salt bridges reproduce across unconstrained folds, but the measured pH-dependent free energies are
  PyRosetta/PROPKA estimates. Rosetta and PROPKA disagree by >1 pKa unit on the key anchor
  (6.75 vs 7.95), so the magnitude of selectivity is genuinely uncertain. See `analysis/pka.md`.
- **The co-folding target was truncated** to domain III (mature 311–480) rather than the full
  621-residue ectodomain, for tractability. The epitope is inside domain III so this is expected to
  be conservative, but it is not the competition construct.

## 5. Licence

Sequences released under **ODC-BY**, consistent with the competition terms.
