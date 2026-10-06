# Target 1 — micro band

**Disulfide-cyclised peptides, 12 to 39 residues, that bind EGFR domain III through the protonated
form of His358.**

Every other entry in this band is, in effect, a small protein. These are not. They are peptides
short enough to be ordered from a solid-phase synthesiser, folded by a single disulfide, and tested
at two pH values in an afternoon. If the panel has room for one cheap, fast, mechanistically
explicit entry alongside the expressed miniproteins, this is what that entry looks like.

## Why these are worth a slot

**They cost almost nothing to try.** A 28-residue cyclic peptide is chemical synthesis, not cloning,
expression, purification and refolding. No construct can fail to express; no prep can come back
insoluble. The whole band can be made as a plate of peptides, and a pH-dependence measurement needs
only the same binding assay run in two buffers.

**They make a falsifiable claim, not a confident score.** The designs do not merely sit near the
histidine. They present backbone carbonyl oxygens to the imidazolium N–H, which is an interaction
that exists only while the ring is protonated. That predicts the direction of the pH effect:
*tighter at acidic pH, weaker at pH 7.4.* If the measurement comes back flat, or inverted, the
design hypothesis is wrong and the experiment has said something. That is a more useful result than
a strong binder with no mechanism attached.

**The evidence behind them is reproducibility, not a single lucky model.** Each design was refolded
many times from scratch, and what is reported is the *rate* at which the interaction reappears, not
the best model found. The top-ranked design docks into the same pose in **40 of 45** independent
refolds of the human complex, a median 1.34 Å from its own best pose, and holds a confident
interface on **both** orthologs (ipSAE 0.42 human, 0.36 mouse). A single predicted complex with a
high confidence score carries none of that information.

**The ranking threw out our own best-looking design.** The most reproducibly docked peptide in the
whole pool — same pose in 45 of 45 human refolds, 1.03 Å, the highest human ipSAE we measured at
0.577 — is **not submitted**. It is compact in every one of its 45 human models and extended in
every one of its mouse models: two different structures, 9.9 Å apart, one per ortholog, and its
mouse interface confidence collapses to 0.076. Pooled across species that reads as "14 % of models
extended", which is how it survived an earlier filter. Measured per species it is not a cross-reactive
binder, so it was dropped. The designs that remain are the ones that behave the same way twice.

**They were not tuned on the sequence they are scored against.** The design campaign ran against the
**mouse** EGFR ortholog. The human challenge sequence was used only afterwards, to evaluate what had
already been designed, with no re-optimisation. Whatever these peptides do on human EGFR is
transfer, not a fit to the evaluation target — and the epitope is conserved, so the same molecules
are directly testable in mouse models.

**They are orthogonal to the rest of the submission.** The mini and large bands target a different
histidine (His433) by a different chemistry, from a standard scaffold-and-inverse-folding protocol.
The two series share no machinery and fail independently, so backing both costs little and hedges a
great deal.

## The mechanism, concretely

Numbering: local position *n* = UniProt *n* + 333 = mature EGFR *n* + 309. The target histidine is
local **25** = UniProt **His358** = mature His334.

At acidic pH the His358 imidazolium carries a hydrogen on **both** ring nitrogens, ND1 and NE2. Each
is then a hydrogen-bond donor. The designs place main-chain carbonyl oxygens to accept from them —
one nitrogen engaged is a hydrogen bond, both engaged is a bidentate clamp that can only form on the
protonated ring. At pH 7.4 the neutral imidazole has one N–H and one lone pair, so at most half the
interaction survives, and the geometry that accepts from a donor now faces an acceptor.

A hydrogen bond here is treated as a **direction**, not a distance. A contact counts only if it is
2.5–3.4 Å, within 45° of the in-plane N–H vector, at least 2.9 Å from every ring carbon, and within
1.2 Å of the ring plane. The ring-carbon clause matters: an early design read 2.75 Å to NE2 while
sitting 2.13 Å from ring carbon CE1 — a collision on the edge of the ring that a distance-only test
scores as a hydrogen bond.

## What is in this directory

One directory per design, each holding the predicted structures it was judged on, the per-model
confidence data, and the sequence. `metrics.json` carries the numbers quoted for that design, so
anything in the submission CSV can be recomputed from the files here.

## Honest limits

- **Nothing here has been measured.** Every number is a property of a structure prediction. There
  are no binding data, no pH titrations, no expression or synthesis results.
- **The bidentate clamp is rare in the predictions.** Most engaged models make one hydrogen bond,
  not two. The pH dependence should therefore be expected to be real but modest, not switch-like.
  A census of the PDB puts the doubly-accepting imidazolium at roughly 1 occurrence in 220, so this
  is a demanding motif and the models reflect that.
- **The predicted pKa shifts mostly point the wrong way.** Of 27 designs examined, **2** show a
  positive shift on the human target; for the rest, burying the histidine lowers its pKa more than
  the hydrogen bond raises it, so the modelled interface would favour the *neutral* ring — the
  switch inverted. No submitted design is positive in both species. The geometry is reproducible;
  its electrostatic consequence, as propka computes it here, is not yet what the mechanism needs.
  Every shift is reported per design, with the spread across models beside it.
- **EGFR domain III carries a free cysteine (Cys137 in local numbering).** These peptides are
  disulfide-cyclised, and one predictor paired a binder cysteine with it. No model from the primary
  oracle shows that, but it is a bench consideration for anyone synthesising them.
- **Mouse and human evidence are not equally deep.** The human complexes were refolded far more
  often than the mouse ones; the per-species model counts are reported beside every rate so the
  comparison can be read for what it is.

The selection procedure, the metrics and the failures are in `../docs/methods_micro.md` and
`../docs/metrics.md`.
