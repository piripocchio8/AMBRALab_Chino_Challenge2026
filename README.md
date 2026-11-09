# AMBRA Lab — Chino group — protein design challenge entries, 2026

De novo binder designs submitted by the **AMBRA group, Department of Chemical Sciences, University
of Naples Federico II**, to the 2026 protein design competition. One directory per challenge target,
each self-contained: designs, predicted structures, the metrics they were selected on, and the
methods that produced them.

```
Target_1/            EGFR domain III, pH-selective binders
  micro/             binders under 40 residues
  mini/              40 to 100 residues
  large/             over 100 residues
  docs/              the methods for this target
  submission.csv     the submitted file (name, sequence, molecule_class)
  metrics_full.csv   the same rows with every metric behind the ranking
Target_2/            TNF-family homotrimer, binders designed to be released by acidification
Target_3/            GLP-1R agonists — two bands, micro (cyclic peptides) and mini (miniproteins)
Target_4/            a zinc-finger-like fold, scramble-controlled selection
Target_5/            KRAS G12D neoantigen on HLA-A*11:01
  ranked/            one directory per design: three structures, sequence, metrics
  docs/metrics.md    what every column means
  _selftest/         the checks run over the directory, and their output
```

Each target directory has the same shape. A size band is present only when that campaign produced
designs in it: `Target_2/` has no `mini/` or `large/` because every candidate in its pool is 39
residues, and an empty directory for a size we did not design would be an empty claim.

## Targets

| target | protein | objective | status |
|---|---|---|---|
| **Target 1** | EGFR domain III (UniProt P00533, residues 334–494) | binders that engage a target histidine in a protonation-dependent way, so that affinity differs between the acidic tumour microenvironment and blood pH | submitted |
| **Target 2** | a TNF-family homotrimer | binders carrying their own histidines against a lysine-rich epitope on one protomer, designed to be *released* on acidification rather than tightened | submitted |
| **Target 3** | GLP-1R (UniProt P43220), class-B GPCR | de novo agonists — disulfide-cyclised peptides of 12–39 residues designed here, and 140-residue de novo miniproteins presenting a natural agonist anchor | prepared |
| **Target 4** | a zinc-finger-like fold, two orthologues | binders selected only where they beat their own composition-matched scramble on both orthologues | prepared |
| **Target 5** | KRAS **G12D** neoantigen decamer VVVGADGVGK on HLA-A\*11:01 | binders that discriminate the neoantigen from wild type and hold the G12D carboxylate against HLA Arg114, the 2.95 Å contact of PDB 7OW6 | prepared |

## How the entries are organised

Every design directory carries the predicted structure or structures it was judged on, together
with the confidence data for each, so that any number quoted in the submission can be recomputed
from what is in the repository. Nothing is reported that cannot be recovered from the files here.

Two independent design series contribute to Target 1, on two different histidines and by two
different chemistries. They are documented separately, in `Target_1/docs/`, because they share no
machinery and fail independently:

- **micro** — short disulfide-cyclised peptides whose main-chain carbonyls **accept** hydrogen bonds
  from the two N–H donors of the protonated imidazolium of **His358** (UniProt; mature His334).
- **mini and large** — scaffolded de novo proteins that form a salt bridge from the protonated
  imidazolium of **His433** (UniProt; mature His409) to an engineered carboxylate, with a reciprocal
  histidine-aspartate anchor.

## How designs are ranked here

A single predicted complex is one draw from a stochastic process, so nothing in this repository is
ranked on a best model. Each design is refolded many times from scratch and judged on what happens
*repeatedly*: how often the intended interaction reappears, how tightly the refolds agree on one
pose, whether the binder is one structure rather than two, and whether that holds against both the
human and the mouse ortholog. Rates are reported with the number of models behind them, because a
rate over five models is not a rate.

Where a property can be put on an independent footing, it is: protonation effects are computed with
propka, interface energies with AutoDock Vina, and structures are cross-checked against a second
co-folding model. Those tools know nothing about how the designs were made, which is the point.

## What these numbers are

Every metric in this repository is a property of a **structure prediction**, not of a measurement.
They describe how confident an oracle is about a modelled pose. **No design here has been tested
experimentally**: there are no binding data, no pH titrations, and no expression results. The
selection criteria, the failures and the limits of the predictions are stated in the methods
documents rather than left to inference.

## Licence and contact

Designs and documentation are released for the purposes of the competition. Correspondence:
the AMBRA group, Department of Chemical Sciences, University of Naples Federico II. marco.chino@unina.it ambralab@unina.it
