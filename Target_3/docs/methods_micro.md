# Target 3, MICRO class: methods

Challenge 2026, Target 3 — de novo agonists for the glucagon-like peptide-1 receptor (UniProt
**P43220**), a class-B GPCR. This document covers the **micro** band: ten disulfide-cyclised
peptides of 12, 15 and 39 residues, designed in the XenoDesign1 repository. The mini band is
documented separately in [`methods_mini.md`](methods_mini.md).

> **Everything below is a structure prediction.** No peptide in this band has been synthesised or
> assayed. Where a word like *agonist* or *active* appears, it names what the design was selected
> for or what a geometric measure called, never what was observed.

---

## 1. The target

- **Receptor:** UniProt P43220, modelled as a **409-residue** chain. Two sequence guards are
  asserted before every fold and the job refuses if either fails: residue **174 is K** and residue
  **357 is R**. A silently truncated or mis-numbered receptor would move every restraint and every
  contact label by the same offset, and that has happened on another target in this project.
- **Active-state reference:** **6X18**. Used for the two receptor-conformation measures in §6 and
  as the frame the deposited models are superposed into, never as a design template.
- **Residue numbering** in the contact labels is UniProt numbering; the modelled chain is offset by
  23 from the construct index, and that offset is applied in one place.

## 2. What was designed

A **disulfide-cyclised macrocycle**, optionally extended. The objective was an agonist-like
engagement of the orthosteric pocket: the native agonist drives activation by inserting its
N-terminus into the receptor core, so the design question was whether a small cycle can reach the
same place.

Three constructs came out of the campaign, sharing one macrocycle size:

| construct | ring | what the rest is |
|---|---|---|
| 12-mer | Cys1–Cys12 | nothing — the macrocycle alone |
| 15-mer | Cys4–Cys15 | a three-residue N-terminal flank |
| 39-mer | Cys1–Cys12 or Cys28–Cys39 | a 27-residue extension at the opposite terminus |

The 39-mers are **elongations of delivered 12-mers**, grown N-ward or C-ward from one of three
parent macrocycles (`p1`, `p2`, `p3` in `parent_family`). Because the macrocycle is the same size
throughout, a difference between constructs is about an exocyclic extension, not about ring size.

**No design was seeded from a natural GLP-1R ligand.** The micro band shares no sequence with
GLP-1, exendin-4 or any deposited agonist; it is not a redesign of a natural peptide. (This is the
opposite choice from the mini band, which deliberately borrows the natural N-terminal decapeptide
as an anchor — see [`methods_mini.md`](methods_mini.md).)

## 3. How they were designed

Forward-folding hallucination: **chai-1 is a structure oracle, not a gradient target.** An
outer **evolutionary algorithm** proposes sequences, chai folds each as a complex with the
receptor, and a scalar objective over the fold's own confidence terms decides what
survives. Four waves ran (`t3w1`–`t3w4b`), differing in construct, in which parent they elongate
and in which end they elongate from; the wave and arm are columns in `metrics_full.csv`.

Two restraint rows were declared during the search:

1. the **disulfide**, as a covalent SG–SG bond between the two declared cysteines;
2. a **pocket restraint**, an 8 Å contact at confidence 0.8 from the binder to receptor **K174**
   and **R357**.

Point 2 is the reason for §4.

**The design search's own objective values are not deposited.** The search scores its final
generation on an *anchored* refine, which is systematically higher than a cold re-fold of the same
sequence, so those numbers describe the search rather than the delivered design — and they are not
comparable with the mini band's composite either. Everything the band is ranked on is a **cold**
number, re-measured on the deposited folds.

## 4. The pocket restraint, and why the band is not ranked with it

A restraint is an instruction. With an 8 Å pocket declared on K174 and R357, "the peptide binds the
pocket" is partly something we told the model, and a confidence score computed under that
instruction is not purely a prediction.

**Pre-registered (H8), before the refolds ran:** if the pocket restraint carries no part of the
ranking, then refolding every candidate with the disulfide alone will leave the ordering
essentially unchanged — Spearman ρ ≥ 0.9 against the restrained ordering, with no design losing
more than 0.1 interface pTM.

**Outcome: falsified.** Over the 48 refolded candidates the two conditions correlate at
**ρ = +0.538**, and **7 of 48** designs lose more than 0.1 — they collapse without the pocket. The
restraint was carrying a substantial part of the score, and on some designs it was carrying the
binding event itself.

The band was therefore re-cut on the **disulfide-only** condition. For the ten deposited designs
the restraint was worth a mean of **+0.0174** interface pTM (range −0.012 to +0.089); the one
design where it mattered most, `AMBRA_T3_micro_06`, scores 0.6991 without it and 0.7882 with it.

