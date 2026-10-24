# Target 3 — micro band

**Ten disulfide-cyclised peptides of 12, 15 and 39 residues, designed de novo in this group to
engage the GLP-1R orthosteric pocket the way the native agonist's N-terminus does.** Thirty-four
further designs from the same pool are documented here and not submitted.

> Every figure below is a property of a structure prediction. No peptide in this directory has
> been synthesised, and nothing here is a measurement of agonism.

## What the designs are

Three constructs, one macrocycle:

| construct | n submitted | what it is |
|---|---|---|
| 12-mer | 2 | the macrocycle alone — Cys1–Cys12 |
| 15-mer | 2 | a 12-residue macrocycle with a short flank, ring at C4–C15 |
| 39-mer | 6 | a 12-residue macrocycle plus a 27-residue extension, at the N- or the C-terminus |

**The macrocycle is the same size in every one of them.** What the longer constructs add is
residues *outside* the ring, so a difference between a 12-mer and a 39-mer is about an exocyclic
extension and not about ring size. Interface confidence rises with chain length on these models,
so the three lengths are **not one ranking**; the band is cut with a per-length quota rather than
by taking the top of a pooled list, and the construct is a column in `../metrics_full.csv`.

The ring is declared as a covalent SG–SG bond, not as a distance preference. Six of the ten carry
it at an internal position (for example 28–39), so the deposition script checks the declared
`cys_positions` against the sequence rather than against the two terminal residues.

## What is in each directory

`AMBRA_T3_micro_01` … `AMBRA_T3_micro_10` are the submitted band, named in rank order;
`AMBRA_T3_micro_11` … `AMBRA_T3_micro_44` are documented and carry a `status` and no rank.

| file | what it is |
|---|---|
| `chai_ssonly_model_0.cif` … `_4.cif` | **the five models the ranking is computed on** — chai-1, with the disulfide restraint and nothing else |
| `chai_scores_model_0.npz` … `_4.npz` | the ipTM / pTM arrays those five models scored |
| `boltz_msa_model_0.cif` … `_4.cif` | Boltz-2 2.2.1, disulfide bond constraint, with an MSA |
| `boltz_confidence_model_0.json` … `_4.json` | Boltz's own confidence record per model |
| `protenix_sample_0.cif` … `_4.cif` | Protenix-v2, **UNRESTRAINED**, with an MSA |
| `protenix_confidence_sample_0.json` … `_4.json` | Protenix's own summary confidence per sample |
| `restraints.csv` | the restraint file as chai was given it — one row, the disulfide |
| `sequence.fasta` | the binder sequence under its deposited name, with its internal campaign id |
| `metrics.json` | every number quoted for that design, field names matching `../metrics_full.csv` |

**No directory carries a "selected" model.** chai is nondeterministic on this system — the same
sequence and seed can land ~9 Å apart — so every figure is a mean or a count over the five, and the
best of *n* draws is a property of *n*.

**`restraints.csv` holds one row, and that is the point.** The search that produced these designs
also declared an 8 Å pocket on K174 and R357. The deposited folds do not. Refolding without the
pocket reorders the pool (ρ = +0.538 over 48 designs, 7 of them collapsing), so the restrained
number is partly an instruction; it is kept beside the deposited one as `chai_iptm_restrained`,
with the difference as `restraint_delta`.

## The band, as measured

`selected_iptm` is chai interface pTM on the disulfide-only folds. The ECL2 column is
fam-0 in *k* of 5 models; the ring column is SG–SG ≤ 2.5 Å in *k* of 5.

| # | design | L | ring | chai ipTM | Δ pocket | S–S | ECL2 fam-0 | pose spread Å | Boltz ipTM | Ptx ipTM |
|---:|---|---:|---|---:|---:|---|---|---:|---:|---:|
| 1 | `AMBRA_T3_micro_01` | 39 | C28–C39 | 0.8200 | −0.014 | 5/5 | 3/5 | 1.37 | 0.962 | 0.654 |
| 2 | `AMBRA_T3_micro_02` | 39 | C28–C39 | 0.7902 | −0.020 | 5/5 | 0/5 | 2.69 | 0.955 | 0.783 |
| 3 | `AMBRA_T3_micro_03` | 39 | C1–C12 | 0.7744 | −0.032 | **3/5** | 1/5 | 2.98 | 0.945 | 0.773 |
| 4 | `AMBRA_T3_micro_04` | 39 | C28–C39 | 0.7547 | −0.020 | **4/5** | **5/5** | 3.89 | 0.853 | 0.575 |
| 5 | `AMBRA_T3_micro_05` | 39 | C1–C12 | 0.7333 | +0.007 | 5/5 | 1/5 | 2.40 | 0.960 | 0.755 |
| 6 | `AMBRA_T3_micro_06` | 39 | C28–C39 | 0.6991 | **−0.089** | 5/5 | **5/5** | 2.07 | 0.937 | 0.776 |
| 7 | `AMBRA_T3_micro_07` | 15 | C4–C15 | 0.8201 | +0.000 | **3/5** | 0/5 | 0.94 | 0.970 | 0.950 |
| 8 | `AMBRA_T3_micro_08` | 15 | C4–C15 | 0.7154 | +0.012 | 5/5 | 3/5 | 1.77 | 0.970 | 0.728 |
| 9 | `AMBRA_T3_micro_09` | 12 | C1–C12 | 0.7132 | +0.001 | 5/5 | 0/5 | 1.10 | 0.972 | 0.830 |
| 10 | `AMBRA_T3_micro_10` | 12 | C1–C12 | 0.7052 | −0.018 | 5/5 | 4/5 | 1.01 | 0.960 | 0.774 |

Negative `Δ pocket` means the restrained fold scored **higher** — the restraint was worth that much.

## Limits

- **Nothing here has been measured.** No binding data, no functional assay, no expression result.
- **The activation readouts do not establish agonism.** The TM6 two-state call passes 40 of 40
  measured models and passes a composition-matched scramble on the reference panel; the ECL2+TM5
  family is a binding-mode prior and does not separate agonists from antagonists on that panel.
  Five of the ten are canonical on it. Neither is a ranking axis.
- **The three oracles disagree about binding.** Over these ten, chai's order against Boltz ipTM is
  ρ = +0.055, against Protenix ipTM +0.188, against Boltz ipSAE +0.370 (n = 10). Each reproduces
  its own order across a seed change far better than it reproduces another's.
- **Protenix was asked a different question.** It cannot take the disulfide constraint, so its arm
  is unrestrained. Do not average it with the other two.
- **Three designs do not close their declared ring in every model** — `micro_03` and `micro_07` in
  3 of 5, `micro_04` in 4 of 5. The flags are in the CSV.
- **Two designs carry no TM6 measurement** (`micro_04`, `micro_10`). They entered from a different
  source than the search cells and were classified on ECL2 but not on TM6. Their cells are blank,
  which means *not measured* — it does not mean they failed.
- **Pose spread is reported and ranks nothing.** It is the mean pairwise binder Cα RMSD across the
  five samples, reference-free, and ranges 0.94–3.89 Å over the band. It was deliberately not used
  as a gate: on this target it reproduces across a seed change at ρ = +0.524 against the ranking
  axis's +0.976, so gating on it would mean gating on the noisier of the two measurements.
- **The 39-mers' extensions are not designed interfaces.** They are extensions of a delivered
  macrocycle, and what the tail contributes to the score has not been separated from what the ring
  contributes.

Selection, gates and the ranking rule are in [`../docs/methods_micro.md`](../docs/methods_micro.md);
column definitions in [`../docs/metrics.md`](../docs/metrics.md).
