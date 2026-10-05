# Target 1 — mini binders (40–100 residues)

Four de-novo designs against the pH-switch histidine of EGFR domain III, contributed by
G. Sgueglia. Each folder holds the design's predicted structures and confidence data as produced
in that work; `docs/sgueglia/METHODS.md` describes how they were made and
`docs/sgueglia/SUBMISSION_full14.csv` carries the full metric table for all fourteen designs of
that series, of which twelve are submitted here.

| design | length | structures |
|---|---|---|
| pHsel-04 | 99 | human (two folds), mouse, RFdiffusion backbone |
| pHsel-05 | 94 | " |
| pHsel-08 | 60 | " |
| pHsel-13 | 98 | " |

Per design: `human_cycle3.cif` and `human_replicate.cif` are two independent folds of the human
complex, `mouse.cif` the mouse ortholog (the cross-reactivity check), and `rfd3_backbone.cif.gz`
the scaffold the sequence was designed onto. Each carries its confidence JSON, ipSAE tables, and
PAE/pLDDT arrays.
