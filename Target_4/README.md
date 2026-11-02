# Target 4 — twenty de novo peptide binders, designed against two orthologues

**What this is.** Twenty peptides, 28–48 residues, made of the standard twenty L-amino acids. They
were designed from scratch by computer — they are not variants of any known binder and have no
sequence relationship to one. **Nothing here has been made or tested in a laboratory.** Every
number in this directory is a property of a structure prediction.

**Submit:** `submission.csv` (the twenty sequences). `SUBMISSION_TEXT.md` is the prose summary.

---

## Terms used in this directory

Read this first; the rest of the document assumes it.

| term | meaning |
|---|---|
| **H** and **M** | The two **orthologues** of the target protein — the same protein from two species. Each is 640–641 residues. A peptide that binds only one of them is not a solution; the brief is to bind both. They are called H and M throughout, deliberately and consistently. |
| **the epitope** | The patch on the target that a peptide was designed to bind. Different design rounds aimed at different patches, so each design carries **its own** epitope, listed per design in `metrics_full.csv` (`pocket_H`, `pocket_M`). |
| **the 189-residue window** | A short fragment cut out of the 640-residue target, containing the epitope. Early design work used this fragment because it is cheap to fold. **It turned out to be misleading** — see "Why full length" below. Residue numbers in `pocket_H` / `pocket_M` are positions within this fragment. |
| **R1, R2, R3** | Three **reference binders**: real molecules, already published, each with an experimentally solved 3-D structure bound to this target. They are not ours. They are used here only as **positive controls** — molecules whose correct answer is already known, so a prediction method can be tested against them. |
| **ipTM** | A score from 0 to 1 that the prediction program outputs for how confident it is in the interface between two chains. Higher is more confident. It is a confidence, not a measured affinity. |
| **CA RMSD** | How far a predicted peptide sits from where the experiment says it sits, in ångströms, after aligning the targets. Below ~5 Å means "essentially the right answer"; 15–20 Å means "wrong place or wrong orientation". |
| **a scramble** | The same peptide with its residues **shuffled into a random order**. Same amino acids, same length, same composition — only the order is destroyed. Used as a negative control. |

---

## 1. How the prediction method was chosen

We did not assume a prediction program works on this target. We tested it.

The three reference binders R1, R2 and R3 were predicted using every combination available to us —
three different prediction programs, the short 189-residue fragment and the full 640-residue
protein, with and without an evolutionary alignment (MSA) supplied, and with and without telling
the program which patch to aim at. Each prediction was then compared against the published
experimental structure.

**Exactly one combination reproduces a published structure**: boltz-2, the **full-length** target,
an MSA supplied for **both** chains, and the target patch declared as a soft 8 Å restraint.

| setup (full-length target) | R1 | R2 | R3 |
|---|---|---|---|
| no MSA, patch declared | 66.0 Å | 18.3 Å | 36.1 Å |
| MSA, **no** patch declared | 89.9 Å | 81.8 Å | 68.2 Å |
| **MSA + patch declared** | **2.8 ± 0.3 Å** | 19.0 Å | 16.5 Å |

R1 is reproduced in **all 5 predicted models (2.44–3.36 Å)**, recovering 89–92 % of the contacts
seen in the experimental structure. Both ingredients are needed: the MSA without the patch is
*worse* than no MSA at all, and the patch without the MSA leaves R1 66 Å away.

R2 and R3 were not reproduced by any setup we tried. **So the method is demonstrably capable on one
of three real binders, and demonstrably fails on the other two.** That is the honest basis for
everything below, and it is why the caveats in section 4 are not boilerplate.

---

## 2. Why full length, and not the short fragment

Cutting a 189-residue fragment out of a 640-residue protein exposes a surface that is normally
buried inside the intact protein — a greasy (hydrophobic) patch at the cut. Predicted peptides are
strongly attracted to it, because covering an exposed greasy patch is energetically favourable.
A peptide can therefore score very well on the fragment while sitting in an artefact of the cut
rather than on its intended site.

