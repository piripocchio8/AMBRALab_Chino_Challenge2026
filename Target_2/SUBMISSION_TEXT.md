# Text for the submission form's description box

*(Paste the block below as-is. The attachable file is `Target_2/DESIGN_STRATEGY.md` in the
repository.)*

> **Not part of the paste.** Earlier drafts of this file carried `[[PENDING: … ]]` markers wherever
> a figure had not been measured, because the folding that selects the band was still running. All
> of them are now resolved — filled from a named result file, or replaced by a sentence saying the
> figure does not exist. A marker is not a number and must never reach a submitted file;
> `scripts/make_target2_submission.py` refuses to write a row that carries one.

---

**Binders designed to be released by acidification, against a TNF-family homotrimer — AMBRA group,
Chino lab, University of Naples Federico II**

We optimised for a **protonation-driven release**, not for affinity, and the intended switch runs in
the **opposite direction** to our Target 1 entry. There, a histidine of the target gains hydrogen
bonds when it is protonated and the binder holds tighter in acid. Here the titratable groups are the
**binder's own histidines**, their intended partner is a **pair of target lysines that carry a
positive charge at every pH of interest**, and protonating the histidines would put **two like
charges in contact**. These designs are built to bind at blood pH and to be destabilised as the pH
falls.

**Nothing in this submission measures protonation, and we would rather say so than let the name
imply otherwise.** No protonation state was varied anywhere in this campaign. The structure oracles
are heavy-atom only and have no concept of one; there is no pH titration and no binding measurement
of any kind. Every statement about acid here describes what the designs were *selected for*.

**20 disulfide-cyclised peptides, 39 aa, canonical residues only**, from **10** backbone families,
**all of them inverse-folding repacks** — no family original cleared the fold floor on both
orthologs. Each carries **two or three histidines at interfacial
positions**, designed to seat against **Lys57 and Lys104** of **one protomer** in the human
construct — **Lys57 and Lys103** in the mouse one, because mouse 104 is a proline, so the site is
derived per species rather than copied across.

**How close the delivered band gets, measured.** On five models per design per ortholog, the
binder's closest heavy atom reaches **2.46–4.85 Å** of Lys57 NZ — under an 8 Å pocket restraint on
Lys57 — and **3.53–11.10 Å** of Lys104 NZ, median **7.81 Å**, with only **7 of 20** inside 7 Å. The
restrained half of the designed pair is engaged; **the unrestrained half is not**. The joint
criterion, both designed histidines within 7 Å of the epitope on one protomer, was the previous
round's instrument and **was not computed for this band**; we name the gap rather than fill the
column from a different arm.

**What is designed is proximity, not a bond.** A histidine that acquires a formal +1 charge within
**5–7 Å** of a permanent ammonium is doing the work the mechanism asks of it; requiring it to
hydrogen-bond the lysine would specify a geometry the mechanism does not need. In the previous round
a 7.0 Å window on a **single protomer** was used, with both designed histidines scored **jointly**,
because the designed epitope spans about 15 Å on one subunit and a scorer that minimises each
histidine over protomers independently is blind to a binder straddling two of them. Correcting that
one point moved the population from **150 of 167 folds with the two histidines on different
subunits** to **48 of 48 with both on protomer A**.

**"Specific" means reproducibly engaged, with whatever residue.** Each histidine must be engaged
with something on the target in a way that repeats across independent refolds. On the previous
round's parent designs one of the two had that property and one did not — His26 hydrogen-bonds
Glu102 (human) / Glu101 (mouse) in 5 of 5 reproducible cases, His13 in 63 % of folds with no
consistent partner — which is why this round requires **any two** interfacial histidines rather than
two named positions, and why the histidine positions differ from design to design.

Sequences were optimised **directly against a structure oracle** by an evolutionary algorithm, then
refined by **interaction-preserving inverse folding (CARBonAra)**, holding both cysteines of the
disulfide and every histidine fixed while the rest of the binder was repacked. That refinement is a
**diversity generator, not an improver**, and we report it as one: over 42 repacks of 8 parents it
does not raise the worse-species interface confidence of its own parent (median +0.028 against a
pre-stated +0.05), and on this round's 325 folds the *typical* repack is **worse** than its own
original on the binding axis (mean-vs-mean −0.028; only 43.8 ± 6.8 % of repacks beat their original,
below the 50 % exchangeability predicts). Repacks do reach the top — 15 of the delivered 20 are
repacks — but not *because* they were repacked.

