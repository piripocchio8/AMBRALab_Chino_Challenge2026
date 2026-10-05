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

Every carboxylate on every scaffold sits at pKa <= 5.44, so there is no competing acid titration in
the window on any design.

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
