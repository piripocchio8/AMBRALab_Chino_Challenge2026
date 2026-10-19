# Design strategy — AMBRA group, Chino lab (University of Naples Federico II)

**Challenge 2, a TNF-family homotrimer. 20 designs, all 39-residue disulfide-cyclised peptides.**

Repository (structures, metrics, methods, restraints):
`github.com/piripocchio8/AMBRALab_Chino_Challenge2026`

> **"Protonation-driven" is the objective, not a result.** No protonation state was varied anywhere
> in this campaign. The structure oracles are heavy-atom only and have no concept of one, there is
> no pH titration, and the two orthologs differ in **sequence and length**, not in pH. Every
> statement about acid in this document is a statement about what the designs were *selected for*.

> **On `[[PENDING: … ]]`.** Earlier drafts used that marker wherever a figure had not been measured,
> because the folding that selects the band was still running. All of them are now resolved — filled
> from a named result file, or replaced by a sentence saying the figure does not exist. A marker is
> not a number, and `scripts/make_target2_submission.py` refuses to write a row that carries one.

---

## 1. The objective we actually optimised

Not affinity, and **not the same switch as Target 1**. There the titratable group belongs to the
target and protonating it *adds* hydrogen bonds, so the binder is designed to hold more tightly in
acid. Here the titratable groups are **the binder's own histidines**, the partner is a **pair of
target lysines that are cationic at every pH of interest**, and protonating the histidines adds
**like-charge repulsion**. The design is therefore built to **bind at blood pH and be released as the
pH falls**.

| | |
|---|---|
| target | a TNF-family homotrimer, folded as the physiological trimer (chains A/B/C) with the binder as chain D |
| epitope | **Lys57 and Lys104** on **one protomer** of the human construct; **Lys57 and Lys103** on the mouse one, because mouse 104 is a proline |
| what the binder brings | **two or more histidines at interfacial positions**, canonical L residues, no non-canonical chemistry |
| mechanism, as designed | histidine neutral at pH 7.4 beside a permanent cation; **imidazolium beside the same cation at pH 6.5** — electrostatic destabilisation of the complex |
| intended direction | **weaker at acidic pH**, the opposite sign to Target 1. Not observed; nothing here varies pH |
| scaffold | 39-residue peptide closed by a real Cys1–Cys39 disulfide, not a head-to-tail amide |

**How far the delivered 20 get towards that geometry**, primary oracle, human arm, five models each
(`metrics_full.csv`): the binder's closest heavy atom reaches **2.46–4.85 Å** of Lys57 NZ, under an
8 Å pocket restraint on Lys57, and **3.53–11.10 Å** of Lys104 NZ — median **7.81 Å**, with **7 of
20** inside 7 Å. The restrained half of the designed pair is engaged; the unrestrained half is not.
The joint criterion, both designed histidines within 7 Å of the epitope on one protomer, **was not
computed for this band** — it belonged to the previous round's instrument, and the gap is named here
rather than filled from a different arm.

**It is proximity that is designed, not a bond.** The criterion is that each designed histidine sits
in a **5–7 Å window** of the epitope on a single protomer. A histidine that acquires a formal +1
charge 6 Å from an ammonium is doing the work the design asks of it; requiring it to hydrogen-bond
the lysine would be specifying a geometry the mechanism does not need. The campaign's scoring uses a
**7.0 Å** window as the figure of merit and keeps a 3.5 Å hydrogen-bond test as a separate readout,
never as the gate.

**"Specific" means reproducibly engaged, with whatever residue.** Each designed histidine has to be
engaged with *something* on the target, in a way that repeats across independent refolds, so that the
pose is a property of the sequence rather than of a draw. On the parent designs, **one of the two
designed histidines has that property and one does not**: His26 hydrogen-bonds Glu102 (human) /
Glu101 (mouse) in 5 of 5 reproducible cases, while His13 hydrogen-bonds in 63 % of folds with no
consistent partner across 20 designs. That asymmetry is a measurement, it was not designed in, and it
is part of why the current round widened the requirement from two named positions to **any two
histidines at interfacial positions**.

### 1.1 Both histidines on the same protomer, and why that sentence is load-bearing

The designed epitope spans about **15 Å on one protomer**. An earlier restraint file aimed the two
histidines at two *different* protomers, which asks for a bridge of about **29 Å** across a subunit
boundary. The consequences were not subtle, and they are the reason this document states the
single-protomer condition before anything else:

| | superseded restraint | corrected restraint |
|---|---|---|
| folds with the two histidines on **different** protomers | 150 of 167 (90 %) | — |
| folds with both histidines on **one** protomer | — | **48 of 48 (100 %)** |
| folds with both within 3.5 Å of one protomer | **0** | — |

The scoring instrument had the same defect in mirror image: it minimised **each** histidine over
protomers A/B/C independently, which cannot see a binder straddling two subunits. The current one
picks the protomer that minimises the **worse** of the two distances, so the two histidines are
scored jointly or not at all.

## 2. How the candidates were produced, and what is disclosed

Backbones were not diffused and threaded. Candidate sequences were optimised **directly against the
structure oracle** by a population-based evolutionary algorithm, then refined by
**interaction-preserving inverse folding with CARBonAra**: the positions carrying the design —
**both cysteines of the disulfide and every histidine** — were held fixed while the rest of the
binder was repacked, conditioned on the target chain as fixed context.