**Membership is a bar, and it was applied to the whole pool rather than to the generator's own best
decile.** Over **3,960** generated variants of 33 originals, **1,357** carry at least two histidines
at interfacial positions and 489 carry three; **292** were carried forward, capped at ten per
original, with no back-filling, and folded alongside the 33 originals — **325 designs**. The
generator's score and the interfacial-histidine count are essentially unrelated (pooled Spearman
−0.078), and its best decile is *depleted* in interfacial histidines (0.276 against 0.343), so
filtering that decile would have selected from the worst-enriched tenth of the pool.

**How the band was cut, stated as it happened.** Gates on the human arm of the primary oracle —
chain contract, Lys57 approach ≤ 5 Å, binder pLDDT ≥ 0.50, at least two interfacial histidines, no
inter-chain clash — left **148 of 325**. Those were ordered by **the primary oracle's median
interface ipTM on the human arm**, with binder pLDDT and predicted pKa drift as tiebreaks, and the
top 50 went into the three-oracle and mouse passes. Two of the five gates are inert on this arm:
the Lys57 gate passes 99.1 % because the 8 Å pocket pulled nine deciles of the population to
2.4–3.7 Å, and the clash and chain-contract gates are integrity checks.

**The delivered 20 are not the top 20 of that order, and the one thing a reader has to know about
this band is what it is selecting for.** The objective of this target is that **both orthologs are
bound** — not selectivity, not ortholog preference — and two criteria were adopted after the
ordering had been computed, as project decisions, to make the band say that. Membership is a
**binder-pLDDT floor of 0.65 applied to the human arm AND the mouse arm**, plus every
primary-oracle quality gate: **34** of 325 clear the floor on both, **30** of those clear the gates,
and the band is the top 20 of those 30. The order is the **worse** of the two orthologs' interface
ipTM, `min(ipTM_H, ipTM_M)`, descending — never the mean, never the maximum, never the difference.

**Ranking on the worse ortholog is the whole selection logic.** A design that binds one ortholog
well and the other poorly ranks **low by construction**, because the number it is ranked on is the
poor one. Two delivered designs make the point: one reaches 0.716 interface ipTM on human and ranks
sixth because its mouse arm is 0.333; another reaches 0.575 on mouse and ranks twelfth because its
human arm is 0.235. An average would have let the good arm pay for the bad one.

**The human-minus-mouse difference is reported per design and is not a selection criterion.** It
gates nothing and orders nothing; over the delivered 20 it runs −0.3404 to +0.3836, positive for 8
designs and negative for 12. **We claim no ortholog preference, for the band or for any design in
it.** The reason we do not select on it is measured: that difference reproduces **within** our
primary oracle (ρ = +0.974 between independent draws) and **not across oracles** (ρ = +0.0533
[−0.0569, +0.1580] against the second oracle, 8.2 % of what their two reliabilities make attainable,
interval containing zero). A quantity one oracle reproduces and no other confirms is a property of
*(design, oracle)*, and selecting on it would be selecting on the oracle.

**Why 0.65.** The floor was taken as low as it had to go to fill a 20-design band from a pool with
more than a handful of backbone families, and no lower: 0.70 leaves 10 designs from 4 families and
0.68 leaves 18 from 6 — neither fills the band — while 0.65 leaves 30 from 10. Dropping to 0.62
would add 12 candidates and move the worse-ortholog ipTM at pool rank 20 by 0.0006.

**Both halves of the rule survive an independent re-draw**, with the thresholds written down before
the numbers were looked at: of the 17 delivered designs that have re-draw data, **17 of 17 still
clear 0.65 on both orthologs** at a different seed, and the ranking key returns at **ρ = +0.9447
[+0.7970, +0.9897]** with 17 of 17 staying inside the re-drawn top 20. Two caveats travel with that
and we state both: for **five** delivered designs the two orthologs are closer together than the
draw-to-draw spread in the key, so which one is the worse is **not established**; and reproducing is
not discriminating — eleven of the twenty sit inside 0.0467 on the key.

