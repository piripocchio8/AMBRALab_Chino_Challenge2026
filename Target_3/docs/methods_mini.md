<!-- Written from the collaborating pipeline's own package, which was read but not re-run.
     Nothing in it was re-measured here; where the package does not record a tool version or a
     parameter, this document says so rather than filling the gap. Parameters the package did not
     carry were later supplied by the pipeline's author and are marked as such; gaps that the
     author's answers do not cover are still marked. The questions it raised, and the author's
     answers to them, are in ../mini/README.md under "Limits". -->
# Target 3, MINI class: methods

Challenge 2026, Target 3 (de novo GLP-1R agonist, receptor UniProt P43220). The deposition is
20 designs in two classes. This document covers the **mini** class only: 10 miniprotein designs,
140 residues each. The 10 **micro** designs are cyclic peptides designed in XenoDesign1 and are
documented separately.

## Provenance and the limits of this document

The mini designs were generated and validated by Gianmattia **outside the XenoDesign1
repository**, in campaign `p15_1099477`. Every number quoted below was produced by that external
pipeline and is reproduced verbatim. **Nothing was re-folded, re-scored or re-measured here.** No
structure prediction was run while staging this class.

Three sources feed this document, and they are not equally strong:

1. **The packaged artifact** `gianmattia_designs.json` (50 designs plus a `meta.cohort` block).
   This is the only machine-readable record available, and it carries **results only**. It
   contains **no method fields at all**: no tool versions, no parameters, no seeds, no reference
   structure, no metric definitions.
2. **The campaign description** relayed with the designs (pipeline outline and design intent).
3. **The pipeline author's written answers**, received after the package. They give the parameters
   the package did not carry and cite, by filename, the scripts each was read from. Those scripts
   were not seen here and nothing was re-run, so these statements are sourced, not verified. The
   answers also report two things the author measured after handing the package over; those are
   described in [`../mini/README.md`](../mini/README.md).

Statements that can be checked against the artifact are marked *(verified in the file)*.
Statements that rest on the campaign description alone are marked *(campaign description;
not in the file)*. Statements that rest on the pipeline author's answers are marked *(pipeline
author; written answers)*; the answers arrived as a document named `PIPELINE_ANSWERS.md`, whose
content is folded in here and which is not kept in the repository. Everything that neither the
pipeline nor the author's answers recorded is marked **NOT RECORDED** where it occurs, and is not
collected in a separate file; searching this document for that marker finds each gap. A methods
section that asserts an unsourced parameter would be worse than one with a stated gap, so the gaps
are left visible.

## Design

### Backbone generation

Backbones were generated with **RFdiffusion3** *(campaign description; not in the file)*, run
through the `rfd3` command-line tool from **rc-foundry 0.2.0**. The contig was
`B1-10,130-130,/0,A1-409`: in the diffusion input's chain labels, chain B residues 1 to 10 are the
fixed anchor, followed by 130 diffused residues, a chain break, and the 409-residue receptor (chain
A) held fixed. Sampling used `infer_ori_strategy: hotspots`, `is_non_loopy: true`,
`inference_sampler.step_scale=3` and `inference_sampler.gamma_0=0.2`, with diffusion seed
`15000 + shard` for `p13`; the other rounds use different seed bases, which the author's answers
leave to each round's sbatch script. Hotspots were passed at atom level, not residue level
(`select_hotspots` in `inputs/rfd3/*.json`): `p3` `A86:CD2 A87:CD1 A88:CD1 A89:NE2`; `p10` and `p12`
`A27:CD1 A42:OG1 A86:CD2`; `p13` `A27:CD1 A42:OG1 A86:CD2 A95:CD2` *(pipeline author; written
answers)*. The model checkpoint, noise schedule, number of steps, partial-diffusion settings and the
number of backbones sampled are **NOT RECORDED**.

