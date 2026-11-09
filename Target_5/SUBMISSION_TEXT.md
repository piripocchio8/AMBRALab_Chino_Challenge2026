# Target 5 — submission narrative

Twenty de novo binders against the KRAS **G12D** neoantigen decamer VVVGADGVGK presented on
HLA-A\*11:01. The wild-type decamer, VVVGAGGVGK, differs from it at exactly one position: glycine
where the neoantigen carries aspartate. A binder that merely grips this groove is therefore
useless — the groove is identical in both. The whole design campaign was built around the one
feature that is not identical, and around a single structural event that can be stated in a
sentence.

## The event we designed for

In the deposited crystal structure of a therapeutic T-cell receptor bound to this exact
peptide–HLA complex (PDB **7OW6**), the carboxylate of peptide Asp6 sits **2.95 Å** from the
guanidinium of HLA **Arg114**. That salt bridge is how the receptor reads the mutation: it is
unavailable to the wild-type peptide, which has no carboxylate at that position. We call a
predicted model that reproduces it **IN**, and the IN state was the selection axis from the first
round to the last.

That is the positive claim of this entry: these designs were not selected for generic groove
affinity and then checked for specificity afterwards. They were selected, throughout, for
**inducing the discriminating salt bridge**.

## The salt bridge was always observed, never declared

This matters for how the numbers should be read, so it is stated plainly. The design search runs
with a declared restraint table — geometry handed to the structure predictor to tell it where the
binder should sit. **No restraint table used to produce any delivered design ever declared the
Asp6–Arg114 contact.** The most any table ever said about the aspartate was where its hydrophobic
neighbourhood is: a 6.5 Å contact between peptide Asp6 and HLA **Ile97**, the pocket beneath it.
Declaring the pocket rather than the bond leaves the salt bridge free to form or not; the binder's
own docking site was additionally moved one residue along the epitope, onto Gly7, so that the
binder would not compete for the very side chain it is meant to free.

So in the restrained arm the IN state is an observation. In the unrestrained arm — the arm that
selection is actually taken from — it is an observation with nothing declared at all: the four
chains are handed to the predictor with no table, no distance restraints, no declared contacts and
no declared disulfide, on each of the two peptides, five models per design and twenty for most of
the shortlist.

## What makes an IN count meaningful

The IN criterion is tested against a measured null rather than a threshold we chose. Predicted
with identical code on the identical oracle:

| system | models IN | median Asp6–Arg114 |
|---|---|---|
| the groove with **no binder at all** | **0 of 50** | 6.31 Å |
| the groove with the **wild-type** decamer | 0 of 65 | no carboxylate exists |
| a published de novo pMHC minibinder transplanted onto this groove | 0 of 25 | — |
| the **therapeutic TCR** of 7OW6 | **42 of 50** | 3.04 Å |

The salt bridge does not form on its own, and it does not form merely because a competent binder of
some other pMHC is sitting on the groove. It forms for the receptor that is known to read this
mutation. A design is credited on this criterion only where its count is separated from the
binder-free control by a one-sided Fisher exact test at p < 0.05 — two of five models, or three of
twenty where the design was replicated.

## The three goals, each with a measurement

**(c) Binding the G12D complex.** Twenty of twenty place the binder on the α1/α2 groove in at
least 60% of unrestrained models. Eleven reproduce the Asp6–Arg114 salt bridge with nothing
declared; five more reproduce it under the single Asp6–Ile97 contact, four of those in 5 of 5
models. Sixteen of twenty therefore produce the discriminating interaction under one condition or
the other, and the two counts are kept in separate columns so they are never conflated.

**(a) Not binding the wild-type peptide.** Every design was predicted on the wild-type complex
under identical conditions; fifteen of twenty clear the margin threshold, which is set at the
unrestrained margin the therapeutic TCR itself shows. The structural discriminator is the stronger
one: the salt bridge eleven designs reproduce **cannot exist** on the wild-type peptide, which has
glycine where the neoantigen has aspartate.

**(b) Not binding the peptide-free heterodimer.** Measured for this submission, because the
challenge asks for it and the campaign had not: all twenty re-predicted as three chains with the
peptide deleted and no restraints. **Every design loses confidence** — binder↔HLA ipTM falls in 20
of 20 (median −0.207) and the binder's own pLDDT falls in 20 of 20 (median −7.7). But the chain
does not leave: 19 of 20 occupy the seat the peptide vacated. We therefore do **not** claim
peptide-free non-binding. Two things are worth saying about that pose. It was never selected
against — goal (b) was not an objective of the search. And it is not a realizable state: a
peptide-free class I heavy chain does not hold its fold, which is why empty HLA is loaded in the ER
rather than found waiting on the surface, so a binder sitting in that groove describes what a
predictor does with an empty channel rather than an interaction that could be measured at the
bench. The two confidence drops are consistent with exactly that. `AMBRA_T5_12` is the one design
with positive structural evidence here: zero atoms in the vacated seat, and its groove contacts
fall away with the peptide. Full numbers in `docs/peptide_free_control.md`.

## Ranking, and what the twenty are

Designs were ranked on four criteria, applied in this order: that the binder lands on the α1/α2
groove with no restraints; that it induces the IN state, against the control above; that it folds
on its own; and that it separates the two peptides. **Eleven of the twenty clear the IN bar** and
are the strongest entries in the set. The remaining nine are deposited on the other three
criteria: they dock on the groove unrestrained, they fold independently, and most prefer the
neoantigen over wild type — but on the salt bridge itself they are not yet distinguishable from an
empty groove, and `metrics_full.csv` says which is which design by design. The full ensemble is
deposited for every entry rather than a single flattering model, together with the three systematic
behaviours of the predictor that bear on reading the numbers.

The sequences are 25 to 62 residues, all disulfide-capped, spanning nine independent design
lineages. The sequence-design engine itself is the subject of a manuscript in preparation and is
described in principle rather than in reproducible detail; everything needed to evaluate these
designs is in this directory. All results are predicted structures — no experiment was performed.