Both numbers are deposited — `selected_iptm` (the ranking axis, unrestrained pocket) and
`chai_iptm_restrained`, with `restraint_delta` as the difference — so the condition always travels
with the score. **The five chai models in each design directory are the disulfide-only folds**, and
each directory's `restraints.csv` holds exactly one row.

A second consequence is worth stating plainly: part of what holds the macrocycle shut in the
restrained folds is the declared bond, not the sequence. The ring is therefore measured on the
shipped structures (§7) rather than assumed.

## 5. Which axis the band is ranked on, and why that one

Before choosing a ranking axis we measured how reproducible each candidate axis is, by refolding
the same sequences from a different seed and correlating the two orderings:

| axis | ρ across a seed change |
|---|---|
| chai interface pTM | **+0.976** |
| reference-free pose dispersion | +0.524 |
| count of conserved interface contacts | +0.210 |

**Never gate on an axis noisier than the one you distrust.** Pose dispersion and conserved-contact
counts are both reported in `metrics_full.csv` and neither is used as a gate or a rank, because
either would mean letting the least reproducible measurement overrule the most reproducible one.
An earlier draft of this band did gate on pose dispersion; that draft was wrong and the measurement
above is why it was withdrawn.

The ranking axis is **chai interface pTM on the disulfide-only fold**, cold, meaned over the folds
available for that design (`chai_n_folds`, with `chai_iptm_spread` beside it — a mean over five
folds and a single draw are not the same measurement).

### The ranking rule, in full

Applied to the 44-design pool in `metrics_full.csv`:

1. **Ring gate.** A design whose declared disulfide never closes in any shipped model is out.
2. **Near-duplicate collapse.** Designs within a fractional Hamming distance of 8/39 of one another
   are collapsed to one. Where two designs are closer than that, the higher score wins only if the
   gap exceeds ten times the measurement error (0.02 ipTM); otherwise the design with more folds
   behind its number wins, because evidence beats a hair's-breadth lead.
3. **Substring containment.** A design that is a substring of another candidate is not deposited
   alongside it. This gate exists because a previous upload was flagged: `CEWPTPDGFLSC` is the
   macrocycle embedded at position 28 of two 39-mers, and submitting both submits a design and its
   own substructure. Equal-length Hamming comparison is blind to this; the check is explicit.
4. **Lineage cap.** At most two designs per lineage, where lineage is wave + arm + seed. A `parent`
   field is used only when it names a real design — on the wave-4 cells it is a pocket-family tag
   (`p1`/`p2`/`p3`), and treating it as a parent once merged every design at the same site into one
   lineage.
5. **Length-stratified quota.** 2 × 12-mer, 2 × 15-mer, 6 × others. Interface confidence rises with
   chain length on these models, so a pooled top-10 would be a length ranking.
6. **Canonical quota.** Places are guaranteed to designs that are fam-0 on the ECL2+TM5 measure in
   at least 3 of 5 models (§6), so the band is not entirely designs that engage some other way.
7. The rest by `selected_iptm`, descending.

**This is a set, not a sharp order.** The band spans 0.6991 to 0.8201 on the ranking axis and the
measurement's own fold-to-fold spread is of order 0.001–0.007; the ordering between adjacent
members is not a claim that one is better. `submission_rank` exists because the upload form reads a
ranking from the top row down.

## 6. The two receptor-conformation readouts, and what they cannot tell you

Neither is a ranking axis. Both are reported because they describe *how* the peptide sits.

### 6.1 TM6 two-state (`tm6_k_active`, `tm6_n`)

Cuts frozen from nine deposited GLP-1R structures, 9/9 under leave-one-out. Over this band it calls
**40 of 40** measured models active-like.

**It does not discriminate.** On a 110-structure pharmacology panel the same measure scores
agonists, antagonists **and a composition-matched scramble** as active-like at 10/10. What it says
is that chai builds the active bundle once anything is in the pocket. It is a measurement; it is
not evidence of agonism, and it orders nothing.

Two deposited designs carry no TM6 number (`micro_04`, `micro_10`): they entered the pool from a
different source than the search cells and were classified on ECL2 but not on TM6. Their cells are
blank, which means **not measured** — not *failed*.

### 6.2 ECL2+TM5 engagement family (`ecl2_fam0_k`, `ecl2_family_n`, `ecl2_canonical`)

Two medoids learned on the same 110-structure panel, measured on receptor ECL2+TM5 after
superposition; silhouette **0.450**. Family 0 is where the canonical N-terminal-into-the-core
agonists fall.

**It is a binding-MODE prior, not a validated agonist classifier.** On the panel it does not
separate agonists from antagonists either. It is used as a **quota** in step 6 of the ranking, to
guarantee the band is not composed entirely of designs engaging in some other way, and it is never
a score. `ecl2_canonical` is fam-0 in at least 3 of 5 models; **five of the ten** deposited designs
are canonical on it.

## 7. The ring, measured

