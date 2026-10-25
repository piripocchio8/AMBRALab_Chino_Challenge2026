# Target 3 — what every column in `metrics_full.csv` means

Target 3 is a de novo **GLP-1R agonist** deposition in two bands: a **micro** band of
disulfide-cyclised peptides of 12–39 residues designed in this group, and a **mini** band of
140-residue de novo miniproteins from a collaborating pipeline. The receptor is UniProt **P43220**
(GLP-1R), modelled as a 409-residue chain, and the active-state reference is **6X18**.

**Columns are band-specific and that is deliberate.** The two bands were scored by different
oracles in different conditions, so they do not share a confidence column: a blank in a micro
column on a mini row means the design was never measured that way, which is always true. The
`series` column says which band a row belongs to.

This file and `OPTIONAL_COLUMNS` in `scripts/make_target3_submission.py` describe the same 86
columns and must be changed together. `submission.csv` carries only the three columns the upload form defines
(`name`, `sequence`, `molecule_class`); everything below is the companion metric table.

A blank cell means **not measured**, never zero. `status` and `molecule_class` are never blank.

---

## Base columns

| column | meaning |
|---|---|
| `name` | the deposited identifier, unique |
| `sequence` | the binder sequence, 20 standard amino acids only |
| `molecule_class` | from the upload form's enumeration; `single_chain` for every Target-3 design |
| `status` | `submitted`, or a sentence saying why a documented design is not submitted |
| `submission_rank` | 1 = the design we would most like tested. Submitted rows carry exactly 1..n |

## Identity and provenance

| column | meaning |
|---|---|
| `binder_length` | residue count; must equal `len(sequence)` or the script refuses |
| `series` | design series label |
| `cyclisation` | e.g. `disulfide C<i>-C<j>`; refused unless the sequence can form it |
| `mechanism` | intended pharmacology — `agonist` for this target |
| `parent_family` | the 12-mer macrocycle parent the design descends from (p1/p2/p3) |
| `wave` / `arm` | the search campaign and arm that produced it |
| `direction` | for elongated designs, whether the extension is N- or C-terminal |
| `design_origin` / `design_round` | pipeline provenance |
| `cys_positions` | the two cysteines that close the ring (1-based) |
| `trimmed` | true if the deposited construct is a trimmed form of a longer design |
| `trimmed_from` | the parent design a trimmed construct came from |

**On trimming — and why those two columns are absent.** Some designs carry a short
low-confidence terminal run. We tested cutting it (residues with pLDDT < 70) and re-folding. It
helped only where the run was genuinely disposable; in designs that engage the receptor canonically
the N-terminal run is the functional reach into the pocket, and cutting it lowered confidence or
broke the disulfide. **No trimmed form was deposited in the end**, so `trimmed` and `trimmed_from`
carry no value on any row and the CSV does not contain them — a column only appears when some row
supplies it. The terminal-order columns below are the measurement the question was decided on.

## Fold confidence — the primary axis

| column | meaning |
|---|---|
| `selected_iptm` | chai interface pTM, **measured with the disulfide restraint only — no pocket restraint**. **The axis the micro band is ranked on.** |
| `selected_ptm` | pTM of the same folds |
| `binder_plddt` | mean predicted lDDT over the binder, 0–1 |
| `state` | `complete` (a 200-step final refold) or `walltime` (the last 120-step cold reground) |
| `score_source` | which file the score was read from |
| `chai_iptm_restrained` | the same designs folded **with** the 8 Å pocket restraint on K174/R357 |
| `restraint_delta` | `selected_iptm` − `chai_iptm_restrained`. Negative means the restraint was worth that much. |
| `chai_iptm_spread` | max − min across the folds behind `selected_iptm` |
| `chai_n_folds` | how many folds that number is a mean over. 1 and 5 are not the same measurement. |
| `pose_disp_mean` / `pose_disp_max` | mean and worst pairwise binder Cα RMSD across the five diffusion samples, Å. **Reference-free** — the samples are already in one target frame — and **not a gate or a rank** (see below). |
| `hb_mean` | mean number of binder–receptor polar contacts per model |
| `hb_conserved` | contacts present in at least 4 of 5 models |
| `hb_partners` | the receptor residues involved, with the region each sits in |

