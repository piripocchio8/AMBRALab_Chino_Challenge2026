# Design strategy — AMBRA group, Chino lab (University of Naples Federico II)

**Challenge 1, EGFR domain III. Twenty designs: 8 micro (39 aa), 4 mini (94–99 aa), 8 large
(101–129 aa).**

Repository (structures, metrics, methods, restraints):
`github.com/piripocchio8/AMBRALab_Chino_Challenge2026`

---

## 1. The objective we actually optimised

Not affinity. **pH selectivity** — binding that differs between the acidic tumour microenvironment
(~6.5) and blood pH (7.4) — built on a histidine of the target itself, whose imidazole is protonated
at the lower pH and neutral at the higher one.

We submit **two independent series against two different histidines by two different chemistries**,
from pipelines that share no code. Neither can take the other down with it.

| | micro | mini and large |
|---|---|---|
| target histidine | **His358** (UniProt P00533; mature His334) | **His433** (mature His409) |
| mechanism | binder main-chain carbonyls **accept** from the protonated imidazolium | salt bridge from the imidazolium to an engineered carboxylate, plus a reciprocal His–Asp anchor |
| size | 39 aa, disulfide-cyclised peptides | 94–129 aa scaffolded proteins |
| route | sequence optimisation against a structure oracle + interaction-preserving inverse folding | RFdiffusion3 → soluble ProteinMPNN → Boltz-2 validation |

The two sites are 75 residues apart. **His358 is the harder of the two**: the double-carbonyl
arrangement occurs in about **0.455 % of histidines in the PDB** (1 in 220), roughly six times rarer
than the carboxylate-bridged arrangement the scaffolded series uses.

## 2. The micro series — a different route, and what it reached

Backbones were not diffused and threaded. Candidate sequences were optimised **directly against the
structure oracle** by a population-based evolutionary algorithm, then refined by
**interaction-preserving inverse folding with CARBonAra**: the specific contacts worth keeping —
hydrogen bonds, charge pairs, aromatic stacking, everything coordinated to the histidine — were held
fixed while the rest of the binder was repacked. Plain hydrophobic contact was deliberately *not*
protected. The leading designs come from that refinement step, not from the search: it recovered
compact backbones the search had found but could not encode in a sequence.

**What this reached that the standard pipeline did not.** The scaffolded route in this same
submission produced nothing below 60 residues and could not aim at His358. The micro designs are
**39 residues** and engage **His358**. Both pipelines were run against the same protein; only one
could address this site at this size. The band also held two **12-residue** cyclic peptides until
they were withdrawn (§4a).

> **A note on disclosure.** The design engine is the subject of a manuscript in preparation and is
> described here in principle rather than in reproducible detail, **ahead of publication**. Nothing
> needed to *evaluate* these designs is withheld: sequences, predicted structures, every per-model
> measurement, the selection gates and their thresholds, the restraint files and the command lines are all in
> the repository, and every design excluded from the band is named with the gate it failed in
> `docs/methods_micro.md` §10. What is held back is how
> candidate sequences were *generated*, not how they were *judged*. We are glad to discuss the method
> in confidence with the organisers.


### Why this histidine, and not the other one

The submission engages two histidines, and the choice of **His358** for the micro series was made for
a reason worth stating: it sits next to a carboxylate the target already provides. **Glu11** (local
numbering) is adjacent to the conserved Asn355–Lys357–His358 cluster and is **identical in position in
both orthologs**, so a binder that holds that cluster can also hold Glu11 against the protonated
His358 — the target supplies its own charge partner for the switch.

That is the same physics the scaffolded series engineers onto the binder (§2b), reached from the
opposite side: there a carboxylate is built into the design to meet the target's histidine; here the
target's own carboxylate is recruited to meet it. His433 has no equivalent partner in reach, which is
why the micro series went to His358 rather than following the scaffolded series to the same site.

Glu11 was deliberately **never declared as a restraint** — the declared contacts are Asn355, Lys357
and His358 — so whether the pair forms is the binder's doing. It is measured, not enforced, and it
varies from **2.9 to 18.1 Å across the shortlist** depending on the binder: the binder decides it. The
leading design holds it under 4 Å in **76 % of human and 100 % of mouse** models. It is scored.

## 2b. The mini and large series — a reciprocal, doubly protonation-dependent interface

