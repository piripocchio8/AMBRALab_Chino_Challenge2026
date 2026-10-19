# Methods: a binder released by acidification, built on His⁺/Lys⁺ repulsion

Challenge 2026, Target 2. Written for challenge reviewers and for other designers who may want to
reuse or criticise the protocol. Every number quoted here was measured by us; where a quantity was
not measured it is said so rather than estimated.

> ### Status of this document
>
> An earlier draft was written **while the folding that selects the band was still running**, and
> marked every unmeasured figure with `[[PENDING: … ]]`, which is a marker and not a number. The
> band now exists and all of those are resolved — filled from a named result file, or replaced by a
> sentence saying the figure does not exist. Figures belonging to the *campaign* rather than to a
> design are given with their denominators and the arm they came from.
>
> **Two things changed in the reconciliation, and both are corrections rather than additions.** The
> ranking rule in §4.4 is the one that actually cut this band, not the previous round's rule an
> earlier draft described. And the pose definition in §4.3 is now the symmetry-aware one, because
> the target is a C3 homotrimer and the previous definition scored chemically identical poses as
> though they were 20 Å apart.

> ### "Protonation-driven" is the objective. Nothing here measures it.
>
> No protonation state was varied anywhere in this campaign. The oracles are heavy-atom only and
> have no concept of one, there is no pH titration and no binding measurement, and the two orthologs
> differ in **sequence and length**, not in pH. Every statement about acid in this document is a
> statement about what the designs were *selected for*.

> ### A note on what is and is not disclosed here
>
> The design engine — a population-based evolutionary optimiser that scores candidate sequences
> directly against the structure oracle, coupled to an interaction-preserving inverse-folding
> refinement — is **the subject of a manuscript in preparation**. Its internal machinery (the
> objective's term set and weights, the population scheme and its operators, the acceptance and
> re-grounding logic) is therefore described here in principle rather than in reproducible detail,
> **ahead of publication**.
>
> Nothing needed to *evaluate these designs* is withheld. The sequences, the predicted structures,
> every per-model measurement, the selection bar and its threshold, the restraint files, the fold
> commands and the failures are all in this repository, and every number quoted can be recomputed
> from the files beside it. What is held back is how the candidate sequences were *generated*, not
> how they were *judged*.
>
> We will release the engine and its parameters with the publication, and are glad to discuss the
> method in confidence with the organisers in the meantime.

---

## 1. The design problem

### 1.1 The target, as folded

Every prediction in this work folds the **physiological homotrimer** with the binder as a fourth
chain: protomers as chains **A, B, C** and the binder as chain **D**. Chain composition is verified
on the delivered folds rather than assumed — a completed prediction reads **A = 149, B = 149,
C = 149, D = 39**.

The human construct, 149 residues per protomer:

```
SDKPVAHVVANPQAEGQLQWLNRRANALLANGVELRDNQLVVPSEGLYLIYSQVLFKGQGCPSTHVLLTHTISRIAVSY
QTKVNLLSAIKSPCQRETPEGAEAKPWYEPIYLGGVFQLEKGDRLSAEINRPDYLDFAESGQVYFGIIAL
```

The mouse construct, 148 residues per protomer:

```
SDKPVAHVVANHQVEEQLEWLSQRANALLANGMDLKDNQLVVPADGLYLVYSQVLFKGQGCPDYVLLTHTVSRFAISYQ
EKVNLLSAVKSPCPKDTPEGAELKPWYEPIYLGGVFQLEKGDQLSAEVNLPKYLDFAESGQVYFGVIAL
```

Positions in this document are positions in **those** constructs.

**The organisers' own Target-2 construct is not established here, and there is no offset to give.**
We could not find its accession or residue range in the documents available to us, and we have not
guessed at one: an offset stated without its source is worse than an absent offset, because it
silently renumbers every distance in this file. Everything here is in construct-local numbering so
that an offset can be applied later without re-deriving anything.

### 1.2 The epitope, and why it is a lysine pair

The human protomer carries **six** lysines — 3, 57, 82, 90, 104, 120. The designed epitope is
**Lys57 and Lys104** on a single protomer. In the mouse protomer the equivalent pair is **Lys57 and
Lys103**: mouse position 104 is a **proline**, so the second site is not at the same index in the two
orthologs. Every restraint used in this work is derived per species from the campaign's own
definition rather than copied across, because an earlier file that ignored this restrained every
mouse fold to a proline.

A lysine ammonium has a side-chain pKa near 10.5, so it carries its positive charge across the whole
pH range of interest. A histidine does not: its imidazole is neutral at pH 7.4 and the imidazolium at
pH 6.5.

### 1.3 The mechanism, stated as the thing being optimised

The binder carries **its own histidines** into that lysine pair. At blood pH they would be neutral
beside a permanent cation; as the pH falls each would acquire a formal +1 charge **next to** a
cation. The design objective is that the complex should be **destabilised** by that, so the binder
holds at pH 7.4 and is released at pH 6.5.

**That paragraph is entirely an objective.** Nothing in this campaign varies a protonation state,
and §2 says why nothing could: the oracle is heavy-atom only and has no hydrogens. The 5–7 Å window
below is a *geometric proxy* chosen because the charge states of the two groups are known from their
pKa values — it is a distance that *would* matter if the ring protonated, measured on structures in
which the ring has no protons at all.

Two consequences follow immediately and they govern the whole protocol:

**It is proximity that is designed, not a hydrogen bond.** The criterion is a **5–7 Å window** from
the designed histidine to the epitope. Coulombic destabilisation does not require a specific bond,
and requiring one would specify a geometry the mechanism does not need. The previous round's scoring
tools used a **7.0 Å** window as the figure of merit throughout, with a 3.5 Å hydrogen-bond test only
as a separate readout; this round measured the two lysine approach distances and the
interfacial-histidine count instead (§4.3), and the 7 Å joint criterion was not recomputed for the
delivered band.

**The two histidines must land on the same protomer.** The designed epitope spans about **15 Å on one
subunit**. A restraint aimed at two different protomers asks for a bridge of about **29 Å** across a
subunit boundary, which is a different molecule's problem. This is not hypothetical: under such a
file, **150 of 167 folds (90 %)** put the two histidines on different subunits and **not one** put
both within 3.5 Å of a single protomer. Under the corrected single-protomer restraint, **48 of 48**
parent folds put both histidines on protomer A.

**"Specific" means reproducibly engaged, with whatever residue.** Each histidine must be engaged with
*something* on the target, repeatably across independent refolds, so that the pose is a property of
the sequence and not of a draw. Measured on the parent designs: **His26 hydrogen-bonds Glu102 (human)
/ Glu101 (mouse) in 5 of 5 reproducible cases**, while **His13 hydrogen-bonds in 63 % of folds with
no consistent partner** (3 distinct partner tags across 20 designs). One of the two designed
histidines has the property and one does not. That is a measurement, it was not designed in, and it
is why the current round's bar is **any two histidines at interfacial positions** rather than two
named ones.

### 1.4 How this differs from Target 1, since both are called "pH switches"

| | Target 1 | Target 2 |
|---|---|---|
| titratable group | a histidine **of the target** | histidines **of the binder** |
| partner | binder carbonyls, or an engineered carboxylate | **target lysines**, cationic at every pH of interest |
| protonation is designed to add | hydrogen bonds | **like-charge repulsion** |
| intended direction | tighter in acid | **released in acid** |
| geometric requirement | a hydrogen bond, by four criteria | **proximity**, 5–7 Å |

They share no chemistry and no machinery, and a failure of one says nothing about the other.
**Neither direction has been observed in either target**; both rows are design objectives.

---

## 2. The structure oracle

Structure prediction uses **Chai-1** as a **forward-folding oracle**. The design loop proposes a
sequence, the oracle predicts the structure of the binder-target complex, and the prediction is
measured. No gradients are taken through the predictor and no part of it is retrained or fine-tuned;
it is a black-box scoring function over candidate sequences.

Two properties of the oracle govern everything downstream.

> **It is heavy-atom only. It has no hydrogens and no concept of protonation state.**

There is no way to ask it for the protonated form of a histidine, so **protonation can only ever be
expressed, and measured, as geometry and charge assignment**. For this target that is less of a
constraint than for Target 1: the mechanism is a distance between two groups whose charge states are
known from their pKa values, so what has to be measured is a distance, not a bond.

> **It is nondeterministic on this system.** The same sequence and the same seed can give poses about
> 9 Å apart.

Everything is therefore a median or a rate over many independent models, with its denominator
reported, and nothing is ranked on a best model — the best of *n* draws is a property of *n*.

**Fold-to-fold spread is the precision bound on every ranking in this document.** Measured over 98
design-species pairs and 294 folds, the within-design standard deviation of the primary distance is
**1.82 Å**, so a three-fold mean carries a standard error of **1.05 Å**. Resolving a 1 Å gap takes
13 folds; a 2 Å gap takes 3.

The second oracle is **Boltz-2**, run on the identical assembly and the identical single restraint,
over all 325 designs of this round.

**The third oracle is Protenix, and it carried no restraint.** It was run over the top 50 only, five
models per design, on both orthologs, with a second human draw at a different seed. Its input JSON
holds only `name` and `sequences`: the string "constraint" does not occur anywhere in it, verified
by reading the file, and the build's constraint embedders are disabled in every configuration block.
**Protenix is therefore a reading of the *unrestrained* experiment**, while the other two carried
the 8 Å Lys57 pocket. Agreement it reached with the primary oracle would have been agreement across
a restraint difference, which is harder to obtain and more interesting if found; disagreement cannot
be pinned on the model alone. Every column carrying its numbers is named
`protenix_unrestrained_*` so that the difference travels with the figure.

**The same quantity was computed the same way on all three.** Interface ipTM is the maximum over the
three (target protomer, binder) pairs in both matrix orientations, per design the median over five
samples with its spread, never the best sample — Protenix's chain-pair matrix is asymmetric, so the
both-orientations rule is load-bearing. Binder pLDDT is the per-token mean over the binder's 39
tokens on all three arms. The per-model measurement is literally the same code; only the translation
from each oracle's output format differs.

**The ortholog each arm folded was read back out of the structures**, not assumed: the first target
chain of each prediction was compared against the two construct sequences (149 aa human, 148 aa
mouse). Protenix was human in 50 of 50; the other two were spot-checked at 25 each. The binder
sequence was verified identical between the human and mouse arm of the same design on all three
oracles, 50 of 50.

---

## 3. Design strategy

