<!-- Written from the collaborating pipeline's own package, which was read but not re-run.
     Nothing in it was re-measured here; where the package does not record a tool version or a
     parameter, this document says so rather than filling the gap. The open questions it raises
     are collected in ../mini/README.md under "Limits". -->
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

Two sources feed this document, and they are not equally strong:

1. **The packaged artifact** `gianmattia_designs.json` (50 designs plus a `meta.cohort` block).
   This is the only machine-readable record available, and it carries **results only**. It
   contains **no method fields at all**: no tool versions, no parameters, no seeds, no reference
   structure, no metric definitions.
2. **The campaign description** relayed with the designs (pipeline outline and design intent).

Statements that can be checked against the artifact are marked *(verified in the file)*.
Statements that rest on the campaign description alone are marked *(campaign description;
not in the file)*. Everything the pipeline did not record is marked **NOT RECORDED**, and is
collected as a question for Gianmattia in `MINI_REPORT.md`. A methods section that asserts an
unsourced parameter would be worse than one with a stated gap, so the gaps are left visible.

## Design

### Backbone generation

Backbones were generated with **RFdiffusion3** *(campaign description; not in the file)*. The
diffusion protocol, model checkpoint, version, noise schedule, number of steps, partial-diffusion
settings, hotspot conditioning format, and the number of backbones sampled are **NOT RECORDED**.

Each design carries a provenance `name` of the form
`<source>_<index>_sh<shard>_m<M>_<n>_model_<K>__<sequence draws>`, for example
`p13_04_sh4_m0_0_model_3__s0__s2_model_0__s1`. The `(source, shard, m*_model_*)` triple identifies
the parent backbone; the trailing tokens identify the sequence draws made on it *(verified in the
file: the 50 packaged designs come from 47 distinct parent-backbone keys)*. What the `source`
labels `p3`, `p10`, `p12`, `p13` denote (separate diffusion rounds, separate scaffold families, or
something else) is **NOT RECORDED**, as is the meaning of the outer `shard` field, which disagrees
with the `sh` token inside `name` for 45 of the 50 designs.

### Sequence design

Sequences were designed with **ProteinMPNN** *(campaign description; not in the file)*. Model
weights, version, sampling temperature, number of sequences per backbone, fixed-position mask,
and whether the receptor was present as context during design are **NOT RECORDED**.

All 50 packaged sequences are 140 residues and use only the 20 standard amino acids; no
non-canonical residue, and no cysteine in any of the 10 deposited designs *(verified in the file)*.

### The agonist anchor

The N-terminal 10 residues of every design are an agonist anchor motif, restrained during design
to a consensus of **23 verified GLP-1R agonists** *(campaign description; the number 23, the
identity of those agonists, and the form of the restraint are not in the file and cannot be
checked here)*.

What the file does show is the residual freedom the restraint left. Over all 50 packaged designs
the anchor positions vary as follows *(verified in the file)*:

| anchor position | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| residues seen | H 33, F 16, Y 1 | A 27, G 17, S 6 | E 50 | G 50 | T 50 | F 50 | T 49, I 1 | S 50 | D 50 | V 22, L 15, Y 12, K 1 |

Positions 3 to 6, 8 and 9 are invariant (`EGTF.SD`), position 7 is invariant but for one design,
and positions 1, 2 and 10 are the free ones. In the 10 deposited designs position 1 is His in all
10, position 2 is A/G/S, and position 10 is L/V/Y/K.

The artifact stores the anchor twice, as a dedicated `anchor` field and as the first 10 residues
of `seq`; the two agree for all 10 deposited designs *(verified in the file)*. The deposited JSON
adds an `anchor_seq` field computed here as `seq[:10]` purely so the check is visible in the file.

Whether the anchor was held fixed during ProteinMPNN sequence design or merely restrained, and
whether the anchor was restrained to a *sequence* consensus, a *structural* pose, or both, is
**NOT RECORDED**.

### Scaffold extension

The anchor is extended into a **four-helix bundle** carrying it, giving the 140-residue
miniprotein *(campaign description; the file records no secondary-structure annotation, so the
bundle topology is not verifiable from the artifact)*. Helix lengths, loop lengths, the register
at which the anchor joins the bundle, and whether the bundle length was fixed at 140 by design or
selected are **NOT RECORDED**. All 50 packaged designs are 140 residues, so the length was at
least uniform across the packaged set *(verified in the file)*.

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

Which structure predictor produced these three runs, at what version, with what MSA or
single-sequence setting, how many seeds or recycles, and what receptor construct was used
(full-length P43220, the extracellular domain only, or a cryo-EM-derived model) are **NOT
RECORDED**. The `b_complex` field takes two values across the 50 designs, `b_complex_a.json` and
`b_complex_b.json`; what distinguishes variant *a* from variant *b* is **NOT RECORDED**. All 10
deposited designs use variant *a*.

## Metric definitions

Standard definitions are given where the metric name is a published one. **The implementation
that produced each number is not recorded**, so these definitions describe what the name
conventionally means, not what the pipeline provably computed.

**From the bound prediction**

- `iptm`: interface predicted TM-score, the predictor's confidence in the relative placement of
  the two chains. Range 0 to 1, higher is better. Deposited 10: 0.9033 to 0.9465.
- `ipsae`, `ipsae_cons`: ipSAE is an interface-restricted score derived from the predicted aligned
  error matrix, designed to be less length-biased than ipTM. Higher is better. The `_cons` variant
  is **NOT DEFINED** in the artifact; the name suggests restriction to the consensus anchor
  region, but that is an inference, not a sourced fact. Deposited 10: `ipsae` 0.8870 to 0.9167,
  `ipsae_cons` 0.5583 to 0.8619.
