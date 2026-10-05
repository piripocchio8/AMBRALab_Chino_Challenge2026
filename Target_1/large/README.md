# Target 1 — large binders (>100 residues)

Eight de-novo designs against the pH-switch histidine of EGFR domain III, contributed by
G. Sgueglia, taken in that work's own submission-rank order. See `docs/sgueglia/METHODS.md` for
how they were made and `docs/sgueglia/SUBMISSION_full14.csv` for the full metric table.

| design | length | rank in source series |
|---|---|---|
| pHsel-01 | 110 | 1 |
| pHsel-02 | 127 | 2 |
| pHsel-03 | 124 | 3 |
| pHsel-06 | 124 | 6 |
| pHsel-07 | 118 | 7 |
| pHsel-09 | 104 | 9 |
| pHsel-10 | 120 | 10 |
| pHsel-11 | 134 | 11 |

Per design: `human_cycle3.cif` and `human_replicate.cif` are two independent folds of the human
complex, `mouse.cif` the mouse ortholog, and `rfd3_backbone.cif.gz` the scaffold. Each carries its
confidence JSON, ipSAE tables, and PAE/pLDDT arrays.