Backbones were not diffused and threaded. Candidate sequences were optimised **directly against the
structure oracle** by a population-based evolutionary algorithm driving an objective function over
candidate sequences, then refined by **interaction-preserving inverse folding with CARBonAra**.
Binders are cyclic, closed by a **real disulfide between the first and last residue** rather than by
a head-to-tail amide, and are built from the twenty standard amino acids only — there is no
non-canonical chemistry anywhere in this target and no D-residue in the submitted band.

### 3.1 The refinement step, and what it is worth

For each candidate, the positions carrying the design are held fixed and the rest of the binder is
rebuilt by a context-aware all-atom inverse-folding model conditioned on the target chain as fixed
context. The held set for this target is **both cysteines of the disulfide and every histidine** —
widened from a fixed four-position set once the measurements in §1.3 showed that engagement is not
confined to the two originally designed histidine positions. The target sequence cannot change and is
verified unchanged in the output.

**It is a diversity generator, not an improver, and it is reported as one.** Over 42 repacks of 8
parents:

| question | pre-stated threshold | measured |
|---|---|---|
| does repacking raise the worse-species interface confidence of its own parent? | median gain > +0.05 | **+0.028**, IQR −0.046 … +0.092, 26 of 42 above parent — **refuted** |
| does the parent backbone set engagement? | η² > 0.50 confirm, < 0.25 refute | **0.131** on the continuous measure — **refuted** |
| do refolds of one sequence agree more than independent draws? | — | **0.561 observed against 0.258 expected** — a sequence has a reproducible propensity |

So repacked sequences differ from one another **for real** without the mean moving. Selecting among
repacks is worth doing; crediting the repack step with an improvement is not. Consistent with that,
two parents and two repacks occupy the top four of the previous round's ranked arm — repacks do reach
the top, they just do not get there *because* they were repacked.

**A defect in that step, found and fixed on 18 October 2026.** The backbone handed to the
inverse-folding model was built without its carbonyl **O** atom. The cost was measured rather than
assumed (score 0.191 → 0.442 over three parents, distributions disjoint in every one) and the code
was corrected. The 42-repack verdict above was computed on input now known to be defective.

**It has since been re-measured on the corrected code, over this round's 325 folds, and it holds.**
Over 32 family originals with at least two complete repacks each, on interface ipTM the *typical*
repack is **worse** than its own original — mean-vs-mean **−0.028**, and only **43.8 ± 6.8 %** of
repacks beat their original, below the 50 % that exchangeability predicts. The best of about nine is
better only because the spread is wide.

**On binder pLDDT the direction is opposite and the result is confounded, so it is named rather than
claimed.** Mean-vs-mean **+0.044**, **62.5 ± 6.5 %** of repacks beat their original, and the gate
fraction differs sharply (originals 33 %, repacks 55 %). But the repacks that were folded are the
**top-scoring qualifiers** of each original while the original itself was never scored by that
model, and that score is plausibly correlated with folding confidence. Separating repacking from the
selection that produced the repacks would need the unselected qualifiers folded, which they were
not.

**A statistic that looks decisive and is not.** An "excess over null" built from each original's own
model-to-model spread is strongly positive on both axes (+0.115 ± 0.036 and +0.132 ± 0.020,
Wilcoxon p ≤ 0.002). It is reported because it was asked for, and it is **not** an effect size: the
primary oracle's within-design spread on interface ipTM has a median of 0.0059, real repacks carry
different sequences and their between-repack spread is an order of magnitude larger, so a max-based
statistic against that null is guaranteed positive the moment repacking changes anything at all.

### 3.2 Filtering before folding

Inverse-folding output is filtered before anything is folded, on the bar in §4.1. Qualifiers are then
ordered by the inverse-folding model's own score, with the entropy over rebuilt positions breaking
ties, and at most ten are taken per parent. **Score is used to order qualifiers, never to select
them**, and §4.1 gives the measurement that forced that distinction.

---

## 4. Selection and validation

### 4.1 The membership bar: at least two interfacial histidines

A variant qualifies when it carries **at least two histidines at interfacial binder positions**,
where interfacial means a binder position with **any heavy atom within 8.0 Å of any target heavy
atom**, measured in that parent's own seed structure.

Applied to **all 3,960** generated variants of **33** parents:

| | n |
|---|---|
| variants examined | **3,960** (33 × 120) |
| clearing ≥ 2 interfacial histidines | **1,357** |
| clearing ≥ 3 | **489** |
| carried forward (qualifiers, score-ordered, ≤ 10 per parent) | **292** |
| parents that cannot supply 2 | **1** |
| parents with ≥ 1 qualifier but fewer than 10 | **7** |

Qualifiers per parent: mean 41.1, standard deviation 36.4, min 0, max 114 — the spread is larger than
the mean, so per-parent yield is not a stable quantity and the cap at ten is doing most of the
levelling.

**No back-filling.** The parent that cannot supply two contributes **no** variants; it is still folded
as a parent in its own right. The seven short parents contribute exactly what they have, and nothing
below the bar was substituted to round them up to ten.

**Why the bar is applied to the whole pool, as a number.** The obvious shortcut is to filter the ten
variants per parent that the inverse-folding model's own score had kept. That would have been wrong,
and measurably so:

| bar | all 3,960 | the score-kept decile (n = 330) | the rest (n = 3,630) |
|---|---|---|---|
| ≥ 2 interfacial histidines | 0.343 | **0.276** | 0.349 |
| ≥ 3 interfacial histidines | 0.123 | **0.076** | 0.128 |

The score-best decile is **depleted** in interfacial histidines, so filtering it would have selected
from the worst-enriched tenth of the pool. Within a parent, score and interfacial-histidine count are
essentially unrelated (Spearman: mean +0.054 over 33 parents, sd 0.138; pooled −0.078), which makes
score a **neutral tiebreak** — it neither helps nor hurts the histidine criterion — while using it as
the *filter* costs about 20 % of the qualifier rate at the ≥ 2 bar and about 40 % at ≥ 3.

A second explanation for the same depletion — that histidine is simply rare in that model's
high-scoring output everywhere, interface or not — is separable (compare histidine frequency at
interfacial and non-interfacial positions within the kept decile) and **is not settled here**.

**Verification before the stored numbers were trusted.** The interface sets and the histidine counts
were re-derived with an independent fixed-column structure parser, so that a shared library bug could
not hide the error: interface sets at 8.0 Å and 6.0 Å for three parents (exact agreement at both
cutoffs), the histidine recount for 30 rows of those parents (exact agreement), and four randomly
drawn selected variants re-counted by hand and confirmed present in their parent's 120 with the
stated score (exact agreement).

### 4.2 The fold the band is judged on

**One restraint row, and it states only where.**

```
chainA,res_idxA,chainB,res_idxB,connection_type,confidence,min_distance_angstrom,max_distance_angstrom,comment,restraint_id
D,,A,K57,pocket,0.8,0.0,8.0,epitope-pocket,pocket_epitope_0
```

No histidine-to-lysine contact row, **no disulfide row**, no intra-chain contacts. All 325 restraint
files in the round are this single row and were checked by md5 to be identical.

**Why a pocket at all, and why 8 Å.** Which surface of a target a binder occupies is a legitimate
input to complex prediction, of the same kind as a known epitope. The row says that **some** binder
atom lies within 8 Å of Lys57; it names no binder residue, no histidine and no bond, and it is
looser than the 5–7 Å window the measurement asks about, so satisfying it does not put a designed
histidine anywhere in particular. It constrains the neighbourhood and leaves the arrangement free to
form or not to form. The previous round carried
**explicit histidine-to-lysine contact rows at 5–7 Å**, which means a Lys57 gate applied to that arm
measured *obedience*. Removing those rows is the single most important difference between the two
rounds, and it is why this round's engagement numbers are worth more than the previous round's.

**Why the declared intra-chain contacts come out.** The challenge refolds submitted designs with none
of our restraints, so the fixture-free condition is the one that counts. Matched arms, identical
except for the three declared intra-chain contacts:

| | fixture on | fixture off | Δ |
|---|---|---|---|
| seated (both histidines ≤ 7 Å) | 23/48 (48 %) | 28/48 (58 %) | +0.10 ± 0.10 — **unchanged** |
| declared pair 4–20, median | 7.66 Å | **15.82 Å** | +8.16 |
| declared pair 7–36, median | 7.64 Å | 11.17 Å | +3.53 |
| declared pair 10–34, median | 8.93 Å | 10.64 Å | +1.71 |

Two of the three exceed the pre-stated 3 Å, so the geometry prediction fails — the fold *does*
rearrange — while engagement is unchanged. **The fixture holds the declared topology and nothing
else**, and a design selected partly for satisfying its own fixture was selected on a term that does
not matter. One design that led the fixture-on arm at 3/3 in both species drops to 2/3 in human with
a 6.3 Å pose spread once the fixture comes out.

### 4.3 The measurement routes

Each was fixed in writing before any ordering was inspected, and each is defined in
[`metrics.md`](metrics.md). In brief:

- **seating**, both designed histidines within **7.0 Å** of the epitope on the protomer that
  minimises the *worse* of the two distances — **this route was the previous round's and was not
  computed for this band.** It is listed here so that its absence is visible, not so that it can be
  read as present. What replaces it on this arm is the pair of approach distances below plus the
  interfacial-histidine count, which together say where the binder is and how many of its histidines
  touch the target, and do **not** say that those histidines are the ones at the lysines;
- **approach to Lys57 and to Lys104** — minimum distance from any binder heavy atom to the lysine's
  NZ, minimised over the three protomers, median over models. Cutoff where one is applied, on Lys57
  only: **5.0 Å**, argued from geometry rather than from this data — a lysine NZ donating a hydrogen
  bond sits at 2.7–3.2 Å, a van der Waals touch of the ammonium against binder carbon at 3.4–4.0 Å,
  and by 5.0 Å a bridging water fits, so past that the lysine is solvated rather than engaged.
  Lys104 is measured and never gated, and it has no mouse counterpart (Pro104 there);
- **interfacial binder histidines** — binder histidines with any heavy atom within **8.0 Å** of any
  target heavy atom, in the folded complex, median over models. A count of histidines touching the
  target, not of histidines at the lysines;
- **binder pLDDT** — mean **per-token** confidence over the binder's 39 tokens, median over models.
  The per-atom route from the model's own B-factor column differs from it by 0.0034 ± 0.0023
  (maximum absolute difference 0.0137 over 1,625 models of this round) and is used only as a
  fallback when the per-token array is unavailable; the Cα-only mean is biased **+0.0298 ± 0.0040**
  against the per-atom route and is never used;
