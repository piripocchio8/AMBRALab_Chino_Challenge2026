# Target 1 — EGFR domain III, pH-selective binders

Twenty de novo binders submitted against **EGFR domain III**, the competition construct
**UniProt P00533 residues 334–494**. The objective is not affinity alone but **pH selectivity**:
binding that differs between the acidic tumour microenvironment and blood pH, by engaging a
histidine whose imidazole is protonated at the lower pH and neutral at the higher one.

```
micro/          8 designs under 40 residues   — disulfide-cyclised peptides, target His358
mini/           4 designs 40–100 residues     — scaffolded proteins, target His433
large/          8 designs over 100 residues   — scaffolded proteins, target His433
docs/           the methods for each series
submission.csv  all 20 rows, ranked, with the metrics they were selected on
```

## Two series, two histidines, two mechanisms

The submission deliberately covers **two different sites** rather than one site twice. They are
independent: a failure of either says nothing about the other.

| | micro | mini and large |
|---|---|---|
| target histidine | **His358** UniProt (mature His334) | **His433** UniProt (mature His409) |
| mechanism | two **main-chain carbonyls** donate to the protonated imidazolium | **salt bridge** from the imidazolium to an engineered carboxylate, plus a reciprocal His–Asp anchor |
| scaffold | disulfide-cyclised peptide, 12–39 residues | motif-scaffolded de novo protein, 60–134 residues |
| methods | [`docs/methods_micro.md`](docs/methods_micro.md) | [`docs/methods_mini_large/`](docs/methods_mini_large/) |

The two sites are 75 residues apart in sequence. His358 is the more demanding of the two: the
double-carbonyl arrangement the micro series builds occurs in **0.455 %** of histidines in the PDB,
about one in 220, where the carboxylate-assisted arrangement the other series uses is six times more
common.

## Numbering

The construct is UniProt P00533 334–494, so for a local residue *n* in these files:

> local *n* = UniProt *n* + 333 = mature EGFR *n* + 309

The micro series' target histidine is local 25 = UniProt 358 = mature 334.

## What each design directory contains

Micro designs carry the five predicted models of the fold they were measured on — `human_selected.cif`
is the one the metrics refer to and `human_model_*.cif` the rest — plus `metrics.json` and
`sequence.fasta`. Mini and large designs carry two independent folds of the human complex, a fold of
the mouse ortholog, the scaffold backbone, and the confidence, ipSAE, PAE and pLDDT data for each.

The spread across models is included on purpose. A single predicted structure of a designed peptide
is one draw from a stochastic process, and several designs in this work looked convincing on one
model and collapsed over fifteen.

## What these numbers are, and are not

Every value in `submission.csv` and in each `metrics.json` is a property of a **structure
prediction**. **No design in this submission has been tested experimentally** — there are no binding
measurements, no pH titrations and no expression data. The methods documents state the selection
criteria, the failures, and what was measured rather than assumed.