Each design carries a provenance `name` of the form
`<source>_<index>_sh<shard>_m<M>_<n>_model_<K>__<sequence draws>`, for example
`p13_04_sh4_m0_0_model_3__s0__s2_model_0__s1`. The `(source, shard, m*_model_*)` triple identifies
the parent backbone; the trailing tokens identify the sequence draws made on it *(verified in the
file: the 50 packaged designs come from 47 distinct parent-backbone keys)*. The `source` labels
`p3`, `p10`, `p12`, `p13` denote the separate RFdiffusion3 sub-campaigns (rounds) that produced the
parent backbones, which were given hotspot sets of different sizes: `p13` and `p3` four hotspots,
`p10` and `p12` three. The outer `shard` field is the p15 shard that produced the design, while the
`sh` token inside `name` is the shard of the parent backbone in the earlier round; they disagree for
45 of the 50 designs because the two runs sharded independently, and both are correct *(pipeline
author; written answers)*.

### Sequence design

Sequences were designed with **ProteinMPNN** *(campaign description; not in the file)*. In the step
the author's answers describe (`h8_anchor.py`, `p15_anchor.sbatch`) the weights were
`soluble_v_48_020.pt`, the sampling temperature was 0.2, 16 sequences were drawn per backbone with
seed `900 + shard`, and residues 11 to 140 were held fixed at their parent values while residues 1
to 10 were restrained as described under *The agonist anchor* below *(pipeline author; written
answers)*. The ProteinMPNN version and whether the receptor was present as context during design are
**NOT RECORDED**, and the answers do not say how the parent sequence at residues 11 to 140 was
produced.

All 50 packaged sequences are 140 residues and use only the 20 standard amino acids; no
non-canonical residue, and no cysteine in any of the 10 deposited designs *(verified in the file)*.

### The agonist anchor

The N-terminal 10 residues of every design are an agonist anchor motif, restrained during design
to a consensus of **23 verified GLP-1R agonists** *(campaign description; the number 23 and the
identity of those agonists are not in the file and cannot be checked here)*. The author's answers
repeat the number 23 and give the form of the restraint, below, but do not name the agonists.

What the file does show is the residual freedom the restraint left. Over all 50 packaged designs
the anchor positions vary as follows *(verified in the file)*:

| anchor position | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| residues seen | H 33, F 16, Y 1 | A 27, G 17, S 6 | E 50 | G 50 | T 50 | F 50 | T 49, I 1 | S 50 | D 50 | V 22, L 15, Y 12, K 1 |

Positions 3 to 6, 8 and 9 are invariant (`EGTF.SD`), position 7 is invariant but for one design,
and positions 1, 2 and 10 are the free ones. In the 10 deposited designs (`anchor_seq` in
`../metrics_full.csv`) positions 3 to 9 are `EGTFTSD` in all ten; position 1 is His in 7, Phe in 2
(`AMBRA_T3_mini_08` and `_10`) and Tyr in 1 (`AMBRA_T3_mini_06`); position 2 is Gly in 4, Ala in 3
and Ser in 3; position 10 is Leu in 4, Tyr in 4 and Val in 2.

The artifact stores the anchor twice, as a dedicated `anchor` field and as the first 10 residues
of `seq`; the two agree for all 10 deposited designs *(verified in the file)*. The deposited JSON
adds an `anchor_seq` field computed here as `seq[:10]` purely so the check is visible in the file.

The anchor was restrained to a *sequence* consensus, not a *structural* pose, and the restraint was
enforced by omission: at each of the ten positions every disallowed amino acid is passed to
ProteinMPNN in `omit_per_residue`, which forces an identity rather than tilting a distribution. The
anchor itself was restrained in this way; it was residues 11 to 140 that were held fixed, at their
parent values, and the script rejects any sequence in which they changed *(pipeline author; written
answers)*. The residues allowed at each position were:

| anchor position | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| residues allowed | H, Y, F | G, A, S | E, D | G | T | F | T, I | S | D | Y, V, L, K |

Positions 4, 5, 6, 8 and 9 are invariant across the 23 agonists and position 7 is 95.7 % conserved
*(pipeline author; written answers)*. The variation in the table of residues seen above is exactly
this allowance: every residue seen in the 50 packaged designs lies within it, and position 3 allowed
E or D though only E appears.

