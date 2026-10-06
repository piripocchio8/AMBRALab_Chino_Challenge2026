# Source material for the mini and large binders

The twelve designs in `Target_1/mini/` and `Target_1/large/` come from the pH-selective EGFR binder
work of **G. Sgueglia**, carried out within this group. The files here are that work's own
documentation, reproduced so the submission is self-contained:

- `METHODS.md` — how the designs were made: motif-scaffolded RFdiffusion3 backbones, soluble
  ProteinMPNN sequences, Boltz-2 co-folding and ipSAE validation.
- `SUBMISSION_NOTES.md` — the notes accompanying that series.
- `SUBMISSION_full23.csv` — the complete metric table for all twenty-three designs of the series. Twelve
  are submitted here; the two lowest-ranked were not carried over.
- `analysis/pka.md`, `analysis/what_predicts_binding.md` — the supporting analyses.
- `README_source.md` — the original repository README, kept verbatim.

**Numbering.** That work uses mature EGFR numbering (1–621), where the competition construct is
UniProt 25–645, so mature *m* = UniProt *m* + 24. Its pH switch is **His409 mature / His433
UniProt**, with Asp436 mature / Asp460 UniProt as the fixed anchor.

**Relationship to the micro binders: a different histidine, not the same one.** An earlier version
of this file said the two series attack the same residue. They do not.

| series | target histidine | UniProt P00533 | mature EGFR |
|---|---|---|---|
| mini and large (this series) | pH switch, with an engineered carboxylate | **His433** | His409 |
| micro (`Target_1/micro/`) | pH switch, with two main-chain carbonyls | **His358** | His334 |

The two sites are 75 residues apart in sequence. So the submission covers two distinct epitopes on
EGFR domain III as well as two distinct chemistries, and a failure of one tells you nothing about
the other. That is a broader bet than a single site, not a redundant one, but it should not be
described as independent confirmation of one mechanism.
