# Target 4 — de novo binders to a 189-residue epitope on two orthologues (H and M)

Twenty designed peptides, 28–48 residues, standard twenty L-amino acids, designed de novo in this
group. Entirely in silico; nothing here has been tested experimentally.

> **A note on what is and is not disclosed here.** The design engine is **the subject of a
> manuscript in preparation**, so it is described in principle rather than in reproducible detail,
> **ahead of publication**. Nothing needed to *evaluate* these designs is withheld: sequences,
> predicted structures, every per-model measurement, the selection rule and the controls behind it
> are all in this directory. What is held back is how the candidates were *generated*, not how
> they were *judged*.

## The oracle, and why this one

Every number is from **boltz-2, the full-length target (640/641 aa), MSA on BOTH chains, the
design's own declared pocket as one soft 8 Å contact (`force: false`), seed 2000, 5 diffusion
samples.** Target MSA depth 3095 (H) and 2590 (M), built with phmmer against UniRef90.

That configuration was chosen by testing, not assumption. Three binders with deposited co-crystal
structures against this target were folded through every available arm and scored by CA RMSD
against the deposit:

| arm (full length) | B1 | B2 | B3 |
|---|---|---|---|
| single-sequence, pocket | 66.0 Å | 18.3 Å | 36.1 Å |
| MSA both chains, **no** pocket | 89.9 Å | 81.8 Å | 68.2 Å |
| **MSA both chains, pocket** | **2.8 ± 0.3 Å** | 19.0 Å | 16.5 Å |

B1 is reproduced in **5 of 5 models (2.44–3.36 Å), recovering 89–92 % of the deposited contact
set**. Both levers are required: the MSA without the pocket is worse than single-sequence, and the
pocket without the MSA leaves B1 66 Å away. B2 and B3 are not reproduced by any arm tried.

## What the numbers can and cannot support

**The threshold.** T_full = **0.6278** — B1's ipTM, the worst (and only) correctly predicted
binder. **No design in 103 reaches it**; the best sit near 0.52 mean across the two orthologues.

**Confidence does not certify a pose.** In this same arm B2 scores ipTM **0.714**, higher than B1,
on a pose **19 Å** from its crystal structure. ipTM orders candidates; it does not say they are
right.

**Declared-epitope approach has no discriminating power, and was NOT used to select.** With the
pocket declared, all three known binders reach the epitope in 5/5 models — including the two that
are 17–19 Å wrong. With the pocket removed, all three fail 0/5 — including B1. The restraint
steers a pose; it does not score one. All 103 designs approach 5/5, which therefore says nothing
about them.

**The selection criterion is the composition-matched scramble.** Each design was re-folded with its
own residues shuffled — same length, same composition, same cysteine count, everything else
identical. Across the 52 designs tested at the time of deposition:

| | beat their own scramble | sign test |
|---|---|---|
| M | 45 / 52 | p = 3.5 × 10⁻⁸ |
| H | 31 / 52 | p = 0.11 |

Designed sequence **order** is distinguishable from composition on M, and is **not** on H. The
median gap on M is +0.045, against an MSA-depth control of +0.010 (n = 3). **All twenty deposited
designs beat their own scramble on both orthologues** — the conservative requirement, since only M
carries signal.

## The sink, and why the ranking is at full length

The 189-residue window exposes the hydrophobic scar of the excised domain. Sink occupancy there
reaches 0.78; at full length, where the domain it was cut from is present, the whole population
sits at **0.00–0.07**. A design ranked on the window can be sitting in that scar rather than on its
designed site. This deposit is ranked at full length for that reason, and per-design sink occupancy
is in `metrics_full.csv`.

## A measurement bug that was found and fixed

The deposited-target frame was built by walking the residue list and adding one offset. 3kas leaves
residues 316–318 unmodelled — inside the compared region — so every residue after the gap was keyed
3 too low, and B1's target-to-target superposition was built from mispaired residues. Keying on the
deposit's **author numbering** fixes it: B1's contact agreement rose from 0.56 to **0.92** and its
RMSD settled at 2.8 ± 0.3 Å across all five models. The scorer now refuses any deposited chain
below 95 % identity to the window after alignment, so a wrong chain cannot pass silently.

## Population

103 unique designs recovered from 162 runs across every wave and host, deduplicated by sequence,
each folded against **both** orthologues with **its own** declared pocket (the campaign moved its
declared epitope three times, so a single constant would have restrained most of the population to
a site it was never designed for). 34 of the 103 were searched against M.

## Files

| path | contents |
|---|---|
| `submission.csv` | the twenty entries |
| `metrics_full.csv` | every number behind the ranking |
| `DESIGN_STRATEGY.md` | how the designs were made and how the twenty were chosen |
| `SUBMISSION_TEXT.md` | prose summary for the submission form |
| `docs/ranking_all.json` | all 103 designs, both orthologues |
| `ranked/AMBRA_T4_nn/` | `sequence.fasta`, `metrics.json`, `complex_Hfull.pdb`, `complex_Mfull.pdb` |