### Scaffold extension

The anchor is extended into a **four-helix bundle** carrying it, giving the 140-residue
miniprotein *(campaign description; the file records no secondary-structure annotation, so the
bundle topology is not verifiable from the artifact)*. The 140-residue length is fixed by the
contig, not selected: every design in every round is 140 *(pipeline author; written answers)*. All
50 packaged designs are 140 residues *(verified in the file)*. Helix lengths, loop lengths and the
register at which the anchor joins the bundle are **NOT RECORDED**.

## Validation: three predictions per design

Each design received three separate structure predictions, recorded in the artifact as three
result files per design: `b_complex_*.json`, `b_alone.json` and `b_pair.json` *(verified in the
file)*.

1. **Bound**: the design in complex with the receptor. Source of `iptm`, `ipsae`, `ipsae_cons`,
   `iplddt`, `pdockq`, `plddt_binder`, `plddt_design`, `min_dist`, `motif_rmsd`, `receptor_rmsd`,
   `hotspots`/`hot_list`, `q_full`, `q_designed`.
2. **Alone**: the design predicted on its own, as a monomer. Source of `mono_plddt`,
   `mono_plddt_designed`, and (by comparison with the bound prediction) `rmsd_all` and
   `rmsd_domain`.
3. **Against a copy of itself**: the design predicted as a homodimer. Source of `self_iptm` and
   `self_contacts`. **This arm is a self-association control, not a binding assay: a LOW
   `self_iptm` is the good outcome.** A design that scores high here is predicted to prefer its
   own copy, which competes with receptor binding and is a liability, not an asset.

The structure predictor was **Boltz-2 2.2.1**, run on GPU with `--diffusion_samples 1 --seed 1
--write_full_pae`. The receptor carried a cached MSA (`inputs/msa/glp1r_receptor_A.a3m`, 9,929
sequences); the binder was `msa: empty`, single-sequence, since a de novo design has no homologues.
The receptor construct was the full 409-residue chain (UniProt P43220 residues 24 to 432), taken
from an AlphaFold3 prediction of the receptor-GLP-1 complex (`fold_glp1r_glp_model_0.cif`)
*(pipeline author; written answers)*. The number of recycles is **NOT RECORDED**. Each design was
predicted at one seed; a later replication at two further seeds, which bears on how far a single
prediction can be trusted, is described in [`../mini/README.md`](../mini/README.md).

The `b_complex` field takes two values across the 50 designs, `b_complex_a.json` and
`b_complex_b.json`. There is no semantic difference between them: the bundle was split in half only
because a single file exceeded a size limit, and nothing distinguishes the variants *(pipeline
author; written answers)*. Which variant each deposited design came from is not carried in the
deposited files.

## Metric definitions

Standard definitions are given where the metric name is a published one. **The implementation
that produced each number is not recorded**, so these definitions describe what the name
conventionally means, not what the pipeline provably computed.

**From the bound prediction**

- `iptm`: interface predicted TM-score, the predictor's confidence in the relative placement of
  the two chains. Range 0 to 1, higher is better. Deposited 10: 0.9033 to 0.9465.
- `ipsae`, `ipsae_cons`: ipSAE is an interface-restricted score derived from the predicted aligned
  error matrix, designed to be less length-biased than ipTM. Higher is better. `ipsae_cons` is not
  defined in the artifact. The author defines it as the conservative direction of ipSAE: the minimum
  across the chain-pair rows of the ipSAE output, where `ipsae` itself is the maximum row
  (`rank_campaign.py`, line 111) *(pipeline author; written answers)*. An earlier version of this
  document guessed that `ipsae_cons` restricts to the consensus anchor region. That guess was wrong:
  `ipsae_cons` does not restrict to the anchor. The author notes that the gap between the two is
  large for some designs and is worth checking before trusting a single ipSAE value. On this target
  ipSAE is also nearly blind to whether the hotspots are contacted; see
  [`../mini/README.md`](../mini/README.md). Deposited 10: `ipsae` 0.8870 to 0.9150, `ipsae_cons`
  0.5583 to 0.8619.