- **pose spread, symmetry-aware** — mean binder Cα RMSD over every *pair* of models. For each pair
  the two target trimers are superposed under each of the six protomer relabellings; a relabelling
  is **admissible** when the target Cα RMSD falls under 3.0 Å; the value reported is the **minimum
  binder RMSD over the admissible relabellings**. Reference-free on purpose: deviation from a
  design's own best pose flatters a scattered set, because the best pose of a scattered set sits in
  the middle of the scatter.

  **This replaces the identity-labelled definition an earlier draft of this file carried, and the
  replacement is not cosmetic.** The target is an exact C3 object — superposing a model's trimer on
  itself under either cyclic relabelling gives a median 0.11 Å (primary oracle) and 0.14 Å
  (Boltz-2) over 1,625 models each, while the improper relabelling gives 21.8–21.9 Å — so exactly 3
  of the 6 relabellings are admissible, in 100.0 % of all 14,625 pairs measured, and the 3.0 Å cut
  sits in a gap that is **entirely empty** between 1 Å and 15 Å. Nothing forces a predictor to give
  the same physical copy the same letter twice. The primary oracle does (0 of 3,250 pairs
  mis-register); Boltz-2 does not (38.3 % do). Under the identity labelling, Boltz-2's within-oracle
  spread reads **22.1 Å with 7.1 % of designs converged** when the correct figures are **14.1 Å and
  21.5 %** — it was measuring a binder displacement under a transform that never aligned the target.
  Two independent checks fix the construction: where both models engage the same protomer the
  winning relabelling is the identity and the number reproduces the old one to floating point (max
  difference 0.00e+00 Å over all 650 design-oracle cells), and a binder-blind route that picks the
  relabelling from the whole 3-vector of contact counts lands within 0.5 Å of the group minimum on
  both oracles. **No pose number in this repository uses the identity labelling**, and the 22.1 Å
  and 7.1 % figures should not be reproduced from any earlier file;
- **interface ipTM** — maximum over the protomer-binder pairs, both matrix orientations, median over
  models. Maximum rather than mean: the binder engages one protomer and averaging over three dilutes
  a real interface threefold;
- **pKa drift** — propka run twice on identical coordinates, complex and binder alone; per model the
  maximum drift over the binder's *surface* histidines (buried fraction below 50 % **in the free
  binder**); per design the median over models.

**A measured parser hazard, because it silently deletes the binder.** The oracle's structure files
wrap a coordinate row when a value prints wide, orphaning the last field onto its own line; a naive
line-by-line parser then drops the remainder of the file, binder included. Measured on this campaign:
**18 of 2,452 models (0.73 %)** carry a wrapped row, **0 skipped, 0 truncated** with the
wrap-tolerant parser. Any number recomputed from the deposited models must be recomputed with one.

### 4.4 The ranking rule that cut this band

Pre-registered for this round, before any ordering was computed: **gates on the human arm of the
primary oracle, then that oracle's median interface ipTM on the human arm, with binder pLDDT as the
first tiebreak and predicted pKa drift as the second.** The top 50 went into the three-oracle and
mouse passes.

> **This is not the rule an earlier draft of this file described.** That draft carried the
> **previous** round's rule — worse-species seating fraction first, interface confidence last. The
> two orderings are not the same, a reader cannot tell them apart from the band, and the correction
> is made here rather than quietly dropped.

**The delivered 20 are not the top 20 of that order, and they are not ordered on the human arm at
all.** Two things were changed after the ordering had been computed, as project decisions: a
**binder-pLDDT floor of 0.65 applied to BOTH orthologs** became the membership criterion, and the
band was re-ranked on the **worse-ortholog interface ipTM**, `min(ipTM_human, ipTM_mouse)`. Both are
§4.4.1. They are recorded here, where the pre-registered rule is stated, because criteria added
after the fact are exactly the kind of thing that has to be declared rather than folded into the
description of the rule.

| gate | cutoff | passed, of 325 | role |
|---|---|---|---|
| G0 chain contract A=149 B=149 C=149 D=39, ≥ 3 parsed models | — | 100.0 % | integrity, **inert** by design |
| G1 median approach to Lys57 NZ | ≤ 5.0 Å | 99.1 % | **inert** on this arm |
| G2 median binder pLDDT | ≥ 0.50 | **53.2 %** | the gate that does the work |
| G3 median interfacial binder histidines | ≥ 2 | 89.2 % | informative-ish |
| G4 no inter-chain clash in more than half the models | — | 100.0 % | integrity, **inert** |

**148 of 325 cleared every gate.** The falsifier stated in advance — that ≥ 90 % clearing everything
would make the gates decoration — did not fire.

**The second oracle was a demotion gate when the top 50 was built, and it is RELAXED for the
delivered band.** The rule pre-registered for this round is: ordering on the primary oracle's axes
alone, but every design with complete Boltz-2 data is **additionally evaluated against the same
gates on the Boltz-2 side**, and a design that clears the primary oracle's gates while failing one
of Boltz-2's is **demoted to a reserve tier** below every design that clears both. No design was
left `pending`: the Boltz-2 arm completed on all 325.

| | n |
|---|---|
| cleared every gate on the primary oracle | **148** |
| of those, also clear every Boltz-2 gate | **95** |
| of those, **demoted** for failing a Boltz-2 gate | **53** — 31 on Boltz-2's binder pLDDT, 15 on its interfacial-histidine count, 4 on its Lys57 approach, 3 on two of them |

That demotion built the top 50, which is the top 50 of the **95**, not of the 148. **It does not
gate the delivered band.** The band was re-cut from all 325 under the both-ortholog fold floor
(§4.4.1), and `boltz_state` was carried through as a reported column rather than applied as an
exclusion. Three delivered designs are ones Boltz-2 demotes: `…_03`, `…_09` and `…_11`. Every
Boltz-2 figure for all three is in `metrics_full.csv` and in their `metrics.json`, and they are
marked **b** in the band table of §8. All three are above the band's floor on the ranking key, so
relaxing the gate is what admitted them; of the 53 demoted designs, 8 have a worse-ortholog
interface ipTM above that floor and 3 of those also clear the fold gate — those 3 are precisely the
ones delivered.

**Why the relaxation, stated as a project decision and not as a result.** The gate was relaxed
rather than the band shrunk because of what the three oracles measurably do and do not share: their
disagreement is on the **binding** axis, where the pairwise cross-oracle agreement on the
human-minus-mouse difference is a single-digit percentage of what the instruments' own
reliabilities make attainable and the confidence interval contains zero, while the floor that now
decides membership is on the **foldedness** axis, where they demonstrably agree (§9.1: ρ = +0.33 to
+0.69, every interval excluding zero) and agree *more* on better models. **It does not follow that
the second oracle's opinion is worthless**, which is why it is still reported design by design and
why the three designs it demotes are named here rather than left to be found in a column.

**The argument for letting a second oracle remove designs, which is what built the top 50.** What
it mostly removed them on is **folding** — the binder-pLDDT gate, in 34 of the 53 — and folding is
the axis the oracles agree about. A second opinion about folding is a second opinion about
something both instruments can see. A second opinion about *binding* would not have been, and none
was used: no cross-oracle binding score enters the ordering at any point.

**A pre-registered decision rule fired, and the deliverable it specified was not produced.** The
same pre-registration fixed in advance what to do with the cross-oracle agreement figure: at
ρ ≥ 0.50 the primary-oracle order stands outright; between 0.25 and 0.50 it stands but the top 50
requires Boltz-2 agreement; **below 0.25, "a single ordered best-50 is not supported" and the
deliverable becomes the intersection of the two oracles' own top-N lists, N grown until the
intersection reaches 50.** The measured ρ is **−0.010** over all 325 and **−0.195** over the
delivered 50, so the third row fired. What was produced instead is the primary oracle's order,
**labelled throughout as a primary-oracle-only ordering**, because with agreement at chance (§9.7)
the intersection rule would have required N to grow to most of the population before it returned 50
designs, which is a different and weaker selection, not a stricter one. **The departure is recorded
here rather than left for a reader to discover from the pre-registration**, and the consequence it
was meant to force is carried instead in words: this is one oracle's ordering, the other two do not
confirm it, and the deposition says so on every page.

**G1 is inert, as pre-stated, and it was left where it is.** 5.0 Å was fixed from first-shell
geometry and the rule committed not to re-cut it to a quantile of this data. The deciles of the
median Lys57 approach over the 325 run 1.67, 2.44, 2.58, 2.71, 2.79, 2.89, 3.00, 3.14, 3.34, 3.64 Å
with a maximum of 12.02: nine deciles sit between 2.4 and 3.7 Å, well inside the 8 Å that was asked
for. The 8 Å pocket did not merely satisfy itself at its own limit; it pulled essentially the whole
population into first-shell contact with Lys57 NZ, which is why **the gate carries no information on
this arm** and why the ordering rests on G2, G3 and the ipTM axis.

**G2's cutoff, measured.** Survivors at ≥ 0.50 / 0.55 / 0.60 / 0.70 are 173 / 122 / 77 / **26** of
325. The previous round's 0.70 floor would have left 8 % of this population, reproducing almost
exactly the 6-of-50 that motivated moving it.

**Why interface ipTM leads, as the rule stated in advance.** It is the only axis here that is
specifically about the binder-target *interface*, it is the quantity this campaign has ranked on
throughout so the numbers stay comparable, and it is not a composite — a weighted composite was
rejected because it hides which axis moved a design.

**The single-label risk was pre-registered, checked, and only partly survives the check.** Three
tests were fixed in advance. The top 50 by interface ipTM and the top 50 by binder pLDDT overlap
**21/50 = 42 %**, above the 20 % that would have falsified the rule, so the stated falsifier did not
fire. But the discriminability test and the correlations are the uncomfortable part:
ρ(interface ipTM, binder pLDDT) = **+0.714** and ρ(interface ipTM, within-oracle pose spread) =
**−0.661** over the 325. **The lead axis is not independent of the pose-consistency label**, and
this project has been burned before by a consistency label whose blind spot became the objective's.
The top of this list may be enriched in **rigid** binders rather than good ones. That was written
into the pre-registration as a warning and it is realised, not refuted.

**The mouse arm selected nothing.** It is a second pass over the 50 the human arm had already
chosen (§6.13). Where the two orthologs appear together the **worse** one is reported and never an
average.

**The evidence against ranking on interface confidence, which was not withdrawn.** Over 100
design-species pairs of the previous round:

| | n = 78 | n = 100 |
|---|---|---|
| pair-interface pTM against **binder pTM** | +0.620 | **+0.634** |
| against the measured histidine distance | +0.090 | −0.143 |
| **partial, controlling binder pTM** | **+0.048** | **−0.155** |

