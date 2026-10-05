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
  submission.csv     the ranked rows submitted
Target_2/ ...        added as each target opens
```

## Targets

| target | protein | objective | status |
|---|---|---|---|
| **Target 1** | EGFR domain III (UniProt P00533, residues 334–494) | binders that engage a target histidine in a protonation-dependent way, so that affinity differs between the acidic tumour microenvironment and blood pH | submitted |

## How the entries are organised

Every design directory carries the predicted structure or structures it was judged on, together
with the confidence data for each, so that any number quoted in the submission can be recomputed
from what is in the repository. Nothing is reported that cannot be recovered from the files here.

Two independent design series contribute to Target 1, on two different histidines and by two
different chemistries. They are documented separately, in `Target_1/docs/`, because they share no
machinery and fail independently:

- **micro** — short disulfide-cyclised peptides that donate two main-chain carbonyls to the
  protonated imidazolium of **His358** (UniProt; mature His334).
- **mini and large** — scaffolded de novo proteins that form a salt bridge from the protonated
  imidazolium of **His433** (UniProt; mature His409) to an engineered carboxylate, with a reciprocal
  histidine-aspartate anchor.

## What these numbers are

Every metric in this repository is a property of a **structure prediction**, not of a measurement.
They describe how confident an oracle is about a modelled pose. **No design here has been tested
experimentally**: there are no binding data, no pH titrations, and no expression results. The
selection criteria, the failures and the limits of the predictions are stated in the methods
documents rather than left to inference.

## Licence and contact

Designs and documentation are released for the purposes of the competition. Correspondence:
the AMBRA group, Department of Chemical Sciences, University of Naples Federico II.
