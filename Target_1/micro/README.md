# Target 1 — micro band

Size band: **micro, fewer than 40 residues**. This directory holds the designs submitted in the
micro band together with their predicted structure models, and the ranked submission CSV built by
`scripts/make_submission_csv.py`. Rows in that CSV are ordered best-first, since the challenge reads
the ranking from the top row down. The design target and the protocol that produced these designs
are described in `docs/methods.md`.

`example_candidates.json` is a runnable **placeholder** input that documents the record format. Its
two records are fictional and must not be submitted. The generated `submission_micro.csv` is a build
product and is untracked until the final designs have been selected; see `.gitignore` at the
repository root.