**The second oracle's quality gate was relaxed for this band, and we would rather name that than
let it be inferred.** The same four gates were applied on the second oracle's models; of the 148,
**95** clear both and **53** were demoted, 31 of them on the second oracle's binder-pLDDT gate. That
demotion built the top 50. It does **not** gate the delivered band, which is cut from all 325 by the
both-ortholog fold floor and the primary oracle's gates. The gate was relaxed because the oracles'
disagreement is on the **binding** axis, where their agreement is a single-digit percentage of what
their own reliabilities make attainable and the interval contains zero, while the floor that decides
membership is on the **foldedness** axis, where they agree and agree more on better models. It does
not follow that the second oracle's opinion is worthless. **Three delivered designs are ones it
demotes** — `AMBRA_T2_micro_03`, `AMBRA_T2_micro_09` and `AMBRA_T2_micro_11` — and every one of its
figures is carried per design in `metrics_full.csv`. No cross-oracle *binding* score enters the
ordering anywhere.

**We rank on interface confidence and the evidence against doing so has not been withdrawn.** Over
100 design-species pairs of the previous round that quantity tracks **how confidently the binder
folded** (r = +0.634), and its partial correlation with the measured histidine distance, controlling
for binder confidence, went from +0.048 at n = 78 to **−0.155 at n = 100**. On this round's 325
designs, ρ(interface ipTM, binder pLDDT) = **+0.714** and ρ(interface ipTM, within-oracle pose
spread) = **−0.661**. The axis that cut this band is largely a foldedness-and-rigidity axis and the
band should be read that way — and it is why the band is ranked on the **worse** of its two
orthologs rather than on either one alone. **The worse ortholog is always reported and never
averaged with the better one.**

**This is a set of 20, not a ranked 20.** The rule reproduces: all 17 delivered designs with an
independent re-draw still clear the 0.65 floor on both orthologs, the worse-ortholog ranking key
returns at ρ = **+0.9447** [+0.7970, +0.9897], and 17 of 17 stay inside the re-drawn top 20. But
reproducing is not discriminating: **eleven of the twenty sit inside 0.0467** on the key, and the
first design cut from the pool is **0.0060** below the lowest delivered one. The rank column exists
because the form reads a ranking from the top row down. And
reproducibility is not quality — ρ(interface ipTM, cross-redraw binder pose RMSD) = **−0.600**
[−0.790, −0.338], so a reproducible ranking is equally consistent with reproducibly ranking **pose
rigidity**.

**Three oracles were run and they disagree about binding.** At n = 50, pairwise Spearman on
interface ipTM: primary–Protenix **+0.194** [−0.131, +0.487], primary–Boltz-2 **−0.195** [−0.454,
+0.090], Protenix–Boltz-2 **−0.026** [−0.311, +0.269] — **every interval contains zero**. On binder
pLDDT the same three are **+0.694**, **+0.576**, **+0.326**, and **every interval excludes it**. The
three agree about folding and no two agree about binding; the weak primary–Protenix association does
not survive controlling for binder pLDDT (partial ρ = +0.104, interval containing zero). **Protenix
carried no restraint at all** — its input holds only the sequences, verified by reading the file —
while the other two carried the same 8 Å Lys57 pocket, so its disagreement cannot be pinned on the
model alone. Of the delivered 20, Boltz-2 puts **7** in its own top 20 of the same 50 and Protenix
**9**, with **3** in both, against **8** and **3.2** expected by chance. Boltz-2 reproduces its own
ranking under a seed change (ρ = +0.587), so its near-zero correlation with the primary oracle is a
genuine disagreement and not an absence of signal. **Consensus was sought and not found**, and we
report that rather than averaging it away.

**The two orthologs, and why the difference between them is reported and not used.** The mouse arm
folds a 148-mer protomer against the human 149-mer; the arms differ in target sequence and
alignment and in nothing else, and the binder sequence was verified identical across arms, 325 of
325. The human-minus-mouse interface-ipTM difference is **reproducible within the primary oracle**
— **ρ = +0.948 [+0.926, +0.964] over all 325 designs**, with both orthologs independently re-drawn
— and is a **genuine second axis** there (|ρ| with the human score = 0.668). But it is **shared
with no other oracle**: on that difference, primary–Boltz-2 is **+0.0533 [−0.0569, +0.1580]**,
primary–Protenix **+0.0566 [−0.0582, +0.1713]** and Boltz-2–Protenix **−0.0139 [−0.1251, +0.0944]**
— **all three intervals contain zero**. Against the ceiling their own reliabilities make attainable,
primary–Boltz-2 shares **8.3 %** (√(0.948 × 0.431) = 0.639). **That is the measured reason this
difference gates nothing and orders nothing in our band**, and why we claim **no ortholog
preference in either direction**: a quantity one instrument reproduces and no other confirms is a
property of *(design, oracle)*, not of *design*.

