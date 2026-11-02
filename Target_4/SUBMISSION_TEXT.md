# Text for the submission form's description box

*(Paste the block below as-is. The attachable file is `Target_4/DESIGN_STRATEGY.md`.)*

---

**De novo binders to a 189-residue epitope on two orthologues — AMBRA group, Chino lab, University
of Naples Federico II**

**Twenty designed peptides of 28–48 residues, designed de novo in our group**, composed of the
standard twenty L-amino acids, with no sequence relationship to any deposited binder of this
target. **Nothing here has been tested experimentally.** Every number is a property of a structure
prediction.

**We chose the oracle by testing whether any oracle can do this at all.** Three binders with
deposited co-crystal structures were folded through every available arm — Chai-1, Protenix and
boltz-2; the 189-residue window and the full-length target; single-sequence and with MSAs; pocket
declared and not — and each prediction was scored by CA RMSD against the deposited complex. One
configuration reproduces a deposited structure: **boltz-2, full length, MSA on both chains, pocket
declared**, which places B1 at **2.8 ± 0.3 Å in 5 of 5 models and recovers 89–92 % of the deposited
contact set.** Both levers are needed — the MSA without the pocket gives 89.9 Å, the pocket without
the MSA gives 66.0 Å. The other two deposited binders are reproduced by no arm we tried.

**We report the ceiling rather than ranking around it.** B1's ipTM in that arm is 0.628, and **no
design among 103 reaches it**; our best sit near 0.52. In the same arm B2 scores 0.714 — higher
than B1 — on a pose 19 Å from its crystal structure, so confidence orders candidates and does not
certify them.

**We did not select on "reaches the declared epitope", because that measure has no power here.**
With the pocket declared, all three known binders reach the epitope in 5 of 5 models including the
two that are 17–19 Å wrong; with the pocket removed, all three fail including the one that is
right. All 103 of our designs reach it 5/5, which tells us nothing.

**We selected on each design against its own composition-matched scramble** — same residues, same
length, shuffled order, everything else identical. Designed order beats composition on M (45/52,
sign test p = 3.5 × 10⁻⁸) and does **not** on H (31/52, p = 0.11), against an MSA-depth control of
+0.010. **All twenty deposited designs beat their own scramble on both orthologues.**

**The ranking is at full length because the 189-residue construct is misleading.** That window
exposes the hydrophobic scar of the excised domain, where designs can score well by sitting in an
artefact; occupancy there reaches 0.78 and falls to 0.00–0.07 once the excised domain is restored.

**One measurement bug is reported rather than buried.** Our deposited-target frame mapped residues
by position in the list, which breaks across unmodelled residues: one deposit omits three, and
B1's superposition was built from mispaired residues. Keying on the deposit's author numbering
raised B1's contact agreement from 0.56 to 0.92. All figures above are post-fix.

**The full ranked population is deposited, not only the winners** — all 103 designs with both
orthologues' numbers are in `docs/ranking_all.json`, so the twenty can be read against the
distribution they came from.
