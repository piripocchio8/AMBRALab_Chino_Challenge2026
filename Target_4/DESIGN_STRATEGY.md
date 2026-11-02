# Target 4 — design strategy and controls

This document assumes no familiarity with our pipeline. Terms are defined in `README.md` §"Terms
used in this directory"; the important ones are repeated here.

## 1. The problem

Bind the **same site on two orthologues** of one protein — the same protein from two species,
called **H** and **M** throughout. Each is 640–641 residues. A peptide that engages only one of
them does not solve the brief.

The difficulty is that the site is **not conserved between the two**. Over the 189-residue region
containing the target site the two orthologues are only **69.8 % identical**, and they differ at
*every* position any of our design rounds declared as a contact point:

| position (in the 189-residue region) | residue in H | residue in M |
|---|---|---|
| 17 | Arg | Gly |
| 18 | Leu | Asn |
| 20 | Tyr | Asp |
| 179 | Ser | Asn |
| 180 | Lys | Gln |

A peptide optimised against one orthologue therefore has no guarantee of transferring, and that is
exactly what the results show.

## 2. How the designs were made

A sequence-design engine developed in this group: it proposes candidate peptide sequences, folds
each one against the target with a structure-prediction oracle, keeps what the oracle rates
highest, and iterates. The engine's internals are the subject of a manuscript in preparation and
are described here in principle rather than in reproducible detail — see the disclosure note at
the end. Every delivered sequence uses only the standard twenty L-amino acids.

The campaign ran in several rounds, and **the target site moved between rounds** — three different
sites were declared over its lifetime (positions 17+180, position 20, and position 179 in the
189-residue numbering). This matters for evaluation: each design is scored against **the site it
was actually designed for**, read from that run's own stored configuration file. Scoring a design
against a different round's site would measure whether it binds somewhere nobody asked it to.

103 unique designs survived deduplication by sequence. **34 of them were designed against M**; the
rest against H.

## 3. Choosing the evaluation method — the part that constrains everything else

We treated "which prediction setup should we trust?" as an experiment with a known answer.

**The controls.** Three published binders of this target — called **R1, R2, R3** here — each have
an experimentally determined structure in complex with the target. They are not our molecules.
Their correct answers are known, so any prediction setup can be scored against them.

**The sweep.** R1–R3 were predicted with three programs (Chai-1, Protenix, boltz-2), against both
the full-length protein and a 189-residue fragment of it, with and without evolutionary alignments
(MSAs) supplied for the chains, and with and without the target site declared to the program as a
soft 8 Å restraint. Every prediction was compared to its experimental structure by CA RMSD.

**The outcome.**

| setup (full-length target) | R1 | R2 | R3 |
|---|---|---|---|
| no MSA, site declared | 66.0 Å | 18.3 Å | 36.1 Å |
| MSA, **no** site declared | 89.9 Å | 81.8 Å | 68.2 Å |
| **MSA + site declared** | **2.8 ± 0.3 Å** | 19.0 Å | 16.5 Å |

One setup reproduces one structure: boltz-2, full length, MSAs on both chains, site declared. R1 in
**5 of 5 models at 2.44–3.36 Å**, recovering 89–92 % of the experimentally observed contacts. Both
ingredients are load-bearing — the MSA *without* the site is worse than no MSA, and the site
*without* the MSA leaves R1 66 Å away.

**R2 and R3 are reproduced by nothing we tried.** The method is capable on one real binder in
three. Everything in this deposit is reported against that standard.

Parameters, for reproduction: boltz-2, `msa` supplied for both chains (target alignment depth 3095
for H, 2590 for M, built with phmmer against UniRef90), one `pocket` constraint at
`max_distance: 8.0, force: false`, `diffusion_samples: 5`, `seed: 2000`.

## 4. Why not the 189-residue fragment

Early rounds evaluated on the fragment because it is cheap to fold. It is also misleading.

Cutting a 189-residue piece out of a 640-residue protein exposes a hydrophobic surface that is
buried in the intact protein. Predicted peptides are strongly drawn to it — covering an exposed
greasy patch is favourable — so a peptide can score well while sitting in an artefact of the cut.
Two independent prediction programs converge on that same patch, so it is a property of the
construct, not of one program.