The estimate **flipped sign** on 28 % more data, and at n = 100 the interval around −0.155 is roughly
±0.20, so both readings are consistent with zero. What it does track, at +0.634, is how confidently
the binder folded: a foldedness number wearing an interface name. Under a confidence-first ordering
the top two delivered designs of **that** round would have been two that are **0 of 3 seated in both
species**.

**That evidence was not withdrawn and it is not softened here: this band was cut on that axis
anyway.** The argument for doing so is the one above — it is the only interface-specific,
non-composite quantity available, and the alternative lead axis of the previous round, the joint
seating fraction, was not computed on this arm. The consequence is that the delivered order is
defensible as *the primary oracle's own ordering*, reproducible under a re-draw (§4.5), and **not**
as an ordering of binding. A reader who discounts interface ipTM entirely should read this band as
20 designs that clear four bars, and should not read the sequence of the rows.

**Gates, not penalties.** A weighted sum lets a design that fails badly on one axis be carried by the
others, so membership is decided by bars and order by the rule above. The previous round reported a
binder-pLDDT floor at **0.70** as a caution rather than adopting it: on that round's instrument it
removed **44 of 50** designs, and **nothing** in 900 restraint-free models of that round reached it
(maximum 0.658), while the same designs' restrained refolds on the smaller design-time construct
ran 0.703–0.779. Two things differ between those numbers — restraints and assembly — so the drop is
not attributable to either alone, and the figure should not be quoted as universal. **On this
round's instrument and construct a fold floor is not population-killing, and a floor of 0.65
applied to both orthologs is now the criterion that decides membership of this band**; §4.4.1 gives
the counts, the floors that were rejected, and the reason the two rounds' figures are not
comparable.

### 4.4.1 The both-ortholog fold floor, the worse-ortholog ranking key, and the funnel

**The objective of this target is that BOTH orthologs are bound.** It is not selectivity and it is
not ortholog preference. Everything in this subsection follows from that, and the two criteria
below were chosen after the ordering had been computed, as project decisions rather than as rules
pre-registered with the gates above.

> **Membership:** binder pLDDT **>= 0.65 on the human arm AND on the mouse arm**, plus every chai
> quality gate.
> **Order:** the **worse** of the two orthologs' interface ipTM, `min(ipTM_H, ipTM_M)`, descending.
> Never the mean, never the maximum, never the difference.

**Ranking on the worse ortholog is the band's whole selection logic.** A design that binds one
ortholog well and the other poorly ranks **low by construction**, because the number it is ranked
on is the poor one. Averaging would let a strong human score pay for a weak mouse score, and taking
the maximum would reward exactly the designs this target is not asking for.

| step | n |
|---|---|
| folded, measured and in the candidate table | 325 |
| binder pLDDT >= 0.65 on **both** orthologs | **34** |
| … and clears every chai quality gate G0-G4 — **the pool** | **30** |
| … and clears the Boltz-2 gate as well *(reported, **not** applied)* | 24 |
| **delivered** — the top 20 of the pool on the worse-ortholog key | **20** |

The ten pool members that are not delivered are documented with a `status` and no
`submission_rank` (§8.1). There is **no ortholog tiering in the order**: the both-ortholog
requirement sits in the gate, so every delivered design already satisfies it and a tier would sort
designs on a criterion they all meet identically.

**Why 0.65 and not 0.70.** The floor was taken as low as it had to go to fill the band from a pool
with more than one backbone family in it, and no lower:

| floor, applied to both orthologs | clears both | and clears the chai gates | distinct parents | worse-ortholog ipTM at pool rank 20 |
|---|---|---|---|---|
| 0.70 | 11 | 10 | 4 | — (cannot fill a band of 20) |
| 0.68 | 20 | 18 | 6 | — (cannot fill a band of 20) |
| **0.65** | **34** | **30** | **10** | **0.2008** |
| 0.62 | 49 | 42 | 14 | 0.2014 |

0.70 and 0.68 cannot deliver 20 designs at all. Going on to 0.62 buys 12 more candidates and moves
the worse-ortholog ipTM at pool rank 20 by **0.0006**, from 0.2008 to 0.2014 — it buys a longer
list and a lower fold floor and essentially nothing on the axis the band is ranked on. 0.65 is the
loosest floor that fills the band and the tightest that can.

**The human-minus-mouse difference is reported per design and is NOT a selection criterion.** It
gates nothing and orders nothing. Over the delivered 20 it runs **−0.3404 to +0.3836**, positive for
8 designs and negative for 12, and the band is deliberately mixed: **no ortholog preference is
claimed for any design or for the band.** The reason it is not used is measured, and it is the same
evidence the rest of this document rests on — the difference reproduces **within** chai (rho =
+0.948 [+0.926, +0.964] over all 325, both orthologs re-drawn) and **not across oracles**
(chai-Boltz +0.0533 [−0.0569, +0.1580], **8.3 %** of what the two instruments' reliabilities make
attainable, interval containing zero). A quantity that
one oracle reproduces and no second oracle confirms is a property of *(design, oracle)*, and
selecting on it would be selecting on the oracle.

**Four of the 34 designs clearing the fold floor fail a chai quality gate** and are not in the pool
— all four on G3, the two-interfacial-histidine membership bar. None of them would have entered the
band: on the worse-ortholog key they would rank 21, 25, 33 and 34. (On the human-only ranking this
band previously used, two G3 failures would have been inside it; on this key they are not. The
earlier statement that the membership bar removed the highest-ranked well-folded designs **does not
hold under this rule** and has been removed rather than carried over.)

**What the floor is worth, measured rather than assumed — and what it cannot say.** The two
criteria were tested against an independent re-draw of the same oracle at a different seed, with the
thresholds written down first (`.tmp` pre-registration, reproduced in the regate report):

- **The gate holds.** Of the 17 delivered designs that have re-draw data, **17 of 17 still clear
  0.65 on both orthologs** at seed 8300, and 17 of 17 on the human arm at seed 9300 (no mouse draw 3
  exists). The per-design change in binder pLDDT is **−0.0002 ± 0.0054** on human and **−0.0002 ±
  0.0067** on mouse. Two designs nevertheless sit closer to the floor than that spread —
  `…_04` is 0.0011 above it on mouse and `…_12` is 0.0016 above it on human — and for those two the
  gate is satisfied **within the instrument's own error**, which is named here rather than absorbed
  into a pass rate.
- **The ranking key holds better than expected.** rho between draw-1 and draw-2 worse-ortholog ipTM
  is **+0.9447 [+0.7970, +0.9897]** over the 22 pool members with both re-draws, and **17 of the 17
  delivered designs with re-draw data stay in the re-drawn top 20** of the same pool. The
  pre-registered expectation was that `min()` of two noisy arms would be *less* reproducible than
  either arm alone and that top-20 membership would be less stable; the first is true but barely
  (the single-arm figures on the same designs are +0.9616 human and +0.9808 mouse) and **the second
  is refuted**.
- **The mechanism behind that prediction is real but small.** Which ortholog is the worse one flips
  between draws for **2 of 22** pool members, both delivered (`…_14` and `…_20`). It does not move
  the key, because when the two arms are that close the minimum is nearly the same number whichever
  one it comes from. The key is robust **exactly where the label is not**.
- **Five delivered designs have `|ipTM_H − ipTM_M|` smaller than the draw-to-draw spread in the key
  (0.0134)**: `…_01` (0.0051), `…_03` (0.0055), `…_10` (0.0130), `…_14` (0.0036) and `…_15`
  (0.0009). For those five **the identity of the worse ortholog is not established by this
  measurement**, and the letter in the `worse_ortholog_which` column should be read as a tie, not
  as a result. They are marked with a dagger in §8.

Scope limit: the re-draw arms exist for the 50-design replicate pool only, so **three delivered
designs have no re-draw at all** and none of the figures above covers them.

### 4.5 What the ranking can resolve

#### Reproducibility, measured on the 50-design replicate pool

The question was pre-registered: does the primary oracle's ordering survive a re-draw that changes
only the seed? It does, and that is **all** it does. The figures in this table are for the primary
oracle's **human-arm** ordering of the 50 — the route that built that pool. They are **not** this
band's gate or its ranking key; those are tested in §4.4.1 and summarised again below.

| | |
|---|---|
| test–retest Spearman on interface ipTM, 50 designs, seed 7300 against 8300 | **+0.940** [+0.857, +0.974] |
| the same on binder pLDDT, reported and not substituted | +0.995 [+0.983, +0.999] |
| mean level shift between draws | 0.0142, mean signed shift −0.0022 |
| rank shift over the 50 | mean 3.4, median 2, maximum 17 |
| top-10 overlap between the two draws | 9 / 10 |
| top-20-of-50 overlap, **the rule that built the top 50, not the delivered band** | **18 / 20** at seed 8300, **19 / 20** at seed 9300 |
| top-25 overlap | 24 / 25 |

**Those overlaps are not this band's reproducibility, and must not be read as it.** They test
membership of the primary oracle's own top 20 of the 50 on its **human** arm, which is neither this
band's gate nor its ranking key. The figures for the rule actually in force are in §4.4.1 and are
stronger: **17 of 17** delivered designs with re-draw data still clear the 0.65 floor on both
orthologs, and **rho = +0.9447 [+0.7970, +0.9897]** between draws on the worse-ortholog ranking key,
with **17 of 17 staying inside the re-drawn top 20** of the same pool.

**The order inside the band is still not a quality ordering, and at its lower end the key barely
separates the designs at all.** Eleven of the delivered twenty sit between worse-ortholog interface
ipTM 0.2008 and 0.2475 — **eleven designs inside 0.0467** — and the first design cut from the pool
is **0.0060** below the lowest delivered one. A key that reproduces is not a key that discriminates:
rho = +0.9447 says the *ordering* comes back, and the eleven-design cluster says most of that
ordering is between designs the instrument cannot tell apart.

**And the sentence that must travel with every reproducibility figure here.** ρ(draw-1 interface ipTM, cross-redraw
symmetry-aware binder pose RMSD) = **−0.600 [−0.790, −0.338]**, n = 50. The designs the ordering
likes are the designs whose pose reproduces. **The ordering reproducing is consistent with the
ordering reproducibly ranking pose rigidity rather than binding.** Reproducibility was the question
asked; it
is not evidence of quality. For the primary oracle, changing the seed adds nothing measurable beyond
the spread already inside one seed's five samples (6.79 Å across seeds against 6.88 and 6.55 Å
within), and the symmetry correction moves that figure by 0.00 Å because this oracle labels its
protomers consistently.

#### From the previous round, on the previous round's instrument

The precision bound in §2 was acted on rather than assumed. Twenty designs were refolded to **13
folds per species — 520 folds** — and the three-fold ordering of the shortlist did **not** survive:

