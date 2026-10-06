# pKa analysis of the pH switch

## The switching ceiling is a hard number

For a 6.5 -> 7.5 window the per-site charge swing `f(6.5) - f(7.5)` is maximal at **pKa = 7.00**
(the window midpoint) where it equals **0.519 charge units**. pKa 6.5 or 7.5 still delivers 79%;
pKa 6.0 or 8.0 only 40%.

**A maximal pKa up-shift is therefore wrong.** An unperturbed surface His already sits near 6.5
(79% of ceiling); over-shifting past 7.5 loses more than it gains. The design target is a modest,
tuned up-shift of about +0.5, and roughly 2 in-window sites are needed per charge unit of swing.

## Measured on the designs

| construct | His in window (% of ceiling) | q(6.5) | q(7.5) | dq | NCPR(7.5) |
|---|---|---|---|---|---|
| R3_01 parent | none (6.33, 6.29) | -11.96 | -13.12 | -1.16 | -0.119 |
| R3_01 Y42H | H42 6.56 (83%) | -11.44 | -13.01 | -1.58 | -0.118 |
| R3_01 Y42H+Y38H | H38 7.21 (96%), H42 7.40 (86%) | -10.23 | -12.31 | **-2.08** | -0.112 |
| R3_03 parent | H63 **7.20 (96%)** | -6.94 | -7.70 | -0.76 | -0.062 |
| R3_03 R42H | H42 **7.19 (97%)**, H63 7.20 (96%) | -7.11 | -8.37 | -1.26 | -0.068 |

Every carboxylate on **these** scaffolds sits at pKa <= 5.44, so there is no competing acid titration
in the window for the constructs tabulated above. **That does not generalise to the whole submission** --
see the full-set run below, where 6 of 23 designs carry at least one acid above pKa 5.5.

## The exhaustive surface scan

Every surface position with a carboxylate in histidine reach, on all 13 scaffolds — 94 positions,
188 variants plus parents, each measured whole-pose at both pH with 8 replicates and PROPKA on the
same relaxed structure (194 tasks, ~23 CPU-hours).

| condition | pass rate |
|---|---|
| titrates (Rosetta packer) | 19/94 (20.2%) |
| pKa inside [6.5, 7.5] (PROPKA) | 39/94 (41.5%) |
| bridge formed <= 4 A | 20/94 (21.3%) |
| fold worse at 7.5, beating its Ala control | 25/94 (26.6%) |
| binding weaker at 7.5 | 62/94 (66.0%) |
| **all four** | **2/94 (Rosetta) / 4/94 (PROPKA)** |
| structurally broken | **0/94** |

Best charge-correct candidate: **R4_04 K38H** -> Glu41, pKa 7.15 (97.8% of ceiling), bridge
3.83 -> 4.40 A, fold +2.52 +- 1.01 REU worse at 7.5 (Ala control +0.79), binding +6.78 REU weaker,
dq -1.20. Lys->His is the best substitution on the charge axis (-1 at 7.5, 0 at 6.5).

## Two method disagreements, unresolved

- **Anchor His433.** PROPKA puts it at pKa 7.95 (74% still protonated at 7.5, i.e. 44% of ceiling);
  Rosetta pH mode put its midpoint at 6.75. They differ by >1 unit and agree only that it exceeds 6.5.
  If PROPKA is right the interface switch runs at under half its theoretical efficiency.
- A carboxylate-pair ("triad") variant of the motif was tested on 33 candidates: the electrochemistry
  is easy (33/33 acids stay ionised) but **0/33 achieved a His hydrogen-bonded to both acids**. The
  motif needs building in during diffusion, not grafting onto a finished backbone.

---

## Full submission: PROPKA on all 23 designs (added with round 5)

Run with `protocol/scripts/round5/ph_pka.py` (PROPKA 3.5.1) on the **primary unconstrained human
co-fold** of every design, in two states:

- **free** — the binder chain alone. This is the state the composition/charge envelope refers to,
  because the free binder is what has to express and stay soluble.
- **complex** — the binder with domain III. The interface shifts the anchor-facing His, so this is the
  state that matters for the switch.

Tables: `metrics/propka_all_designs.csv` (one row per design), `metrics/propka_histidines.csv` (one
row per His per state), raw PROPKA output in `metrics/propka_raw/*.pka`. Eight summary columns are
also carried in `SUBMISSION.csv`, populated for all 23 designs.

> **Window note.** The sections above use a 6.5 / **7.5** window (ceiling 0.519 e/site at pKa 7.00).
> This run uses 6.5 / **7.4** to match the blood-pH figure used elsewhere in the submission, so its
> ceiling is **0.476 e/site at pKa 6.95**. Percentages are not interchangeable between the two.

### Net charge of the free binder

| | range across 23 | median |
|---|---|---|
| q(pH 6.5) | -11.24 .. -3.72 | -6.85 |
| q(pH 7.4) | -12.10 .. -4.65 | -8.04 |
| dq = q(7.4) - q(6.5) | -1.80 .. -0.52 | **-0.90** |
| charge / residue, pH 6.5 | -0.0985 .. -0.0448 | |
| charge / residue, pH 7.4 | -0.1090 .. -0.0525 | |

