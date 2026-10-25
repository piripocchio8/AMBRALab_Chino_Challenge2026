# Target 3 — mini band

**Ten de novo miniproteins of 140 residues, each presenting a ten-residue agonist anchor on the
N-terminus of a designed helical bundle.** Produced by a collaborating RFdiffusion3 + ProteinMPNN
pipeline run **outside** this repository. Seven further designs are documented here as reserves.

> **Nothing in this directory was folded, scored or re-measured in this repository.** Every number
> is the source pipeline's own, copied verbatim, and every structure is one it produced. Where this
> repository added a field it says so in each `metrics.json` (`binder_length` and `anchor_seq` are
> computed here from the sequence; nothing else is).

---

## The novelty check, and what it taught us about the anchor

**This band was re-selected.** A first set of ten — the source package's ranks 1–10 — was put
through the deposition platform's novelty check. **Five passed and five were rejected**, each
rejection reading *"contains a known binder fragment"*.

The split is exact and it is informative:

| source rank | anchor | verdict |
|---|---|---|
| 1 | `HGEGTFTSDL` | passed |
| 2 | `HGEGTFTSDV` | passed |
| 3 | `HAEGTFTSDL` | **rejected** |
| 4 | `HSEGTFTSDL` | passed |
| 5 | `HAEGTFTSDV` | **rejected** |
| 6 | `HAEGTFTSDL` | **rejected** |
| 7 | `HAEGTFTSDK` | **rejected** |
| 8 | `HSEGTFTSDY` | passed |
| 9 | `HAEGTFTSDY` | **rejected** |
| 10 | `HSEGTFTSDY` | passed |

**The matched fragment is `HAEGTFTSD` — GLP-1's own first nine residues.** Every rejection contains
it; no design that passed does. That single rule reproduces all ten outcomes, and two near misses
show it is that fragment specifically rather than general similarity to a natural agonist:

- **Rank 2 carries a different exact nine-residue fragment of GLP-1** — `EGTFTSDVS`, GLP-1
  residues 3–11 — and it **passed**. So the check is not simply "any 9-mer of GLP-1".
- **Rank 1 carries exendin-4's exact N-terminal decapeptide** `HGEGTFTSDL` and it **passed**. So
  **exendin-4 is not in the platform's known-binder set**; GLP-1 is.

The practical consequence for anyone designing against this target: an anchor may keep the
`EGTFTSD` core and vary **position 2** away from GLP-1's alanine. `HG…` and `HS…` were observed to
clear the check, and `HA…` was observed to fail. All ten designs in the first set began with His, so
anchors that differ at position 1 (`FA…`, `FG…`, `FS…`, `YA…`) were never submitted to it; they
avoid `HAEGTFTSD`, so they should clear it if the rule above is right, but that is an inference
from the rule and not an observed outcome. Three of the deposited ten (`AMBRA_T3_mini_06`, `_08`
and `_10`) begin with Y or F and rest on that inference, and no outcome of a platform check on the
rebuilt band is recorded here.

### How the replacements were chosen

1. **Exclude every design containing `HAEGTFTSD`.** That is 15 of the 50 in the package.
2. **Keep the five that passed**, in their original order.
3. **Take the five highest-scoring eligible designs from the package's second block** (source ranks
   35–50) — the set built with the sequence identity to the natural agonists deliberately reduced.
4. **One design per parent backbone.** Source rank 41 outscores rank 42 and is *not* deposited: it
   shares a parent backbone with rank 35. This follows the pipeline author's own instruction to
   select for fold diversity if the first set had to be replaced, and it also removes a redundancy
   the first set carried — its ranks 1 and 9 were two sequences on one backbone, 57.9 % identical.
   **Highest pairwise identity in the deposited ten is now 30.0 %.**

The rule and the rank list live in `scripts/build_target3_ranking.py` as `GLP1_NTERM` and
`MINI_RANKS`; the build refuses outright if any chosen design carries the fragment or if two of
them share a backbone.

