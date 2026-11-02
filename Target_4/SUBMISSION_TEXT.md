# Text for the submission form's description box

*(Paste the block below as-is. The attachable file is `Target_4/DESIGN_STRATEGY.md`.)*

---

**De novo peptide binders against two orthologues of the target — AMBRA group, Chino lab,
University of Naples Federico II**

**Twenty peptides of 28–48 residues, designed from scratch by computer in our group**, built from
the standard twenty L-amino acids. They are not variants of any known binder and share no sequence
relationship with one. **None of them has been made or tested in a laboratory** — every number we
report is a property of a structure prediction.

**We tested whether any prediction method can solve this target before trusting one on our own
designs.** Three published binders of this target, each with an experimentally solved structure in
complex with it, were predicted using every combination available to us: three prediction programs,
the full-length protein and a short fragment of it, with and without evolutionary alignments
(MSAs), and with and without telling the program which surface patch to aim at. Each prediction was
compared with the published experimental structure.

**Exactly one combination reproduces a published structure** — boltz-2, full-length target, MSAs
supplied for both chains, target patch declared as a soft restraint. It places that binder
**2.8 ± 0.3 Å from the experimental answer in all five predicted models**, recovering 89–92 % of
the experimentally observed contacts. Both ingredients are necessary: the MSA without the patch
gives 89.9 Å, the patch without the MSA gives 66.0 Å. **The other two published binders are
reproduced by none of the setups we tried.** The method is therefore demonstrably capable on one
real binder out of three, and we report our designs against that standard rather than against a
more flattering one.

**We did not select our twenty on prediction confidence, and we did not select them on whether the
peptide reaches its intended patch.** Both were tested as criteria and both fail: when the patch is
declared, all three published binders reach it in 5 of 5 models — including the two whose
predictions are 17–19 Å wrong; when it is not declared, all three fail — including the one that is
right. And confidence does not certify an answer: one published binder scores a *higher* confidence
than the binder the method actually gets right, on a prediction 19 Å from the experimental
structure.

**We selected on a negative control instead.** Every design was predicted a second time with its
own residues shuffled into random order — identical composition and length, only the arrangement
destroyed. A design whose score does not beat its own shuffle has demonstrated nothing beyond its
amino-acid content. Across all 103 candidate designs, the designed arrangement beats the shuffle on
one orthologue in **80 of 103** (sign test p = 7.3 × 10⁻⁹) and on the other in 63 of 103
(p = 0.015), against a +0.010 control for a possible confounding effect. **All twenty deposited
designs beat their own shuffle on both orthologues.**

**We rank on the full-length protein because a short fragment is misleading.** Cutting the target
down exposes a buried greasy surface at the cut, which predicted peptides are strongly drawn to:
occupancy of that artefact reaches 78 % of a peptide's contacts on the fragment and falls to 0–7 %
on the intact protein. A design can score well on a fragment while sitting in the scar of the cut.

**What we do not claim.** No design reaches the confidence score of the one published binder the
method predicts correctly — 0.628 against our best of about 0.52. That gap is real and we state it
rather than rank around it. High confidence does not mean a correct pose. And nothing here has been
tested experimentally.

**We also report a measurement error we found in our own code and fixed.** Comparing a prediction
to an experimental structure requires aligning the two targets residue by residue; our code assumed
the experimental structure contained every residue. One reference structure is missing three
unresolved residues inside the compared region, which mismatched every residue after the gap and
distorted the comparison. Keying on the residue numbering recorded in the experimental file fixed
it — contact agreement rose from 0.56 to 0.92. All figures above are from after the fix.

**The full candidate population is deposited, not only the winners.** All 103 designs with both
orthologues' numbers are in `docs/ranking_all.json`, so the twenty can be read against the
distribution they were drawn from.
