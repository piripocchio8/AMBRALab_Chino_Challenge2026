# Source material for the mini and large binders

The twelve designs in `Target_1/mini/` and `Target_1/large/` come from the pH-selective EGFR binder
work of **G. Sgueglia**, carried out within this group. The files here are that work's own
documentation, reproduced so the submission is self-contained:

- `METHODS.md` — how the designs were made: motif-scaffolded RFdiffusion3 backbones, soluble
  ProteinMPNN sequences, Boltz-2 co-folding and ipSAE validation.
- `SUBMISSION_NOTES.md` — the notes accompanying that series.
- `SUBMISSION_full14.csv` — the complete metric table for all fourteen designs of the series. Twelve
  are submitted here; the two lowest-ranked were not carried over.
- `analysis/pka.md`, `analysis/what_predicts_binding.md` — the supporting analyses.
- `README_source.md` — the original repository README, kept verbatim.

**Numbering.** That work uses mature EGFR numbering (1–621), where the competition construct is
UniProt 25–645, so mature *m* = UniProt *m* + 24. Its pH switch is **His409 mature / His433
UniProt**, with Asp436 mature / Asp460 UniProt as the fixed anchor.

**Relationship to the micro binders.** The micro designs in `Target_1/micro/` attack the *same*
target histidine by a different chemistry: two main-chain carbonyls donating to the protonated
imidazolium, rather than a salt bridge to an engineered carboxylate. The two mechanisms are
independent, which is why both are submitted.