- `iplddt`: mean pLDDT over interface residues in the complex. Higher is better. Which residues
  count as interface, and at what distance cutoff, is **NOT RECORDED**. Deposited 10: 0.8379 to
  0.8796.
- `plddt_binder`, `plddt_design`: mean pLDDT over the binder chain and over the designed segment,
  in the complex prediction. The two differ by a median of +0.0025 over all 50, so the two windows
  overlap almost completely. The package does not state the windows; they are recovered from the
  deposit. The B-factor column of `complex.pdb` holds pLDDT x 100 per residue, and its chain A mean
  over residues 1 to 140 reproduces `plddt_binder`, and over residues 11 to 140 `plddt_design`, for
  all ten deposited designs, to within the rounding of the four decimals the CSV carries (largest
  difference 0.00005). Of the windows starting at residue 1 to 20 and ending at residue 120 to 140,
  no other reproduces either column for all ten. Deposited 10: 0.8836 to 0.9184 and 0.8866 to
  0.9219.
- `pdockq`: predicted DockQ, a published composite of interface pLDDT and the number of interface
  contacts used as a proxy for docking quality. Higher is better. The exact formula variant and
  the contact cutoff are **NOT RECORDED**. Deposited 10: 0.5972 to 0.6642.
- `min_dist`: minimum interatomic distance across the interface, in angstrom. Which atom types
  are considered is **NOT RECORDED**. Deposited 10: 1.90 to 3.36 A; 1.90 A is
  `AMBRA_T3_mini_06` and the next lowest is 2.60 A (`AMBRA_T3_mini_09`). Because the atom types
  are not recorded, this document cannot say whether 1.90 A is a close contact or a clash.
- `motif_rmsd`: RMSD of the 10-residue anchor, in angstrom, against its intended agonist pose.
  Lower is better. The reference is the GLP-1 peptide chain of the AlphaFold3 model of the
  receptor-GLP-1 complex from which the receptor construct was taken. The measurement superposes on
  receptor C-alpha only and then reports the anchor's displacement under that transform
  (`h3_measure.py`), so it is anchor placement in the receptor frame, not a free-floating fit
  *(pipeline author; written answers)*. Deposited 10: 0.528 to 0.962 A.
- `receptor_rmsd`: RMSD of the receptor, in angstrom, against a reference that is **NOT
  RECORDED**. Over all 50 it spans 2.07 to 4.20 A with a standard deviation of 0.31 A, so it is
  close to constant and carries little design-to-design signal. Deposited 10: 2.901 to 3.196 A.
- `hotspots` and `hot_list`: the number and the indices of the targeted hotspot residues.
  `hotspots` equals `len(hot_list)` for all 50 *(verified in the file)*. The index set is constant
  within each `source` (p13 gives `[27, 42, 86, 95]`, p3 gives `[86, 87, 88, 89]`, p10 and p12
  give `[27, 42, 86]`), so this field reads as a per-sub-campaign **design input**, not a
  per-design measured outcome, and the author's answers bear this out: the hotspots were specified
  to RFdiffusion3 (see *Backbone generation*). The indices are receptor residues, numbered 1-based
  in the modelled 409-residue chain, which is UniProt P43220 residues 24 to 432, so the UniProt
  number is the deposited number plus 23 *(pipeline author; written answers)*.
- `q_full`, `q_designed`: not defined anywhere in the artifact. The author defines both as net
  formal charge, counted as (K + R) - (D + E), over the whole 140-residue chain and over residues 11
  to 140 respectively (`build_artifact_data.py`, lines 49 and 50); they are not pI and not a
  titration *(pipeline author; written answers)*. Both are small integers (`q_full` 3 to 7,
  `q_designed` 5 to 8) and `q_designed - q_full` equals exactly 2 in 49 of the 50 designs. The
  author attributes a difference of about 2 to the anchor being acidic by construction.

**From the alone prediction**

