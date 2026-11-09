# Target 5 — KRAS G12D neoantigen presented on HLA-A\*11:01

Twenty de novo binders designed against the decamer **VVVGADGVGK**, residues 5–14 of KRAS carrying
the G12D substitution, in the groove of **HLA-A\*11:01**. The wild-type decamer differs at one
position: **VVVGAGGVGK**, glycine where the neoantigen has aspartate. Everything in this directory
exists to answer one question — does the binder tell those two apart, and does it do so by engaging
the aspartate itself?

```
submission.csv      the submitted rows: name, sequence, molecule_class
metrics_full.csv    the same twenty with every number they were chosen on
ranked/AMBRA_T5_nn/ one directory per design
    complex_G12D.pdb   binder + HLA + β2-microglobulin + the G12D decamer
    complex_WT.pdb     the same binder on the wild-type decamer
    binder_alone.pdb   the binder predicted with no target present
    sequence.fasta     the submitted sequence
    metrics.json       every number for this design, including per-model values
docs/metrics.md     what each column means and how it was measured
DESIGN_STRATEGY.md  how the designs were produced and selected
SUBMISSION_TEXT.md  the narrative submitted alongside the file
_selftest/          the checks run over this directory, and their output
```

## The claim, and the control that makes it a claim

The binders are selected for an interaction that can be stated in one sentence: the **carboxylate
of peptide Asp6 is held within 4 Å of the guanidinium of HLA Arg114**. In the deposited crystal
structure of a therapeutic T-cell receptor bound to this same peptide–HLA complex (PDB **7OW6**)
that distance is **2.95 Å**. We call a model that reaches it **IN**.

It is not a free outcome of the prediction. Measured with the same code, on the same oracle:

| system | models IN | median Asp6–Arg114 |
|---|---|---|
| the groove with **no binder at all** | **0 of 50** | 6.31 Å |
| the groove with the **wild-type** peptide (no carboxylate exists) | 0 of 65 | — |
| a published de novo pMHC minibinder transplanted onto this groove | 0 of 25 | — |
| the **therapeutic TCR** of 7OW6 | **42 of 50** | 3.04 Å |

So an unrestrained model that reaches 4 Å is an event, not a background rate, and every IN count in
`metrics_full.csv` is read against **0 of 50**. The threshold used for selection is a one-sided
Fisher exact test against that control at p < 0.05, which is 2 of 5 models, or 3 of 20 where the
design was replicated to twenty.

## What "unrestrained" means here, and why it is the axis

Designs were produced with a declared restraint table — a jig that tells the predictor where the
binder should sit. Every number in `metrics_full.csv` prefixed *unrestrained* comes from a fold
given the four chains and **no table at all**: no distance restraints, no declared contacts, no
disulfide declaration. The jig is how the design was made; it is not evidence that the design
works, and under restraint the IN state is nearly free. The restrained numbers are reported too,
in the columns marked *restrained*, because that is what the campaign admitted each design on, but
the selection is on the unrestrained arm.

## Honest limits

- **Two of the twenty stand at five models**, not twenty: `AMBRA_T5_16` and `AMBRA_T5_17`. Their
  on-groove and IN fractions carry the wider interval printed in `metrics_full.csv`.
- **Eight of the twenty meet the IN criterion**; the other twelve are, on that axis, not
  distinguishable from an empty groove. They are here on the other three criteria — they land on
  the groove unrestrained, they fold on their own, and most separate the two peptides — and the
  per-design numbers say which is which.
- **All of this is predicted structure.** No experiment was performed. The oracle is a single
  structure predictor, and three of its systematic behaviours are quantified in `docs/metrics.md`
  rather than hidden: sub-2 Å contacts are its signature on the deposited crystal too, its ψ3
  backbone switch does not survive comparison with 7OW5, and its ipTM is not calibrated to affinity.