**Why the restrained column is kept.** Refolding the pool without the pocket reorders it
(ρ = +0.538 over 48 designs; 7 collapse). The restrained number is therefore partly an instruction
rather than a prediction, and the band is ranked on the unrestrained one. Keeping both means the
condition always travels with the score.

**Why pose dispersion ranks nothing.** Across a seed change the ranking axis reproduces at
ρ = +0.976, pose dispersion at +0.524 and the conserved-contact count at +0.210. Gating on either
of the latter would let the least reproducible measurement overrule the most reproducible one.

**`state` is not cosmetic.** A `complete` and a `walltime` row are not folded to the same depth, so
their scores are not strictly like-for-like. Prefer `complete` rows when comparing.

## Receptor activation conformation (TM6 two-state)

| column | meaning |
|---|---|
| `tm6_k_active` / `tm6_n` | models called active-like, of models measured |

**Read this as a measurement, not a ranking.** It calls **40 of 40** measured models in the
submitted band active-like, and on the 110-structure pharmacology panel the same measure scores
agonists, antagonists **and a composition-matched scramble** at 10/10. It says the model built the
active bundle once anything was in the pocket. Cuts were frozen before predictions were made. Two
submitted designs have **blank** cells here: they entered the pool from a different source and were
classified on ECL2 but not on TM6. Blank means *not measured*, not *failed*.

## ECL2+TM5 engagement family — the discriminating measure

| column | meaning |
|---|---|
| `ecl2_fam0_k` / `ecl2_family_n` | models in family 0, of models classified |
| `ecl2_canonical` | true when family 0 dominates (≥3 of 5 models). **Five of the ten** submitted micro designs. |
| `ecl2_tm5_mix` | confidence of the engaged part of ECL2+TM5, scaled by how much of it is engaged |

