# Text for the submission form's description box

*(Paste the block below as-is. The attachable file is `Target_3/DESIGN_STRATEGY.md` in the
repository.)*

---

**De novo GLP-1R agonists — AMBRA group, Chino lab, University of Naples Federico II**

**Twenty designs in two bands, deposited as consecutive blocks under one ranking.** Ranks 1–10 are
**disulfide-cyclised peptides of 12, 15 and 39 residues**, designed de novo in our group with no
sequence relationship to GLP-1, exendin-4 or any deposited agonist. Ranks 11–20 are **140-residue
de novo miniproteins** from a collaborating RFdiffusion3 + ProteinMPNN pipeline, each presenting
a variant of the natural GLP-1/exendin-4 N-terminal decapeptide — about 7 % of the chain — on a
designed four-helix bundle. None of them carries GLP-1's own nine-residue N-terminus.

**The block boundary is not a claim.** The two bands were produced by different pipelines, scored
by different oracles, in different conditions. Their confidence numbers were never on one scale, so
we did not interleave them; merging would be arithmetic on incomparable numbers. On their own
oracles' numbers the miniproteins score higher, and they are longer, which raises interface
confidence by itself.

**Nothing here has been tested.** No binding assay, no cAMP or β-arrestin readout, no expression,
no synthesis. Every number is a property of a structure prediction.

**Two of our columns have names that sound like pharmacology, and neither is.** A TM6 two-state
measure calls 40 of 40 of our models "active-like" — but on a 110-structure pharmacology panel the
same measure scores agonists, antagonists **and a composition-matched scramble** at 10/10, so it
reports that the model built the active bundle once anything was in the pocket. An ECL2+TM5
engagement family (silhouette 0.450) marks the canonical N-terminal-into-the-core binding mode, and
on that same panel it does **not** separate agonists from antagonists (between-minus-within
−0.002, CI [−0.180, +0.511]). We use it as a quota, never as a score. Five of our ten peptides are
canonical on it.

**The cyclic band is ranked without the restraint it was designed under, and that changed it.** The
design search declared an 8 Å pocket restraint on receptor K174 and R357. A restraint is an
instruction, so we pre-registered a test: if it carried no part of the ranking, refolding every
candidate with the disulfide alone would leave the order unchanged at ρ ≥ 0.9. **It was falsified
— ρ = +0.538 over 48 candidates, and 7 of 48 collapse without the pocket.** We re-cut the band on
the disulfide-only folds, deposited those structures, and kept both numbers and their difference in
the metric table so the condition always travels with the score. For the ten submitted, the
restraint was worth a mean of +0.017 interface pTM and at most +0.089.

**We chose the ranking axis by measuring which axis reproduces.** Refolding the same sequences from
a different seed, chai interface pTM returns at ρ = +0.976, reference-free pose dispersion at
+0.524 and conserved interface-contact counts at +0.210. We rank on the first and gate on neither
of the others: gating on a noisier measurement than the one you distrust is not a safeguard. An
earlier draft of this band did gate on pose dispersion and was withdrawn when that number came in.

**The declared macrocycle is measured, not assumed.** 45 of 50 predicted models close the declared
disulfide at SG–SG ≤ 2.5 Å; three designs close it in 3 or 4 models of 5 and carry a flag. Our
build script refuses any row whose declared cysteine positions are not two distinct cysteines of
its own sequence.

**Three oracles, all given an alignment, and they disagree.** chai-1 takes its evolutionary signal
from ESM-2 embeddings; Boltz-2 and Protenix-v2 take theirs from an MSA. Every Boltz and Protenix
number we had on our peptides was previously single-sequence, which switched those two off while
chai kept its own pathway; we rebuilt them with alignments from a local UniRef90 database
(receptor depth 2,280; depth 1 for every binder, because a de novo 12-mer has no homologues). The
miniproteins' Boltz-2 numbers are their pipeline's own: a 9,929-sequence receptor alignment and a
single-sequence binder. Protenix is **unrestrained** — its constraint embedders are disabled in the
released configuration and the checkpoint carries no constraint tensors — so it was asked a
different question and is not averaged with the others. Over the ten peptides, Spearman ρ between
chai's order and Boltz ipTM is +0.055, Protenix ipTM +0.188, Boltz ipSAE +0.370, while each oracle
reproduces its own order across a seed change at +0.87 or better. **We rank on one oracle and report
the others as checks, never as votes.**

**The rank is an order on a set, not a gradient.** The peptide band spans 0.699 to 0.820 on the
ranking axis while the measurement's own fold-to-fold spread is 0.001–0.007. `submission_rank`
exists because the form reads a ranking from the top row down.

**Every design directory ships what its numbers were read off**: for each peptide, fifteen
structures — five chai-1 (disulfide only), five Boltz-2 (with MSA) and five Protenix-v2
(unrestrained, with MSA) — plus the score arrays, the confidence records and the restraint file as
the oracle received it. For each miniprotein, the three predictions its pipeline made: bound to the
receptor, alone, and against a copy of itself (a self-association check, where a **low** interface
score is the good outcome; ours run 0.12–0.47).

**What would falsify this entry cheaply.** The cyclic band borrows nothing, so a binding
measurement on either 12-mer settles in one experiment whether a 12-residue macrocycle can engage
this receptor's orthosteric site at all; a flat result is a clean negative about the construct
rather than an unexplained failure. The miniproteins' anchor is already known to engage, so what
they test is whether a de novo scaffold presents it — and a functional readout separates "the
scaffold works" from "the anchor works on its own".

**No design here has been tested experimentally.** Every number is a property of a structure
prediction. The design engine for the cyclic band is the subject of a manuscript in preparation and
is described in principle ahead of publication; every sequence, every predicted structure — fifteen
per cyclic design, three per miniprotein — every per-model measurement, every restraint file as the
oracle received it, and the scripts that build the submission from them are public at
**github.com/piripocchio8/AMBRALab_Chino_Challenge2026**, under `Target_3/`.