- `mono_plddt`, `mono_plddt_designed`: mean pLDDT over the whole chain and over the designed
  segment, predicted as a monomer. Higher is better; it reports whether the design folds on its
  own. The same check on `alone.pdb` recovers the windows as residues 1 to 140 and 11 to 140, for
  all ten deposited designs. `mono_plddt_designed` exceeds `mono_plddt` by a median of +0.023 over
  all 50; in the deposited ten the residues outside the designed window, 1 to 10 (the anchor), are
  the lower-confidence part, with a mean pLDDT in `alone.pdb` of 0.456 to 0.793 per design.
  Deposited 10: 0.8369 to 0.9332 and 0.8604 to 0.9440.
- `rmsd_all`, `rmsd_domain`: RMSD in angstrom between the monomer prediction and the bound
  conformation, over all residues and over a "domain" subset. Lower is better. `rmsd_all` is over
  all 140 residues and `rmsd_domain` over residues 30 to 140. Each is a Kabsch superposition
  computed over exactly the residue set being measured, with no separate frame and no reference
  beyond the two structures compared, which are the same design predicted bound and predicted alone
  *(pipeline author; written answers; `measure_monomer.py`, `refine_mono.py`)*. This matters:
  `rmsd_domain` is tight (0.209 to 2.128 A in the deposited 10) while `rmsd_all` is strongly bimodal
  over the 50, with 23 designs below 10 A and 27 between 12.9 and 21.4 A and a clean gap in between.
  The author's answer is that the bimodality comes from the superposition and not from a change of
  fold: the construct is a long N-terminal stalk carrying the anchor plus a compact domain, and
  superposing across that hinge lets a rigid-body swing of the stalk dominate even when the domain
  is unchanged. The median `rmsd_all` is 10.28 A with 31 % within 3 A, against 0.42 A and 97 % for
  residues 30 to 140 (n = 210). Residues 11 to 140 is not a safe window either: its median is still
  5.81 A, because dropping the anchor from the residue set does not remove its effect on the
  superposition. The author adds that monomer pLDDT is 0.584 over the anchor against 0.901 over the
  designed region (n not stated in the answers), so the part that moves is also the part the
  predictor is least sure of. The full window series is in [`../mini/README.md`](../mini/README.md).

**From the self prediction**

- `self_iptm`: ipTM of the design against a copy of itself. **LOW IS GOOD.** This is the
  self-association control. Deposited 10: 0.1226 to 0.467; cohort median 0.262, and the cohort
  reports only 1 design of 210 at or above 0.80.
- `self_contacts`: number of inter-chain contacts in that self prediction. The contact definition
  and distance cutoff are **NOT RECORDED**. Lower presumably indicates less self-association, but
  it is not independent of `self_iptm`. Deposited 10: 325 to 1526.

**Composite**

- `score`: the pipeline's own ranking score: the mean of three min-max normalised terms over the
  gated set, namely anchor RMSD inverted, ipSAE, and binder pLDDT (`rank_campaign.py`) *(pipeline
  author; written answers)*. It is one formula with one normalisation, computed once over the
  campaign's whole gated set (187 designs, see the cohort table below) and not per block. `score`
  can therefore be compared design to design across the whole packaged set, across the boundary
  between the 4-of-4 and the 3-of-3 designs included *(pipeline author; this corrects the author's
  earlier answer that it could not)*. The rescaling is computed within a campaign, so `score` values
  are not comparable across campaigns. `rank` is not a score ordering; see *Selection of the
  deposited 10*. Deposited 10: 0.7408 to 0.9122.

## Cohort-level numbers, as reported by the pipeline

From `meta.cohort` in the artifact, covering **210 refolds** (a larger population than the 50
designs packaged in the file, so these are not recomputable here):

| quantity | value |
|---|---|
| refolds | 210 |
| gated | 187 |
| full epitope | 195 |
| consensus compliant | 210 of 210 |
| monomer pLDDT, median | 0.88 |
| monomer pLDDT >= 0.80 | 200 of 210 |
| domain RMSD, median | 0.42 A |
| domain RMSD within 3 A | 203 of 210 |
| self-ipTM, median | 0.262 |
| self-ipTM >= 0.80 | 1 of 210 |
| receptor ipTM, median | 0.923 |

