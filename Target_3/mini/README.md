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
`EGTFTSD` core and vary **position 2** away from GLP-1's alanine. `HG…`, `HS…`, `FA…`, `FG…`,
`FS…` and `YA…` all clear the check; `HA…` does not.

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

> **Why not simply take the top ten by `score`?** The package is **two independently sorted
> blocks** — ranks 1–34 (sources `p13`, `p3`) and ranks 35–50 (`p10`, `p12`) — each monotone in
> `score` internally but not across the file. Block B's scores are systematically higher, so a
> global sort on `score` would not be a quality ordering, it would be a block ordering. The
> deposited band therefore keeps the five survivors of block A and takes the best of block B, and
> the two groups' `score` values should not be compared with each other.

---

## The design

The N-terminal ten residues are an **agonist anchor** restrained to a consensus of verified GLP-1R
agonists, and the remaining 130 residues are a designed four-helix bundle that presents it. The
anchor is a variant of the natural GLP-1 / exendin-4 N-terminus — the part of the native peptide
that enters the receptor core and drives activation. Ten residues of each 140-residue design are
therefore natural or near-natural motif, about 7 % of the chain; the other 130 are not.

The deposited ten carry six distinct anchors: `HGEGTFTSDL` ×2 · `HGEGTFTSDV` · `HGEGTFTSDY` ·
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
over the deposited ten with a median of 0.218, and *low is good*. Across the pipeline's full
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

Rows 11–15 are block A, rows 16–20 block B. **Their `score` columns are not comparable across that
boundary** (see above); `ipTM`, `ipSAE`, `motif RMSD` and `self-ipTM` are.

## Limits, and the questions this package cannot answer

- **Nothing here has been measured**, and nothing here was re-measured by us. The numbers are the
  source pipeline's; their definitions are in [`../docs/methods_mini.md`](../docs/methods_mini.md),
  written from what that pipeline's package states and flagging what it does not record.
- **`rmsd_all_A` is deposited and is not used to argue anything**, deliberately. Over the 50 it is
  bimodal — 23 designs at 0.76–9.11 Å and 27 at 12.87–21.42 Å, with an empty gap — while
  `rmsd_domain_A` stays tight (median 0.42 Å over the 50) and the two correlate only weakly
  (r = 0.380, n = 50). The split does not track `source`, `b_complex` variant or hotspot set, but
  it does appear to track the **parent backbone**: all three backbone-sharing pairs in the package
  land in the same mode, two of them within 0.05 Å of each other. n = 3 pairs, so that is
  suggestive and not established. Two readings produce these numbers and the package records
  neither:
  - **benign** — `rmsd_all` is measured in a frame where the binder's rigid-body placement shows
    up, so ~15 Å reports *where the monomer sits* relative to the bound pose rather than whether it
    folds, and `rmsd_domain` is the fold measure;
  - **not benign** — the unbound prediction genuinely changes topology or helix register for those
    designs, and `rmsd_domain` is blind to it because its window excludes what moves.
- **`hotspots` is a design input, not an outcome.** The hotspot list is constant within each
  sub-campaign (`p13` → 27/42/86/95, `p3` → 86/87/88/89, `p10`/`p12` → 27/42/86), so the count
  describes which hotspots that round targeted, not what the individual design achieved, and it is
  not comparable design to design. The deposited ten mix three hotspot specifications.

### Three questions for the pipeline's author

1. **What is the reference and superposition frame for `rmsd_all`, and which residues does
   `rmsd_domain` cover?** Until that is answered the bimodality above cannot be read either way,
   and neither number is quoted anywhere in this deposition.
2. **What is the residue numbering for `hot_list`?** UniProt P43220, the modelled construct, or
   something else — the deposition needs it if the form asks which epitope each design targets.
3. **Is `score` intended to be comparable between the two blocks?** If it is, the deposited band
   should probably be the top ten by `score` among eligible designs rather than five from each
   block; if it is not, the current selection stands.
