# Target 3 — design strategy

**De novo GLP-1R agonists — AMBRA group, Chino lab, Department of Chemical Sciences, University of
Naples Federico II.**

Target: the glucagon-like peptide-1 receptor (UniProt **P43220**), a class-B GPCR, modelled as a
409-residue chain against the active-state reference **6X18**.

**Twenty designs in two bands:** ten disulfide-cyclised peptides of 12–39 residues designed in this
group (**micro**, ranks 1–10), and ten 140-residue de novo miniproteins from a collaborating
RFdiffusion3 + ProteinMPNN pipeline (**mini**, ranks 11–20).

> **These are predictions. None of them has been tested.** There is no binding assay, no cAMP or
> β-arrestin readout, no expression and no synthesis anywhere in this entry. Two of the columns we
> report have names that suggest a pharmacological claim — a TM6 "active-like" call and an ECL2
> "canonical" engagement family — and §4 explains why neither is one.

---

## 1. Two answers to the same question, deliberately kept apart

A class-B GPCR agonist works by inserting a peptide N-terminus into the receptor core. There are
two obvious ways to attempt that de novo, and this entry does both rather than choosing:

**The mini band borrows the thing that is known to work.** Its first ten residues are a variant
of the natural GLP-1 / exendin-4 N-terminal decapeptide, restrained to a consensus of verified
agonists — though not GLP-1's own nine-residue N-terminus, which the deposition platform's
novelty check rejects as a known binder fragment and which this band was re-selected to avoid. The remaining 130 residues are a designed four-helix bundle whose job is to
present that anchor. The question it asks is: *can a de novo scaffold hold a known pharmacophore in
the right place?* It is the lower-risk arm, and it is honest about what it borrows — about 7 % of
each chain is natural sequence.

**The micro band borrows nothing.** It is a 12-residue disulfide macrocycle, designed from scratch,
with no sequence relationship to GLP-1, exendin-4 or any deposited agonist. The question it asks is
harder: *can something an order of magnitude smaller than the native peptide reach the same place
at all?* Six of the ten are that macrocycle extended by a 27-residue tail; two are the cycle plus a
short flank; two are the bare cycle.

The two bands are **not interleaved into one ranking**, and this is the single most important thing
to know about the submitted order. Their confidence numbers come from different oracles, run in
different conditions, on different machines, and were never on the same scale. Merging them would
be arithmetic on incomparable numbers, and the result would look more precise than anything we
measured. Micro occupies ranks 1–10 and mini ranks 11–20 because the form reads a ranking from the
top row down — **not** because every micro design is a better candidate than every mini design. On
their own oracles' numbers the mini designs score higher, and they are longer, which raises
interface confidence on these models by itself.

## 2. How the micro band was designed

Forward-folding hallucination: **chai-1 is a structure oracle, not a gradient target.** An
outer **evolutionary algorithm** proposes sequences, chai folds each as a complex with the 409-residue receptor, and a scalar
objective over the fold's own confidence terms decides what survives. Four waves ran, differing in
construct, in which parent macrocycle they extend and from which terminus.

The disulfide is declared to chai as a **covalent SG–SG bond**, not as a distance preference.

## 3. The one methodological decision that changed the band

The search also declared an **8 Å pocket restraint** on receptor K174 and R357. A restraint is an
instruction: with it in place, *"the peptide binds the pocket"* is partly something we told the
model rather than something it predicted.

We pre-registered a test of whether that mattered — stating the prediction and the falsifying
number before running it: *if the restraint carries no part of the ranking, refolding every
candidate with the disulfide alone will leave the ordering essentially unchanged, ρ ≥ 0.9, with no
design losing more than 0.1 interface pTM.*

**It was falsified.** The two conditions correlate at **ρ = +0.538** over 48 candidates, and **7 of
48** designs collapse when the pocket is removed. On some designs the restraint was carrying the
binding event itself.

So the band was re-cut and is ranked on the **disulfide-only** folds, and those are the structures
deposited. Both numbers and their difference are in `metrics_full.csv`, so the condition always
travels with the score. For the ten deposited, the restraint was worth a mean of +0.017 interface
pTM and at most +0.089.

A second consequence follows: part of what holds the macrocycle shut in a restrained fold is the
declared bond. So the ring is **measured on the shipped structures** — 45 of 50 chai models close
it — rather than assumed, and the three designs that close it in fewer than 5 of 5 carry a flag.

## 4. What our activation readouts can and cannot establish

Two measures describe how the peptide sits in the receptor. **Neither is evidence of agonism**, and
we would rather say so than let the names imply otherwise.

- **TM6 two-state.** Cuts frozen from nine deposited GLP-1R structures, 9/9 under leave-one-out. It
  calls 40 of 40 measured models in this band active-like. On a 110-structure pharmacology panel
  the same measure scores agonists, antagonists **and a composition-matched scramble** at 10/10. It
  reports that the model built the active bundle once anything was in the pocket. It ranks nothing.