> **A note on disclosure.** The design engine is the subject of a manuscript in preparation and is
> described here in principle rather than in reproducible detail, **ahead of publication**. Nothing
> needed to *evaluate* these designs is withheld: sequences, predicted structures, every per-model
> measurement, the selection bar and its threshold, the restraint files and the command lines are all
> in the repository. What is held back is how candidate sequences were *generated*, not how they
> were *judged*. We are glad to discuss the method in confidence with the organisers.

**What the refinement step is, and what it is not.** It is a diversity generator. Measured over 42
repacks of 8 parents, it does **not** raise the worse-species interface confidence of its own parent
(median +0.028 against a pre-stated +0.05, with an inter-quartile range straddling zero), and the
parent backbone does not set engagement either (13 % of the variance between parent families on a
continuous measure). What repacking does is scatter sequences whose engagement differs **for real**:
refolds of one sequence agree with each other more than twice as often as independent draws at the
same base rate (0.561 observed against 0.258 expected). **Selecting among repacks is worth doing;
crediting the repack step with an improvement is not**, and the submitted band is drawn on that
understanding. Two parents and two repacks occupy the top four of the earlier ranked arm, which is
what that reading predicts.

One correction on the record, because it bears on the above: the inverse-folding backbone was built
without its carbonyl oxygen until 18 October 2026. The omission was measured (score 0.191 → 0.442
over three parents, distributions disjoint in every one) and fixed. **The verdict has since been
re-measured on the corrected code, over this round's 325 folds, and it holds**: across 32 family
originals with at least two complete repacks each, the typical repack is still *worse* than its own
original on the binding axis (mean-vs-mean −0.028; only 43.8 ± 6.8 % of repacks beat their original,
below the 50 % exchangeability predicts). On binder pLDDT there is a mean shift upward (+0.044,
62.5 ± 6.5 %) which cannot be attributed to repacking alone, because the repacks that were folded
are the top-scoring qualifiers of each original while the original was never scored by that model.
Named, not corrected.

## 3. How the band was selected

### 3.1 The membership bar

**At least two histidines at interfacial binder positions**, where interfacial means a binder
position with any heavy atom within **8.0 Å** of any target heavy atom in that candidate's own seed
structure. Applied to **all 3,960** generated variants of 33 parents, not to the decile each parent
kept on its generator's own score:

| | n |
|---|---|
| variants examined | 3,960 (33 parents × 120) |
| clearing **≥ 2** interfacial histidines | **1,357** |
| clearing ≥ 3 | 489 |
| carried forward, capped at 10 per parent, no back-filling | **292** |
| parents that cannot supply 2 | **1**, named in the methods |

**Why the scope matters, as a number.** Among the ten variants per parent that the generator's own
score had kept, the qualifier rate is **0.276** at the ≥ 2 bar against **0.343** over all 3,960 — the
score-best decile is *depleted* in interfacial histidines, so filtering the kept decile would have
selected from the worst-enriched tenth of the pool. Generator score and interfacial-histidine count
are essentially unrelated within a parent (pooled Spearman −0.078), which makes ordering the
qualifiers by score a **neutral tiebreak** rather than a second criterion.

### 3.2 The ranking rule that actually cut this band

**Gates on the human arm of the primary oracle, then that oracle's median interface ipTM on the
human arm, with binder pLDDT and predicted pKa drift as tiebreaks.** The top 50 of that order were
carried into the three-oracle and mouse passes.

**The delivered 20 are not the top 20 of that order, and they are not ordered on the human arm at
all.** Two criteria were adopted after the ordering had been computed, as project decisions: a
**binder-pLDDT floor of 0.65 applied to BOTH orthologs** decides membership, and the band is ranked
on the **worse-ortholog interface ipTM**. §3.2.1 gives both, the funnel, and the floors that were
rejected. They are stated as what they are: added late, not pre-registered with the gates below.

This is a change from an earlier draft of this document, which described the **previous** round's
rule — worse-species seating fraction first, interface confidence last — and it is corrected here
rather than quietly kept, because the two orderings are not the same and a reader cannot tell them
apart from the band.

| gate | cutoff | passed, of 325 |
|---|---|---|
| chain contract A=149 B=149 C=149 D=39, ≥ 3 parsed models | — | 100.0 % (integrity, inert) |
| median binder heavy atom to Lys57 NZ | ≤ 5.0 Å | 99.1 % — **inert**: the 8 Å pocket pulled nine deciles to 2.4–3.7 Å |
| median binder pLDDT | ≥ 0.50 | **53.2 %** — the gate that does the work |
| median interfacial binder histidines | ≥ 2 | 89.2 % |
| no inter-chain clash in more than half the models | — | 100.0 % (integrity, inert) |

**148 of 325 cleared every gate**; all 20 delivered designs clear all of them on human (Lys57 at
most 4.85 Å, binder pLDDT 0.652–0.862, at least two interfacial histidines). The quality gates were
defined on human and are not retroactively applied to mouse — the **fold floor of §3.2.1 is applied
to both arms**, and on mouse the band runs 0.651–0.832 with a minimum interfacial histidine count
of 1.

### 3.2.1 The both-ortholog fold floor and the worse-ortholog ranking key

