# Target 2 — TNF-family homotrimer, binders designed to be released by acidification

De novo binders against a **TNF-family homotrimer**, folded as the physiological trimer with the
binder as a fourth chain. The design objective is not affinity and it is not the same objective as
Target 1: these designs carry **their own histidines** towards a **lysine-rich epitope on one
protomer**, close enough that protonating those histidines at acidic pH would put **two like charges
in contact**. The intended behaviour is a **release** on acidification, not a tightening.

> **"Protonation-driven" names the objective, and nothing here measures it.** No protonation state
> was varied anywhere in this campaign. The structure oracles are heavy-atom only and have no
> concept of a protonation state, there is no pH titration, and the two orthologs differ in
> **sequence and length**, not in pH. Wherever this deposition says protonation, read *what the
> designs were selected for*, never *what was observed*.

```
micro/            the delivered band: 20 directories, one per design, each with the
                  models it was measured on, its restraint file, its sequence and
                  a metrics.json carrying every number quoted for it
docs/             the methods, the metric definitions, and ranking.json (the build input)
submission.csv    the submitted file: name / sequence / molecule_class, nothing else
metrics_full.csv  the same 20 rows with every metric they were measured on
```

> **On `[[PENDING: … ]]`.** Earlier drafts of these files used that marker wherever a figure had not
> been measured. A marker is not a number, is not a placeholder value, and must not survive into a
> deposited file; `scripts/make_target2_submission.py` refuses to write a row that carries one. All
> sixteen markers are now resolved — either filled from a named result file, or replaced by a
> sentence saying the figure does not exist. `grep -rn 'PENDING' Target_2/` now returns only boxes
> like this one, which explain the convention.

## One band, and why there is only one

Target 1 is split into micro / mini / large by binder length. Every candidate in this target's pool
is a **39-residue cyclic peptide** closed by a Cys1–Cys39 disulfide, so the whole band falls in the
same size class and `mini/` and `large/` are absent rather than empty: this campaign produced nothing
in those size classes, and a directory for a size we did not design would be an empty claim.

**What we could not establish, and are not guessing at.** We could not find, in the documents
available when this was written, the organisers' own definition of the Target-2 categories, the
construct they publish, or the number of designs the target accepts. `micro/` here uses *Target 1's*
size definition (under 40 residues), not a Target-2 category we have verified. The band is **20
designs**, which is the size of the set we deliver and **not** an allowance we checked. If the
organisers' Target-2 scheme differs, the directory and the count are what must change, not the
designs.

## The objective, stated plainly

The target protomer presents a **lysine pair** on one face: **Lys57** and **Lys104** in the human
construct, **Lys57** and **Lys103** in the mouse one — mouse 104 is a proline, so the second lysine
is not at the same index in the two orthologs and the restraint is derived per species rather than
copied. A lysine ammonium is cationic across the whole pH range of interest. A histidine is not: it
is neutral at blood pH and the imidazolium at tumour pH.

So a binder that **seats two of its own histidines** against that lysine pair would be uncharged
against cationic where it binds at pH 7.4, and would become **cationic against cationic** as the pH
falls. That is the switch, and its intended sign is the opposite of Target 1's:

| | Target 1 (EGFR domain III) | Target 2 (this target) |
|---|---|---|
| titratable group | a histidine **of the target** | histidines **of the binder** |
| partner | binder main-chain carbonyls, or an engineered carboxylate | **lysines of the target**, cationic throughout |
| what protonation is intended to do | add hydrogen bonds | add **like-charge repulsion** |
| intended direction | tighter at acidic pH | **released at acidic pH** |

The two targets are therefore not the same experiment run twice, and a failure of one carries no
information about the other. **Neither direction has been observed**; both are design objectives.

### How far the delivered band actually gets towards that geometry

Stated here rather than at the end, because it is the first thing a reader should have. Measured on
the 20 delivered designs, primary oracle, human arm, five models each
(`metrics_full.csv`, and `metrics.json` in every design directory):