"Gated" means anchor RMSD below 2.0 A, at least 3 hotspots contacted, and receptor RMSD below 5.0 A.
"Full epitope" means contacting every hotspot of that design's own set: 4 of 4 for `p13` and `p3`, 3
of 3 for `p10` and `p12`. Contact is a heavy-atom distance under 5.0 A, measured from the designed
region only with the anchor excluded, so the anchor sitting in its pocket cannot satisfy it
(`h5_epitope.py`). The path from 210 refolds to the 50 packaged designs is: 210 refolds, 187 gated,
deduplicated at 70 % sequence identity over the designed region keeping the best-ordered member of
each cluster, then the top 50 *(pipeline author; written answers)*. The medians over the 50 packaged
designs are close to the reported
cohort medians (monomer pLDDT 0.8695 vs 0.88; domain RMSD 0.4225 vs 0.42; self-ipTM 0.2452 vs
0.262; receptor ipTM 0.9233 vs 0.923), which is consistent but is not a check, since the two
populations differ.

## Selection of the deposited 10

The 10 deposited mini designs are the artifact's ranks 1, 2, 4, 8 and 10 and its ranks 35, 36, 38,
39 and 42, deposited as `AMBRA_T3_mini_01` to `_10` in that order. The first five are the survivors
of a first selection, the artifact's ranks 1 to 10, which was put through the deposition platform's
novelty check; five of those were rejected. The other five are the five highest-scoring eligible
designs (those without `HAEGTFTSD`) of the artifact's second block, one per parent backbone. The
re-selection, the check's outcomes and the rule are described in
[`../mini/README.md`](../mini/README.md); the rule and the rank lists are `GLP1_NTERM` and
`MINI_RANKS` in `scripts/build_target3_ranking.py`. **No re-scoring or re-weighting was performed in
XenoDesign1**, and the selected designs keep the artifact's relative order. Every "deposited 10"
figure in this document is for this set.

One property of the artifact's `rank` must be stated, because it changes what the selection means:
`rank` is **not** an ordering on `score`, although `score` itself is comparable across the file. The
file is two blocks, each sorted by `score`: ranks 1 to 34 (sources p13 and p3, `score` falling
0.7864 to 0.1245) and ranks 35 to 50 (sources p10 and p12, `score` falling 0.9122 to 0.7167).
Selecting ranks 1 to 10 would therefore have taken the top of the first block only and left out 7
designs whose `score` is higher than that of rank 10, including the highest `score` in the whole
file. The cause is the packaging order, not a preference for any round. The
packaging step sorted by hotspot count first and then by `score` (`best_dir.py`, `--order tier`), so
every design meeting 4 of 4 hotspots sorts above every design meeting 3 of 3 regardless of `score`.
`p13` and `p3` target four hotspots and `p10` and `p12` target three, so the two blocks are the two
hotspot-set sizes, not two rounds; within each block the ordering is by `score` and is meaningful
*(pipeline author; written answers)*. An earlier version of this document suggested that `rank`
might encode a deliberate preference for the p13/p3 rounds. That reading was mistaken. It follows
that `rank` is not a score ordering, and that a design with 3 of 3 hotspots is not worse than one
with 4 of 4: it targeted three points and hit all three.

`score` is a different matter, since it was normalised once over the whole gated set. In the
deposited ten, `AMBRA_T3_mini_10` (3 of 3, 0.7408) scores below `AMBRA_T3_mini_01` to `_04` (4 of 4,
0.7560 to 0.7864), and `AMBRA_T3_mini_06` to `_09` (3 of 3, 0.8299 to 0.9122) score above all five
4-of-4 designs. The band takes five designs from each block because `rank` is not a score ordering
(a pick by rank would have drawn from the 4-of-4 block alone), not because the two blocks' scores
cannot be compared. The pipeline's author considers five from each block a reasonable reading, and
a global sort on `score` among the eligible designs would also have been defensible; the deposited
selection was left as it was made.