Two families were learned on a **110-structure pharmacology panel** (silhouette 0.450; nearest-medoid
reproduces the panel's own clustering for 100% of it). **Family 0 = canonical N-terminal engagement** —
the loop sits 2.01 ± 1.45 Å from 6X18's His7, core recovery 0.89. Family 1 is non-canonical
(9.62 ± 6.54 Å, 0.60). Canonical engagement is the structural hallmark of how a real agonist inserts
its N-terminus into the TMD core, and designs achieving it are flagged `ecl2_canonical`.

> **Caveat, stated plainly: this reads binding *mode*, not pharmacology.** On the same panel the
> family split does **not** separate agonists from antagonists — between-minus-within on the family
> proportion is **−0.002, CI [−0.180, +0.511]**. `ecl2_canonical` is therefore a **mechanistic prior**
> — this design engages the pocket the way agonists do — and **not a validated agonist classifier**. No
> ranking claim in this deposition should be read as a predicted efficacy. (The only loop measure whose
> CI excluded zero was ECL1's mixture, and it is a peptide-length counter, r = +0.880 with ligand
> length; it is not used here.)

## Ring closure

| column | meaning |
|---|---|
| `ss_distance_median` | median SG–SG distance across models, Å |
| `ss_bonded_k` / `ss_n` | models closing the declared disulfide, of models measured |

Bonded iff **SG–SG ≤ 2.5 Å**, the same cut the engine itself writes. Closure is **model-dependent for
some designs**: a design can close in most models and not in its highest-ipTM one. `ss_bonded_k/ss_n`
is therefore reported per design and a low ratio is carried in `risk_flags` — a declared macrocycle
whose staple forms in a minority of models is a real liability, not a rounding detail.

## Terminal order (how the trim question was decided)

| column | meaning |
|---|---|
| `ring_plddt` / `tail_plddt` | mean binder pLDDT inside the macrocycle vs outside it (0–100) |
| `tail_lt70` | residues outside the ring with pLDDT < 70 |
| `nterm_run_lt70` / `cterm_run_lt70` | length of the contiguous sub-70 run at each terminus |

These separate "the extra mass is ordered" from "the extra mass is a disordered tail", which the
overall `binder_plddt` averages away.

## Flags

| column | meaning |
|---|---|
| `risk_flags` | known liabilities (e.g. unreliable ring closure, a `walltime` score, exocyclic disorder) |
| `notes` | free text |

## The second and third oracles — reported, never ranked on

| column | meaning |
|---|---|
| `boltz_msa_iptm_max` / `_mean` / `_spread` | Boltz-2 interface pTM over its five models: the max, the mean, and max − min |
| `boltz_msa_ptm_mean` | Boltz-2 pTM, meaned over the five |
| `boltz_msa_ipsae_max` / `_mean` | **ipSAE** (Dunbrack scale, token-level) from Boltz-2's full PAE matrix |
| `boltz_msa_binder_plddt` | mean pLDDT over the **binder chain only**, 0–100 |
| `boltz_condition` | the restraint Boltz was given |
| `protenix_msa_*` | the same six quantities for Protenix-v2 |
| `protenix_condition` | **always "UNRESTRAINED"** — see below |
| `receptor_msa_depth` | sequences in the receptor alignment both models were given |
| `binder_msa_depth` | sequences in the binder alignment. **1 for every design**: a de novo peptide has no homologues. |

**All three oracles were given their own evolutionary pathway.** chai takes its signal from ESM-2
embeddings; Boltz-2 and Protenix-v2 take theirs from an alignment. Every Boltz and Protenix number
measured on this target before this deposition was run **single-sequence**, which switched off the
two models that need an alignment while chai kept its own — not a comparison. The deposited numbers
were produced with alignments built from a **local UniRef90** database (the binder sequences are
unpublished designs and did not leave the machine): receptor depth **2,280**, binder depth 1.

Giving Boltz the alignment **removed a failure mode rather than raising a ceiling**: three of the
ten had collapsed single-sequence and recovered (ipSAE 0.012 → 0.906 on one), while on the other
seven ipTM moved a median +0.002.

> **Protenix is unrestrained because it cannot be restrained.** Its constraint embedders are
> `enable: False` in the released configuration and the checkpoint carries no constraint tensors.
> It was asked a different question from the other two. **Do not average its numbers with theirs.**

> **Protenix's five samples are not five independent draws.** Their within-run spread (0.016 ipTM)
> is far smaller than the movement across a seed change — 3.4× to 22× that. Read them as one draw
> with a width.

> **`complex_plddt` is not in this table, for either model.** It averages the binder into a
> 409-residue receptor, so on a 12-mer it is ~97 % receptor and reads as a confident binder while
> the binder's own atoms sit near 0.5. Only the binder chain's own mean is deposited.

> **The oracles disagree, and the band is ranked on chai.** Over the ten submitted micro designs,
> Spearman ρ between chai's ordering and Boltz ipTM is **+0.055**, Protenix ipTM **+0.188**, Boltz
> ipSAE **+0.370**, Boltz against Protenix +0.321 (n = 10; every interval is wide). Each oracle
> reproduces **its own** ordering across a seed change far better — Boltz at +0.87 to +0.94 — so
> this is disagreement about binding, not noise. Boltz also saturates at this length: 0.964 ± 0.009
> over twenty 12-mers, with ipTM 0.97 beside a binder pLDDT of 0.52. We rank on one oracle and
> report the others **as checks, never as votes**; a blended score would produce a number none of
> them computed.

---

## The mini band's own columns

Every one of these is the collaborating pipeline's number, copied verbatim and **not re-measured
here**. They are in separate columns from the micro band's for that reason. Full definitions, and
what that pipeline's package does and does not record, are in
[`methods_mini.md`](methods_mini.md).

| column | meaning |
|---|---|
| `anchor_seq` | the N-terminal ten residues — the agonist anchor, restrained to a consensus of verified agonists |
| `n_hotspots` / `hotspot_positions` | the receptor hotspots that **sub-campaign** targeted. A design **input**, constant within a source, so **not comparable design to design**. |
| `motif_rmsd_A` | RMSD of the anchor motif to its target geometry, Å |
| `receptor_rmsd_A` / `rmsd_domain_A` / `rmsd_all_A` | receptor and binder RMSDs as the pipeline reports them |
| `min_dist_A` | closest binder–receptor approach, Å |
| `mini_iptm` / `mini_ipsae` / `mini_ipsae_consensus` | interface confidence of the bound prediction |
| `mini_plddt_binder` / `mini_plddt_design` / `mini_iplddt` | pLDDT over the binder, over the designed region, and at the interface |
| `mini_pdockq` | pDockQ of the bound prediction |
| `mono_plddt` / `mono_plddt_designed` | pLDDT of the design folded **alone** |
| `self_iptm` / `self_contacts` | the design folded against **a copy of itself**. **A LOW value is the good outcome** — this is a self-association check, and a design that binds itself competes with binding the receptor. |
| `mini_score` | the pipeline's own composite |

> **`rmsd_all_A` is deposited and is not used to argue anything.** `rmsd_all_A` is the RMSD of the
> binder between its bound and its alone prediction over all 140 residues, and `rmsd_domain_A` the
> same over residues 30–140, each after a Kabsch superposition on those same residues (pipeline
> author; written answers). Over the pipeline's 50 designs `rmsd_all_A` is bimodal — 23 at
> 0.76–9.11 Å and 27 at 12.87–21.42 Å with an empty gap — while `rmsd_domain_A` stays tight (median
> 0.42 Å). Six of the deposited ten (`AMBRA_T3_mini_01`, `_03`, `_04`, `_05`, `_08`, `_09`;
> 13.598–17.583 Å) are in the high mode; the other four lie between 1.289 and 4.324 Å. Of the two
> readings the package left open, the benign one is correct (pipeline author; written answers): the
> fold is unchanged, and the high mode is a superposition artefact of a flexible N-terminal segment,
> a rigid-body swing of the low-confidence stalk that carries the anchor. Over residues 30–140 the
> distribution is unimodal (see [`../mini/README.md`](../mini/README.md)). Read `rmsd_domain_A` as
> the fold measure and `rmsd_all_A` as the placement of that segment.

> **`rank`, in the source package, is not an ordering on `mini_score`; `mini_score` itself is
> comparable across the whole set.** The package was sorted by hotspot count first and `score`
> second, so every design meeting 4 of 4 hotspots (ranks 1–34) sorts above every design meeting 3
> of 3 (ranks 35–50) whatever its score (pipeline author; written answers). The submitted ten are
> the five 4-of-4 designs (rows 11–15) and then the five 3-of-3 designs (rows 16–20), each group in
> source order, so the submitted order is a block order, not a score order. `mini_score` is one
> formula with one min–max normalisation over the campaign's whole gated set (187 designs), not per
> block, so it can be compared design to design across rows 11–20 (pipeline author; this corrects
> the author's earlier answer that it could not): `AMBRA_T3_mini_06` (row 16) scores 0.9122 and
> `AMBRA_T3_mini_01` (row 11) 0.7864. Read `mini_score` by its value and the row number as a block.
> See [`../mini/README.md`](../mini/README.md) for the selection rule and the novelty finding that
> forced it.

---

### What this table does not contain

No wet-lab measurement of any kind. Every number is computational structure prediction — two
structure predictors, no binding assay and no efficacy measurement. `mechanism` records design
*intent*, and the ECL2 caveat above governs how far the structural evidence reaches.
