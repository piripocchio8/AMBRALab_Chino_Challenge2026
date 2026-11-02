# Text for the submission form's description box

*(Paste the block below as-is. The attachable file is `Target_4/DESIGN_STRATEGY.md` in the
repository.)*

---

**De novo binders to a 189-residue target window — AMBRA group, Chino lab, University of Naples
Federico II**

**Twenty designed peptides of 28–46 residues, de novo, produced by forward-folding hallucination on
Chai-1.** Our framework assigns D or L per position, but across all 129 runs of this campaign the
search returned no D residue, so **all twenty are all-L** and composed of the standard twenty amino
acids. They have no sequence relationship to any deposited
binder of this target. They are deposited in two consecutive blocks under one ranking: ranks 1–15
(`h_anchored`) and ranks 16–20 (`dual_lean`).

**Nothing here has been tested.** No binding assay, no expression, no synthesis. Every number in
this deposit is a property of a structure prediction.

**We selected the oracle by asking whether any oracle can do this at all.** Five binders with
deposited co-crystal structures against this target were folded through Chai-1, Protenix and
boltz-2, against both the 189-residue window and the 640-residue full-length target, with and
without the pocket declared, and each prediction was scored by CA RMSD against the deposited
complex. **One configuration out of all of them reproduced a deposited structure**: boltz-2 on the
189-residue window with the pocket declared, single-sequence, which placed B1 at 2.86 Å in 4 of 5
models and ranked its own failing model last. Everything in this deposit is ranked on that one
configuration. At full length no oracle reproduced anything — the best was 13.9 Å — and we measured
why rather than guessing: the fraction of contacts landing on the designed window falls to 0.40
there, and to a median of **0.06** for our own designs without a restraint. Those folds describe
some other surface and we did not use them.

**Our ranking threshold is one real binder's confidence, and we are explicit that it is one.**
T = 0.6428 is the ipTM that this oracle assigned to the single deposited complex it got right.
Clearing T means the oracle is as confident about a design as it was about that complex — nothing
more. The same oracle reaches 0.85 ipTM on a pose 18 Å from the crystallographic answer, so
confidence above T is not evidence of binding.

**The target is a dual-binder problem and we did not solve it.** The two orthologue windows are
69.8 % identical and differ at *every* pocket position we declared (R/G, L/N, Y/D, S/N, K/Q).
Twenty-three of our 70 designs clear T on the H orthologue. **None clears it on M.** The cause is in
our own configuration files rather than in the chemistry: every design wave but one declares the H
window as its target, so the designs were never optimised against M and they do not score against
it. We report this instead of ranking around it.

**We also cannot calibrate the M numbers at all.** The deposited binders are not known to bind the
paralogue, so no molecule exists whose M complex the oracle could be checked against. An M ipTM in
our table is a measured number with no positive control behind it. **No design in this deposit is
claimed to bind M.** The five `dual_lean` entries are the strongest M engagement the campaign
produced (ipTM 0.443–0.530, four of them from one design family); they do not clear T on H and are
included because the brief asks for a dual binder, not because they are shown to be one.

**Pose dispersion is reported for every design and gates none of them.** Our pre-registered 6.0 Å
dispersion gate was calibrated on Chai-1; on this oracle it excludes 4 of the same 5 molecules that
have deposited co-crystal structures, so enforcing it would have imported a known miscalibration
into the selection. The numbers are in `metrics_full.csv` as a spread, not as a verdict.

**The full ranked population is deposited, not only the winners.** `docs/ranking_all.json`
carries all 70 designs with both orthologues' numbers, so the twenty can be seen against the
distribution they were drawn from.
