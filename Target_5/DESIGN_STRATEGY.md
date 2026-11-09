# How these twenty were produced and chosen

## 1. The target, and the one thing worth designing for

The neoantigen decamer **VVVGADGVGK** (KRAS residues 5–14, G12D) presented by **HLA-A\*11:01**,
with β2-microglobulin. The assembly folded in every prediction is four chains: HLA heavy chain,
β2-microglobulin, the decamer, and the designed binder.

The wild-type decamer differs at one position — **VVVGAGGVGK**, glycine for aspartate — and that
single side chain is the entire basis for discrimination. The groove is the same, the peptide
backbone register is the same, the anchors are the same. So the campaign was organised around the
structural event that uses the difference: the carboxylate of peptide **Asp6** reaching the
guanidinium of HLA **Arg114**, which is **2.95 Å** in the deposited crystal **7OW6** of a
therapeutic TCR on this same complex. A model that reproduces it is **IN**.

**This was the selection axis from the first round to the last**, in both arms of the campaign. It
is the reason the entry is being offered: not a set of binders that stick to a groove and were
screened for specificity afterwards, but a set selected throughout for inducing the salt bridge
that distinguishes the two peptides.

## 2. How the designs were made

A sequence-design engine developed in this group: it proposes candidate sequences, folds each one
as a complex against the target with a structure-prediction oracle, keeps what the oracle rates
highest, and iterates. The oracle is used as an oracle — it is not differentiated through. The
engine's internals are the subject of a manuscript in preparation and are described here in
principle rather than in reproducible detail; see the disclosure note at the end. Every delivered
sequence uses only the standard twenty L-amino acids, and every binder is disulfide-capped, 25 to
62 residues.

Two further operations generated most of the entries here:

- **redesign** — the delivered sequence re-sampled by soluble ProteinMPNN inside its own predicted
  complex, with the interface positions held fixed. The fold is the oracle's in both cases; only
  the sequence changed.
- **elongation** — ten residues added at one terminus, then redesigned. Entries whose identifier
  carries `eN10` or `eC10` are these.

## 3. Declaring the pocket, not the bond

During the search a **restraint table** is declared: distance restraints that tell the oracle where
the binder should sit, plus a disulfide where applicable. This is where a campaign aimed at a salt
bridge can quietly cheat, by declaring the salt bridge and then reporting it. We did not, and the
tables in the run records show it.

**No restraint table used to produce any delivered design declares the Asp6–Arg114 contact.** What
the design arms declare about the aspartate is a single 6.5 Å contact between peptide **Asp6** and
HLA **Ile97** — the hydrophobic pocket beneath the carboxylate, not the bond above it. That one
declaration moves the peptide into the salt-bridge-competent rotamer in **25 of 50** binder-free
folds, against **0 of 75** with no table at all, and it does so without naming Arg114.

A second edit protects the same side chain from the binder. The epitope pocket that docks the
binder was declared on Asp6 in the first arm, which pulls the binder onto the very residue the
design is trying to leave free; in the later arms it was moved one position along, onto **Gly7**,
so the binder lands on the same epitope while the aspartate is free to drop into the groove. Three
provenances are represented in the twenty — the original arm, the Ile97 arm, and the Ile97 arm with
the pocket on Gly7 — and `metrics_full.csv` carries the design identifier of each.

The consequence is the claim we want read: **in the restrained arm the IN state is an observation,
and in the unrestrained arm it is an observation with nothing declared at all.**

## 4. Validation on a separate, unrestrained arm

A design evaluated under its own restraint table is being asked whether the restraint table works.
So every delivered binder was re-predicted with **no table at all** — four chains, nothing
declared — on the G12D peptide and on wild type, five models each, and forty of the fifty
shortlisted designs were replicated to twenty models. The replicates are byte-identical input with
the same seed; the oracle is non-deterministic, and independence was checked before any statistic
was taken from them (0 of 40 designs returned a replicate identical to itself).

The two arms do not always agree, and that is informative rather than a defect: under restraint the
Asp6–Arg114 contact comes nearly free, so the restrained count cannot discriminate, and the
unrestrained count can. Selecting on the unrestrained arm is what gives the eight IN-positive
entries their weight.

## 5. Controls

Four systems were predicted with the identical code path and measured with the identical script:

- the groove with **no binder**, 50 models — 0 IN, median 6.31 Å. This is the null the IN counts
  are tested against.
- the groove with the **wild-type** decamer, 65 models — 0 IN. Position 6 is glycine, so the
  measurement cannot succeed; this confirms the script, not the biology.
- the **therapeutic TCR** of 7OW6, 50 models — 42 IN, median 3.04 Å. The positive control, and the
  demonstration that the oracle can reach the state at all.
- a published de novo pMHC minibinder transplanted onto this groove, 25 models — 0 IN. A competent
  binder of a different pMHC does not produce the contact by accident.

A scrambled-CDR series of the TCR degrades monotonically from 34 of 50 to 0 of 25 as more of the
recognition loops are destroyed, which is the behaviour a real readout should show.

## 6. Selection

Four criteria, applied in order, each design tiered by **which** it misses rather than how many: a
design missing the fourth outranks one missing the second. Within a tier: on-groove fraction, then
IN fraction, then the unrestrained margin. The criteria are defined in `docs/metrics.md`.

Eight of the twenty clear the IN criterion against the binder-free control and head the ranking.
The other twelve are deposited on the remaining three criteria — on-groove unrestrained, folds
alone, separates the two peptides — and their IN counts are reported with their denominators and
confidence intervals rather than rounded away.

Three decisions in the final set were taken by the principal investigator on inspection of the
coordinates, and are recorded as such rather than folded into the ranking:

1. Two designs with **IN 0 of 20** but the cleanest folds and the largest restrained margins were
   kept (`AMBRA_T5_18`, `AMBRA_T5_19`).
2. Six ranked designs were removed — three for a terminal segment judged unsound on inspection,
   three for failing to fold on their own. The second judgement reproduces as a measurement (gate
   F); the first does not reproduce by any measurement we have — two of the three rejected sit
   among the **lowest** terminal displacements in the set, and a design with an identical
   free-terminus profile was kept. It is recorded here as what it is: an expert judgement on the
   structures, not a metric.
3. The replacements were chosen for lineage diversity and required to fold alone. The set spans
   **nine independent lineages**; the largest contributes eight of the twenty.

## 7. Reproducing any number

Each design directory holds the three structures its numbers come from and a `metrics.json` with
the per-model values. The coordinate file deposited for the G12D complex is the model whose
Asp6–Arg114 distance is the **median** of its ensemble — the representative on the selection axis,
not the best model in it. `deposited_model_index` and `d6_all_models_A` in `metrics.json` place it.

## A note on what is and is not disclosed here

The sequence-design engine is **the subject of a manuscript in preparation**, so it is described
above in principle rather than in reproducible detail, **ahead of publication**.

Nothing needed to *evaluate these designs* is withheld: the sequences, the predicted structures,
every per-model measurement, the selection rule, the controls behind it, what the restraint tables
did and did not declare, and the ranked set of fifty from which the twenty were drawn are all
recoverable from this directory, and every number quoted can be recomputed from the files beside
it. What is held back is how the candidate sequences were *generated*, not how they were *judged*.

We will release the engine and its parameters with the publication, and are glad to discuss the
method in confidence with the organisers in the meantime.
