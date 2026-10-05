# Submission notes

**Challenge:** EGFR Challenge 01, Anthropic x Adaptyv 2026.
**Deadline:** 6 October 2026, 23:59 AoE (UTC-12).

## File to upload

`SUBMISSION.csv` — 14 designs, ordered by ranking preference (row 1 = most preferred). Nine carry
their original sequence and five a surface/core polarity-optimised sequence; the `sequence_origin`
column records which, and `optimised_mutations` lists the substitutions.

Required columns are present and first, exactly as the brief specifies:

| column | value |
|---|---|
| `name` | `pHsel-01` … `pHsel-14` |
| `sequence` | single-chain amino-acid sequence, 60–134 aa (brief allows 10–250) |
| `molecule_class` | `protein` for all 14 (single-chain, not nanobody/scFv/Fab) |

57 further columns carry the metrics, so the file can be submitted as-is without stripping.

## Design-count caps

| track | cap | our submission |
|---|---|---|
| Track 1 (labs/companies) | up to 40 | 14 — under the cap |
| Track 2 (individuals/small teams) | up to 20 | 14 — under the cap |
| Track 3 (open) | up to 20 | 14 — under the cap |

14 fits every track, so no truncation is needed. We deliberately did **not** pad to the cap: these
are the designs that passed the acceptance gate in all three independent folds, and adding weaker
material would dilute the ranking without adding information.

## Eligibility checks against the brief

- **de novo:** yes. Backbones are motif-scaffolded RFdiffusion3 from a geometric His–carboxylate
  motif; no existing binder, antibody framework or natural EGFR ligand was used as a starting point.
- **epitope:** domain III, the recommended epitope. The motif is built on target His433 and Asp460
  (UniProt P00533), both inside domain III.
- **length:** 60–134 aa, inside the 10–250 range.
- **molecule class:** single-chain protein.
- **metrics, structures, methodology:** included (`metrics/`, `designs/`, `METHODS.md`) — these are
  encouraged rather than required.
- **repository link:** this repository.

## Ranking basis

Ranked by **ipSAE of the worst of three independent unconstrained folds**, not the best. See
`README.md` section 3 for why, and `analysis/what_predicts_binding.md` for the honest statement that
no computational metric here strongly predicts binding — the order is a preference, not a prediction.

`risk_flags` is populated per design rather than silently folded into the score, so a reviewer can
re-rank on their own criteria. Flag meanings:

| flag | basis |
|---|---|
| `alanine>10.4%` | above the ceiling of all 7 sub-micromolar all-alpha binders (4.5-10.4%) |
| `alanine>15.8%` | above the highest-alanine binder observed at all; 0/16 bound above 20% in that class, 2/76 in our own 800-design EGFR cohort |
| `hydrophobic>0.42` | above the all-alpha class range; binders sit at 0.376 |
| `short<80aa` | 31-45 aa bound at 0%; 60 aa is above that but below the productive regime |
| `near-neutral-charge` | the 0 to +0.05 e/residue band expressed at only 67% |
| `bridge-geometry-off` | salt-bridge geometry outside the native envelope (`realism_dev` > 3.39) |

Alanine does not affect expression (p = 0.47) and does not discriminate within our length band
(p = 1.00, underpowered), so these flags mark distance from the observed binder envelope rather than
a demonstrated effect. They are reported per design rather than folded into the score so a reviewer
can re-rank on their own criteria.

## Known weakness, stated plainly

Every design is 60–134 aa. Three independent cuts of the Adaptyv EGFR data put the productive regime
much longer (all-alpha binders median 228 aa; >= 200 aa gives 26.9% vs 9.8% at 100–200 aa within one
method group, Fisher p = 0.00086). We did not have time to regenerate at 180–250 aa before the
deadline. This is the single change we would make with more time, and it is independent of the
pH-switch machinery, which is scaffold-agnostic.