**The idea, which is the point of this series.** Most pH-switch designs hang the whole effect on one
titratable contact. These use **two His–carboxylate salt bridges pointing in opposite directions**,
both of which strengthen as the pH falls:

| | the target brings | the binder brings | behaviour |
|---|---|---|---|
| **switch pair** | **His433**, protonated at pH 6.5 | an engineered **Asp/Glu** | salt bridge forms when the target's histidine is protonated, lost by pH 7.4 |
| **anchor pair** | **Asp460** | an engineered **His** | salt bridge forms when the *binder's own* histidine is protonated |

One histidine is borrowed from the target; the other is supplied by the binder and points the other
way. Because **both** histidines titrate across the same window, the two bridges switch on together
going from blood pH to tumour pH — the protonation dependence is doubled rather than carried by a
single contact, and the second pair also fixes the register of the interface rather than merely
adding affinity.

That makes the binder's anchor histidine a **design variable, not a passive clamp**: its pKa is set
by the electrostatic environment built around it. The campaign demonstrates this rather than
asserting it — when buried cysteines were redesigned away, substituting an apolar residue for a
serine that sits in that network costs **1.8–4.9 REU** of pH-switch ΔΔG (`pHsel-07` falls from +5.98
to +1.06), even though the swap is free on every interface metric. Selectivity and affinity are
separable here, and the design optimises the former explicitly.



**How they were built.** Motif-scaffolded RFdiffusion3 backbones on nine enumerated anchor-pair
geometries drawn from PDB His–carboxylate contacts, soluble ProteinMPNN sequences, Boltz-2 co-folding
with ipSAE. Two later stages changed what the series is:

- **Composition-first redesign (round 5).** Eight of an earlier fourteen sat outside the amino-acid
  composition envelope of experimentally confirmed sub-µM α-helical EGFR binders. Round 5 enforces
  that envelope (alanine ≤ 0.104, hydrophobic AVILMFWY 0.329–0.42, net charge −19.3…−5.0,
  pI 4.60–5.00) **before any folding** rather than resurfacing designs afterwards; an alanine bias of
  −2.0 moved the gate pass rate from 4.7 % to 49.2 %. **11 of the 12 submitted sit inside it.**
- **Cysteine removal.** 18 unpaired buried cysteines across 12 designs, redesigned at those positions
  only and accepted only where the design was no worse on every axis — including the pH switch, which
  is where the result above came from. **All 12 ship with zero free thiols.**

**Acceptance is strict.** Both designed bridges must re-form **with no restraint, in two independent
seeds** — the salt bridge replicates across folds at only ρ = +0.36, so a bridge seen once
unconstrained is not evidence — with ipSAE ≥ 0.50 and binder pLDDT ≥ 0.85 on the *worst* seed, the
fold retained within 2.0 Å, and bridge geometry inside a native envelope built from 39 crystal and
AlphaFold His–carboxylate contacts. Of 98 founders, **84 fail on bridge-geometry realism alone**:
interface confidence and fold stability are effectively free at that stage, and native-like bridge
*geometry* is the scarce property.

Measured on the submitted twelve: ipSAE **0.833–0.912 human / 0.794–0.891 mouse**, binder pLDDT
**0.915–0.965**, His433 bridge **2.64–3.34 Å**, PyRosetta pH-mode ΔΔG for 7 of them
(**0.47–5.98 REU** favouring the acidic form). Eight of the twelve come from rounds 4–5.

One honest note recorded by that work: **a `force: true` co-folding contact constraint does not mean
the contact forms** — in round 4 the worst designed bridge had a median of 16.7 Å across constrained
folds with both constraints present and verified. Bridge thresholds must be calibrated on the current
round's distribution.

**The two series together give the pH switch a control, and it works.** Running propka on a
scaffolded complex and on the same coordinates with the binder deleted: the target's His433 goes from
pKa **6.26 free to 6.89 bound** — 36.5 % → 71.1 % protonated at pH 6.5 against 6.8 % → 23.6 % at
pH 7.4, widening the selectivity window from 0.298 to 0.474. The term breakdown shows the binder's
engineered carboxylate contributing **+1.60 (H-bond) and +1.52 (coulombic) against −2.73 of
desolvation** at 100 % burial. The micro series' neutral main-chain carbonyls contribute +0.44 and
+0.55 against −1.28 and come out negative. Same tool, same protein, opposite sign, and the only
difference is whether the acceptor carries a charge — which is why the micro series' pH evidence is
read from geometry while the scaffolded series' is supported by propka directly. It also confirms the
free target histidine titrates normally (6.8 % protonated at pH 7.4), so there is a real window to
exploit rather than a histidine already saturated before the binder arrives.