Measured: occupancy of that patch reaches **0.78** (78 % of a peptide's contacts) on the fragment,
and falls to **0.00–0.07** on the full-length protein, where the rest of the protein covers it
again. Per-design values are in `metrics_full.csv` (`sinkfrac_fulllength_H/M`).

Every number in this deposit is therefore from the **full-length** protein.

---

## 3. How the twenty were chosen

**Not by confidence**, and **not by whether the peptide reaches its intended patch.** Both were
tested and both failed as selection criteria:

- **Reaching the intended patch does not discriminate.** When the patch is declared to the program,
  all three reference binders reach it in 5 of 5 models — *including R2 and R3, whose predictions
  are 17–19 Å wrong*. When the patch is not declared, all three fail in 5 of 5 — *including R1,
  the one that is right*. The restraint steers the peptide; it does not evaluate it. All 103 of our
  designs reach their patch 5/5, which therefore says nothing about any of them.
- **Confidence does not certify an answer.** In this same setup R2 scores ipTM **0.714**, *higher*
  than R1's 0.628, on a prediction 19 Å from the experimental structure.

**Selection used a negative control instead.** Every design was predicted a second time with its
own residues shuffled into random order — same composition, same length, everything else identical.
If a design's score is no better than its own shuffle, its score reflects what it is *made of*, not
how it is *arranged*, and it has shown nothing.

Across all 103 designs:

| | design beats its own shuffle | sign test |
|---|---|---|
| on **M** | **80 / 103** | p = 7.3 × 10⁻⁹ |
| on **H** | 63 / 103 | p = 0.015 |

So designed *arrangement* carries real signal on M and much weaker signal on H. A control for a
confounding factor (whether having an MSA for the peptide itself inflates the score) measured
+0.010, far below the median effect of +0.035.

**All twenty deposited designs beat their own shuffle on both orthologues** — 54 of 103 qualify,
and the twenty are the highest-confidence members of that set. Designs are ordered by their mean
ipTM across the two orthologues.

---

## 4. What this deposit does **not** claim

**No design reaches the confidence of the one reference binder the method gets right.** R1 scores
ipTM 0.628; our best designs reach about 0.52. That gap is real and is not argued away.

**Confidence does not mean correct** (see R2 above, 0.714 on a 19 Å error).

**Nothing has been tested experimentally.** No binding assay, no synthesis, no expression.

These twenty are the designs for which we have the strongest computational evidence — specifically,
that their score depends on the order of their residues and not merely on their composition, on the
one prediction setup we could show reproduces a real answer. That is the claim, and it is the whole
claim.

---

## 5. A measurement error we found and fixed

When comparing a prediction to an experimental structure, the two targets must be aligned
residue-by-residue first. Our code did this by walking down the list of residues and applying a
single offset — which is only correct if the experimental structure contains every residue.

One of the three reference structures is missing three residues that were not resolved
experimentally, and the gap falls inside the compared region. Every residue after the gap was
therefore matched to the wrong partner, and R1's comparison was computed in a distorted frame.

The fix keys on the residue numbering recorded in the experimental file, which skips gaps
correctly. R1's contact agreement rose from 0.56 to **0.92** and its error settled at 2.8 ± 0.3 Å
across all five models. **Every figure in this document is from after the fix.** The checker now
also refuses any reference structure that fails to match the target sequence, so a wrong file
cannot pass silently.

---

## 6. Where the designs came from

103 unique designs were produced across several design rounds on several compute clusters, then
deduplicated by sequence. Each was predicted against **both** orthologues using **its own**
declared epitope — the campaign aimed at three different patches over its lifetime, so a single
shared epitope would have restrained most designs to a site they were never designed for.

34 of the 103 were designed against M specifically; **eight of the twenty deposited designs come
from that group**, and they have the most balanced two-orthologue profiles in the set.

---

## 7. Files

| path | contents |
|---|---|
| `submission.csv` | the twenty sequences — **this is the submission** |
| `SUBMISSION_TEXT.md` | prose summary for the submission form |
| `metrics_full.csv` | every number behind every deposited design |
| `DESIGN_STRATEGY.md` | fuller account of the method and the controls |
| `docs/metrics.md` | definition of every column in `metrics_full.csv` |
| `docs/ranking_all.json` | all 103 designs with both orthologues' numbers, not only the winners |
| `ranked/AMBRA_T4_01 … _20/` | per design: sequence, metrics, and the predicted complex with each orthologue |

> **Note on two superseded directories.** `h_anchored/` and `dual_lean/` are left over from an
> earlier version of this deposit that ranked designs on the 189-residue fragment. They are
> **not** part of this submission — `ranked/` is. They are retained rather than deleted so the
> change is auditable; they can be removed with
> `git rm -r Target_4/h_anchored Target_4/dual_lean`.