| | measured on the band |
|---|---|
| binder heavy atom to **Lys57** NZ, median over models, per design | **2.46 – 4.85 Å** — **under an 8 Å pocket restraint on Lys57** |
| binder heavy atom to **Lys104** NZ, same route | **3.53 – 11.10 Å**, median of the 20 **7.81 Å**; **7 of 20** are within 7 Å |
| binder histidines in contact with the target (any heavy atom ≤ 8 Å), median over models | on human, 2 for 17 designs and 3 for 3; on mouse, 2 for 15, 3 for 3 and **1** for 2 |

The first row is the restraint being satisfied. The second row is not restrained by anything, and it
says plainly that **the second half of the designed epitope is not engaged**: the lysine *pair* that
the mechanism is built on is, on this evidence, a lysine *site*. The third row says histidines are at
the interface, which is the membership bar, and not that they are at the lysines.

**The joint criterion — both designed histidines within 7 Å of the epitope on one protomer — was
not computed for this band.** It was the previous round's instrument; this round measured the three
quantities above instead. We would rather name the gap than fill the column with a number from a
different arm.

## How the band was chosen

**The band was ordered on interface confidence, and that is a change from what earlier drafts of
this file said.** It is stated first because it is the most load-bearing correction in this
deposition.

The 325 folded designs were cut by gates on the **human** arm of the primary oracle, and the
survivors were ordered by **the primary oracle's median interface ipTM on the human arm**, with
binder pLDDT and the predicted pKa drift as tiebreaks. The top 50 of that order were carried into
the three-oracle and mouse passes.

| gate | cutoff | passed, of 325 |
|---|---|---|
| chain contract A=149 B=149 C=149 D=39 and ≥ 3 parsed models | — | 100.0 % (integrity, inert) |
| median binder heavy atom to Lys57 NZ | ≤ 5.0 Å | 99.1 % — **inert**, because the 8 Å pocket pulled nine deciles of the population to 2.4–3.7 Å |
| median binder pLDDT | ≥ 0.50 | **53.2 %** — the gate that does the work |
| median interfacial binder histidines | ≥ 2 | 89.2 % |
| no inter-chain clash in more than half the models | — | 100.0 % (integrity, inert) |

**148 of 325 cleared every gate.**

### The both-ortholog fold floor and the worse-ortholog ranking key

**The objective of this target is that BOTH orthologs are bound.** Not selectivity, not ortholog
preference. The band's membership and its order both follow from that, and both were decided after
the ordering above had been computed, as project decisions rather than rules pre-registered with
the gates.

> **Membership:** binder pLDDT **≥ 0.65 on the human arm AND on the mouse arm**, plus every
> primary-oracle quality gate.
> **Order:** the **worse** of the two orthologs' interface ipTM, `min(ipTM_H, ipTM_M)`, descending.
> Never the mean, never the maximum, never the difference between them.

**Ranking on the worse ortholog is the band's whole selection logic.** A design that binds one
ortholog well and the other poorly ranks **low by construction**, because the number it is ranked on
is the poor one. `AMBRA_T2_micro_06` reaches 0.716 on human and sits at rank 6 because its mouse arm
is 0.333; `AMBRA_T2_micro_12` reaches 0.575 on mouse and sits at rank 12 because its human arm is
0.235. An average would have let the good arm pay for the bad one, and a maximum would have rewarded
exactly the designs this target is not asking for.

| step | n |
|---|---|
| binder pLDDT ≥ 0.65 on **both** orthologs | **34** |
| … and clears every primary-oracle gate — **the pool** | **30** |
| … and clears the second oracle's gate too *(reported, **not** applied)* | 24 |
| **delivered** — the top 20 of the pool on the worse-ortholog key | **20** |