## 3. Why these peptides are worth bench time

**Cheap and fast to falsify, and well inside the expression regime.** These are made the same way as
every other entry — cell-free from synthesised DNA — and that favours them: in this competition's own
800-design EGFR dataset, length is the strongest *negative* term for expression and the 60–134 aa band
expressed 143/144. Short, disulfide-cyclised, low-alanine designs are the easy case for a PURE system
carrying DsbC and a glutathione buffer. The pH question is then answered by one binding assay in two
buffers.

**The length risk, stated plainly, because it comes from our own analysis of their data.** On that
same 800-design EGFR set the hit rate is 3.4 % at ≤30 aa and **0 % at 31–45 aa**, against 34.7 % at
200+ aa — and **all eight of these sit at 39 aa**, in the empty bin. That is worse than we intended:
the band carried two 12-residue peptides in the favourable bin until they were withdrawn (§4a). We
submit the eight anyway, for three reasons. That prior comes from campaigns optimising **affinity**;
this one optimises **selectivity**, and a modest binder with a real pH window is what the challenge
asks for. The site forces the size: the scaffolded route in this same submission could not reach
His358 at all, so there is no 200-aa version of this experiment to compare against. And the bins are
small — a 0 % bin of a few dozen designs is not a law — so the honest reading is that **this size
regime is close to untested at this target**, which is part of why eight cheap peptides are worth a
plate.

## 4a. Two designs withdrawn, and why

The submitted band is **not** the band our measurements chose. Two 12-residue cyclic peptides —
`micro_07__open__v0` and `micro_08__open__v6` — passed every selection gate and were withdrawn
because the competition's **novelty check timed out on both**, twice, and could not be completed,
while all eighteen longer designs scored (one at 4/4, six at 3/4). We replaced them with the next two
eligible designs rather than submit entries that carry no novelty score.

The cause is almost certainly length rather than sequence. That pipeline predicts a structure and
measures similarity with TM-align, and TM-score's normalisation

&nbsp;&nbsp;&nbsp;&nbsp;*d*₀ = 1.24·∛(*L* − 15) − 1.8

takes the cube root of a **negative** number for any chain shorter than 15 residues and stays
non-positive up to 18. At *L* = 12 it is undefined; at *L* = 39, 94 and 129 — every design that
scored — it is well behaved. In C, `pow(-3, 1./3)` is NaN, and NaN makes every comparison false,
which in an iterative superposition search gives a hang rather than an error. We could not reproduce
the hang locally against a small database, so this is the leading explanation and **not** a proven
one.

**What it cost, stated rather than absorbed.** We lost both designs in the only length bin with a
non-zero hit rate; both replacements came from the dominant lineage, taking it from four of eight to
**six of eight**; and the band went from one recorded waiver to **three**. The withdrawn designs
remain in this repository with all of their measurements, and we would rather they were tested.

**The mechanism predicts a direction, not just an affinity.** Neutral imidazole carries one N–H; the
other ring nitrogen holds a lone pair. A geometry in which **both** ring nitrogens donate to acceptors
is only constructible if the ring is the **imidazolium**. That commits us to a sign — tighter at
acidic pH — and a flat or inverted result refutes the design hypothesis outright, which is more
informative than an unexplained binder.

**They were never tuned on the sequence they are scored against.** The campaign ran against the
**mouse** ortholog; the human challenge sequence was used only afterwards to evaluate what already
existed, with no re-optimisation. Their behaviour on human EGFR is transfer, not a fit to the
evaluation target — and the same molecules are directly testable in mouse models.

## 4. How the eight were selected

Each design was refolded from scratch until it carried **45 models against human and 30–35 against
mouse**, under its own restraint file so the two numbers mean the same thing — **5,849 predicted
structures** across the campaign. Nothing is ranked on a best model; everything is a rate reported
with its denominator.

Four measurements, each on 0–1, each published beside the total:

