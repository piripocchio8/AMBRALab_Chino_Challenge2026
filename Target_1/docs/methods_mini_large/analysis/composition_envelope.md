# The composition envelope: where it comes from, and what it is not

Round 5 gates every candidate on four composition axes before folding, and eight of the twenty-three
submitted designs are flagged as outside them. That makes this the most consequential single
criterion in the submission, so its provenance belongs on the record.

## The bounds

| axis | bound | centroid used as the design target |
|---|---|---|
| alanine fraction | <= 0.104 | 0.085 |
| hydrophobic AVILMFWY | 0.329 – 0.42 | 0.376 |
| net charge at pH 7 | −19.3 … −5.0 | — |
| pI | 4.60 – 5.00 | — |

## Where they come from

They are the **observed range of a small set of all-alpha EGFR binders from the previous Adaptyv
competition round that were experimentally confirmed sub-micromolar.** Each bound is the minimum or
maximum actually seen in that set — the alanine ceiling of 0.104 is the highest value among them,
the hydrophobic interval is their full span, and the centroid is their mean.

**This analysis is not included in this repository.** It was performed on the published round-2
all-alpha cohort, and the figures quoted from it in `README.md` section 4 — median binder length
228 aa against ~100 aa for non-binders, 8.5% alanine and 0.376 hydrophobic fraction for the eleven
confirmed binders of that class, and 15.8% alanine as the highest value in any observed binder — are
**external**: a reader cannot check them against anything shipped here. They are reported because
they drove design decisions, and flagged as external for exactly that reason.

By contrast, everything in `analysis/what_predicts_binding.md` **is** computed on data we assembled
(the 3027-design / 32-target Proteinbase harvest and its 800-design EGFR subset) and is internally
checkable.

## What this envelope is not

- **Not a fitted model.** No regression, no cross-validation, no held-out test. It is a bounding box
  around a handful of successes.
- **Not a physical limit.** A design outside it is not predicted to fail; it is outside the range
  where this particular class of binder has been observed to succeed.
- **Not derived from a large n.** The confirmed sub-micromolar all-alpha set is on the order of ten
  designs. Four bounds from ten observations will be tight in some directions by chance.
- **Not consistent with our own binding analysis on one axis.** `what_predicts_binding.md` finds that
  alanine does **not** discriminate binding within the 100–140 aa regime our designs occupy
  (p = 1.00) and does not affect expression (p = 0.47). The alanine ceiling is therefore an argument
  from *sitting inside the observed envelope of successes*, not from a demonstrated effect on
  binding. We applied it anyway, because when a mechanism is as unusual as a pH switch it is worth
  staying inside the region where the scaffold class is known to work.

## How to re-derive or replace it

`metrics/cumulative_ranking_inputs.csv` carries each design's four axis values and its envelope
verdict, so the ranking can be recomputed under any other bounds. The penalty applied in the ranking
is 0.030 ipSAE-equivalent per violated axis; set it to zero and the envelope stops influencing order
entirely.