The ten pool members that are not delivered are documented with a `status` and no
`submission_rank`. There is **no ortholog tiering in the order**: the both-ortholog requirement is
in the gate, so every delivered design already meets it.

**Why 0.65 and not higher.** The floor was taken as low as it had to go to fill the band from a pool
with more than a handful of backbone families in it, and no lower. At **0.70** only 10 designs clear
both arms and the chai gates, from 4 families; at **0.68**, 18 designs from 6 — neither can deliver
20. At **0.65** there are 30 from 10 families. Going on down to 0.62 would give 42 candidates and
move the worse-ortholog ipTM at pool rank 20 by **0.0006**, from 0.2008 to 0.2014: a longer list and
a lower fold floor, and nothing on the axis the band is ranked on.

**The human-minus-mouse difference is reported per design and is not a selection criterion.** It
gates nothing and orders nothing. Over the delivered 20 it runs **−0.3404 to +0.3836**, positive for
8 designs and negative for 12. **No ortholog preference is claimed, for the band or for any design
in it.** The reason it is not used is measured: the difference reproduces **within** the primary
oracle (ρ = +0.974 between draws) and **not across oracles** (ρ = +0.0533 [−0.0569, +0.1580] with
the second oracle, 8.2 % of what their two reliabilities make attainable, interval containing zero).
A quantity one oracle reproduces and no other confirms is a property of *(design, oracle)*, and
selecting on it would be selecting on the oracle. The reliability figure is now measured on all 325
designs with both orthologs independently re-drawn; it was previously a top-50 figure of +0.9739,
measured on the primary oracle's own winners.

All 20 clear every gate on the human arm: Lys57 approach at most 4.85 Å, binder pLDDT 0.652–0.862,
at least two interfacial histidines. On mouse, binder pLDDT runs 0.651–0.832 and the minimum
interfacial histidine count is 1.

**Both halves of the rule survive an independent re-draw**, with the thresholds written down before
the numbers were looked at. Of the 17 delivered designs that have re-draw data, **17 of 17 still
clear 0.65 on both orthologs** at a different seed, and the worse-ortholog ranking key returns at
**ρ = +0.9447 [+0.7970, +0.9897]** with **17 of 17 staying inside the re-drawn top 20** of the same
pool. Two caveats travel with that, and the deposition states both: **five delivered designs have
their two orthologs closer together than the draw-to-draw spread in the key**, so which one is the
worse is not established for them; and a key that reproduces is not a key that discriminates —
eleven of the twenty sit inside **0.0467** on it.

**The second oracle was a demotion gate when the top 50 was built, and it is relaxed here.** The
rule pre-registered for this round applies the *same four gates* on the Boltz-2 side and demotes any
design that clears the primary oracle's gates but fails one of Boltz-2's. **Of the 148, 95 clear
both and 53 were demoted** — 31 on Boltz-2's binder-pLDDT gate, 15 on its interfacial-histidine
gate, 4 on its Lys57 gate, 3 on two of them. That demotion built the top 50, which is the top 50 of
the **95**. **It does not gate this band:** `boltz_state` is carried as a reported column for every
design, and **three delivered designs are ones Boltz-2 demotes** — `AMBRA_T2_micro_03`,
`AMBRA_T2_micro_09` and `AMBRA_T2_micro_11`. Every Boltz-2 figure for all three is in
`metrics_full.csv`.

It was relaxed rather than the band shrunk because the oracles' disagreement is on the **binding**
axis — where the cross-oracle agreement is a single-digit percentage of attainable with an interval
containing zero — while the floor that decides membership is on the **foldedness** axis, where they
demonstrably agree (ρ = +0.33 to +0.69, all intervals excluding zero) and agree *more* on better
models. It does not follow that the second oracle's opinion is worthless, which is why it is still
reported design by design and why the three designs it demotes are named here.