- `iplddt`: mean pLDDT over interface residues in the complex. Higher is better. Which residues
  count as interface, and at what distance cutoff, is **NOT RECORDED**. Deposited 10: 0.8476 to
  0.8758.
- `plddt_binder`, `plddt_design`: mean pLDDT over the binder chain and over the designed segment,
  in the complex prediction. The two differ by a median of +0.0025 over all 50, so the two windows
  overlap almost completely; the exact residue windows are **NOT RECORDED**. Deposited 10:
  0.8836 to 0.9223 and 0.8866 to 0.9249.
- `pdockq`: predicted DockQ, a published composite of interface pLDDT and the number of interface
  contacts used as a proxy for docking quality. Higher is better. The exact formula variant and
  the contact cutoff are **NOT RECORDED**. Deposited 10: 0.6236 to 0.6684.
- `min_dist`: minimum interatomic distance across the interface, in angstrom. Which atom types
  are considered is **NOT RECORDED**. Deposited 10: 2.39 to 3.36 A, which is in the range of a
  close contact rather than a clash.
- `motif_rmsd`: RMSD of the 10-residue anchor, in angstrom, against its intended agonist pose.
  Lower is better. **The reference structure against which it is measured is NOT RECORDED.**
  Deposited 10: 0.564 to 1.415 A.
- `receptor_rmsd`: RMSD of the receptor, in angstrom, against a reference that is **NOT
  RECORDED**. Over all 50 it spans 2.07 to 4.20 A with a standard deviation of 0.31 A, so it is
  close to constant and carries little design-to-design signal. Deposited 10: 3.028 to 3.63 A.
- `hotspots` and `hot_list`: the number and the indices of the targeted hotspot residues.
  `hotspots` equals `len(hot_list)` for all 50 *(verified in the file)*. The index set is constant
  within each `source` (p13 gives `[27, 42, 86, 95]`, p3 gives `[86, 87, 88, 89]`, p10 and p12
  give `[27, 42, 86]`), so this field reads as a per-sub-campaign **design input**, not a
  per-design measured outcome. Whether the indices number receptor or binder residues, and in
  what numbering scheme, is **NOT RECORDED**.
- `q_full`, `q_designed`: **NOT DEFINED** anywhere in the artifact. Both are small integers
  (`q_full` 3 to 7, `q_designed` 5 to 8) and `q_designed - q_full` equals exactly 2 in 49 of the
  50 designs. No definition is quoted here because none can be sourced.

**From the alone prediction**

- `mono_plddt`, `mono_plddt_designed`: mean pLDDT over the whole chain and over the designed
  segment, predicted as a monomer. Higher is better; it reports whether the design folds on its
  own. `mono_plddt_designed` exceeds `mono_plddt` by a median of +0.023 over all 50, consistent
  with the designed window excluding a lower-confidence terminal region, though that is an
  inference. Deposited 10: 0.8345 to 0.9368 and 0.8602 to 0.9518.
- `rmsd_all`, `rmsd_domain`: RMSD in angstrom between the monomer prediction and the bound
  conformation, over all residues and over a "domain" subset. Lower is better. **The residue
  window called "domain", and the superposition frame used for each, are NOT RECORDED.** This
  matters: `rmsd_domain` is tight (0.224 to 2.128 A in the deposited 10) while `rmsd_all` is
  strongly bimodal over the 50, with 23 designs below 10 A and 27 between 12.9 and 21.4 A and a
  clean gap in between. See `MINI_REPORT.md`.

**From the self prediction**

- `self_iptm`: ipTM of the design against a copy of itself. **LOW IS GOOD.** This is the
  self-association control. Deposited 10: 0.1226 to 0.467; cohort median 0.262, and the cohort
  reports only 1 design of 210 at or above 0.80.
- `self_contacts`: number of inter-chain contacts in that self prediction. The contact definition
  and distance cutoff are **NOT RECORDED**. Lower presumably indicates less self-association, but
  it is not independent of `self_iptm`. Deposited 10: 325 to 1526.

**Composite**

- `score`: the pipeline's own ranking score. **The formula, the terms it combines and their
  weights are NOT RECORDED.** Deposited 10: 0.7408 to 0.7864.

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

The thresholds behind "gated" and "full epitope", and the path from 210 refolds to the 50 packaged
designs, are **NOT RECORDED**. The medians over the 50 packaged designs are close to the reported
cohort medians (monomer pLDDT 0.8695 vs 0.88; domain RMSD 0.4225 vs 0.42; self-ipTM 0.2452 vs
0.262; receptor ipTM 0.9233 vs 0.923), which is consistent but is not a check, since the two
populations differ.

## Selection of the deposited 10

The 10 deposited mini designs are those carrying `rank` 1 to 10 in the artifact, taken as the
artifact supplies them. **No re-ranking, re-scoring or re-weighting was performed in XenoDesign1.**

One property of that field must be stated, because it changes what the selection means: `rank` is
**not** a global ordering on `score`. The file is two independently sorted blocks, ranks 1 to 34
(sources p13 and p3, `score` falling 0.7864 to 0.1245) and ranks 35 to 50 (sources p10 and p12,
`score` falling 0.9122 to 0.7167). Taking ranks 1 to 10 therefore takes the top of the first block
only and leaves out 7 designs whose `score` is higher than that of rank 10, including the highest
`score` in the whole file. Whether `rank` encodes a deliberate preference for the p13/p3 rounds,
or whether the two blocks were simply concatenated, is **NOT RECORDED**, and is the first question
for Gianmattia in `MINI_REPORT.md`.