```
pre-registered   Spearman rho over the 12 shortlisted designs = +0.329   (threshold 0.70) -> REFUTED
context only     rho over all 20 measured designs             = +0.722
```

The registered statistic is the shortlist one. The all-20 figure clears the line only because the
eight band designs sort to the bottom at both samplings, which inflates a rank correlation without
saying anything about the designs in contention; reporting it would be choosing the number that
agrees with us.

**The higher sampling did not produce an order either.** The leaders' 95 % intervals overlap, so the
thresholded measure reports a **set**; the continuous measure separates them only *inside* the 7 Å
window, on the mean, with four of five changing rank between mean and median. A pre-registered
candidate discriminator — the consistency of a design's own spread, 0.57 Å against 1.23–3.75 Å for
the rest — was tested on fresh prediction seeds and **refuted** (1.10, 0.92, 1.94, 1.75).

Two movements worth naming, because they are what a noisy cut costs: one design rose from rank 8 to
joint first while another fell from 3 to 9, and a design excluded by the shortlist cut came in at
rank 8 when the band below the cut was measured too. **A cut inherits the error of the measurement
that drew it**, so re-ranking only what the cut selected cannot find its own mistakes.

**So the head of this band is a set, not a sequence, and more folds is not the lever that changes
that.** The published order is published so it can be argued with.

---

## 5. What has been achieved, and where the evidence is against us

Reported separately from the protocol, because these are results and not methods.

> **§5.1 to §5.5 are the *previous* round's measurements, on the previous round's designs.** They
> are here because they are the closest thing to a non-circular check that exists in this campaign,
> and because the restraint-free question they answer is the one that matters most. **The delivered
> band has no restraint-free arm of its own**: every fold it was cut on carries the 8 Å pocket, so
> none of these numbers has been repeated on these 20 designs. What the delivered band itself says
> about the epitope is in §8: Lys57 at 2.44–4.70 Å under the restraint, Lys104 at a median of
> 8.72 Å with nothing restraining it.

### 5.1 The binders reach the face; they do not yet reproduce the arrangement unaided

Every candidate of the previous round was refolded with the restraints **removed**, by two oracles —
**900 models** in all (540 by the primary oracle, 180 restraint-free and 180 pocket-restrained by the
second):

| | primary oracle | second oracle, restraint-free |
|---|---|---|
| binder within 8 Å of **both** lysines | **33 of 36** systems | 27 of 36 |
| the **designed** two-histidine arrangement | **4 of 36** | **0 of 36** |

And the narrower restraint-free check, on the five designs that have such data:

| | restraint-free | with the 8 Å pocket |
|---|---|---|
| distance to Lys57 | **6.48 – 17.73 Å** | 2.72 – 3.72 Å |
| interface confidence | **0.078 – 0.138** | 0.10 – 0.42 |

Every one fails a 5 Å contact test on restraint-free coordinates. This was checked for a parser
artefact before being believed: the geometry code reproduces the stored values on 108 restraint-free
models with a **maximum difference of 0.0000**.

**What this does not show.** It does not show these designs cannot bind. A 39-mer against a
447-residue trimer, given no prior for where to look, will be placed somewhere on a large surface. It
shows that **nothing in this campaign has yet demonstrated unaided engagement of the epitope**, and
that no ranking here may be read as an ordering of unaided engagement.

### 5.2 The null control, which is not flattering

The binder is typically closer to a lysine the design never named than to the designed pair
(**4.57 Å against 11.11 Å**). Ranked among the six lysines of the human protomer, **Lys57 comes
second in both oracles independently** against a chance expectation of 3.5, and the second designed
lysine comes fourth. There is a weak, reproducible preference for the Lys57 face and **none** for the
second site.

### 5.3 The measurement that widened the bar

Relaxing the requirement from the two originally designed histidine positions to **any** histidine of
the binder roughly **triples** the hit rate — **32 of 540 models to 94 of 540** within 7 Å of Lys57.
The two designed positions still dominate, but about a third of the engagements come through other
histidines. That is the measurement behind the current round's membership bar in §4.1, and it is also
why the inverse-folding step now holds every histidine rather than four fixed positions.

### 5.4 Two metrics that do not work on this system

**ipSAE was exactly 0.000 on the PREVIOUS, restrained round — and it is computed for this one.**
The observation below is about that earlier round and remains true of it; it is **no longer the
reason the column is absent**, because the column is now present. For this round, ipSAE is measured
on **all three oracles, both orthologs, all 325 designs** (canonical Dunbrack scale, raw per-token
PAE, 10 Å cutoff, maximum over the three (protomer, binder) pairs and both directions, median over
the five samples) and is shipped as a per-design column.

**What that measurement says, and it is not what a second axis would say.** Mean ipSAE on the human
arm is **0.0355** (primary), **0.0433** (Protenix) and **0.3278** (Boltz-2); on mouse, 0.0300 /
0.0461 / 0.2396. Within each oracle, ρ(ipSAE, interface ipTM) is **+0.867** (primary), **+0.879**
(Protenix) and **+0.972** (Boltz-2) — for Boltz-2 it is effectively a relabelling of ipTM.
**60.6 % of primary-oracle designs and 62.8 % of Protenix designs sit at or below the metric's own
floor** of 1/(1 + 10²) = 0.0099, and **51 % of Protenix designs are exactly 0**. Cross-oracle, ipSAE
mirrors ipTM rather than adding to it: primary–Protenix **+0.227 [+0.120, +0.331]**, primary–Boltz-2
−0.015, Protenix–Boltz-2 −0.054. **On this target "ipSAE + ipTM" is close to 2 × ipTM and does not
constitute a second axis**, and the column is shipped on that understanding.

On the previous, restrained round the primary oracle returned ipSAE on **all 540** restrained
models measured:
the target-binder PAE bottoms out at **21.7 Å** and nothing falls under the score's 10 Å cutoff. That
is a real statement about a 39-mer on a 447-residue trimer, not a bug, and it is reported so nobody
recomputes it expecting otherwise.

**The second oracle's interface score carries no information about where the binder is.** Its largest
value in the pocket arm (0.726) belongs to the design with the **worst** binder confidence and the
**largest** histidine distance. Read it beside a measured distance or not at all.

### 5.5 A conclusion withdrawn

An earlier reading of this campaign — that the histidines which titrate are not the designed ones —
was an **artefact of the restrained folds it was computed on**: the restraint buries the designed
histidines against their lysines and moves their predicted pKa out of the window. On restraint-free
coordinates they come back into it (**2.10 → 6.55** and **4.27 → 6.16** on one design's mouse fold,
with the summed drift going **+0.389 → +1.008**). The conclusion is withdrawn and the pKa column is
reported with the arm it was computed on.

---

## 6. Limitations

Stated plainly, because several of them are load-bearing.

1. **Unaided engagement has not been demonstrated.** §5.1. Every restraint-free measurement available
   misses the epitope by 6.5–17.7 Å, and the designed arrangement appears in 4 of 36 systems by one
   oracle and 0 of 36 by the other.

2. **The arm the band is ranked on is not restraint-free.** It carries an 8 Å pocket on Lys57. That
   is a statement of *where* and not of the interaction — and it is a much weaker statement than the
   previous round's explicit 5–7 Å histidine-to-lysine rows — but it is not nothing, and the pass
   fraction under any Lys57 criterion must be read with that in front of it.

3. **The second designed lysine is not engaged.** Over the delivered 20, the binder's closest heavy
   atom reaches 3.53–11.10 Å of Lys104 NZ, median **7.81 Å**, with 7 of 20 inside 7 Å — against
   2.46–4.85 Å for Lys57, which is the one the restraint names. The mechanism is built on a lysine
   *pair*; the evidence supports a lysine *site*.

4. **The joint seating criterion was not computed for this band.** "Both designed histidines within
   7 Å of the epitope on one protomer" was the previous round's instrument. This round measured the
   two approach distances and the interfacial-histidine count instead. The column is absent rather
   than carried across from a different arm.

5. **The band is a set, not an order.** §4.5. Both halves of the rule survive a re-seed — 17 of 17
   delivered designs with re-draw data still clear the 0.65 floor on both orthologs, and the
   worse-ortholog key returns at ρ = +0.9447 [+0.7970, +0.9897] with 17 of 17 staying in the
   re-drawn top 20 — but reproducing is not discriminating: **eleven of the twenty sit inside
   0.0467 on the key**, and the first design cut from the pool is 0.0060 below the lowest delivered
   one. And a reproducible ranking is consistent with reproducibly ranking **pose rigidity**:
   ρ = −0.600 against cross-redraw pose spread.

6. **The lead axis is largely a foldedness axis.** §4.4. ρ(interface ipTM, binder pLDDT) = +0.714
   and ρ(interface ipTM, within-oracle pose spread) = −0.661 over the 325, and the previous round's
   evidence against ordering on interface confidence was never withdrawn.

7. **The three oracles disagree about which designs bind.** §9. All three pairwise interface-ipTM
   correlations have intervals containing zero at n = 50 while all three binder-pLDDT correlations
   exclude it, and the third oracle carried **no restraint** while the other two carried the same
   pocket. Consensus was sought and not found.

8. **Model confidence on these designs is low.** Nothing in 900 restraint-free models of the
   previous round reaches a binder pLDDT of 0.70, maximum 0.658; on this round's restrained arm only
   26 of 325 do, and the delivered band runs 0.522–0.862 on human and 0.432–0.832 on mouse. These
   are geometries inside structures the oracle is not confident about, and they should be read that
   way.

9. **Nothing here measures protonation, and the one predicted-pKa axis does not support the
   mechanism.** No protonation state was varied; the oracles are heavy-atom only. Over the delivered
   20 the predicted drift runs −1.39 to +0.68 with a median of **−0.27** and only **2 of 20**
   positive; over all 325 the median is −0.01, 22 % are positive, and ρ(interface ipTM, pKa drift) =
   −0.155. propka is additive and has no term for a geometry that requires a charged ring, so it
   tends to reward histidines that stay solvent-exposed — but that limitation explains why the axis
   is weak evidence, it does not convert a negative median into support. We claim a **design
   direction**, not a size and not an observation.

10. **The pKa axis is orthogonal to everything that precedes it.** Spearman +0.12 to +0.15 against
    interface confidence, binder pLDDT and pose spread in the previous round, and it could not
    separate the top four designs — all pairwise differences inside two standard errors. A funnel
    whose last step is uncorrelated with its first three is discarding them.

11. **One of the two originally designed histidines has no consistent partner.** §1.3. His13
    hydrogen-bonds in 63 % of folds across 20 designs with 3 distinct partner tags. That is why the
    current bar asks for any two interfacial histidines, and why the histidine positions vary across
    this band.