The declared disulfide is measured on each shipped model with the engine's own cut (SG–SG ≤ 2.5 Å),
rather than taken from the configuration:

- **45 of 50** chai models across the band close the declared ring;
- `micro_03` and `micro_07` close it in 3 of 5, `micro_04` in 4 of 5 — all three carry a risk flag;
- `ss_distance_median` is the median SG–SG distance over the five.

A disulfide that closes in three models of five is not the same object as one that closes in all
five, so the column is *k* of *n* and never a median alone.

The deposition script enforces the declaration against the sequence: a row claiming
`cyclisation = disulfide Ci-Cj` is refused unless residues *i* and *j* of its own sequence are two
distinct cysteines. (Target 2's script tested the two *terminal* residues instead, which is correct
for a band that is entirely Cys1–CysN macrocycles and wrong here, where six of ten carry the ring
internally.)

## 8. The second and third oracles

Reported, never ranked on.

| | version | condition | MSA |
|---|---|---|---|
| **chai-1** | the ranking oracle | disulfide restraint only | ESM-2 embeddings (its own pathway) |
| **Boltz-2** | 2.2.1 | disulfide bond constraint | local UniRef90 |
| **Protenix-v2** | released checkpoint | **UNRESTRAINED** | local UniRef90 |

**All three were given their own evolutionary pathway.** Every Boltz and Protenix number measured
on this target before this deposition was run single-sequence, which switched off the two models
that need an alignment while chai kept its own. The deposited numbers correct that: alignments were
built from a **local** UniRef90 database (the binder sequences are unpublished designs and did not
leave the machine), giving receptor depth **2,280** and **depth 1 for every binder** — a de novo
12-mer has no homologues, which is a result rather than a reason to skip the arm. Giving Boltz the
alignment mostly removed a failure mode rather than raising a ceiling: three of the ten had
collapsed single-sequence and recovered (ipSAE 0.012 → 0.906 on one), while on the other seven
ipTM moved a median +0.002.

**Protenix is unrestrained because it cannot be restrained.** Its constraint embedders are
`enable: False` in the released configuration and the checkpoint carries no constraint tensors. It
was asked a different question from the other two and its numbers must not be averaged with theirs.

**Read Protenix's five samples as one draw with a width.** Their within-run spread (0.016 ipTM) is
far smaller than the movement across a seed change (3.4× to 22× that), so they are not five
independent draws.

**`complex_plddt` is never reported as a binder metric** for either model. It averages the binder
into a 409-residue receptor, so on a 12-mer it is ~97 % receptor and reads as a confident binder
while the binder's own atoms sit near 0.5. Only the binder chain's own mean is deposited.

### What the three say about each other

Over the ten deposited designs, Spearman ρ between chai's ordering and:

- Boltz-2 ipTM: **+0.055**
- Protenix-v2 ipTM: **+0.188**
- Boltz-2 ipSAE: **+0.370**
- Boltz-2 against Protenix-v2: +0.321

(n = 10, so every one of these intervals is wide.) On the larger pool the same pattern held, and
each oracle reproduces **its own** ordering across a seed change far better than it reproduces
another's — Boltz at +0.87 to +0.94 — so this is disagreement about binding, not measurement noise.
Boltz-2 also saturates on short binders here: 0.964 ± 0.009 over twenty 12-mers, with ipTM 0.97
alongside a binder pLDDT of 0.52, so its ipTM has little resolving power at this length.

**We rank on one oracle and report the others.** Blending them would average the disagreement away
and produce a number no oracle actually computed.

## 9. ipSAE

Computed with `xenodesign.metrics.ipsae_token`, the token-level form on the Dunbrack scale. The
chain-level `ipsae()` collapses d0 for a short binder and is not used.

## 10. What is deposited, and what can be recomputed

Each of `Target_3/micro/AMBRA_T3_micro_01` … `_10` carries fifteen models — five per oracle — plus
the score arrays, the confidence records, the restraint file as chai was given it, the sequence and
a `metrics.json` whose field names match `metrics_full.csv`. Every figure quoted in this deposition
can be recomputed from those files. Nothing is reported that cannot.

The 34 documented designs carry their metrics in `metrics_full.csv` with a `status` saying why they
are not submitted; their coordinates are not deposited.

## 11. Limits

- No design has been synthesised or assayed. There are no binding data and no functional readout.
- Neither receptor-conformation measure establishes agonism (§6).
- The three oracles disagree about binding (§8).
- The 39-mers' 27-residue extensions are elongations of a delivered macrocycle, and what the
  extension contributes to the score has not been separated from what the ring contributes.
- `chai_n_folds` is 1 for several designs. A single draw and a mean over five are both in the
  column; the spread is beside it, and chai is nondeterministic on this system.
- Pose dispersion ranges 0.94–3.89 Å across the band and is not a gate (§5).
- The band is a set, not a sharp order (§5).