**Four of the 34 designs clearing the fold floor fail a primary-oracle gate**, all four on the
two-interfacial-histidine membership bar. None of them would have entered the band: on the
worse-ortholog key they would rank 21, 25, 33 and 34.

**The evidence against ranking on interface confidence was not withdrawn, and it stands against
this band.** Over 100 design-species pairs of the previous round the binder's pair-interface pTM
tracks **how confidently the binder folded** (r = +0.634) and not the engagement it is supposed to
stand for; its partial correlation with the measured histidine distance, controlling for binder
pTM, moved from +0.048 at n = 78 to −0.155 at n = 100. On *this* round's 325 designs the same
pattern is visible from the other side: ρ(interface ipTM, binder pLDDT) = **+0.714** and ρ(interface
ipTM, within-oracle pose spread) = **−0.661**. The ordering that produced this band is therefore
**largely a foldedness-and-rigidity ordering**, and should be read that way.

**The mouse arm selects, because the objective is that both orthologs are bound.** The primary
oracle's mouse pass covers all 325 candidates and enters the rule twice: the fold floor must be
cleared on the mouse arm as well as the human one, and the ranking key is the **worse** of the two
orthologs' interface ipTM. Where the two are reported together the worse one is given, never an
average — a design that works on one ortholog and not the other is not cross-reactive, and an
average hides exactly that, which is why the band is ranked on the worse one rather than merely
reporting it. The worse ortholog is mouse for 8 of the 20 and human for 12; for **five** designs
the two arms are closer together than the measurement's own draw-to-draw spread, so which one is
worse is **not established** and those five are marked in the band table rather than printed with a
letter that reads as a result.

## What this submission does not claim

**No design in this target has been tested experimentally.** There are no binding measurements, no
pH titrations and no expression data. Every number in `metrics_full.csv` and in each `metrics.json`
is a property of a **structure prediction**.

**It is a set of 20, not a ranked 20.** The rule reproduces: all 17 delivered designs with re-draw
data still clear the 0.65 floor on both orthologs at a different seed, and the worse-ortholog key
returns at ρ = +0.9447 with 17 of 17 staying inside the re-drawn top 20. But **reproducing is not
discriminating**: eleven of the twenty sit inside **0.0467** on the key, and the first design cut
from the pool is **0.0060** below the lowest delivered one. `submission_rank` exists because the
upload form reads a ranking from the top row down; it is the worse-ortholog interface ipTM from the
primary oracle's first draw, and nothing else.

**A reproducible ranking is not evidence of quality.** ρ(primary-oracle interface ipTM,
cross-redraw binder pose RMSD) = **−0.600** [−0.790, −0.338], n = 50: the designs the ordering likes
are the designs whose pose reproduces. Reproducibility is the question that was asked and answered;
"these bind" is not.

**Three oracles were run, and they disagree about binding.** At n = 50 all three pairwise interface
ipTM correlations have confidence intervals containing zero, while all three pairwise binder-pLDDT
correlations exclude it. The three agree about folding and no two of them agree about binding; the
numbers are in [`DESIGN_STRATEGY.md`](DESIGN_STRATEGY.md) §5 and
[`docs/methods_micro.md`](docs/methods_micro.md) §9. Consensus was sought and not found.

**Unaided engagement of the epitope has not been demonstrated.** On folds of the *previous* round
carried out with the epitope restraint removed entirely, the five designs that have such data miss
Lys57 by **6.5 to 17.7 Å**, and their interface confidence collapses from 0.10–0.42 to 0.078–0.138.
A wider restraint-free check over 900 models finds the binder on the epitope — within 8 Å of both
lysines in 33 of 36 systems by the primary oracle — while the *designed* two-histidine arrangement
appears in 4 of 36 by the primary oracle and 0 of 36 by the second. **The delivered band has no
restraint-free arm of its own.** The binders find the face; they do not yet reproduce the
arrangement unaided.