**All 23 designs are more negative at pH 7.4 than at 6.5**, which is the intended direction: less
net charge at the acidic pH where binding should be tight, more at blood pH.

Against the envelope from the confirmed sub-uM all-alpha binders (net charge -19.3..-5.0,
charge/residue -0.12..-0.05, both defined at pH 7):

- net charge inside at **both** pH: **21/23** (`pHsel-04`, `pHsel-18` are *not negative enough*)
- charge/residue inside at **both** pH: **19/23** (`pHsel-04`, `pHsel-12`, `pHsel-16`, `pHsel-23`, all less negative. **Every one of these misses is a round-3/4 design**; all 9 round-5 designs are inside.
- only `pHsel-01` exceeds |NCPR| 0.10 at pH 7.4 (-0.109), marginally.

> **The structural and sequence-based models disagree about which designs miss, and in opposite
> directions.** A Biopython Henderson-Hasselbalch calculation on sequence alone flags `pHsel-01` as
> *too* negative (charge/residue -0.124) and puts everything else inside; PROPKA puts `pHsel-01`
> comfortably inside and instead flags four designs as *insufficiently* negative. PROPKA returns less
> negative charges throughout because burial raises Asp/Glu pKa, so the carboxylates are less ionised
> than a sequence model assumes. Both agree that 19-21 of 23 are fine; neither boundary call should be
> treated as firm.

### Histidine pKa — the switch itself

**19 of 23 designs carry at least one histidine inside the switching window** (>= 50% of ceiling),
with a best-His median of **86% of ceiling** and 7 designs at >= 90%. Round 5 does slightly better
than rounds 3-4 on this axis: **8/9 vs 11/14**, with a His-only charge swing of 0.425 vs 0.411 e.

Best examples (complex state): `pHsel-18` HIS20 pKa **6.94 = 100%** of ceiling and `pHsel-04` HIS55 pKa **6.99 = 100%** — both essentially
centred on the 6.5/7.4 midpoint — then `pHsel-15` HIS55 6.83 (98%), `pHsel-03` HIS54 7.21 (93%), `pHsel-14` HIS118 7.25 (91%), `pHsel-08` HIS67 7.26 (91%).

Four designs have **no** in-window histidine and should be read as having little intrinsic charge
switch: `pHsel-10` (49.8%, pKa 7.80 -- just under the 50% cut), `pHsel-16` (28%, pKa 8.13), `pHsel-17` (46%, pKa 6.05), `pHsel-20` (26%, pKa 5.72).

Two failure modes recur and are worth naming:

- **Dead second histidines.** Several designs carry a second His at pKa 3.5-6.0 contributing <= 31%
  of ceiling. It costs nothing but buys nothing.
- **Over-shifting.** `pHsel-06` (pKa 7.62, 64%), `pHsel-10` (pKa 7.80, 50%), `pHsel-16` (pKa 8.13, 28%) are
  shifted past the window and lose more than they gain, exactly as the ceiling argument at the top of
  this file predicts.

### A sequence-only estimate understates the designed chemistry

Using model pKa 5.98 for His, a sequence calculation attributes only **0.195 e** per histidine to the
6.5 -> 7.4 swing, making the N-terminal amine (0.435 e) look like the dominant contributor at ~46% of
dq against ~31% for histidine. With PROPKA structural pKa the His-only contribution is
**0.134-1.027 e (median 0.414)**, i.e. **2.1x larger on the medians** (1.6x on a per-design basis,
since designs differ in how many histidines they carry), and histidine becomes the **largest single
contributor at a median 50%** of the swing. The structural calculation is the one to quote.

### Carboxylate co-titration

Carboxylate pKa medians are 4.33-4.65 per design, so the acids are essentially fully ionised across
the window for most designs. But **7 of 23 designs carry at least one acid above pKa 5.5**, which partially short-circuits the switch by titrating alongside the
histidine. This is reported per design as `acids_n_above_5p5` in `metrics/propka_all_designs.csv`.

### Effect of the cysteine removal

Nine designs had buried unpaired cysteines replaced (METHODS 7c). Where pH selectivity was measured,
the substitution mattered far more than its chemistry suggests: at identical positions, different
residues swing ddG_bind by up to **3.7 REU**. `pHsel-09` goes from +0.85 REU (`C17S;C50S`) to
-2.81 REU (`C17M;C50T`); `pHsel-07` from +3.65 (`C48S;C91A`) to -1.66 (`C48S;C91V`). A buried
cysteine adjacent to the switch is therefore part of the electrostatic environment that sets the
anchor His pKa, not inert packing -- and no interface metric detects this, which is why selectivity
had to be a selection criterion rather than a post-hoc check. All PROPKA figures above are recomputed
on the replacement sequences.

> **Where the numbers live.** `metrics/propka_all_designs.csv` and `metrics/propka_histidines.csv`
> describe the designs **as submitted**, and `metrics/propka_raw/*.pka` holds the raw PROPKA output
> behind them. For the nine designs whose cysteines were replaced these were recomputed on the new
> sequences; `metrics/round5_all_metrics.csv` and `metrics/round5_ph_selectivity.csv` remain the
> round-5 *campaign* record and carry a `disposition` column marking which rows are
> `shipped_as_designed`, `sequence_superseded` or `not_submitted`.
