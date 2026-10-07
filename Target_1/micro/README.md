# Target 1 — micro band

**Disulfide-cyclised peptides of 39 residues that bind EGFR domain III through the protonated
form of His358.**

Every other entry in this band is, in effect, a small protein. These are not. They are peptides
folded by a single disulfide and testable at two pH values in an afternoon. The band also held two
**12-residue** cyclic peptides, in the length bin where this competition's own EGFR dataset reports
its highest hit rate, until they were withdrawn — see the note at the end of this file.

## Why these are worth bench time

**They reach a size and a site the standard pipeline did not.** The scaffolded route in this same
submission — RFdiffusion3 backbones, ProteinMPNN sequences, the current standard — produced nothing
below 60 residues and nothing it could aim at His358; it targets **His433**, 75 residues away, by a
different chemistry. These designs are **39 residues** and engage **His358**. Two independent
pipelines were run against the same protein and only one of them could address this site at this
size. That is the result, not a footnote.

**The harder of the two motifs.** His433 is approached by a salt bridge to an engineered carboxylate.
His358 is approached by main-chain carbonyls accepting from the imidazolium — a motif that occurs in
**0.455 % of histidines in the PDB, about one in 220**, roughly six times rarer than the
carboxylate-bridged arrangement. The micro series is aimed at the less accessible target.

**The method is new, and is being published separately.** The design engine — a population-based
evolutionary optimiser scoring candidates directly against the structure oracle, with an
interaction-preserving inverse-folding refinement — is the subject of a manuscript in preparation, so
it is described here in principle rather than in reproducible detail, ahead of publication. Nothing
needed to judge these designs is withheld: sequences, structures, every per-model measurement, the
gates and their thresholds, and the designs we rejected are all here. What is held back is how the
candidates were generated, not how they were judged.

**A different method, and the reason it matters here.** Backbones were not diffused and threaded.
Sequences were optimised directly against the structure oracle by an evolutionary algorithm, then
refined by **interaction-preserving inverse folding with CARBonAra**: the specific contacts worth
keeping — hydrogen bonds, charge pairs, aromatic stacking, everything coordinated to the histidine —
were held fixed while the rest of the binder was repacked. Plain hydrophobic contact was explicitly
not protected. The leading designs come from that refinement step, not from the search: it recovered
compact backbones the search had found but could not encode in a sequence.

**The structure states the protonation.** Neutral imidazole has one N–H; the other ring nitrogen
holds a lone pair. A model in which **both** ring nitrogens donate to acceptors is only constructible
if the ring is the imidazolium. That is a far stronger statement than a predicted pKa, and it is what
these designs are selected on.

**The evidence is a rate, not a best model.** Each design carries **45 models against the human
target and 30–35 against the mouse one**, folded under its own restraints so the two numbers mean the
same thing — 5,849 predicted structures across the campaign. The top design scores ipSAE **0.368 on
human and 0.390 on mouse**: not a human binder that tolerates mouse, the same interaction in both. It
is **0.25 Å** between its human-bound and mouse-bound conformations, and **0.37 Å** between the
binder folded *alone* and the binder in its complex — the peptide already holds the binding-competent
fold, so the target does not have to fold it.

**They were never tuned on the sequence they are scored against.** The campaign ran against the
**mouse** ortholog; the human challenge sequence was used only afterwards to evaluate what already
existed. Their behaviour on human EGFR is transfer, not a fit to the evaluation target — and the same
molecules are directly testable in mouse models.

**They are cheap to falsify.** The pH question is answered by one binding assay in two buffers, and
the mechanism predicts the *direction* — tighter at acidic pH. A flat or inverted result refutes the
design hypothesis outright, which is more useful than a strong binder with no mechanism attached.
On length: these are expressed cell-free from synthetic DNA like every other entry, so they carry
the same expression route and not a privileged one — but length is the strongest negative expression
term in the competition's own 800-design EGFR dataset, and at 39 residues these sit well below the
length at which expression starts to fail.

## The mechanism, concretely

Numbering: local *n* = UniProt *n* + 333 = mature EGFR *n* + 309. The target histidine is local
**25** = UniProt **His358** = mature His334.

