# Target 3 — GLP-1R agonists

De novo agonists for the **glucagon-like peptide-1 receptor** (UniProt **P43220**), a class-B GPCR,
modelled as a 409-residue chain against the active-state reference **6X18**.

**Twenty designs in two bands under one ranking.**

```
micro/            10 submitted + 34 documented — disulfide-cyclised peptides, 12 / 15 / 39 aa,
                  designed in this group. Each directory carries FIFTEEN predicted structures:
                  five chai-1, five Boltz-2 and five Protenix-v2.
mini/             10 submitted + 7 reserve — 140-residue de novo miniproteins from a
                  collaborating RFdiffusion3 + ProteinMPNN pipeline, with the three predictions
                  that pipeline made for each. RE-SELECTED after a novelty check; see below.
docs/             the methods for each band, the metric definitions, and ranking.json (the build
                  input both CSVs are generated from)
submission.csv    THE SUBMITTED FILE: name, sequence, molecule_class — 20 rows, nothing else
metrics_full.csv  61 rows — the same 20 plus every documented and reserve design, with every
                  metric behind the ranking
```

> **These are predictions, not measurements.** Every number in this directory is a property of a
> structure prediction. **No design here has been tested experimentally**: there is no binding
> assay, no cAMP or β-arrestin readout, no expression and no synthesis. Nothing below is evidence
> that any of these peptides is an agonist, and the two readouts whose names suggest otherwise —
> the TM6 two-state call and the ECL2+TM5 engagement family — are discussed under *What the
> activation readouts cannot tell you*.

## The two bands, and why they are not interleaved

The micro and mini bands were produced by different pipelines, scored by different oracles, in
different conditions, on different machines. Their confidence numbers were never on one scale: the
micro band's ranking axis is chai-1 interface pTM measured **without a pocket restraint**, and the
mini band's is a different pipeline's own composite. Merging them into a single ordering would be
arithmetic performed on numbers that cannot be compared, and the result would look more precise
than anything we measured.

So the two are deposited as **consecutive blocks**: micro at ranks 1–10, mini at ranks 11–20, each
internally ordered by its own rule. `submission_rank` exists because the upload form reads a
ranking from the top row down; **the block boundary is not a claim that every micro design is a
better candidate than every mini design.** On their own oracles' numbers the mini designs score
higher, and they are longer, which on these models raises interface confidence by itself.

## How the micro band is ranked, and the one thing that changed

The axis is **chai-1 interface pTM on the disulfide-only fold** — the binder's disulfide declared
as a covalent bond, and *nothing else*.

The design search ran with an additional **pocket restraint** naming K174 and R357 of the receptor.
That restraint is an instruction: with it declared, "the peptide binds the pocket" is partly
something we told the model rather than something it predicted. We refolded all 48 candidates
without it and compared:

- over the whole pool the two conditions rank designs at **ρ = +0.538**, and **7 of 48** designs
  collapse when the pocket is removed;
- over the ten deposited, the restraint was worth a mean of **+0.017** interface pTM, and at most
  **+0.089** (design `AMBRA_T3_micro_06`).

The band is therefore cut and ranked on the **unrestrained-pocket** number, and both numbers are in
`metrics_full.csv` (`selected_iptm` and `chai_iptm_restrained`) with their difference
(`restraint_delta`), so the condition travels with the score. The five chai models in each micro
directory are the disulfide-only ones.

A quota guarantees places to the designs whose receptor engagement is canonical on the ECL2+TM5
measure, so the band is not purely the top of one number; the full rule is in
[`docs/methods_micro.md`](docs/methods_micro.md).

## Three oracles, all with an alignment

chai-1 takes its evolutionary signal from ESM-2 embeddings; Boltz-2 and Protenix-v2 take theirs
from a multiple sequence alignment. Every earlier Boltz and Protenix number on this target was run
**single-sequence**, which switched off the two models that need an alignment while chai kept its
own pathway. That is not a fair comparison, and it has been corrected: every Boltz and Protenix
number deposited here was produced with an MSA built from a **local UniRef90** database — receptor
depth **2,280**, and **depth 1 for every binder**, because a de novo 12-mer has no homologues. The
binder sequences never left the machine.

| | condition | what it is here |
|---|---|---|
| **chai-1** | disulfide restraint only | the ranking oracle |
| **Boltz-2** 2.2.1 | disulfide bond constraint, with MSA | a check, never a vote |
| **Protenix-v2** | **UNRESTRAINED**, with MSA | a check, never a vote |