A control rules out the easy explanation that nothing about the mouse arm is measurable by anyone.
On the **binder-pLDDT** difference — an axis whose levels the two oracles agree about and whose
difference each measures reliably (+0.9627 and +0.6203, ceiling 0.7728) — they share **14.9 %** of
what was attainable, **ρ = +0.1152 [+0.0069, +0.2182], interval excluding zero**. So: 14.9 % with
an interval excluding zero on the axis they agree about, against 8.3 % with an interval containing
zero on the one they do not. **The differencing is where agreement dies.** And it is **not**
protonation: the orthologs differ in sequence and length, not in pH.

**Where the independent evidence disagrees with us, and it does.** The delivered band has **no
restraint-free arm of its own**; every fold it was cut on carries the 8 Å pocket. In the previous
round, on folds with the restraint removed entirely, the five designs that have such data miss Lys57
by **6.5 to 17.7 Å** and their interface confidence collapses from 0.10–0.42 to 0.078–0.138. Over a
wider restraint-free check of **900 models** across two oracles the binder reaches the face — within
8 Å of both lysines in 33 of 36 systems by the primary oracle, 27 of 36 by the second — while the
designed two-histidine arrangement appears in **4 of 36** and **0 of 36**. A null control is not
flattering either: the binder was typically closer to a lysine the design never named (4.57 Å) than
to the designed pair (11.11 Å), and Lys57 ranks second of six lysines in both oracles independently
against a chance expectation of 3.5. **Nothing in this campaign has yet demonstrated unaided
engagement of the epitope**, and the ranking must not be read as an ordering of unaided engagement.
A 39-mer given no prior for where to look on a 447-residue trimer will be placed somewhere on a
large surface, so this is a statement about what has been demonstrated, not a demonstration that the
designs fail.

**Neither do the oracles place the binder in the same position.** Symmetry-aware binder RMSD across
oracles on the delivered 50 is 15.3–17.2 Å with the same site reached in 5–9 of 50; across all 325
designs the cross-oracle figure is 19.5 Å, which is **0.285 Å** from a scrambled-partner null. Each
oracle does reproduce its own pose better than an unrelated design's, by 4.6 Å and 2.7 Å
respectively, so this is disagreement rather than noise.

**Metrics that do not work on this system**, reported so they are not re-derived. **ipSAE is
computed for this band** — all three oracles, both orthologs, all 325 designs — and it is **not a
second axis**: within oracle, ρ(ipSAE, interface ipTM) is +0.867 for the primary oracle, +0.879 for
Protenix and +0.972 for Boltz-2, and 60.6 % of primary-oracle and 62.8 % of Protenix designs sit at
or below the metric's own floor of 0.0099, with 51 % of Protenix designs exactly 0. On this target
"ipSAE + ipTM" is close to 2 × ipTM. (Separately, on the **previous, restrained** round the primary
oracle returned ipSAE exactly 0.000 on all 540 models, because the target-binder PAE bottoms out at
21.7 Å and nothing reaches the score's 10 Å cutoff; that remains true of that round.) The second
oracle's largest interface score in the pocket arm belongs to the design with the worst binder
confidence and the largest histidine distance. A predicted pKa shift is reported and treated with
care — propka is additive, has no term for a geometry that requires the imidazolium, and over this
band it runs **−1.39 to +0.68 with a median of −0.27 and only 2 of 20 positive**, so it does not
support the mechanism in either direction. One earlier conclusion of ours drawn from restrained
folds was an artefact and has been withdrawn.

**The length risk, from the organisers' own data, as in our Target 1 entry.** That 800-design EGFR
set gives a 3.4 % hit rate at ≤ 30 aa and **0 % at 31–45 aa**, and all of these are 39 aa. It is a
different target and that prior comes from campaigns optimising affinity, while this one optimises a
protonation-driven release that a modest binder can still show; the bins are also small enough that
the regime is closer to untested than excluded. We state it rather than leave it to be found.

**No design here has been tested experimentally** — no binding data, no pH titration, no expression
results. Every number is a property of a structure prediction. The design engine is the subject of a
manuscript in preparation and is described in principle ahead of publication; every sequence,
structure, per-model measurement, restraint file and command line needed to evaluate the designs is
public at **github.com/piripocchio8/AMBRALab_Chino_Challenge2026**.