Measured: occupancy of that patch reaches **0.78** on the fragment and **0.00–0.07** on the
full-length protein. The highest-scoring design under the old fragment-based ranking sat at 0.78 —
i.e. it was ranked first for binding the scar of the cut. This deposit is ranked at full length and
reports per-design occupancy (`sinkfrac_fulllength_H/M`).

## 5. Why the twenty were not chosen on confidence or on reaching the site

Both were tested as selection criteria against R1–R3 and both fail.

**Reaching the declared site carries no information.** With the site declared, all three published
binders reach it in 5 of 5 models — including R2 and R3, whose predictions are 17–19 Å wrong. With
the site not declared, all three fail in 5 of 5 — including R1, the one that is right. The
restraint steers the peptide to the site; it does not evaluate whether the peptide belongs there.
All 103 of our designs reach their site 5/5, which separates none of them.

**Confidence does not certify an answer.** R2 scores ipTM 0.714 — higher than R1's 0.628 — on a
prediction 19 Å from the experimental structure.

## 6. What the twenty were chosen on

**A negative control: the design against its own shuffled sequence.** Each design was predicted a
second time with its residues permuted into random order — identical amino-acid composition,
identical length, identical everything else including the target, the MSAs and the declared site.
If a design does not outscore its own shuffle, its score reflects what it is made of rather than
how it is arranged.

Across all 103 designs:

| | beats its own shuffle | sign test |
|---|---|---|
| on M | **80 / 103** | p = 7.3 × 10⁻⁹ |
| on H | 63 / 103 | p = 0.015 |

Median advantage +0.035 ipTM on M. A possible confounder — that supplying an MSA for the peptide
itself raises its score, which shuffles never get — was measured separately at **+0.010**, well
below the effect.

**54 of 103 beat their shuffle on both orthologues. The twenty deposited are the
highest-confidence members of that set**, ordered by mean ipTM across the two orthologues.
Designs that fail the control are not deleted; they are ranked after every design that passes, and
the reason is in their row of `docs/ranking_all.json`.

Eight of the twenty come from the 34 designs searched against M, and those have the most balanced
two-orthologue profiles in the campaign.

## 7. Limits, stated

- **No design reaches R1's confidence** (0.628). Our best is about 0.52.
- **Nothing has been tested experimentally.**
- The evaluation rests on **one** reproduced structure out of three available controls.
- The shuffle control establishes that residue *order* matters to the score. It does not establish
  binding, affinity, or selectivity.
- The H-side shuffle signal (p = 0.015) is an order of magnitude weaker than the M-side one.

## 8. A measurement error found and corrected

Comparing a prediction to an experimental structure requires first aligning the two copies of the
target residue by residue. Our code walked the residue list and applied one constant offset, which
is correct only if the experimental file contains every residue. One reference structure is missing
three residues that were never resolved experimentally, and that gap falls **inside** the compared
region — so every residue after it was matched to the wrong partner and R1's comparison was
computed in a distorted frame.

Keying instead on the residue numbering recorded in the experimental file, which skips unresolved
gaps correctly, fixed it: R1's contact agreement rose from 0.56 to **0.92** and its error settled
at 2.8 ± 0.3 Å across all five models. Every figure in this deposit is from after the fix, and the
checker now refuses any reference structure falling below 95 % sequence identity to the target
region.

---

## A note on what is and is not disclosed here

The design engine is **the subject of a manuscript in preparation**, so it is described above in
principle rather than in reproducible detail, **ahead of publication**.

Nothing needed to *evaluate these designs* is withheld: the sequences, the predicted structures,
every per-model measurement, the selection rule and the controls behind it, the declared sites, and
the full ranked population of 103 are all in this directory, and every number quoted can be
recomputed from the files beside it. What is held back is how the candidate sequences were
*generated*, not how they were *judged*.

We will release the engine and its parameters with the publication, and are glad to discuss the
method in confidence with the organisers in the meantime.
