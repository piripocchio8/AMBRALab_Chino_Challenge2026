# How these twenty were produced and chosen

## The target

The neoantigen decamer **VVVGADGVGK** (KRAS residues 5–14, G12D) presented by **HLA-A\*11:01**,
with β2-microglobulin. The assembly folded in every prediction is four chains: HLA heavy chain,
β2-microglobulin, the decamer, and the designed binder. The discriminating feature is a single
side chain — the aspartate the wild-type sequence does not have — and the structural event the
designs are built around is that aspartate's carboxylate reaching the HLA **Arg114** guanidinium,
2.95 Å in the deposited crystal **7OW6**.

## Design

Binders were produced by forward-folding search: a sequence is proposed, the complex is predicted,
an objective is read off the prediction, and the sequence is changed. The predictor is used as an
oracle, not differentiated through. During the search a **restraint table** is declared — distance
restraints that tell the predictor where the binder should sit and, where applicable, a disulfide.
Two further operations generated most of the entries here:

- **redesign** — the delivered sequence re-sampled by soluble ProteinMPNN inside its own predicted
  complex, with the interface positions held fixed. The fold is the oracle's in both cases; only
  the sequence changed.
- **elongation** — ten residues added at one terminus, then redesigned. Entries whose identifier
  carries `eN10` or `eC10` are these.

Every binder is disulfide-capped, 25 to 62 residues.

## Validation, and why it is on a separate arm

A design evaluated under its own restraint table is being asked whether the restraint table works.
So every delivered binder was re-predicted with **no table at all** — four chains, nothing
declared — on the G12D peptide and on wild type, five models each, and forty of the fifty
shortlisted designs were replicated to twenty models. The replicates are byte-identical input with
the same seed; the predictor is non-deterministic, and independence was checked before any
statistic was taken from them (0 of 40 designs returned a replicate identical to itself).

The two arms disagree, and the disagreement is informative rather than a defect: under restraint
the Asp6–Arg114 contact is nearly free, and most designs that show it restrained lose it when the
table is removed.

## Controls

Four systems were predicted with the identical code path and measured with the identical script:

- the groove with **no binder**, 50 models — 0 IN, median 6.31 Å. This is the null the IN counts
  are tested against.
- the groove with the **wild-type** decamer, 65 models — 0 IN. Position 6 is glycine, so the
  measurement cannot succeed; this confirms the script, not the biology.
- the **therapeutic TCR** of 7OW6, 50 models — 42 IN, median 3.04 Å. The positive control.
- a published de novo pMHC minibinder transplanted onto this groove, 25 models — 0 IN. A
  competent binder of a different pMHC does not produce the contact by accident.

A scrambled-CDR series of the TCR degrades monotonically from 34 of 50 to 0 of 25 as more of the
recognition loops are destroyed, which is the behaviour a real readout should show.

## Selection

Four criteria, applied in order, a design tiered by **which** it misses rather than how many: a
design missing the fourth outranks one missing the second. Within a tier, on-groove fraction, then
IN fraction, then the unrestrained margin. The criteria are defined in `docs/metrics.md`.

Three decisions in the final set were taken by the principal investigator against the ranking and
are recorded rather than folded into it:

1. Two designs with **IN 0 of 20** but the cleanest folds and the largest restrained margins were
   kept (`AMBRA_T5_18`, `AMBRA_T5_19`).
2. Six ranked designs were removed — three for a terminal segment judged unsound on inspection of
   the coordinates, three for failing to fold on their own. The first judgement is not reproduced
   by any measurement we have: two of the three rejected sit among the **lowest** terminal
   displacements in the set, and a design with an identical free-terminus profile was kept. It is
   recorded here as what it is, an expert judgement on the structures, not a metric.
3. The replacements were chosen for lineage diversity and required to fold alone. The set spans
   **nine lineages**; the largest contributes eight of the twenty.

## Reproducing any number

Each design directory holds the three structures its numbers come from and a `metrics.json` with
the per-model values. The coordinate file deposited for the G12D complex is the model whose
Asp6–Arg114 distance is the **median** of its ensemble — the representative on the selection axis,
not the best model. `deposited_model_index` and `d6_all_models_A` in `metrics.json` place it.