**There is a null control, and it is not flattering.** In the previous round the binder was
typically closer to a lysine the design never named than to the designed pair (4.57 Å against
11.11 Å). Lys57 ranks second of the six lysines of the human protomer in both oracles independently,
against a chance expectation of 3.5, and the second designed lysine ranks fourth. There is a weak,
reproducible preference for the Lys57 face and none for the second site — which is what the Lys104
distances on this band say too.

**The predicted pKa axis does not support the mechanism on this band.** Over the 20, the best
surface-histidine drift runs **−1.39 to +0.68** with a median of **−0.27**, and only **2 of 20** are
positive. The axis is reported with its limitation in front of it
([`docs/metrics.md`](docs/metrics.md)) and it is not evidence of a pH switch in either direction.

## Numbering

The construct folded in every prediction here is the **149-residue** protomer of the human ortholog
and the **148-residue** protomer of the mouse one, assembled as chains A/B/C with the binder as chain
D. `Lys57` and `Lys104` (human) / `Lys103` (mouse) are positions in those constructs; the exact
sequences are in [`docs/methods_micro.md`](docs/methods_micro.md) §1.

**The organisers' own Target-2 construct is still not established here.** We could not find its
accession or residue range in the documents available to us, so no offset between it and the 149-mer
folded here is given — there is no such figure to give, and we would rather leave it absent than
state a guess. Everything in this directory is in construct-local numbering so that an offset can be
applied later without re-deriving anything.

## What each design directory contains

One directory per delivered design, `micro/AMBRA_T2_micro_01` … `micro/AMBRA_T2_micro_20`, plus
`micro/AMBRA_T2_micro_21` … `micro/AMBRA_T2_micro_30` for the ten designs that are documented and
**not submitted** (below), each holding exactly:

| file | what it is |
|---|---|
| `human_model_0.cif` … `human_model_4.cif` | the five primary-oracle models of the human complex that every human figure for this design is a median or a count over |
| `mouse_model_0.cif` … `mouse_model_4.cif` | the same five for the mouse complex |
| `restraints.csv` | the restraint file as given to the oracle — one row, the 8 Å pocket on Lys57 |
| `sequence.fasta` | the binder sequence under its deposited name |
| `metrics.json` | every number quoted for that design, with the same field names as `metrics_full.csv` |

**There is no "selected model", on purpose.** Nothing here is ranked on a best model: every figure
is a median or a count over the five, because the primary oracle is nondeterministic on this system
and the best of *n* draws is a property of *n*. A `selected.cif` would invite exactly the reading
this band cannot support.

**Ten designs are documented and not submitted.** `AMBRA_T2_micro_21` through
`AMBRA_T2_micro_30` each clear every selection criterion — the 0.65 fold floor on both orthologs
and every primary-oracle gate — and are absent from `submission.csv` only because the qualifying
pool holds 30 designs and the band delivers 20. They were cut on the ranking key, and the cut is
narrow: the first design below the line is at worse-ortholog interface ipTM **0.1948** against
**0.2008** for the lowest-ranked delivered design. In `metrics_full.csv` each carries a `status`
saying so and **no** `submission_rank`.

**A blank cell in `metrics_full.csv` means *not measured for this design*,** never zero and never
false. The re-draw columns, the cross-redraw pose column and the three "in its own oracle's top 20"
columns exist for the 50-design replicate pool only, and three delivered designs sit outside it.

**The second and third oracles' coordinates are not deposited**, only their per-design numbers in
`metrics_full.csv`. Depositing them would have roughly tripled the size of this directory, and every
cross-oracle statement in these documents is a population figure rather than a per-model one. The
primary oracle's human and mouse models are deposited in full, so the columns the band was cut on
can be recomputed from the files here.

The spread across models is included on purpose. The primary oracle is nondeterministic on this
system — the same sequence and seed can give poses about 9 Å apart — so a single predicted complex is
one draw, and this campaign has already had a ranking overturned by paying for more draws.