At acidic pH the imidazolium carries a hydrogen on both ring nitrogens, ND1 and NE2, and each is a
donor. The designs place acceptors to take them: one nitrogen engaged is a hydrogen bond, both is a
clamp that cannot form on the neutral ring. At pH 7.4 at most half the interaction survives, and the
geometry that accepts from a donor now faces an acceptor.

A hydrogen bond is treated as a **direction**, not a distance: 2.5–3.4 Å, within 45° of the in-plane
N–H vector, at least 2.9 Å from every ring carbon, within 1.2 Å of the ring plane. The ring-carbon
clause matters — an early design read 2.75 Å to NE2 while sitting 2.13 Å from ring carbon CE1, a
collision that a distance-only test scores as a hydrogen bond.

**Carboxylate acceptors are the strongest version of this.** A charged Asp/Glu on the ring is a
charge–charge interaction rather than a neutral hydrogen bond, and the measurements single it out:
across a controlled test, the only cases where a predicted pKa moves in the intended direction at all
are those with a binder carboxylate. Three designs present one to His358 in a substantial fraction of
models, one of them in both orthologs; that design is submitted.

## What is in this directory

One directory per design: the five predicted models it was judged on (`human_model_*.cif`), the one
the metrics refer to (`human_selected.cif`), `sequence.fasta`, and `metrics.json` carrying every
number quoted for that design, so anything in the submission CSV can be recomputed from the files
here.

## Limits

- **Nothing here has been measured.** Every number is a property of a structure prediction — no
  binding data, no pH titrations, no expression or synthesis results.
- **The bidentate clamp is rare in the predictions**, as the motif is rare in nature. Expect the pH
  dependence to be real but modest rather than switch-like.
- **Predicted pKa shifts are reported but not scored**, and the reason is given in
  [`../docs/methods_micro.md`](../docs/methods_micro.md) §10.4: propka credits each hydrogen bond at
  about half a pKa unit while burial of the histidine costs more than a unit, so it returns a
  negative shift for a geometry that cannot exist without the cation. The geometry is the evidence.
- **Three of the eight passed every selection gate but one** — the rate at which they make the
  designed bond on the human target (4 %, 13 % and 0 % against a 15 % floor). Each is marked with
  the gate it missed and by how much, in the `gate_waived` column, rather than the threshold being
  loosened to admit it. The other five pass every gate, and no design is admitted by maintainer
  override. It was one waiver before the withdrawal below; replacing two gate-passing designs cost
  us two more.
- **Two designs were withdrawn after selection, and this band is not the one our measurements
  chose.** Two 12-residue cyclic peptides passed every gate but the competition's novelty check
  **timed out** on both and could not be completed, while all eighteen longer designs scored. The
  likely cause is length: TM-score's normalisation, *d*₀ = 1.24·∛(*L* − 15) − 1.8, takes the cube
  root of a negative number below *L* = 15 and stays non-positive to *L* = 18, and it is TM-score
  that the novelty pipeline thresholds on. We could not reproduce the hang, so that is a hypothesis.
  Their folders, sequences and every measurement remain in this directory under
  `AMBRA_T1_micro_04` and `AMBRA_T1_micro_08`, and they are carried in `submission.csv` and
  `metrics_full.csv` alongside the rest so the supporting material documents all ten micro
  designs; the two were **deselected in the upload form** and are not part of the submission.
  `metrics_full.csv` says which is which in its `status` column, and only the twenty submitted
  carry a `submission_rank`. Their numbers are never reassigned to another molecule.
- **Six of the eight share one backbone**, across three lineages in all. That is a concentration
  risk and it is stated: if that backbone is wrong, half the band fails together. It is the lineage
  with equal interface confidence on both orthologs (ipSAE 0.368 human / 0.390 mouse), and all three
  oracles return it as one conformation.
- **EGFR domain III carries a free cysteine** (local 137). These peptides are disulfide-cyclised and
  one predictor paired a binder cysteine with it; no model from the primary oracle shows it, but it
  is a bench consideration.

Selection, metrics and the gates are in [`../docs/methods_micro.md`](../docs/methods_micro.md) and
[`../docs/metrics.md`](../docs/metrics.md).
