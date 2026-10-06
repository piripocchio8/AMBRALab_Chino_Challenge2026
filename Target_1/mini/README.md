# Target 1 — mini binders (40–100 residues)

Four de-novo designs against the pH-switch histidine (**His433**) of EGFR domain III, contributed by G. Sgueglia and taken in that work's own submission-rank order.

These engage a **different histidine by a different chemistry** from the micro band: a salt bridge from the protonated imidazolium to an engineered carboxylate, with a reciprocal histidine–aspartate anchor. The two series share no machinery and fail independently.

| design | length | source rank | round | ipSAE human / mouse | binder pLDDT |
|---|---|---|---|---|---|
| `pHsel-04` | 94 | 4 | 4 | 0.912 / 0.876 | 0.946 |
| `pHsel-05` | 97 | 5 | 5 | 0.879 / 0.886 | 0.932 |
| `pHsel-06` | 98 | 6 | 5 | 0.872 / 0.835 | 0.939 |
| `pHsel-15` | 99 | 15 | 3 | 0.870 / 0.882 | 0.965 |

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