12. **The repack verdict has been re-measured, and it holds.** §3.1. The inverse-folding backbone
    was missing its carbonyl oxygen until 18 October 2026. On this round's 325 folds, whose repacks
    were produced after that correction, the typical repack is still **worse** than its own family
    original on the binding axis (mean-vs-mean −0.028; 43.8 ± 6.8 % of repacks beat their original,
    below the 50 % exchangeability predicts). On binder pLDDT there is a mean shift upward (+0.044;
    62.5 ± 6.5 %) which **cannot be attributed to repacking alone**, because the repacks folded are
    the top-scoring qualifiers of each original while the original is unscored. Separating the two
    would need the unselected qualifiers folded, which they were not. Named, not corrected.

13. **The mouse evidence now selects, because the objective is that both orthologs are bound.**
    The mouse arm is a full pass over all **325** candidates, 5 models per design, with the binder
    sequence verified identical across arms and the ortholog read back out of the structures rather
    than assumed. It enters the rule twice: the fold floor must be cleared **on the mouse arm as
    well as the human one**, and the ranking key is the **worse** of the two orthologs' interface
    ipTM. The worse ortholog is reported and never averaged — it is mouse for 8 of the 20 and human
    for 12 — and for five designs the two arms are closer together than the measurement's own
    draw-to-draw spread, so which one is worse is **not established** and is marked as such in §8.
    **The human-minus-mouse difference selects nothing**: it is reproducible inside that oracle
    (**ρ = +0.948 [+0.926, +0.964], n = 325**) and shared with no other (**+0.0533 [−0.0569,
    +0.1580]** with the second oracle, **8.3 %** of attainable, interval containing zero), so it is
    a property of *(design, oracle)* and not of *design* — which is the measured reason it is
    reported as a figure and used as no part of the rule. It is also a
    difference between two orthologs that differ in sequence and length, **not** a pH measurement.

14. **No design in this target has been tested experimentally.** No binding data, no pH titration, no
    expression result. Every number here is a prediction or a geometric measurement on a prediction.

15. **The organisers' construct definition is not established here.** §1.1. Numbering is
    construct-local throughout so that an offset can be applied later without re-deriving anything,
    and the number of designs this target accepts is likewise unknown — 20 is the size of the band we
    deliver, not an allowance we verified.

---

## 7. Reproducing these numbers

### 7.1 The restraint

One row, given in §4.2, in the format
`chainA,res_idxA,chainB,res_idxB,connection_type,confidence,min_distance_angstrom,max_distance_angstrom,comment,restraint_id`.
Chain **A** is one protomer of the target, chain **D** the binder. Commas inside the `comment` field
are rejected by the parser.

### 7.2 The folds

Both oracles are given the identical assembly — the homotrimer as chains A/B/C, each carrying the
same **2,228-sequence** alignment for the target, and the binder as the last chain with **no**
alignment, because a designed peptide has no homologues. Five diffusion samples per prediction, 200
sampling steps, 3 recycling steps.

**Primary oracle** — input is a FASTA of the four chains plus the restraint file above:

```
>protein|target_A
<target protomer, human or mouse>
>protein|target_B
<target protomer>
>protein|target_C
<target protomer>
>protein|binder
<sequence from sequence.fasta>
```

**Second oracle (Boltz-2)**, given the same two things and nothing else:

```yaml
version: 1
sequences:
  - protein: {id: A, sequence: <target protomer>, msa: <msa>/target2_H.a3m}
  - protein: {id: B, sequence: <target protomer>, msa: <msa>/target2_H.a3m}
  - protein: {id: C, sequence: <target protomer>, msa: <msa>/target2_H.a3m}
  - protein: {id: D, sequence: <binder>,          msa: empty}
constraints:
  - pocket:
      binder: D
      contacts: [[A, 57]]
      max_distance: 8.0
```

```
boltz predict <dir> --out_dir <out> --cache <weights> --accelerator gpu --devices 1 \
    --output_format mmcif --diffusion_samples 5 --sampling_steps 200 --recycling_steps 3 \
    --seed 11 --num_workers 0 --no_kernels
```

`--num_workers 0` is not cosmetic: with workers the run deadlocks on this stack, and `--no_kernels`
is required because the accelerated kernel path raises an import error on the pinned build. Neither
changes the prediction.

**Third oracle (Protenix)** — the same four chains, **and no constraint block at all**. Its input
JSON carries `name` and `sequences` and nothing else; the string "constraint" does not occur in it.
Five samples, seed 7000, with a second human draw at seed 8000.

### 7.3 What a reader can check without running anything

Everything the band was cut on, from the files in this repository.

`micro/AMBRA_T2_micro_01` … `micro/AMBRA_T2_micro_20`, one directory per delivered design, plus
`micro/AMBRA_T2_micro_21` … `micro/AMBRA_T2_micro_30` for the ten documented designs that are not
submitted (§8.1):

| file | what it is |
|---|---|
| `human_model_0.cif` … `human_model_4.cif` | the five primary-oracle models of the human complex that every human figure for this design is a median or a count over |
| `mouse_model_0.cif` … `mouse_model_4.cif` | the same five for the mouse complex |
| `restraints.csv` | the restraint file as given to the oracle — the single pocket row of §4.2 |
| `sequence.fasta` | the binder sequence under its deposited name |
| `metrics.json` | every number quoted for that design, field names matching `metrics_full.csv` |

**There is no `selected.cif`, deliberately.** Nothing here is ranked on a best model: every figure
is a median or a count over the five, because the oracle is nondeterministic on this system and the
best of *n* draws is a property of *n*. A selected model would invite exactly the reading this band
cannot support.

`metrics_full.csv` carries the same fields for all 30 rows — the 20 submitted and the ten
documented — with `status` and `submission_rank` telling them apart, and with `n_models_human` and
`n_models_mouse` beside every rate; read those first, because a median over five models is a median
over five models. A **blank** cell in that table means *not measured for this design*, never zero
and never false: the re-draw, cross-redraw and "in its own oracle's top 20" columns exist for the
top-50 replicate pool only, and three delivered designs sit outside it. `submission.csv` carries
only `name`, `sequence` and `molecule_class`, and only the 20 submitted rows.

**What is not deposited, and why.** The second and third oracles' coordinates are not here, only
their per-design numbers in `metrics_full.csv`: depositing them would have roughly tripled the size
of this directory, and every cross-oracle statement in these documents is a population figure rather
than a per-model one. There is **no restraint-free arm** for this band at all — §6.2 — so no such
coordinates exist to deposit.

**Recomputing from the deposited models needs a wrap-tolerant parser.** The primary oracle's
structure files wrap a coordinate row when a value prints wide, orphaning the last field onto its
own line; a naive line-by-line reader then drops the remainder of the file, binder included. On this
round's chai arm that happened in **16 of 325 folds (4.9 %)**, 34 rows in all, and a line-by-line
parser would have scored those 16 as target-only.

---

## 8. The submitted band

**Twenty designs, and the row order is not a claim.** The `#` column is the primary oracle's
first-draw interface-ipTM position, which is what the upload form reads from the top down. The
*selection* of these 20 out of 50 reproduces under an independent re-draw; the order inside it and
its boundary do not (§4.5). Read the table as a set.

Every value is a median over **five** independent models of that design and ortholog, from the
`.cif` files in the same design's directory. Names are abbreviated `…_NN` for
`AMBRA_T2_micro_NN`. **The band is ordered on the `worse` column** — the lower of the two orthologs'
interface ipTM — so the row order is the ranking key and the per-ortholog ipTM pair beside it is
not. `F01`-`F10` are backbone families; **every design in this band is an inverse-folding repack**,
because no family original cleared the fold floor on both orthologs. A design marked **b** is one
Boltz-2 demotes on its own quality gates; that gate does not exclude from this band (§4.4). A
dagger on the `worse is` column marks a design whose two orthologs are closer together than the
draw-to-draw spread in the key, so **which ortholog is the worse one is not established** for it
(§4.4.1). The `H − M` column is **reported and is not a selection criterion**: it gates nothing and
orders nothing. "oracles" counts how many of the three place the design in their **own** top 20 of
the same 50 and "re-draws" is survival in that top 20 at seeds 8300 and 9300 — both are defined on
the top-50 replicate pool, test the *human-arm* ordering rather than this band's key, and are
written `—` for the three delivered designs outside that pool, which is *not measured*, not
*measured and failed*.

