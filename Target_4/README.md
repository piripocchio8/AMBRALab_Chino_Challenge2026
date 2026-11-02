# Target 4 — de novo binders to a 189-residue target window (H and M orthologues)

Twenty designed peptides of 28–46 residues, composed of the standard twenty L-amino acids,
designed de novo in this group and ranked on boltz-2. Entirely in silico; no experimental work.

> **A note on what is and is not disclosed here.** The design engine is **the subject of a
> manuscript in preparation**, so it is described in principle rather than in reproducible detail,
> **ahead of publication**. Nothing needed to *evaluate* these designs is withheld: the sequences,
> the predicted structures, every per-model measurement, the selection threshold and how it was
> derived, the declared restraints and the full ranked population are all in this directory, and
> every number quoted can be recomputed from the files beside it. What is held back is how the
> candidate sequences were *generated*, not how they were *judged*. We will release the engine with
> the publication and are glad to discuss the method in confidence with the organisers meanwhile.

**Files**

| path | contents |
|---|---|
| `submission.csv` | the twenty entries: `name,sequence,molecule_class` |
| `metrics_full.csv` | every number behind the ranking, one row per design |
| `DESIGN_STRATEGY.md` | how the designs were produced and how the twenty were chosen |
| `SUBMISSION_TEXT.md` | the prose summary |
| `docs/metrics.md` | what each column means and what it does not |
| `docs/ranking_all.json` | the full ranked population, all 70 designs, both orthologues |
| `h_anchored/`, `dual_lean/` | per-design `sequence.fasta`, `metrics.json`, `complex_H.pdb`, `complex_M.pdb` |

## The one measurement this deposit rests on

A binder's score here is its ipTM from **boltz-2 against the 189-residue target window, with the
design's own declared pocket, single-sequence (`msa: empty`), seed 2000, five diffusion samples.**

That configuration was not chosen for convenience. Five binders with deposited co-crystal
structures against this target were put through every oracle and arm available — Chai-1 and
Protenix as well as boltz-2, window and full-length target, pocket declared and not. **Exactly one
combination reproduced a deposited complex**: boltz-2, 189-residue window, pocket declared, which
placed B1 at **2.86 Å CA RMSD** from its crystal structure in 4 of 5 models and ranked its own
failure last. Independently repeated: 2.96/3.61/2.81/3.49/55.90 Å against 2.99/3.68/2.86/3.53/53.81.

Against the **full-length** target no oracle reproduced anything (best 13.9 Å; boltz B1 65.9 Å,
Jaccard 0.000 on the contact set). The mechanism was measured rather than assumed: the fraction of
contacted target residues lying inside the 189-residue window falls from 1.00 at window length to
0.40 at full length, and for the design population in the unrestrained full-length arm to a median
of **0.06**. One soft 8 Å `force: false` contact does not hold a binder on a 189-residue patch
against 451 residues of competing surface. Full-length numbers from this campaign describe poses
docked somewhere else and are not used here.

## The threshold

Ranking uses a threshold, not a composite and not the worse of the two orthologues.

| real binder | ipTM (window, pocket) | CA RMSD vs deposit | |
|---|---|---|---|
| B1 | **0.6428** | 2.86 Å | correct |
| B2 | 0.8500 | 17.6 Å | right epitope, wrong orientation |
| B3 | 0.4380 | 13.9 Å | wrong |

**T = 0.6428** — the worst ipTM among the real binders this oracle nevertheless predicts correctly
(CA RMSD < 5 Å). Counting B2 as additionally correct-on-epitope gives the same number, which is the
only robustness check available at n = 5 and is reported as such, not as a validation.

What T is: the confidence this oracle assigned to a complex it got right. What T is not: a
probability of binding. B2 sits far above T on a pose 18 Å from the crystallographic answer, so
clearing T earns a design only the statement that the oracle is as confident about it as it was
about the one complex it reproduced.

## What the result actually is

**No design clears T on both orthologues.** Twenty-three of 70 clear it on H; none clear it on M,
where the whole population sits at a median ipTM of 0.27.

This is the expected outcome rather than a surprise, and the reason is in the campaign's own
configuration files: every wave but one declares `fasta_path: t4/H_t4.fasta`. Stage-1 and waves 2
through 7 were searched against **H alone**. M entered only at stage 2 and in the phase-2 family.
The designs were not optimised against M, and they do not score on M.

**No design in this deposit is claimed to bind M.** There is also no way to calibrate the M numbers:
the deposited binders are not known to bind the paralogue, so no molecule exists whose M complex the
oracle could be checked against. T is an H-side threshold, and an M ipTM here is a measured number
with nothing behind it.

The twenty are therefore split to show that shape rather than hide it:

- **`h_anchored` (15)** — highest ipTM on H among the designs clearing T on H. These are the
  convincing ones, on the one axis where the instrument has a verified true positive.
- **`dual_lean` (5)** — highest ipTM on M among the designs not already taken. None clears T on H.
  They are here because the brief is a dual binder and these carry the strongest M engagement the
  campaign produced. Four of the five come from the two-hairpin family.

## Pose dispersion is reported and not gated

`pose_disp_*_A` is the binder CA RMSD about the medoid pose over the five models, after superposing
on the target. It is in `metrics_full.csv` for every design and no design was included or excluded
on it. The campaign's pre-registered 6.0 Å gate was calibrated on Chai-1, and on this oracle it
excludes 4 of the 5 molecules with deposited co-crystal structures; applying it would import a known
miscalibration into the delivery. Read it as a spread, not as a verdict.

## Population and provenance

70 unique designs recovered from 129 runs across every wave and host, deduplicated by sequence
(the higher search ipTM survives). Five design families, each folded against **its own** declared
pocket, fragment-local in the 189-residue window:

| family | n | pocket H | pocket M |
|---|---|---|---|
| stage-1 | 24 | 17, 180 | 18, 180 |
| wave-3 family | 16 | 20 | 20 |
| two-hairpin | 20 | 179 | 179 |
| wave-2 | 9 | 180 | 180 |
| phase-2 | 1 | 20 | 20 |

A single pocket constant would have restrained three quarters of the population to a site it was
never designed for. One run was refused outright because its family could not be resolved from its
run id; it was neither folded nor ranked.
