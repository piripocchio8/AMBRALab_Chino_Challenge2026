# Target 1 — large binders (>100 residues)

Eight de-novo designs against the pH-switch histidine (**His433**) of EGFR domain III, contributed by G. Sgueglia and taken in that work's own submission-rank order.

These engage a **different histidine by a different chemistry** from the micro band: a salt bridge from the protonated imidazolium to an engineered carboxylate, with a reciprocal histidine–aspartate anchor. The two series share no machinery and fail independently.

| design | length | source rank | round | ipSAE human / mouse | binder pLDDT |
|---|---|---|---|---|---|
| `pHsel-01` | 110 | 1 | 3 | 0.900 / 0.890 | 0.962 |
| `pHsel-02` | 127 | 2 | 4 | 0.895 / 0.891 | 0.947 |
| `pHsel-03` | 129 | 3 | 5 | 0.889 / 0.878 | 0.958 |
| `pHsel-07` | 126 | 7 | 5 | 0.870 / 0.880 | 0.937 |
| `pHsel-08` | 117 | 8 | 5 | 0.851 / 0.829 | 0.915 |
| `pHsel-09` | 110 | 9 | 5 | 0.842 / 0.844 | 0.953 |
| `pHsel-10` | 118 | 10 | 4 | 0.870 / 0.888 | 0.933 |
| `pHsel-11` | 101 | 11 | 5 | 0.833 / 0.794 | 0.929 |

Interface confidence is **close to equal on the two orthologs** across the band, which is the cross-reactivity property the challenge asks for.

Per design: `human_cycle3.cif` and `human_replicate.cif` are two independent folds of the human
complex, `mouse.cif` the mouse ortholog (the cross-reactivity check), and `rfd3_backbone.cif.gz`
the scaffold the sequence was designed onto. Each carries its confidence JSON, ipSAE tables and
PAE/pLDDT arrays; `metrics.json` holds that design's row of the source metric table.

Methods are in [`../docs/methods_mini_large/methods.md`](../docs/methods_mini_large/methods.md);
the full table for all twenty-three designs of the series is
[`../docs/methods_mini_large/SUBMISSION_full23.csv`](../docs/methods_mini_large/SUBMISSION_full23.csv).

> **Names are not stable across versions of the source series.** Every `pHsel-NN` label was
> reassigned when the series grew from fourteen designs to twenty-three, so a name here does not
> refer to the same molecule it did in an earlier revision. Designs are identified by sequence and
> carry their source rank and local id in `metrics.json`.