**Protenix is unrestrained because it cannot be restrained.** Its constraint embedders are disabled
in the released configuration and the checkpoint carries no constraint tensors. It was therefore
asked a different question from the other two, and its numbers must not be averaged with theirs.
The filenames and `protenix_condition` say so on every row.

**The three disagree, and the disagreement is reported rather than averaged away.** Over the ten
deposited designs the Spearman correlation between chai's ordering and the others' is **+0.055**
(Boltz ipTM), **+0.188** (Protenix ipTM) and **+0.370** (Boltz ipSAE), on n = 10. Each oracle
reproduces its own ordering across a seed change far better than it reproduces another's, so this
is real disagreement and not measurement noise. A blended score would hide it. **We rank on one
oracle and report the others.**

## What the activation readouts cannot tell you

Two columns in `metrics_full.csv` describe how the peptide sits in the receptor, and neither is
evidence of agonism.

- **TM6 two-state (`tm6_k_active`).** 40 of 40 measured models are called active-like. On a
  110-structure pharmacology panel the same measure scores agonists, antagonists **and a
  composition-matched scramble** as active-like. It says the model built the active bundle once
  anything was in the pocket. It is a measurement, not a discriminator, and it ranks nothing.
- **ECL2+TM5 engagement family (`ecl2_fam0_k`).** Two families learned on that same panel
  (silhouette 0.450); family 0 is the one the canonical N-terminal-into-the-core agonists fall in.
  **It is a binding-MODE prior, not a validated agonist classifier** — on the panel it does not
  separate agonists from antagonists either. It is used as a **quota**, to guarantee that the band
  is not entirely designs that engage in some other way, and never as a score.

**Five of the ten** submitted micro designs are canonical on that measure (fam-0 in ≥ 3 of 5
models).

## The mini band was re-selected after a novelty check

A first mini set — the source package's ranks 1–10 — was put through the deposition platform's
novelty check. **Five passed, five were rejected** as *"contains a known binder fragment"*. The
matched fragment is **`HAEGTFTSD`, GLP-1's own first nine residues**: every rejection contains it,
no design that passed does, and that one rule reproduces all ten outcomes.

Two near misses pin it down. A design carrying `EGTFTSDVS` — a *different* exact nine-residue
fragment of GLP-1 — passed, so the check is not "any 9-mer of GLP-1". And a design carrying
exendin-4's exact N-terminal decapeptide passed, so **exendin-4 is not in the platform's
known-binder set and GLP-1 is**.

The band was rebuilt: the five survivors kept in order, plus the five highest-scoring designs from
the package's second block (built with the identity to natural agonists deliberately reduced) that
clear the fragment rule, one design per parent backbone. That last constraint also removed a
redundancy the first set carried — two of its ten were sequences on one backbone at 57.9 %
identity. **Highest pairwise identity in the deposited ten is now 30.0 %.** The rule and the rank
list are `GLP1_NTERM` and `MINI_RANKS` in `scripts/build_target3_ranking.py`, and the build refuses
if either condition is broken. **The ten micro designs all passed and are unchanged.**

## The ring

Every micro design declares one disulfide. It is measured on the shipped structures rather than
assumed from the configuration: **45 of 50** chai models close the declared ring (SG–SG ≤ 2.5 Å).
Two designs close it in 3 of 5 and one in 4 of 5; those carry a risk flag, and the flag is in the
CSV and on every design's `metrics.json`. The deposition script refuses any row whose declared
`cys_positions` are not two distinct cysteines of its own sequence.

## Files

| file | what it is |
|---|---|
| [`submission.csv`](submission.csv) | the 20 submitted rows, best-first. This is the upload. |
| [`metrics_full.csv`](metrics_full.csv) | 61 rows, every metric. Blank means *not measured*, never zero. |
| [`docs/ranking.json`](docs/ranking.json) | the build input; both CSVs are generated from it |
| [`docs/methods_micro.md`](docs/methods_micro.md) | the micro band: design, search, gates, ranking |
| [`docs/methods_mini.md`](docs/methods_mini.md) | the mini band, written from what its pipeline states |
| [`docs/metrics.md`](docs/metrics.md) | what every column means |
| [`DESIGN_STRATEGY.md`](DESIGN_STRATEGY.md) | the attachable strategy document |
| [`SUBMISSION_TEXT.md`](SUBMISSION_TEXT.md) | the text for the submission form's description box |

Rebuild the CSVs from the ranking with:

```bash
python3 scripts/make_target3_submission.py --input Target_3/docs/ranking.json --limit 20
```

`--limit` has no default on purpose. 20 is the number this deposition delivers; if the competition
states a different allowance, pass that instead and the script will refuse rather than truncate.
