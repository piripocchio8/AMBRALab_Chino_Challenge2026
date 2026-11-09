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
    complex_G12D_Ile97_restrained.pdb   ranks 9 and 10 only: the same complex under
                       the single declared Asp6-Ile97 contact they were promoted for
    sequence.fasta     the submitted sequence
    metrics.json       every number for this design, including per-model values
docs/metrics.md     what each column means and how it was measured
docs/epitope_contacts.json  per design, every peptide and HLA residue it touches
docs/peptide_free_control.md  the binder on HLA + b2m with no peptide: challenge goal (b)
ORGANIZERS.md       everything the selection process asks of a submission, point by point
DESIGN_STRATEGY.md  how the designs were produced and selected
SUBMISSION_TEXT.md  the narrative submitted alongside the file
_selftest/          the checks run over this directory, and their output
```

## The claim, and the control that makes it a claim

The binders are selected for an interaction that can be stated in one sentence: the **carboxylate
of peptide Asp6 is held within 4 Å of the guanidinium of HLA Arg114**. In the deposited crystal
structure of a therapeutic T-cell receptor bound to this same peptide–HLA complex (PDB **7OW6**)
that distance is **2.95 Å**. We call a model that reaches it **IN**.

This was the selection axis for the whole campaign, in both arms — the designs were chosen for
inducing the discriminating salt bridge, not for groove affinity with specificity checked
afterwards. And the salt bridge was always **observed, never declared**: no restraint table used to
produce any delivered design names Arg114. What the design arms declare about the aspartate is the
hydrophobic pocket beneath it (peptide Asp6 to HLA **Ile97**, 6.5 Å), with the binder's own docking
site moved one residue along the epitope so it does not compete for the side chain it is meant to
free. `DESIGN_STRATEGY.md` §3 gives the tables.

It is also not a free outcome of the prediction. Measured with the same code, on the same oracle:

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

Designs were produced with a declared restraint table — geometry that tells the predictor where the
binder should sit. Every number in `metrics_full.csv` prefixed *unrestrained* comes from a fold
given the four chains and **no table at all**: no distance restraints, no declared contacts, no
disulfide declaration. The table is how the design was made; it is not evidence that the design
works, and under restraint the IN state comes nearly free, so the restrained count cannot
discriminate between designs. The restrained numbers are reported too, in the columns marked
*restrained*, because that is what the campaign admitted each design on — but the selection, and
the eleven IN-positive entries, come from the unrestrained arm.

## Strength of the set, and its limits

- **Eleven of the twenty clear the IN criterion** against the binder-free control: ranks 1–8 and
  11–13. Ranks 9 and 10 are the two designs promoted for reaching the salt bridge 5 of 5 under a
  single declared contact, which `DESIGN_STRATEGY.md` §6 sets out. They are the entries this submission rests on.
- **The other nine are deposited on the remaining three criteria** — they land on the groove
  unrestrained, they fold on their own, and most prefer the neoantigen over wild type — but on the
  salt bridge itself they are not yet distinguishable from an empty groove. `metrics_full.csv` says
  which is which, design by design, with denominators and confidence intervals.
- **The set spans nine independent design lineages**, 25 to 62 residues, all disulfide-capped, so
  it is not twenty variations on one scaffold; the largest lineage contributes eight.
- **Two of the twenty stand at five models**, not twenty: `AMBRA_T5_18` and `AMBRA_T5_19`. Their
  on-groove and IN fractions carry the wider interval printed in `metrics_full.csv`.
- **Goal (b) is measured, and the answer is partial.** Every design is less confident of the
  peptide-free heterodimer — interface ipTM down in 20 of 20, binder pLDDT down in 20 of 20 — but
  19 of 20 still occupy the groove the peptide vacated. That pose is not a realizable state (empty
  class I does not hold its fold), and goal (b) was never an objective of the search. We report it
  rather than claim it: `docs/peptide_free_control.md`.
- **All of this is predicted structure.** No experiment was performed. The oracle is a single
  structure predictor, and three of its systematic behaviours are quantified in `docs/metrics.md`
  rather than hidden: sub-2 Å contacts are its signature on the deposited crystal too, its ψ3
  backbone switch does not survive comparison with 7OW5, and its ipTM is not calibrated to affinity.