> **Why five from each block?** The package's `rank` is not a score ordering. It was sorted by
> hotspot count first and `score` second, so ranks 1–34 (sources `p13`, `p3`, 4 of 4 hotspots,
> block A) all sort above ranks 35–50 (`p10`, `p12`, 3 of 3, block B) whatever their `score`;
> within each block `rank` follows `score`. `score` itself is normalised once over the campaign's
> whole gated set, so it **can** be compared across the two blocks; `rank` is what cannot. A pick
> by rank would have come from block A alone and left out 3-of-3 designs that score higher than
> source rank 10 (`AMBRA_T3_mini_06` scores 0.9122, against 0.7408 for source rank 10). The
> deposited band therefore keeps the five survivors of block A and takes the five best eligible
> designs of block B. The reason is that `rank` is not a score ordering, not that the two blocks'
> scores cannot be compared; a global sort on `score` among eligible designs would also have been
> defensible (see the author's third answer below), and the selection was left as it was made.

---

## The design

The N-terminal ten residues are an **agonist anchor** restrained to a consensus of verified GLP-1R
agonists, and the remaining 130 residues are a designed four-helix bundle that presents it. The
anchor is a variant of the natural GLP-1 / exendin-4 N-terminus — the part of the native peptide
that enters the receptor core and drives activation. Ten residues of each 140-residue design are
therefore natural or near-natural motif, about 7 % of the chain; the other 130 are not.

The deposited ten carry eight distinct anchors: `HGEGTFTSDL` ×2 · `HGEGTFTSDV` · `HGEGTFTSDY` ·
`HSEGTFTSDL` · `HSEGTFTSDY` ×2 · `YAEGTFTSDY` · `FAEGTFTSDV` · `FAEGTFTSDL`.

## The three predictions per design

The pipeline folded each design three ways, and all three are deposited:

| file | what it is | what a good result looks like |
|---|---|---|
| `complex.pdb` | the design bound to the receptor | high interface confidence, low motif RMSD |
| `alone.pdb` | the design by itself | the designed fold, unaided |
| `self_pair.pdb` | the design against a **copy of itself** | **a LOW interface score.** This is a self-association check: a design that binds itself competes with binding the receptor |

**Chains in these files are A = binder, B = receptor** — the opposite of the micro band's
convention, because they were written by a different pipeline. They are deposited as produced.

The self-association arm is the one that is easiest to misread: `self_iptm` runs **0.123–0.467**
over the deposited ten with a median of 0.200, and *low is good*. Across the pipeline's full
210-refold cohort only **1 of 210** designs reached 0.80. `AMBRA_T3_mini_05` (0.467) and
`AMBRA_T3_mini_07` (0.428) are the two highest here and are the two to watch.

## What is in each directory

`AMBRA_T3_mini_01` … `AMBRA_T3_mini_10` are the submitted band; `AMBRA_T3_mini_reserve_01` … `_07`
are documented reserves, every remaining block-B design that clears the fragment rule.

| file | what it is |
|---|---|
| `complex.pdb`, `alone.pdb`, `self_pair.pdb` | the three predictions above |
| `sequence.fasta` | the sequence under its deposited name, with the source pipeline's tag |
| `metrics.json` | every number quoted for the design, plus a provenance block |

The source pipeline's own identifiers (`p15_01_sh8_p13_04_…`) are kept in `sequence.fasta`,
`metrics.json` and the `notes` column of `../metrics_full.csv`, so any row here can be traced back
to the campaign that produced it.

## The band, as the source pipeline reports it

| # | design | source rank | ipTM | ipSAE | motif RMSD Å | mono pLDDT | self-ipTM | score | anchor |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| 11 | `AMBRA_T3_mini_01` | 1 | 0.9465 | 0.903 | 0.60 | 0.854 | 0.181 | 0.7864 | HGEGTFTSDL |
| 12 | `AMBRA_T3_mini_02` | 2 | 0.9166 | 0.902 | 0.74 | 0.878 | 0.171 | 0.7822 | HGEGTFTSDV |
| 13 | `AMBRA_T3_mini_03` | 4 | 0.9404 | 0.890 | 0.56 | 0.870 | 0.123 | 0.7641 | HSEGTFTSDL |
| 14 | `AMBRA_T3_mini_04` | 8 | 0.9036 | 0.887 | 0.62 | 0.837 | 0.212 | 0.7560 | HSEGTFTSDY |
| 15 | `AMBRA_T3_mini_05` | 10 | 0.9033 | 0.888 | 0.65 | 0.865 | 0.467 | 0.7408 | HSEGTFTSDY |
| 16 | `AMBRA_T3_mini_06` | 35 | 0.9458 | 0.911 | 0.53 | 0.903 | 0.223 | 0.9122 | YAEGTFTSDY |
| 17 | `AMBRA_T3_mini_07` | 36 | 0.9451 | 0.915 | 0.90 | 0.933 | 0.428 | 0.8613 | HGEGTFTSDL |
| 18 | `AMBRA_T3_mini_08` | 38 | 0.9392 | 0.914 | 0.96 | 0.860 | 0.140 | 0.8393 | FAEGTFTSDV |
| 19 | `AMBRA_T3_mini_09` | 39 | 0.9375 | 0.903 | 0.56 | 0.861 | 0.256 | 0.8299 | HGEGTFTSDY |
| 20 | `AMBRA_T3_mini_10` | 42 | 0.9062 | 0.892 | 0.80 | 0.860 | 0.187 | 0.7408 | FAEGTFTSDL |

Rows 11–15 are block A (4 of 4 hotspots), rows 16–20 block B (3 of 3). The row number is a block
order, not a score order: `score` is on one scale across all ten rows (see above), so it can be
compared across that boundary. Rows 16–19 score above every row of 11–15, and row 20 (0.7408) equals
row 15 and sits below rows 11–14.

## Limits, and the questions put to the pipeline's author

- **Nothing here has been measured**, and nothing here was re-measured by us. The numbers are the
  source pipeline's; their definitions are in [`../docs/methods_mini.md`](../docs/methods_mini.md),
  written from what that pipeline's package states and its author's later written answers, and
  flagging what is still not recorded.
- **`rmsd_all_A` is deposited and is not used to argue anything**, deliberately. Over the 50 it is
  bimodal — 23 designs at 0.76–9.11 Å and 27 at 12.87–21.42 Å, with an empty gap — while
  `rmsd_domain_A` stays tight (median 0.42 Å over the 50) and the two correlate only weakly
  (r = 0.380, n = 50). The split does not track `source`, `b_complex` variant or hotspot set, but
  it does appear to track the **parent backbone**: all three backbone-sharing pairs in the package
  land in the same mode, two of them within 0.05 Å of each other. n = 3 pairs, so that is
  suggestive and not established. Two readings produce these numbers and the package records
  neither (the pipeline's author has since said which; see below):
  - **benign** — `rmsd_all` is measured in a frame where the binder's rigid-body placement shows
    up, so ~15 Å reports *where the monomer sits* relative to the bound pose rather than whether it
    folds, and `rmsd_domain` is the fold measure;
  - **not benign** — the unbound prediction genuinely changes topology or helix register for those
    designs, and `rmsd_domain` is blind to it because its window excludes what moves.
- **`hotspots` is a design input, not an outcome.** The hotspot list is constant within each
  sub-campaign (`p13` → 27/42/86/95, `p3` → 86/87/88/89, `p10`/`p12` → 27/42/86), so the count
  describes which hotspots that round targeted, not what the individual design achieved, and it is
  not comparable design to design. The deposited ten mix three hotspot specifications.

### The pipeline author's answers to the three questions

The three questions that stood here were put to the author of the pipeline, who answered in writing
from the scripts and run logs of campaign `p15_1099477` and its ancestors. The answers are the
author's and are sourced to scripts that were not seen here; nothing in them was re-measured in this
repository. The author notes that the handover package carried results only, and that the omissions
were the pipeline's fault for not exporting its own configuration, not the deposition's for
declining to guess.

1. **The reference and frame for `rmsd_all`, and the window for `rmsd_domain`.** `rmsd_all` is over
   all 140 residues and `rmsd_domain` over residues 30–140. Each is a Kabsch superposition computed
   over exactly the residue set being measured, with no separate frame and no reference beyond the
   two structures compared, which are the same design predicted bound and predicted alone.

   **Of the two readings above, the benign one is correct**, and the deposition was right not to
   quote `rmsd_all`. The construct is a long N-terminal stalk carrying the anchor plus a compact
   domain. Superposing across that hinge lets a rigid-body swing of the stalk dominate, even when
   the domain is unchanged. Moving the window shows it (n = 210):

   | window | median RMSD | within 3 Å |
   |---|---:|---:|
   | all 140 | 10.28 Å | 31 % |
   | 11–140 | 5.81 Å | 41 % |
   | 30–140 | 0.42 Å | 97 % |
   | 40–140 | 0.29 Å | 99 % |
   | 50–120 | 0.24 Å | 99 % |

   Over 30–140 the distribution is unimodal, not bimodal: 174 of 210 below 1 Å, 20 between 1 and 2,
   9 between 2 and 3, 7 between 3 and 5, none beyond. The topology does not change, so the
   not-benign reading, that the unbound prediction changes topology or helix register where
   `rmsd_domain` cannot see it, is not what the author found. One further piece of evidence is that
   monomer pLDDT is 0.584 over the anchor against 0.901 over the designed region (n not stated in
   the answers), so the part that moves is also the part the predictor is least sure of, which is
   what a flexible terminal segment looks like.

   Residues 11–140 is not a safe window either, despite being the obvious "designed region":
   dropping the anchor from the residue set does not remove its effect on the superposition, and the
   median is still 5.81 Å. Use 30–140 or tighter.

2. **The numbering of `hot_list`.** Receptor residues, 1-based in the modelled 409-residue chain.
   That chain is UniProt P43220 residues 24–432, so the UniProt number is the deposited number plus
   23. The hotspots were specified to RFdiffusion3 at atom level, not residue level; the atoms for
   each sub-campaign are in [`../docs/methods_mini.md`](../docs/methods_mini.md). The chain label
   `A` in that diffusion input is the receptor, which is not the labelling of the deposited
   structures; see the chain-order warning below.

3. **Whether `score` is comparable between the two blocks.** The blocks are not two rounds. The
   packaging step sorted by hotspot count first and then by `score` (`best_dir.py`, `--order tier`),
   so every design meeting 4 of 4 hotspots sorts above every design meeting 3 of 3 regardless of
   `score`. `p13` and `p3` target four hotspots and `p10` and `p12` three, so the two blocks are the
   two hotspot-set sizes. Within each block the ordering is by `score` and is meaningful. `rank` is
   therefore not a score ordering, and a design with 3 of 3 is not worse than one with 4 of 4: it
   targeted three points and hit all three.

   `score` itself is comparable between the blocks. It is one formula, the mean of three min–max
   normalised terms (anchor RMSD inverted, ipSAE, binder pLDDT), and the ranking script applies one
   min–max normalisation over the campaign's whole gated set (187 designs), not one per block, so it
   can be compared design to design across the whole packaged set, the 4-of-4 / 3-of-3 boundary
   included. This corrects the author's earlier answer that it could not. In `../metrics_full.csv`
   the two groups' scores do overlap: its five 4-of-4 designs score 0.7408 to 0.7864 and its twelve
   3-of-3 designs (five deposited, seven reserves) 0.7167 to 0.9122, which is consistent with one
   scale. The rescaling is computed within a campaign, so `score` cannot be compared across
   campaigns. The author's view is that keeping the blocks separate was right, that taking five from
   each block is a reasonable reading, and that a global sort on `score` among eligible designs
   would also be defensible. The deposited selection is therefore left as it was made, and the
   reason for it is that `rank` is not a score ordering, not that the blocks' scores are
   incomparable.

**A warning on chain order.** The author adds that chain labelling is not consistent between the
pipeline's tools, and that both chains restart at residue 1. Every script in the pipeline therefore
resolves chains by residue count and sequence, never by label: 140 is the binder, 409 is the
receptor. A re-measurement of these structures that selects on chain ID will silently read the wrong
chain.

### Two things measured after the handover

Neither was in the package, and both bear on how much weight the numbers above carry. Both are the
author's, from runs made after the package was handed over, and neither was re-measured here.

**Three-seed replication.** All 150 top-ranked designs were re-predicted at two further Boltz seeds
from byte-identical input (runs `p18s2_1106925` and `p18s3_1106926`). 132 of the 150 hold the gate
in all three seeds. Confidence values are stable between seeds: binder pLDDT moves by a median of
0.005 and ipSAE by 0.016. The geometry is not: anchor RMSD moves by a median of 0.48 Å and by up to
1.52 Å. Of 27 replicate-level failures, 24 are anchor RMSD and 3 are hotspot count; receptor RMSD
never fires.

The consequence is that a single prediction cannot tell you which designs are unstable. Separating
the 132 stable designs from the 18 unstable on replicate-1 values alone gives an AUC of 0.487 for
ipSAE and 0.468 for binder pLDDT, which is chance, with medians identical to three decimals. Only
the RMSD terms carry anything, and that is a restatement of the threshold.

Of the ten deposited designs, nine hold the gate in all three seeds. The exception is the design
with anchor `FAEGTFTSDV`, `AMBRA_T3_mini_08`: its anchor RMSD is 0.96 / 2.40 / 2.19 Å across the
three seeds, crossing the 2 Å threshold twice, while its ipSAE stays at 0.901–0.914. The gate is
defined in [`../docs/methods_mini.md`](../docs/methods_mini.md).

**ipSAE is near-blind to epitope adherence on this target.** It was measured three independent ways:
median ipSAE 0.882 at 4 of 4 hotspots against 0.871 at 0 of 4 over 1,200 folds; 0.894 against 0.870
over a second set of 480; and in the p15 gated set the ordering inverts. Epitope engagement is
therefore established by the geometric check alone, and ipSAE should only order a set already
verified that way. That is its role in the band table above: it orders designs that came from the
gated set, and it is not evidence that any of them engages the hotspots.