| # | design | worse | worse is | ipTM H / M | H − M | binder pLDDT H / M | family / origin | His positions | K57 / K104, human (Å) | iface His H / M | pose spread, H (Å) | pKa drift | oracles | re-draws |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | …_01 | **0.6579** | M† | 0.663 / 0.658 | +0.0051 | 0.845 / 0.832 | F01 repack | 17,37 | 2.65 / 8.97 | 2 / 2 | 3.06 | −0.15 ± 0.74 | 3/3 | Y / Y |
| 2 | …_02 | **0.5608** | M | 0.729 / 0.561 | +0.1680 | 0.832 / 0.771 | F01 repack | 14,37 | 2.46 / 6.43 | 2 / 2 | 0.94 | −0.69 ± 0.17 | 3/3 | Y / Y |
| 3 | …_03 **b** | **0.5538** | H† | 0.554 / 0.559 | −0.0055 | 0.777 / 0.665 | F02 repack | 15,16 | 2.59 / 4.96 | 2 / 2 | 2.54 | −0.08 ± 0.14 | — | — |
| 4 | …_04 | **0.4474** | M | 0.533 / 0.447 | +0.0852 | 0.681 / 0.651 | F03 repack | 23,26 | 3.66 / 7.83 | 2 / 2 | 1.61 | −0.30 ± 0.04 | 2/3 | Y / Y |
| 5 | …_05 | **0.4160** | M | 0.519 / 0.416 | +0.1030 | 0.766 / 0.717 | F04 repack | 12,14 | 3.57 / 8.96 | 2 / 2 | 1.70 | −0.02 ± 0.00 | 2/3 | Y / Y |
| 6 | …_06 | **0.3328** | M | 0.716 / 0.333 | +0.3836 | 0.862 / 0.750 | F01 repack | 14,26 | 2.61 / 8.82 | 2 / 2 | 2.61 | −0.38 ± 0.36 | 2/3 | Y / Y |
| 7 | …_07 | **0.2910** | H | 0.291 / 0.617 | −0.3259 | 0.670 / 0.754 | F05 repack | 13,34 | 2.76 / 7.79 | 2 / 2 | 5.55 | −0.14 ± 0.67 | 1/3 | Y / Y |
| 8 | …_08 | **0.2818** | M | 0.640 / 0.282 | +0.3580 | 0.792 / 0.694 | F04 repack | 14,36 | 4.17 / 9.89 | 2 / **1** | 0.70 | −0.09 ± 0.11 | 2/3 | Y / Y |
| 9 | …_09 **b** | **0.2568** | M | 0.349 / 0.257 | +0.0925 | 0.681 / 0.671 | F06 repack | 13,20,34 | 2.91 / 4.80 | 3 / 3 | 2.47 | 0.00 ± 0.39 | — | — |
| 10 | …_10 | **0.2475** | M† | 0.261 / 0.247 | +0.0130 | 0.698 / 0.695 | F07 repack | 10,11,12 | 4.78 / 8.18 | 3 / 3 | 4.95 | **+0.68** ± 0.91 | 2/3 | **n** / Y |
| 11 | …_11 **b** | **0.2374** | H | 0.237 / 0.265 | −0.0280 | 0.672 / 0.662 | F08 repack | 21,26,35 | 2.51 / 7.62 | 3 / 3 | 13.81 | **+0.30** ± 0.34 | — | — |
| 12 | …_12 | **0.2348** | H | 0.235 / 0.575 | −0.3404 | 0.652 / 0.736 | F07 repack | 11,23 | 2.75 / 4.66 | 2 / 2 | 9.59 | −0.26 ± 1.49 | 1/3 | **n** / **n** |
| 13 | …_13 | **0.2241** | H | 0.224 / 0.240 | −0.0157 | 0.751 / 0.725 | F09 repack | 14,26 | 3.68 / 9.83 | 2 / 2 | 4.44 | −0.35 ± 0.15 | 2/3 | **n** / **n** |
| 14 | …_14 | **0.2220** | H† | 0.222 / 0.226 | −0.0036 | 0.691 / 0.677 | F05 repack | 13,34 | 3.08 / 5.54 | 2 / 2 | 8.64 | −0.89 ± 0.40 | 2/3 | **n** / **n** |
| 15 | …_15 | **0.2117** | H† | 0.212 / 0.213 | −0.0009 | 0.702 / 0.697 | F07 repack | 10,23 | 4.08 / 7.46 | 2 / 2 | 11.55 | −0.35 ± 0.37 | 2/3 | **n** / **n** |
| 16 | …_16 | **0.2051** | H | 0.205 / 0.245 | −0.0396 | 0.672 / 0.661 | F07 repack | 10,23 | 3.48 / 3.53 | 2 / **1** | 9.61 | −0.38 ± 0.53 | 2/3 | **n** / **n** |
| 17 | …_17 | **0.2034** | H | 0.203 / 0.303 | −0.0993 | 0.671 / 0.693 | F05 repack | 13,34 | 4.85 / 11.10 | 2 / 2 | 14.92 | −1.39 ± 0.83 | 2/3 | **n** / **n** |
| 18 | …_18 | **0.2014** | H | 0.201 / 0.438 | −0.2370 | 0.699 / 0.760 | F02 repack | 16,25 | 2.70 / 6.47 | 2 / 2 | 2.20 | −0.27 ± 0.46 | 3/3 | **n** / **n** |
| 19 | …_19 | **0.2010** | H | 0.201 / 0.321 | −0.1195 | 0.740 / 0.732 | F04 repack | 14,34 | 3.17 / 9.40 | 2 / 2 | 4.27 | −0.40 ± 1.71 | 1/3 | **n** / **n** |
| 20 | …_20 | **0.2008** | H | 0.201 / 0.229 | −0.0279 | 0.720 / 0.692 | F10 repack | 21,26 | 2.51 / 10.73 | 2 / 2 | 4.85 | −0.02 ± 0.49 | 1/3 | **n** / **n** |

Full per-design figures — every oracle, both orthologs, both draws, the standard deviations, the
second and third oracles' confidences, the gates and the composition columns — are in
`metrics_full.csv` and in each design's `metrics.json`.

**Eight things to read off that table, stated rather than left to be noticed.**

1. **The band is ranked on its worse ortholog, so it contains no strong-on-one-arm designs by
   construction.** The worse-ortholog interface ipTM runs **0.2008 to 0.6579**. Designs with a large
   gap between the arms are pushed down rather than rewarded: `…_06` reaches 0.716 on human and
   ranks sixth because its mouse arm is 0.333, and `…_12` reaches 0.575 on mouse and ranks twelfth
   because its human arm is 0.235. That is the selection logic working, and it is the reason the
   `ipTM H / M` pair must not be read as the ranking.
2. **No ortholog preference is claimed, for the band or for any design in it.** The `H − M` column
   runs **−0.3404 to +0.3836** and is positive for 8 designs and negative for 12. It is reported
   because it is measured. It is not a gate, it orders nothing, and §4.4.1 gives the measured reason
   it is not used: it reproduces inside chai and no second oracle confirms it.
3. **The K104 column is the mechanism's own test and it still fails.** Lys57 is reached at
   2.46-4.85 Å by every design, under an 8 Å pocket restraint that names it. Lys104, which nothing
   restrains, sits at **3.53-11.10 Å, median 7.81 Å, with 7 of 20 inside 7 Å**. The designed lysine
   *pair* is a lysine *site* on this evidence. The count inside 7 Å is higher than in either earlier
   band, which is a property of the designs this gate admitted and not of the mechanism.
4. **Six designs do not reproduce their own pose within 8 Å across five models** (`…_11`, `…_12`,
   `…_14`, `…_15`, `…_16`, `…_17`, at 8.6-14.9 Å). The human-arm ipTM correlates with that column at
   −0.661 over the 325, so a design that folds confidently on both arms and still scatters its pose
   is an informative row, not a safe one.
5. **Two designs clear the interfacial-histidine bar on human and not on mouse** (`…_08`, `…_16`,
   at 1). The gates were defined on human and are not retroactively applied, and these two are named
   rather than quietly carried.
6. **Ten of the seventeen designs with re-draw data leave the primary oracle's human-arm top 20 of
   the 50 at seed 8300, and nine at seed 9300.** That column tests a human-arm ordering, which is
   neither this band's gate nor its ranking key. On the rule
   actually in force, 17 of those 17 stay inside the re-drawn top 20 of the pool and 17 of 17 still
   clear the fold floor on both orthologs (§4.4.1). Both sets of numbers are reported; only the
   second set is about this band.
7. **Three delivered designs are ones Boltz-2 demotes** (`…_03`, `…_09`, `…_11`, marked **b**).
   The Boltz gate was relaxed for this band (§4.4) and their Boltz figures are carried in full in
   `metrics_full.csv`.
8. **The predicted pKa drift does not pick out the engaged designs.** It is positive in 2 of 20,
   median −0.27, and its largest positive value (`…_10`, +0.68) belongs to a design 8.18 Å from
   Lys104. This is the direction propka's additive model predicts — a solvent-exposed histidine
   drifts positive, an engaged buried one negative — and it is why the axis is a tiebreak and not
   evidence.

### 8.1 Designs that were measured and are not in the band

Target 1's convention is to name each documented design that is not submitted together with the bar
it missed. **No design in this band missed a bar**: all 20 clear every chai quality gate and the 0.65
binder-pLDDT floor on **both** orthologs, and `gate_waived` is blank in every row.

**Ten designs are carried in `metrics_full.csv` and in `micro/` with a `status` and no
`submission_rank`: `AMBRA_T2_micro_21` through `AMBRA_T2_micro_30`.** Each clears every selection
criterion — the fold floor on both arms and every chai quality gate — and is absent from the
submission only because the qualifying pool holds **30** designs and the band delivers 20. They were
cut on the ranking key, and the cut is narrow: the first design below the line is at worse-ortholog
interface ipTM **0.1948** against **0.2008** for the lowest-ranked delivered design, **0.0060
apart**. They are named because designs excluded by arithmetic on a continuous key, rather than by a
bar, are exactly the case a reader should be able to see — and because ten of them, rather than one,
makes the width of that cut impossible to miss.

The remaining 295 candidates missed the fold floor on one or both orthologs, or a quality gate, and
are not named design by design, because naming them would mean publishing campaign identifiers this
deposition deliberately does not carry.

What can be said is the funnel, with its denominators:

| | n |
|---|---|
| generated variants examined against the membership bar | **3,960** (33 originals × 120) |
| clearing ≥ 2 interfacial histidines | 1,357 |
| carried forward, score-ordered, ≤ 10 per original, no back-filling | **292** |
| folded this round (292 repacks + the 33 originals) | **325** |
| clearing all five gates on the human arm of the primary oracle | **148** |
| also clearing every gate on the second oracle (the rest demoted to a reserve tier) | **95** |
| carried into the three-oracle and mouse passes (top 50 of the 95 by interface ipTM) | **50** |
| clearing the binder-pLDDT floor at 0.65 on **both** orthologs, over all 325 | **34** |
| … and clearing all five primary-oracle gates — **the pool the band is drawn from** | **30** |
| **delivered** — top 20 of that pool on the worse-ortholog key | **20** |

The two selection routes are not nested, and the table should not be read as if they were. The
**50** is the top of the Boltz-gated, human-arm-ipTM-ordered route and exists because the
three-oracle and mouse passes were run on it; the **30** is cut from all 325 by the both-ortholog
fold floor plus the primary-oracle gates, with the Boltz gate relaxed, and is what the delivered
band comes from. Three of the delivered 20 are not in the 50.

The 50 spans **17** of the 33 families and is 45 repacks and 5 originals; the delivered 20 spans
**10** families and is **20 repacks and no originals** — no family original cleared the fold floor
on both orthologs — with at most **4** designs from any one family. The distribution is reported
rather than engineered: no per-family cap was applied, because capping would mean replacing a
design that clears every criterion with one that does not. Over the delivered 20 the worse-ortholog
interface ipTM runs **0.2008–0.6579**, with the human arm at 0.2008–0.7288 and the mouse arm at
0.2126–0.6579.

**Those are low numbers in absolute terms, and that is the honest headline of the round.** Over all
325 designs the primary oracle's median interface ipTM is **0.147** on the human arm with a 90th
percentile of **0.310**, and the delivered band's ranking key — the **worse** of two arms — runs
0.2008 to 0.6579. The band is not the top of that one-arm distribution and does not claim to be: it
is the designs the oracle is confident **folded on both orthologs**, ordered by an interface score
it is not confident about on either. A band selected for binding two targets cannot also be the top
of a one-target ranking, and this document would rather say which it is.