- **ECL2+TM5 engagement family.** Two families learned on that panel (silhouette 0.450); family 0
  is where the canonical N-terminal-into-the-core agonists fall. On the panel the split does **not**
  separate agonists from antagonists (between-minus-within −0.002, CI [−0.180, +0.511]). It is a
  **binding-mode prior, not a validated classifier**, and it is used only as a **quota** — to
  guarantee the band is not composed entirely of designs engaging some other way. Five of the ten
  submitted micro designs are canonical on it.

If either of these were a validated efficacy predictor we would rank on it. They are not, so we do
not.

## 5. How we chose what to rank on

Before picking a ranking axis we measured how reproducible each candidate axis is, by refolding the
same sequences from a different seed:

| axis | ρ across a seed change |
|---|---|
| chai interface pTM | **+0.976** |
| reference-free pose dispersion | +0.524 |
| conserved interface-contact count | +0.210 |

**Never gate on an axis noisier than the one you distrust.** Pose dispersion and contact counts are
reported and neither gates nor ranks. An earlier draft of this band *did* gate on pose dispersion;
that draft was withdrawn when this measurement came in.

On top of the axis, five gates: a ring gate, a near-duplicate collapse on fractional Hamming
distance, a **substring-containment** check, a lineage cap of two per wave/arm/seed, and a
length-stratified quota (2 × 12-mer, 2 × 15-mer, 6 × others), because interface confidence rises
with chain length and a pooled top-ten would be a length ranking.

The substring check exists because a previous upload was flagged for it: one of our 12-mers is
embedded verbatim at position 28 of two of our 39-mers, so depositing both would submit a design
and its own substructure. Equal-length Hamming comparison cannot see that.

**The band is a set, not a sharp order.** It spans 0.699 to 0.820 on the ranking axis while the
measurement's own fold-to-fold spread is of order 0.001–0.007.

## 6. Three oracles, all given an alignment

| | condition | role |
|---|---|---|
| chai-1 | disulfide restraint only | the ranking oracle |
| Boltz-2 2.2.1 | disulfide bond constraint, with MSA | a check |
| Protenix-v2 | **unrestrained**, with MSA | a check |

chai takes its evolutionary signal from ESM-2 embeddings; the other two take theirs from an
alignment. Every Boltz and Protenix number we had measured on this target before this deposition
was single-sequence — which switched off the two models that need an alignment while chai kept its
own pathway. That is not a comparison, and we corrected it for the peptide band: every Boltz and
Protenix number for the ten peptides was produced with alignments from a local UniRef90 database
(receptor depth 2,280; **depth 1 for every binder**, because a de novo 12-mer has no homologues).
The binder sequences never left the machine. The miniproteins' Boltz-2 predictions were made by the
collaborating pipeline with its own receptor alignment (9,929 sequences) and a single-sequence
binder.

Giving Boltz the alignment **removed a failure mode rather than raising a ceiling**: three of the
ten had collapsed single-sequence and recovered; on the other seven ipTM moved a median +0.002.

**Protenix is unrestrained because it cannot be restrained** — its constraint embedders are
disabled in the released configuration and the checkpoint carries no constraint tensors. It was
asked a different question, and its numbers are not averaged with the others'.

**The three disagree about binding.** Over the ten deposited, Spearman ρ between chai's ordering
and Boltz ipTM is +0.055, Protenix ipTM +0.188, Boltz ipSAE +0.370 (n = 10). Each oracle reproduces
*its own* ordering across a seed change far better than it reproduces another's. We rank on one and
report the others as checks, never as votes: a blended score would average the disagreement away
and produce a number none of them computed.

## 7. What we are not claiming

- That any of these peptides is an agonist, a partial agonist, or a binder.
- That the submitted order reflects a measured difference in quality between adjacent entries.
- That the micro band outranks the mini band, or the reverse.
- That the receptor-conformation measures predict efficacy.
- That the 27-residue extensions on the 39-mers are designed interfaces; they are extensions of a
  delivered macrocycle, and their contribution has not been separated from the ring's.

## 8. What would falsify this entry cheaply

The micro band is the informative arm precisely because it borrows nothing: a binding measurement
on the two 12-mers settles, in one experiment, whether a 12-residue macrocycle can engage this
receptor's orthosteric site at all. A flat result there is a clean negative about the construct,
not an unexplained failure. The mini band's anchor is already known to engage; what it tests is
whether a de novo scaffold presents it, and a functional readout separates "the scaffold works"
from "the anchor works on its own".

---

Methods: [`docs/methods_micro.md`](docs/methods_micro.md),
[`docs/methods_mini.md`](docs/methods_mini.md). Column definitions:
[`docs/metrics.md`](docs/metrics.md). Every number quoted here can be recomputed from the
structures and metrics deposited under `micro/` and `mini/`.
