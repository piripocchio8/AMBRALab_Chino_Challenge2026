# Target 1 — EGFR domain III, pH-selective binders

Twenty de novo binders submitted against **EGFR domain III**, the competition construct
**UniProt P00533 residues 334–494**. The objective is not affinity alone but **pH selectivity**:
binding that differs between the acidic tumour microenvironment and blood pH, by engaging a
histidine whose imidazole is protonated at the lower pH and neutral at the higher one.

```
micro/          8 designs under 40 residues   — disulfide-cyclised peptides, target His358
mini/           4 designs 40–100 residues     — scaffolded proteins, target His433
large/          8 designs over 100 residues   — scaffolded proteins, target His433
docs/           the methods for each series
submission.csv  the submitted file: 20 ranked rows, exactly name/sequence/molecule_class
metrics_full.csv  the same 20 rows with every metric they were selected on
```

## Why these are worth bench time

**Two independent shots for the price of one entry, and they are not variations on a theme.** The
two series target different histidines by different chemistries, from pipelines that share no
machinery. Neither can take the other down with it.

**One of them reaches a site and a size the standard pipeline could not.** The scaffolded route —
RFdiffusion3 backbones, ProteinMPNN sequences, the current standard — produced nothing below 60
residues and could not aim at His358; it targets His433. The micro series is **12–39 residues** and
engages **His358**, a site whose double-carbonyl motif is about **six times rarer** in the PDB than
the carboxylate-bridged arrangement the scaffolded route uses. Both pipelines were run against the
same protein; only one of them could address this site at this size. The micro designs also come
from a different method — sequences optimised directly against the structure oracle by an
evolutionary algorithm, then refined by interaction-preserving inverse folding with CARBonAra, rather
than diffused backbones threaded with a sequence model.

**The micro band is cheap and fast to falsify.** Eight disulfide-cyclised peptides of 12–39 residues
are solid-phase synthesis, not expression — no cloning, no insoluble prep — and the pH question is
answered by running one binding assay in two buffers. Whatever the answer, it arrives quickly.

**The mechanism predicts a direction, not just an affinity.** These designs accept hydrogen bonds
from the protonated imidazolium, an interaction that exists only while the ring carries its proton.
That commits us to a sign: tighter at acidic pH, weaker at pH 7.4. A flat or inverted result refutes
the design hypothesis, which is more informative than an unexplained binder.

**The selection evidence is reproducibility, not a best model.** Every design was refolded many
times from scratch and ranked on the *rate* at which the interaction reappears, on how tightly the
refolds agree on a single pose, on the interface confidence against **both** orthologs, and on
whether it is the same structure in both. Every micro design carries **45 human and 30–35 mouse
models**; the top one scores ipSAE **0.368 on human and 0.390 on mouse** and differs by **0.25 Å**
between its two bound conformations. Designs that looked excellent on one model, or on one species, were dropped on exactly this
test — including the single most reproducibly docked peptide we have, which turned out to be
extended in every one of its mouse models and is therefore not submitted.

**The micro designs were never tuned on the sequence they are scored against.** That campaign ran
against the **mouse** ortholog; the human challenge sequence was used only afterwards to evaluate
what already existed, with no re-optimisation. Their behaviour on human EGFR is transfer rather than
a fit to the evaluation target, and the same molecules are directly testable in mouse models.

## Two series, two histidines, two mechanisms

The submission deliberately covers **two different sites** rather than one site twice. They are
independent: a failure of either says nothing about the other.

| | micro | mini and large |
|---|---|---|
| target histidine | **His358** UniProt (mature His334) | **His433** UniProt (mature His409) |
| mechanism | **main-chain carbonyls accept** from the protonated imidazolium's two N–H donors | **salt bridge** from the imidazolium to an engineered carboxylate, plus a reciprocal His–Asp anchor |
| scaffold | disulfide-cyclised peptide, 12–39 residues | motif-scaffolded de novo protein, 60–134 residues |
| methods | [`docs/methods_micro.md`](docs/methods_micro.md) | [`docs/methods_mini_large/`](docs/methods_mini_large/) |

The mini and large bands were refreshed from the source series on 6 Oct 2026, when it grew from
fourteen designs to twenty-three with a fifth design round. That round enforces an amino-acid
**composition envelope** — taken from experimentally confirmed sub-micromolar all-alpha EGFR binders
— *before* any folding, rather than resurfacing designs afterwards, and a later pass removed 18
unpaired buried cysteines across 12 designs. Eight of the twelve designs carried here come from
rounds 4–5. Interface confidence across the band is close to equal on the human and mouse orthologs
(ipSAE 0.83–0.90 against 0.79–0.89), which is the cross-reactivity property the challenge asks for.

> `pHsel-NN` names were **reassigned** in that revision: a name does not refer to the same molecule
> it did before. Designs are matched by sequence, and each carries its source rank and local id.

The two sites are 75 residues apart in sequence. His358 is the more demanding of the two: the
double-carbonyl arrangement the micro series builds occurs in **0.455 %** of histidines in the PDB,
about one in 220, where the carboxylate-assisted arrangement the other series uses is six times more
common.

## Numbering

The construct is UniProt P00533 334–494, so for a local residue *n* in these files:

> local *n* = UniProt *n* + 333 = mature EGFR *n* + 309

The micro series' target histidine is local 25 = UniProt 358 = mature 334.

## What each design directory contains

Micro designs carry the five predicted models of the fold they were measured on — `human_selected.cif`
is the one the metrics refer to and `human_model_*.cif` the rest — plus `metrics.json` and
`sequence.fasta`. Mini and large designs carry two independent folds of the human complex, a fold of
the mouse ortholog, the scaffold backbone, and the confidence, ipSAE, PAE and pLDDT data for each.

The spread across models is included on purpose. A single predicted structure of a designed peptide
is one draw from a stochastic process, and several designs in this work looked convincing on one
model and collapsed over fifteen.

## What these numbers are, and are not

Every value in `metrics_full.csv` and in each `metrics.json` is a property of a **structure
prediction**. **No design in this submission has been tested experimentally** — there are no binding
measurements, no pH titrations and no expression data. The methods documents state the selection
criteria, the failures, and what was measured rather than assumed.