**Two movements from the previous round, because they are what a noisy cut costs.** One design rose
from rank 8 to joint first while another fell from 3 to 9, and a design excluded by the shortlist
cut came in at rank 8 when the band below the cut was measured too. **A cut inherits the error of
the measurement that drew it**, so re-ranking only what the cut selected cannot find its own
mistakes — and this round re-ranked only its own top 50.

---

## 9. Three oracles, and where they disagree

**Consensus was sought and not found. That is the result of this section, and it is reported rather
than averaged away.**

Three things travel with every number below. **(a) The third oracle carried no restraint** (§2),
while the other two carried the same 8 Å Lys57 pocket — read from the three input files, not
assumed. **(b) All three folded the ortholog they were supposed to**, read back out of the
structures. **(c) Interface ipTM is the same quantity on all three arms**: the maximum over the
three (protomer, binder) pairs in both matrix orientations, per design the median over five samples,
never the best sample.

### 9.1 Levels, which are not comparable, and orderings, which are

**The population this section compares.** Every cross-oracle comparison below over "the same 50" is
over designs that cleared **both** oracles' quality gates — the 50 were drawn from the 95 of 148
that clear the primary oracle's gates and Boltz-2's. That is not a formality: Boltz-2 acted as a
**demotion gate** when that pool was built, so these are not the primary oracle's unconditioned top
50. The figures over **all 325** are over the whole folded population and carry no such
conditioning, and the two are labelled separately throughout. **For the delivered band the Boltz-2
gate is relaxed and conditions nothing** (§4.4).

| axis, over the same 50 designs, all of which clear both oracles' quality gates | primary | Protenix (unrestrained) | Boltz-2 |
|---|---|---|---|
| interface ipTM, mean ± sd | 0.309 ± 0.162 | **0.456 ± 0.208** | **0.802 ± 0.106** |
| binder pLDDT, mean ± sd | 0.658 ± 0.088 | 0.599 ± 0.145 | 0.633 ± 0.088 |

The confidence scores are **not on a common scale** and are never averaged into one number; they are
compared as ranks.

| pairwise Spearman, n = 50 | interface ipTM | 95 % CI | binder pLDDT | 95 % CI |
|---|---|---|---|---|
| primary – Protenix | **+0.194** | [−0.131, +0.487] | **+0.694** | [+0.463, +0.847] |
| primary – Boltz-2 | **−0.195** | [−0.454, +0.090] | **+0.576** | [+0.362, +0.726] |
| Protenix – Boltz-2 | **−0.026** | [−0.311, +0.269] | **+0.326** | [+0.051, +0.555] |
| primary – Boltz-2, all 325 (reference) | −0.010 | [−0.116, +0.102] | +0.674 | [+0.604, +0.736] |

**Every binding interval contains zero; every folding interval excludes it. The three oracles agree
about folding and no two of them agree about binding.** Disattenuating by each oracle's own
within-run reliability changes nothing, and the one test that could have broken the tie in the
primary oracle's favour does not fire: ρ(primary, Protenix) − ρ(Boltz-2, Protenix), bootstrapped
over designs to respect the dependence between two correlations sharing an oracle, is **+0.220
[−0.207, +0.637]**. On binder pLDDT the same difference is **+0.368 [+0.167, +0.584]**, which does
exclude zero — the third oracle is closer to the primary one *about folding*, and only about
folding.

### 9.2 The control: is the weak agreement just the folding agreement?

With binder pLDDT partialled out (Spearman on rank transforms, bootstrapped over designs, n = 50):
primary – Protenix **+0.104** [−0.187, +0.377], primary – Boltz-2 −0.197 [−0.464, +0.093],
Protenix – Boltz-2 −0.030 [−0.316, +0.266]. **Nothing survives.** Even the weak primary–Protenix
association is not separable from their shared view of how well the binder folds.

### 9.3 Do not read an early number

The same code, the same designs, as the third oracle's arm filled: ρ(primary, Protenix) on interface
ipTM ran **+0.754** (n = 14), +0.696 (20), +0.398 (31), +0.235 (38), **+0.194** (50). Reported at
n = 14 it would have read "the third oracle sides with the first, consensus is defensible". The
designs folded first were the top-ranked ones, where all three happen to agree; the disagreement
lives in the rest of the 50. This is the clearest instance in this campaign of why a first result is
not a result.

### 9.4 Is the second oracle disagreeing, or is there nothing to disagree with?

A near-zero correlation has two readings and the primary arm alone cannot separate them. A
self-correlation under a seed change settles it, because test–retest *is* the reliability of the
design-level figure and therefore the ceiling on any correlation it can have with anything.

| arm | test–retest on interface ipTM | 95 % CI | on binder pLDDT |
|---|---|---|---|
| primary | **+0.940** | [+0.857, +0.974] | +0.995 |
| Boltz-2 | **+0.587** | [+0.359, +0.747] | +0.904 |
| Protenix (unrestrained) | **+0.624** | [+0.533, +0.705] | — |

**These are across-seed test–retest figures and not within-run ICC, and the distinction decides
every ceiling in this document.** ICC(1,k) = (MSB − MSW)/MSB over the five diffusion samples
overestimated test–retest on **all three** oracles — primary 0.996 → 0.940, Boltz-2 0.611 → 0.587,
**Protenix 0.989 → 0.624** — because five samples from one run share a trajectory and are not
independent re-draws. Substituting ICC would have inflated Protenix's ceilings by roughly 60 %. The
two formulas, so the arithmetic can be checked: **ICC(1,k) = (MSB − MSW)/MSB** and
**ρ_max = √(r_a · r_b)**.

**Boltz-2 reproduces its own ranking, so its near-zero correlation with the primary oracle is a
genuine disagreement about which designs bind, not an absence of signal** — the more interesting and
more awkward of the two possibilities. The largest correlation the two instruments could ever have
shown is √(0.940 × 0.587) = **0.742**; observed, **−0.195** on the 50 and **−0.010** over all 325.
Its unreliability accounts for at most a factor of 0.74 of the attenuation; the remainder is real.

This qualifies rather than overturns the mechanical reason to call Boltz-2 the outlier: its
interface ipTM is pinned near its ceiling (83.7 % of 325 designs above 0.7) and its model-to-model
spread (median 0.105) is about the size of its design-to-design spread (0.100), against the primary
oracle's 0.0059 against 0.119. It is a poor instrument; it is **not** a null one.

### 9.5 A second axis the scores cannot see: where each oracle puts the binder

Symmetry-aware cross-oracle binder Cα RMSD over the same 50 designs:

| pair | mean | sd | same site (≤ 8 Å) |
|---|---|---|---|
| primary – Protenix | 17.16 Å | 7.42 | 7/50 = 14 % |
| Boltz-2 – Protenix | 16.99 Å | 6.79 | 5/50 = 10 % |
| primary – Boltz-2 | 15.30 Å | 6.35 | 9/50 = 18 % |

**No pair of oracles docks the binder in the same place**, on a target whose longest dimension this
is comparable to. Over all 325 designs the cross-oracle median is **19.54 Å**, within 4 Å in 2.1 %,
and **0.285 Å** from a scrambled-partner null in which each design is paired against a different
design — formally non-zero at n = 325 and practically nothing, with 46 % of designs closer to a
random other design's second-oracle pose than to their own. Each oracle does reproduce its *own*
pose better than an unrelated design's, by 4.6 Å (primary) and 2.7 Å (Boltz-2), so this is
disagreement and not noise. Whatever a consensus of two of them would mean, it is not a consensus
about a pose.

### 9.6 Would a consensus have changed the band?

Yes, and there is no basis for preferring the result. Borda on within-set ranks — the only
combination rule that does not assume a shared scale, which these three demonstrably lack — gives a
top 20 of the 50 overlapping **the primary oracle's own top 20 of the 50** by **14/20** for
primary + Protenix and 13/20 for primary + Boltz-2. **Adding the third oracle as an equal vote
changes 6 of those 20**, and on the evidence of §9.1 and §9.2 there is no reason to prefer either
list, because the two orderings are not demonstrably related.

That comparison is against the ipTM-ordered top 20 of the 50, which **was** the delivered band
before the pLDDT floor re-cut it (§4.4.1) and is no longer. It is left as it was measured rather
than re-run against the new band, and labelled for what it is: a statement about two interface-ipTM
orderings of the same 50, on the axis the three oracles do not agree about.

### 9.7 Agreement on the delivered 20, design by design

The rule was stated before it was computed: a design "agrees" for an oracle if that oracle places it
in **its own** top 20 of the same 50, by its own human-arm interface ipTM. Under chance alone 8/20
is expected for each oracle and 3.2/20 for both.

**Two things make this a weaker comparison than it looks for the delivered band.** First, the rule
is defined on the top-50 replicate pool and **three delivered designs sit outside it**, so for
those three the flag is **undefined and written blank**, not false — a design that was never a
candidate for a set is not a design that was rejected from it. Second, and more important, the rule
ranks each oracle on its **human arm**, which is not the key this band is ordered on; it is a
comparison of one-arm orderings, carried because it is what was measured.

| | agreement, over the 17 delivered designs the rule is defined on |
|---|---|
| Boltz-2 | **6 / 17** (6.8 expected under chance) |
| Protenix (unrestrained) | **10 / 17** (6.8 expected) |
| both | **3 / 17** (2.7 expected) |

**The agreement is at chance on the load-bearing pair**, and the one figure above it — Protenix at
10 of 17 — rests on 17 designs and on an oracle that carried no restraint, so it is reported and
not leaned on. On the 50-design pool, where all of its members are inside the rule, loosening it
did not rescue the agreement either: top-25 gave 8 / 12 / 4 against 5.0 expected and top-30 gave
10 / 13 / 5 against 7.2.
The per-design columns are `boltz_in_own_top20`, `protenix_in_own_top20` and
`oracles_placing_it_in_their_own_top20` in `metrics_full.csv`.

### 9.8 What n = 50 cannot do

It cannot resolve |ρ| below about **0.28** at 95 % confidence. Every "the interval contains zero"
above should be read as *not demonstrable at this n*, not as *zero*; the cross-oracle intervals are
wide enough to contain weak true agreement. What the data **do** exclude is agreement anywhere near
the attainable ceiling. Nor can any amount of this kind of folding say which oracle is right: that
needs an axis none of them produces — a physics rescore, a buried-surface or contact-count measure,
or an experiment.

### 9.9 The oldest piece of the same disagreement

From the previous round, and still the sharpest form of it: on restraint-free coordinates the two
oracles disagreed in the direction that matters, the second finding the designed two-histidine
arrangement in **0 of 36** systems against the primary oracle's 4 of 36. These designs were
optimised against the primary oracle, so its view of them is the **least** independent evidence
available and the one most likely to be optimistic.