**The objective is that BOTH orthologs are bound.** Not selectivity, not preference. Membership is
a binder-pLDDT floor of **0.65 on the human arm AND the mouse arm** plus every primary-oracle
quality gate; the order is the **worse** of the two orthologs' interface ipTM, `min(ipTM_H,
ipTM_M)`, descending — never the mean, never the maximum, never the difference.

| step | n |
|---|---|
| binder pLDDT ≥ 0.65 on **both** orthologs, over all 325 | **34** |
| … and clears every primary-oracle gate — **the pool** | **30** |
| … and clears the second oracle's gate too *(reported, **not** applied)* | 24 |
| **delivered** — top 20 of the pool on the worse-ortholog key | **20** |

**Ranking on the worse ortholog is the selection logic, not a presentation choice.** A design that
binds one ortholog well and the other poorly ranks low **by construction**: `AMBRA_T2_micro_06` is
0.716 on human and ranks sixth on a 0.333 mouse arm, `AMBRA_T2_micro_12` is 0.575 on mouse and ranks
twelfth on a 0.235 human arm. There is **no ortholog tiering** in the order — the both-ortholog
requirement is in the gate, so every delivered design already meets it.

**Why 0.65.** Applied to both arms, 0.70 leaves 10 designs from 4 families and 0.68 leaves 18 from
6 — neither fills a band of 20. 0.65 leaves 30 from 10 families. 0.62 would leave 42 from 14 and
move the worse-ortholog ipTM at pool rank 20 from 0.2008 to **0.2014**: a longer list and a lower
fold floor, and 0.0006 on the axis the band is ranked on.

**The human-minus-mouse difference is reported and is not a criterion.** It gates nothing, orders
nothing, runs −0.3404 to +0.3836 over the band and is positive for 8 designs and negative for 12.
**No ortholog preference is claimed.** The reason is measured and is the same evidence §5 rests on:
the difference reproduces within the primary oracle (ρ = +0.974 between draws) and not across
oracles (ρ = +0.0533 [−0.0569, +0.1580], 8.2 % of attainable, interval containing zero), so it is a
property of *(design, oracle)* rather than of *design*.

**Ten of the 30 are not delivered**, each documented with a `status` and no `submission_rank`. The
cut is narrow: the first design below the line is at 0.1948 against 0.2008 for the lowest delivered
one.

**Both halves of the rule survive an independent re-draw**, thresholds written down first. Of the
17 delivered designs with re-draw data, **17 of 17 still clear 0.65 on both orthologs** at a
different seed (per-design change −0.0002 ± 0.0054 human, −0.0002 ± 0.0067 mouse), and the ranking
key returns at **ρ = +0.9447 [+0.7970, +0.9897]** (n = 22 pool members) with **17 of 17** staying
inside the re-drawn top 20. Two caveats are carried rather than suppressed: **five** delivered
designs have their two arms closer together than the draw-to-draw spread in the key, so which one
is the worse is **not established** for them; and **eleven of the twenty sit inside 0.0467** on the
key, so a rule that reproduces is still not a rule that discriminates.

**Four of the 34 designs clearing the fold floor fail a primary-oracle gate**, all on the
two-interfacial-histidine bar; none would have entered the band, ranking 21, 25, 33 and 34 on the
key.

**The second oracle was a demotion gate when the top 50 was built, and it is RELAXED here.** Of the
148, **95** clear both oracles' gates and **53** were demoted — 31 on Boltz-2's binder-pLDDT gate,
15 on its interfacial-histidine gate, 4 on its Lys57 gate, 3 on two of them. That built the top 50.
It does **not** gate the delivered band: `boltz_state` is carried per design, and three delivered
designs are ones Boltz-2 demotes — `AMBRA_T2_micro_03`, `AMBRA_T2_micro_09` and
`AMBRA_T2_micro_11` — with every Boltz-2 figure for all three in `metrics_full.csv`. It was relaxed
because the oracles' disagreement is on the **binding** axis, where their agreement is a
single-digit percentage of attainable with an interval containing zero, while the floor that
decides membership is on the **foldedness** axis, where they agree (§5) and agree more on better
models. It does not follow that the second oracle's opinion is worthless, which is why it is
reported design by design rather than dropped.

The argument for letting a second oracle remove designs, which is what built the top 50: the gate
that did most of the removing is **binder pLDDT**, and folding is the one axis on which the three
oracles demonstrably agree (§5). A second opinion about folding is a second opinion about something
both oracles can see. A second opinion about *binding* would not have been, and none was used — no
cross-oracle binding score enters the ordering anywhere.

**The evidence against ranking on interface confidence was not withdrawn, and it stands against this
band.** Over 100 design-species pairs of the previous round the binder's pair-interface pTM tracks
**how confidently the binder folded** (r = +0.634) and not the engagement it is supposed to stand
for; the partial correlation with the measured histidine distance, controlling for binder pTM, went
from **+0.048 at n = 78 to −0.155 at n = 100**. On this round's 325 designs the same pattern shows
from the other side: ρ(interface ipTM, binder pLDDT) = **+0.714**, ρ(interface ipTM, within-oracle
pose spread) = **−0.661**. The axis that cut this band is **largely a foldedness-and-rigidity axis**,
and the band should be read that way. The lead-axis risk was pre-registered before the ordering was
computed and the pre-registered check did not fire — the top 50 by interface ipTM and the top 50 by
binder pLDDT overlap 21/50 = 42 %, above the 20 % that would have falsified the rule — but passing
that check is not the same as the axis meaning what its name says.

**The mouse arm selects, because the objective is that both orthologs are bound.** The primary
oracle's mouse pass covers all 325 candidates and enters the rule twice (§3.2.1): the fold floor
must be cleared on it as well as on human, and the ranking key is the **worse** of the two arms.
Where the two orthologs appear together the worse one is given and never an average: a design that
works on one ortholog and not the other is not cross-reactive, and an average hides exactly that.
The worse ortholog is mouse for **8 of the 20** and human for 12; for **five** designs the two arms
are closer together than the measurement's own draw-to-draw spread, so which is worse is **not
established** and they are marked as such.

### 3.3 The condition the band is ranked in is the condition the challenge folds

The challenge refolds submitted designs with none of our restraints, so the delivered ranking is read
off the arm with the design's declared intra-chain contacts **removed**. Those contacts hold the
declared topology and nothing else: releasing them moves the intra-chain distances by 8.16 Å, 3.53 Å
and 1.71 Å on the three declared pairs — two of the three past the pre-stated 3 Å — while seating is
unchanged (23/48 against 28/48, a difference of 0.10 ± 0.10). **A design selected partly for
satisfying its own fixture was selected on a term that does not matter**, and one design that led the
fixture-on arm at 3/3 in both species drops to 2/3 in human with a 6.3 Å pose spread once the fixture
comes out.

### 3.4 What the ranking can and cannot resolve

**On this band, measured.** Both halves of the rule reproduce; neither discriminates as well as
reproducing might suggest. All 17 delivered designs that have an independent re-draw still clear
the 0.65 fold floor on **both** orthologs, shifting by **−0.0002 ± 0.0054** (human) and **−0.0002 ±
0.0067** (mouse), n = 17; the worse-ortholog ranking key returns at **ρ = +0.9447 [+0.7970,
+0.9897]** over the 22 pool members with both re-draws, and **17 of 17** delivered designs stay
inside the re-drawn top 20 of the pool. But **eleven of the delivered twenty sit inside 0.0467** on
that key and the first design cut from the pool is **0.0060** below the lowest delivered one. **The
band is defensible as a selection; the order inside it, and membership at its boundary, is not.**

The top-20-of-50 overlap figures of **18/20** and **19/20** between draws test the primary oracle's
own **human-arm** top 20 of the 50, which is neither this band's gate nor its key; ten of the
seventeen delivered designs with re-draw data leave that top 20 at seed 8300 and nine at 9300. The figures above are the ones
about this band. Neither set covers the three delivered designs outside the 50-design replicate
pool, which have no re-draw at all.

**And reproducibility is not quality.** ρ(primary-oracle interface ipTM, cross-redraw binder pose
RMSD) = **−0.600 [−0.790, −0.338]**, n = 50: the designs the ordering likes are the designs whose
pose reproduces. A reproducible ranking is equally consistent with reproducibly ranking pose
rigidity. That sentence travels with every reproducibility figure here, including the pLDDT one.

**From the previous round, on the instrument used then.** The fold-to-fold spread of the primary measure is **1.82 Å**, so a three-fold mean carries a standard
error of **1.05 Å**. Most of the shortlist is separated by less than 2 Å, which means a three-fold
ranking of it is reading the error bar. That was acted on rather than assumed: 20 designs were
refolded to **13 folds per species, 520 folds**, and the three-fold order did not survive
(Spearman ρ = **+0.329** on the twelve shortlisted designs, against a pre-stated 0.70). The
higher-sampled arm did not produce an order either — the leaders' 95 % intervals overlap, and the
continuous form of the measure separates them only *inside* the 7 Å window, on the mean, with four of
five changing rank on the median.

**So the head of this list is a set, not a sequence, and more folds is not the lever that changes
that.** One candidate discriminator — the consistency of a design's own spread — was pre-registered
and tested on fresh seed blocks and **refuted** (0.57 Å did not reproduce: 1.10, 0.92, 1.94, 1.75).
The submitted order is published so it can be argued with, and the designs within the head should be
read as co-equal.

## 4. Why these peptides are worth bench time

**The switch is cheap to falsify and it commits to a direction.** One binding assay in two buffers
answers it. The mechanism predicts **weaker binding at acidic pH**; a flat result, or a tighter one,
refutes the design hypothesis outright rather than leaving an unexplained binder. It is worth saying
plainly that this is the only thing that *can* answer it: nothing computed in this campaign varies
pH, and the one predicted-pKa axis available is negative at the median over this band (−0.27, range
−1.39 to +0.68, 2 of 20 positive) and is reported with its limitation in front of it.

**The direction is the useful one for this target class.** A binder that holds at blood pH and lets go
in an acidified compartment is a different tool from one that does the reverse, and it is not the
behaviour the obvious histidine design gives you. Target 1 in this same submission builds the
opposite sign on a different protein, by a mechanism that shares no chemistry with this one.

**They are small, canonical and cyclised.** 39 residues, the twenty standard amino acids, closed by a
real disulfide between the terminal cysteines. They take the same cell-free route from synthesised
DNA as every other entry.

**The length risk, stated plainly, because it is the same one Target 1 carries.** In this
competition's own 800-design EGFR dataset the hit rate is 3.4 % at ≤ 30 aa and **0 % at 31–45 aa**
against 34.7 % at 200 aa and above. That dataset is a different target and the prior comes from
campaigns optimising **affinity**; this one optimises a **protonation-driven release**, which is a
property a modest binder can have. We state the number because a reviewer will find it, and because
the bins are small enough that the regime is closer to untested than excluded.

## 5. Independent validation, including where it disagrees with us

Every design in the current round is folded by **two independent oracles**, the primary one and
**Boltz-2**, each given the same single statement: an 8 Å pocket on Lys57 of one protomer, with
**no** histidine-to-lysine contact row and **no** disulfide row. Their confidence scores are not on a
common scale and are not averaged into one number.

A third oracle (**Protenix**) and the **mouse ortholog** were run as a separate pass over the top 50
once that set existed. All three oracles and both orthologs are complete at n = 50 for the figures
below.

### 5.1 Three oracles, and the consensus that was sought and not found

**This is the most important single result in this section, and it is a disagreement.** Pairwise
Spearman over the same 50 designs, each oracle's own median interface ipTM on the human arm over its
own five models, 95 % bootstrap intervals:

| pair | interface ipTM | binder pLDDT |
|---|---|---|
| primary – Protenix | **+0.194** [−0.131, +0.487] | **+0.694** [+0.463, +0.847] |
| primary – Boltz-2 | **−0.195** [−0.454, +0.090] | **+0.576** [+0.362, +0.726] |
| Protenix – Boltz-2 | **−0.026** [−0.311, +0.269] | **+0.326** [+0.051, +0.555] |

**Every binding interval contains zero; every folding interval excludes it. The three oracles agree
about folding and no two of them agree about binding.** The weak primary–Protenix association does
not survive controlling for binder pLDDT (partial ρ = +0.104 [−0.187, +0.377]), so what little there
is is not separable from their shared view of how well the binder folds.

Three things travel with that table.

**Protenix carried no restraint.** The primary oracle and Boltz-2 both carried the 8 Å pocket on
Lys57; Protenix's input JSON holds only `name` and `sequences`, with no constraint block anywhere in
it, verified by reading the file. Its reading is therefore of the *unrestrained* experiment.
Agreement across a restraint difference would have been harder to obtain and more interesting if
found; disagreement cannot be pinned on the model alone.

**The oracles do not put the binder in the same place either.** Symmetry-aware binder RMSD over the
same 50 — primary vs Protenix **17.16 Å** (same site, within 8 Å, in 7 of 50), Boltz-2 vs Protenix
**16.99 Å** (5 of 50), primary vs Boltz-2 **15.30 Å** (9 of 50). Over all 325 designs the
cross-oracle figure is **19.54 Å**, which is **0.285 Å** from a scrambled-partner null. Whatever a
consensus of two of them would mean, it is not a consensus about a pose.

**Do not read an early number.** As the Protenix arm filled, ρ(primary, Protenix) on interface ipTM
ran +0.754 (n = 14), +0.696 (n = 20), +0.398 (n = 31), +0.235 (n = 38), **+0.194 (n = 50)**. The
designs folded first were the top-ranked ones, where all three happen to agree; the disagreement
lives in the rest.

**Is Boltz-2 disagreeing, or merely noisy?** Both, and the first matters more. Its own test–retest
under a seed change is **ρ = +0.587 [+0.359, +0.747]** against the primary oracle's **+0.940
[+0.857, +0.974]**, so the largest correlation the two instruments could have shown is
√(0.940 × 0.587) = **0.742**. Observed: **−0.195** on the top 50 and **−0.010** over all 325. Its
unreliability accounts for at most a factor of 0.74 of the attenuation; the rest is genuine
disagreement about which designs bind.

**Agreement on the delivered band, by a rule stated before it was computed:** a design "agrees" for
an oracle if that oracle puts it in its own top 20 of the same 50, on its own human-arm interface
ipTM. Two things weaken it as a statement about this band. It is defined on the 50-design replicate
pool and **three delivered designs sit outside it**, for which the flag is blank — not measured, not
false. And it ranks each oracle on its **human arm**, which is not the key this band is ordered on,
so it compares one-arm orderings. Over the **17** delivered designs the rule is defined on:
**Boltz-2 agrees on 6 of 17, Protenix on 10 of 17, both on 3 of 17** — against **6.8 and 2.7
expected by chance**. The one figure above chance, Protenix at 10 of 17, rests on 17 designs and on
the oracle that carried no restraint, so it is reported and not leaned on. On the 50-design pool
itself, loosening the rule did not rescue the agreement either: top-25 gave 8 / 12 / 4 (5.0
expected), top-30 gave 10 / 13 / 5 (7.2 expected). Per design, the three columns are in
`metrics_full.csv` (`boltz_in_own_top20`, `protenix_in_own_top20`,
`oracles_placing_it_in_their_own_top20`).

A consensus **ordering** is therefore **not** better supported than the primary oracle alone: adding
Protenix as an equal vote (Borda on within-set ranks) changes **6 of the 20** of the primary
oracle's own top-20-of-50, and the two oracles' interface rankings are not demonstrably related, so
there is no basis for preferring either list. This is a statement about the *ordering* only. The
second oracle did act on **membership** of the 50, through the quality-gate demotion in §3.2 — but
**not** on membership of the delivered band, where that gate is relaxed (§3.2.1); no cross-oracle binding
score enters anywhere.

**What n = 50 cannot do.** It cannot resolve |ρ| below about 0.28 at 95 % confidence. Every "the
interval contains zero" above should be read as *not demonstrable at this n*, not as *zero*. What
the data do exclude is agreement anywhere near the attainable ceiling.

### 5.2 The mouse ortholog, and why the difference between the two is reported and not used

The mouse arm folds a **148-residue** protomer against the human arm's 149, as chains A/B/C with the
same binder as chain D. The two arms differ in the target sequence and, for Boltz-2, in the target
alignment; in nothing else. The Lys57 pocket restraint transfers unchanged because residue 57 is a
lysine in both. `approach_K104` does not exist on mouse — position 104 is a proline there — so it is
left empty rather than substituted, and it is never differenced across orthologs. The binder
sequence was verified identical between the human and mouse arm of the same design on all three
oracles — **325 of 325** on the primary oracle, both orthologs and both draws — and the ortholog
each arm actually folded was read back out of the structures rather than assumed.

Define Δ = interface ipTM(human) − interface ipTM(mouse) per design, per oracle. The questions were
pre-registered before the second mouse draw existed.

| | primary oracle | Boltz-2 | Protenix |
|---|---|---|---|
| Is Δ reproducible across an independent draw? | **ρ = +0.948** [+0.926, +0.964], **n = 325** | +0.431 [+0.133, +0.682], n = 50 | **+0.2175** [+0.0957, +0.3311], n = 325 |
| Is Δ a second axis rather than a relabelled human score? ρ(Δ, human ipTM) | **+0.668** [+0.433, +0.826] | +0.425 [+0.149, +0.652] | +0.700 [+0.526, +0.805] |
| Do the oracles agree about *which* designs carry a given Δ? ρ on Δ, n = 325 | primary–Boltz-2 **+0.0533** [−0.0569, +0.1580] | | primary–Protenix **+0.0566** [−0.0582, +0.1713]; Boltz-2–Protenix **−0.0139** [−0.1251, +0.0944] |

**Every one of those three agreement intervals contains zero.** Δ is reproducible inside the
primary oracle, is a genuine second axis there, and is **shared with no other oracle**. That is why
Δ is a reported per-design figure in this deposition and **not** a gate, a tiebreak or a sort key
(§3.2.1): a quantity one instrument reproduces and no other confirms is a property of
*(design, oracle)*, not of *design*.

**The chai Δ reliability is now measured on all 325, and it fell.** Until the mouse second draw
completed it was a top-50 figure of +0.9739 — measured on the primary oracle's own winners, where
range restriction and the winner's curse both inflate it. Over the full population it is
**+0.9480 [+0.9257, +0.9639], n = 325**, and recomputing the same statistic on the top 50 through
the same code returns +0.9739 exactly, which is how we know the drop is population and not method.

**As fractions of what the instruments' reliabilities make attainable**, with the formula
ρ_max = √(r_a · r_b) and r the **across-seed test–retest**:

| pair | ceiling | observed | fraction | interval contains zero |
|---|---|---|---|---|
| primary–Boltz-2, like-for-like on the top 50 | √(0.9739 × 0.4312) = **0.648** | +0.0533 | **8.2 %** | yes |
| primary–Boltz-2, **mixed n** (primary 325, Boltz-2 50) | √(0.9480 × 0.4312) = **0.639** | +0.0533 | **8.3 %** | yes |
| primary–Protenix, like-for-like on the top 50 | √(0.9739 × 0.1938) = **0.434** | +0.0566 | **13.0 %** | yes |
| primary–Protenix, **both at n = 325** | √(0.9480 × 0.2175) = **0.454** | +0.0566 | **12.5 %** | yes |
| Boltz-2–Protenix | **0.306** | −0.0139 | **−4.5 %** | yes |

**The asymmetry is stated rather than buried.** The primary oracle's Δ reliability is measured on
all 325; **Boltz-2's is still the top-50 figure** (+0.4312), because its mouse second draw covers 50
designs only, so every primary–Boltz-2 ceiling is a **mixed-n** quantity. Protenix now has two full
325-design mouse draws, so primary–Protenix can be given at a matched n for the first time. Moving
the primary oracle's reliability from +0.9739 to +0.9480 moves the headline fraction from 8.2 % to
**8.3 %** — the correction is real and it is small, and saying so is more useful than implying the
recompute overturned something.

**And the Protenix fractions say more about Protenix than about the designs.** Its own Δ
reliability is **+0.2175 [+0.0957, +0.3311]** — an instrument that barely reproduces its own Δ. A
low "fraction of attainable" against a ceiling built on that is weak evidence either way, which is
why the **primary–Boltz-2 pair is the load-bearing one**.

**The control that makes this unavoidable, and which got sharper at n = 325.** "The oracles
disagree about Δ" has a second reading — that nothing about the mouse arm is measurable by anyone.
It is refuted. The same two oracles were put on the **binder-pLDDT** delta, an axis whose *levels*
they agree about and whose delta each measures reliably by its own test–retest (+0.9627 and
+0.6203, ceiling √(0.9627 × 0.6203) = **0.7728**). At n = 50 that control found ρ = −0.003 and read
as a clean null. **At n = 325 it is ρ = +0.1152 [+0.0069, +0.2182] — 14.9 % of attainable, and the
interval excludes zero.** That makes the contrast with Δ ipTM **sharper, not softer**: **14.9 % with
an interval excluding zero against 8.3 % with an interval containing zero**. The disagreement is
not about ipTM and not about the mouse arm. It is the differencing.

Carry the mixed-n caveat here too: the 0.7728 ceiling is built from Δ binder-pLDDT reliabilities
measured on the **top 50**, while the observed +0.1152 is over all 325.

**The three reliabilities every ceiling in this document rests on, stated once.** They are
**across-seed test–retest** figures on interface ipTM — primary **+0.940**, Boltz-2 **+0.587**,
Protenix **+0.624** — and **not** within-run ICC over the five diffusion samples. The distinction is
load-bearing: ICC(1,k) = (MSB − MSW)/MSB overestimated test–retest on **all three** oracles (primary
0.996 → 0.940, Boltz-2 0.611 → 0.587, **Protenix 0.989 → 0.624**), and using it would have inflated
Protenix's ceilings by roughly 60 %. The reason is that five diffusion samples share one trajectory
and are not independent re-draws. The two formulas are given so a reader can check the arithmetic:
ICC(1,k) = (MSB − MSW)/MSB and ρ_max = √(r_a · r_b).

**A population-level claim made in an earlier draft of this document is WITHDRAWN.** That draft
reported mean Δ over the delivered band and over the 325 as evidence that the oracles "agree on the
sign while agreeing on nothing about which designs carry it". **That inference is withdrawn, not
hedged.** The delivered designs of the earlier bands were selected on an axis containing Δ, so the
mean Δ of the winners is a **selection artefact** — the winner's curse — and an independent re-draw
is the only unbiased estimate of it. The current band is not selected on Δ at all (§3.2.1), which
removes the artefact but does not resurrect the claim: **this document asserts no population-level
ortholog preference in either direction.** For the record and as a reported figure only, Δ over the
delivered 20 is negative for **12** designs on the primary oracle, **8** on Boltz-2 and **4** on
Protenix — three oracles that do not even agree on how many of these twenty prefer which ortholog.

**And it is not protonation.** Δ is a difference between two orthologs that differ in sequence and
length. No protonation state was varied, no pH was changed, and the delta inherits the same
ambiguity as the ranking: ρ(Δ, cross-redraw pose RMSD) = **−0.438 [−0.658, −0.152]**.

**What was once "cannot be computed" is now measured.** An earlier draft of this document recorded
that Protenix's across-seed replicate was 38 of 50, shard-ordered and therefore not a random
subset, that its human-arm test–retest from that partial set was **+0.482** and "was still falling
as the prefix grew" (+0.794 at n = 16 → +0.482 at 38), and that **no** Protenix mouse replicate
existed so the reliability of its Δ was **unknown**. All three statements are now superseded:

- **The "still falling" trend was prefix noise and the inference is deleted.** At the full n the
  Protenix human-arm ipTM test–retest is **+0.6242 [+0.5329, +0.7050]** (prefix 100 gave +0.649,
  prefix 325 +0.624), and under the full-sample distribution P(ρ₃₈ ≤ 0.482) ≈ **15 %** — an ordinary
  draw, not a downward drift.
- **Protenix has two full 325-design mouse draws** (seeds 7000 and 8000). Its ipTM(M) test–retest is
  **+0.5561 [+0.4639, +0.6375]** and its Δ test–retest is **+0.2175 [+0.0957, +0.3311]**. The
  figures called unknown are measured — and +0.2175 is a **weak** reliability, which is the point
  of quoting it.
- The surrounding argument stands unchanged and is the reason this correction matters: the
  within-run spread over five samples would have suggested 0.995, that substitution would have
  overstated reliability by 0.995 → 0.624, and it was correctly refused.

**Agreement is better on better models — for the fold, and not for binding.** Stratifying by a
held-out third-oracle quality measure, primary–Protenix agreement on **binder pLDDT** rises across
tertiles **+0.344 → +0.507 → +0.726**, a high-minus-low of **+0.382 [+0.169, +0.597]** and **+0.413**
after per-stratum attenuation correction — it grows, and grows *more* once corrected, because the
per-tertile reliabilities are flat. On **interface ipTM and ipSAE**, all **18** tertile contrasts
(3 pairs × 2 axes × 3 stratifiers) have intervals containing zero, and the ipTM point estimates lean
**negative** (−0.086 / −0.101 / −0.181), moving further negative under attenuation correction. With
n = 108 per tertile only |ρ| ≳ 0.19 is resolvable, and that limit belongs beside the claim. So the
oracles **do** converge about the fold on good models; a consensus **binding** ranking is no better
supported in the top third than in the bottom.

**Where the independent evidence already disagrees with us, on the previous round.** Folds with the
epitope restraint removed entirely are the honest test, and this campaign has not passed it:

| | measured |
|---|---|
| designs with restraint-free data | 5 |
| their distance to Lys57, restraint-free | **6.48 to 17.73 Å** (all fail a 5 Å contact test) |
| the same designs with the 8 Å pocket present | 2.72 to 3.72 Å |
| interface confidence, restraint-free against pocket-restrained | **0.078–0.138** against 0.10–0.42 |

Over a wider restraint-free check of **900 models** across two oracles, the binder reaches the
epitope — within 8 Å of both lysines in **33 of 36** systems by the primary oracle and 27 of 36 by
the second — while the **designed** two-histidine arrangement appears in **4 of 36** and **0 of 36**
respectively. Relaxing the requirement from the two named positions to **any** designed histidine
roughly triples the hit rate (32 of 540 models to **94 of 540** within 7 Å of Lys57), which is the
measurement behind the current round's wider bar.

**The delivered band has no restraint-free arm of its own.** Every fold it was cut on carries the
8 Å pocket. The restraint-free evidence above is the previous round's, on the previous round's
designs, and it is quoted here because it is the closest thing to a non-circular check that exists —
not because it was repeated on these 20.

This does not show the designs cannot bind. A 39-mer against a 447-residue trimer, given no prior for
where to look, will be placed somewhere on a large surface. It shows that **nothing in this campaign
has yet demonstrated unaided engagement of the epitope**, and that the ranking must not be read as an
ordering of unaided engagement.

**Two metrics that do not work on this system, reported so nobody re-derives them.** The primary
oracle returns ipSAE **exactly 0.000** on all 540 restrained models, because the target-binder PAE
bottoms out at 21.7 Å and nothing falls under the score's 10 Å cutoff — a real statement about a
small binder on a large target, not a bug. And the second oracle's largest interface score in the
pocket arm (0.726) belongs to the design with the **worst** binder confidence and the **largest**
histidine distance. Read either beside a measured distance or not at all.

**A predicted pKa shift is reported and treated carefully.** propka is run twice on the same
coordinates, once on the complex and once on the binder alone, so nothing but the target's presence
differs. Its additive model has no term for a geometry that *requires* the imidazolium, and burying a
histidine moves its desolvation penalty strongly negative, so an engaged buried histidine can read as
a negative shift. One conclusion drawn earlier in this campaign — that the histidines which titrate
are not the designed ones — was an **artefact of the restrained folds it was computed on** and has
been withdrawn: on restraint-free coordinates the designed histidines come back into the window
(2.10 → 6.55 and 4.27 → 6.16 on one design's mouse fold).

## 6. What we are claiming, and what we are not

Every number here is a property of a structure prediction. **No design in this target has been tested
experimentally** — no binding measurement, no pH titration, no expression data.

**What the measurements support:** that these binders reach the designed face of the trimer, and that
individual sequences differ reproducibly in how well they seat two histidines there — a sequence has
a propensity, not just a draw (0.561 three-fold agreement against 0.258 expected from independence).

**What they do not support:** unaided reproduction of the designed two-histidine arrangement, which
has not been demonstrated on restraint-free coordinates; an ordering of the head of the band, which
is a set of co-equal designs at any sampling we can afford; engagement of the *second* designed
lysine, which the delivered band does not show; and any claim about the *direction or the magnitude*
of the pH effect, which is read from geometry and charge, has not been computed as a free energy,
and has not been measured at any pH.

### 6.1 The band, in one paragraph

Twenty 39-residue disulfide-cyclised peptides, **10** backbone families, **all inverse-folding
repacks** — no family original cleared the fold floor on both orthologs — with two or three
histidines each. They are the designs clearing a **binder-pLDDT floor of 0.65 on BOTH orthologs**
and every primary-oracle quality gate, out of 325 folded, ordered by the **worse** of the two
orthologs' interface ipTM. Every figure below is a median or a count over **five** independent
models per design per ortholog, 200 models in `micro/` for the band; nothing is a best model.

| over the 20 | human | mouse |
|---|---|---|
| **worse-ortholog interface ipTM — the ranking key** | **0.2008 – 0.6579**, worse arm is mouse for 8 and human for 12 ||
| interface ipTM (primary oracle) | 0.201 – 0.729 | 0.213 – 0.658 |
| binder pLDDT | 0.652 – 0.862 | 0.651 – 0.832 (**the floor applies to both**) |
| human-minus-mouse ipTM — **reported, not a criterion** | −0.3404 – +0.3836; positive for 8, negative for 12. **No ortholog preference is claimed** ||
| binder heavy atom to Lys57 NZ (8 Å pocket present) | 2.46 – 4.85 Å | 1.96 – 4.17 Å |
| binder heavy atom to Lys104 NZ (unrestrained; no equivalent on mouse) | 3.53 – 11.10 Å, median 7.81, 7 of 20 within 7 Å | not applicable |
| interfacial binder histidines | 2 for 17, 3 for 3 | 2 for 15, 3 for 3, **1** for 2 |
| binder pose spread across the five models, symmetry-aware | 0.70 – 14.92 Å, 14 of 20 within 8 Å | not computed |
| predicted best surface-histidine pKa drift | −1.39 – +0.68, median −0.27, 2 of 20 positive | not computed |

| and across oracles and draws | |
|---|---|
| still clear the 0.65 floor on **both** orthologs under an independent re-draw | **17 / 17** of those that have re-draw data |
| the worse-ortholog ranking key between draws | **ρ = +0.9447** [+0.7970, +0.9897]; **17 / 17** stay in the re-drawn top 20 |
| in the second oracle's own top 20 of the same 50 | **6 / 17** (6.8 expected by chance) |
| in the third oracle's own top 20 | **10 / 17** (6.8 expected) |
| in both | **3 / 17** (2.7 expected) |
| demoted by the second oracle's quality gates, **reported and not excluded** | **3 / 20** |

The oracle-agreement and re-draw rows have a denominator of 17, not 20: they are defined on the
50-design replicate pool, and three delivered designs sit outside it. A blank in those columns of
`metrics_full.csv` means *not measured*, never *measured and failed*.

The membership criterion reproduces. The order does not, the boundary does not, and the three oracles do not
agree about which of these bind.

---

*AMBRA group, Department of Chemical Sciences, University of Naples Federico II.
marco.chino@unina.it · ambralab@unina.it*