| axis | weight | what it asks |
|---|---|---|
| cross-reactivity | 0.30 | interface confidence (ipSAE, binder–target ipTM) and engagement rate, taken from the **lower** of the two species — never the average |
| pH sensitivity | 0.25 | both ring nitrogens engaged; a binder carboxylate on the ring; the target's own Glu11 held in a charge pair with it in both species |
| binding consistency | 0.25 | does it dock in the same place on every refold — the average RMSD between its binder poses, every model superposed on the **target** alone, so the binder's own shape never enters the superposition and what is left is purely where it sits |
| fold consistency | 0.20 | is it one structure, in **both** species, and does the free peptide already hold it |

Gates decide membership before any score is applied. Three of them cannot be waived, because each is
a mechanism failure rather than a weak number: a design **extended in either species**; one whose
binder **lands somewhere different on every refold**, since binding in a different place each time is
not binding; and one holding a **binder lysine or arginine against the imidazolium**, which
destabilises the cation and pushes the histidine's pKa the wrong way — against the design's own
switch. The remaining gates — a floor on how often the designed bond is made on the human target, and
an interface-confidence floor read from the worse species — may be waived to fill a slot, which then
goes to the best-scoring design missing exactly one of them, recorded with which gate and by how much.

The pose measure is deliberately **reference-free**. Deviation from a design's own best pose needs a
reference and flatters a scattered set: when the poses are spread, the best one sits in the middle of
the scatter and every model looks closer to it than the models are to each other. One design reads
5.05 Å to its own best pose and 13.32 Å pairwise, with 2 % of its models within 2 Å of each other. The
pairwise average makes that visible, and the shortlist separates cleanly under it — 1.1–8.9 Å, then a
gap, then 10.4–15.5 Å.

A hydrogen bond is treated as a **direction, not a distance**: 2.5–3.4 Å, within 45° of the in-plane
N–H vector, ≥2.9 Å from every ring carbon, within 1.2 Å of the ring plane. The ring-carbon clause
matters — an early design read 2.75 Å to NE2 while sitting 2.13 Å from ring carbon CE1, a collision a
distance-only test scores as a hydrogen bond.

## 5. Independent validation, including where it disagrees with us

All eight were refolded by **Boltz-2 2.2.1** and **Protenix** (`protenix_base_constraint_v0.5.0` —
the only checkpoint that reads the pocket constraint), given the same two statements, against both
orthologs.

**They agree about the molecule.** The dominant lineage comes back as one conformation from all
three: Boltz fold spread **0.23–0.24 Å** across independent seeds, Protenix 0.21–1.72 Å, the primary
oracle 0.31–0.34 Å. Protenix is confident about the complexes (iPTM up to 0.88).

**They are less convinced about the bond.** The rate at which an acceptor reaches His358 in
hydrogen-bonding geometry falls as you move away from the oracle the designs were optimised against:
primary 0.00–0.60 on human, Boltz 0.10–0.40, Protenix 0.00–0.30. We report this because it is the
honest shape of the evidence: the fold is corroborated three ways, the specific hydrogen bond is
corroborated weakly by one independent model and largely not by the other.

**A predicted pKa shift is reported but deliberately not scored.** propka credits each hydrogen bond
at about half a pKa unit while burial of the histidine costs more than one, so it returns a *negative*
shift for a geometry that cannot exist without the cation. Its own term breakdown on a bidentate
model: desolvation −0.99 → −2.27 as burial goes 24 % → 66 %, against hydrogen-bond terms of +0.44 and
+0.55. The geometry is the evidence; the numbers are published so the judgement can be checked.

## 6. What we are claiming, and what we are not

Every number here is a property of a structure prediction.

What the measurements support: these peptides reproducibly place a binder main-chain carbonyl in
hydrogen-bonding geometry on the target imidazolium, fold to one conformation against both orthologs,
and in the leading case hold that conformation **unaided** (0.37 Å between the free binder and its
bound form) with **equal interface confidence on human and mouse** (ipSAE 0.368 / 0.390).

What they do not support: a sharp switch. The bidentate clamp is rare in the predictions, as the motif
is rare in nature. Expect the pH dependence to be real but modest.

**Six of the eight micro designs share one backbone**, three lineages in all. That is a concentration
risk we state rather than hide, and one the withdrawal in §4a made worse, since both replacements
came from that lineage: it is the only lineage with equal interface confidence on both orthologs and
the only one all three oracles return as a single conformation — but if that backbone is wrong,
three quarters of the band fails together.

---

*AMBRA group, Department of Chemical Sciences, University of Naples Federico II.
marco.chino@unina.it · ambralab@unina.it*
