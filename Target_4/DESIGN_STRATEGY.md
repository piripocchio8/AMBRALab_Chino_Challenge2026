# Target 4 — design strategy

## The problem as posed

A dual binder: one peptide engaging the same site on two orthologues of a target, H and M. The two
189-residue windows are **69.8 % identical**, and they differ at every position the campaign ever
declared as a pocket:

| fragment-local column | H | M |
|---|---|---|
| 17 | R | G |
| 18 | L | N |
| 20 | Y | D |
| 179 | S | N |
| 180 | K | Q |

That divergence is the whole difficulty. The epitope is not conserved, so a dual binder cannot be
obtained by designing against one orthologue and relying on the site being the same in the other.

## How the designs were produced

Forward-folding hallucination on Chai-1 (the HalluDesign paradigm: the oracle scores, it is not
differentiated through), with D or L available per position. Across all 120 runs of this campaign
the search returned **no D residue**, so every delivered design is all-L; the capability was
available and was not used by the objective. The search ran in waves,
and across the campaign the declared pocket moved three times — which is why every number in this
deposit is keyed to the design's own pocket rather than to a campaign-wide constant.

| family | n | declared pocket | what it is |
|---|---|---|---|
| stage-1 | 24 | 17 + 180 (H), 18 + 180 (M) | the original two-point site |
| wave-2 | 9 | 180 | a single lysine |
| wave-3 family | 16 | 20 | a single tyrosine |
| phase-2 | 1 | 20 | tyrosine, searched against M |
| two-hairpin | 20 | 179 | neither lysine nor tyrosine — Ser in H, Asn in M |

The two-hairpin family is the latest construct: two hairpins on a 38–46 residue scaffold, declared
against column 179, searched in two stages.

**Single-target search.** The wave configurations declare `fasta_path: t4/H_t4.fasta` for stage-1
and waves 2 through 7. Only stage 2 and the phase-2 family ever saw M. This was a choice made under
time pressure early in the campaign, and it is the direct cause of the result reported below: the
designs are good on the orthologue they were optimised against and flat on the one they were not.

## How the oracle was chosen

Not by reputation and not by self-reported confidence. Five binders with deposited co-crystal
structures against this target were folded through every available oracle and arm — Chai-1,
Protenix and boltz-2; the 189-residue window and the 640-residue full-length target; pocket declared
and not — and each prediction was scored by **CA RMSD against the deposited complex**, with the
binder residues paired by sequence offset rather than by index (one deposit resolves 93 of 94
residues, and index pairing silently shifts every subsequent pair; that bug alone reported B1 at
18.2 Å when it is at 2.8 Å).

One configuration reproduced a deposited structure: **boltz-2, 189-residue window, declared pocket,
`msa: empty`, 8.0 Å `force: false` contact, 3 recycling steps, 200 sampling steps, 5 diffusion
samples, seed 2000.** B1 at 2.81/2.86 Å, 4 of 5 models correct, the failing model ranked last by the
oracle's own confidence.

Every other combination failed. At full length the best result from any oracle was 13.9 Å, and the
contact census explains it: the fraction of contacted target residues inside the designed window
drops to 0.40 for boltz on B1 and to a median of 0.06 for the design population in the unrestrained
arm. Those folds measure some other surface.

## How the twenty were chosen

The rule is a threshold, not an average and not the worse of the two orthologues.

**T = 0.6428** — the worst ipTM among the real binders this oracle predicts correctly (CA RMSD
< 5 Å vs deposit). Only B1 qualifies at < 5 Å; including B2, which reaches the right epitope in the
wrong orientation, returns the same number.

All 70 designs were folded against both orthologues at the window, each with its own pocket, and
tiered: clears T on both / on one / on neither.

**Tier 1 is empty.** Twenty-three designs clear T on H. None clears it on M; the population median on
M is 0.27 against 0.74 on H among the H-passers. Given single-target search, this is what the
configuration predicted, and it is reported rather than worked around.

The twenty are therefore drawn in two bands:

- **`h_anchored` (15)** — the top fifteen by H ipTM among the twenty-three clearing T on H.
- **`dual_lean` (5)** — the five highest M ipTM among the remainder (0.443–0.530). None clears T on
  H. Four are two-hairpin designs, which is the one family that shows any M-side tendency.

## What would settle the open question

The dual-binding claim is unresolved, not refuted. Two things would move it, in order of cost:

1. **An M-side positive control.** There is currently none: no molecule is known to bind the
   paralogue, so the oracle's M output cannot be calibrated at all. Without it, an M ipTM of 0.53 is
   uninterpretable — it may be a weak binder or the oracle's ceiling on that surface.
2. **A genuinely dual search.** Every design here but one family optimised H alone. A search scoring
   both orthologues per candidate is the experiment that this deposit does not contain, and it is
   the one that would answer the question as posed.

## Reporting limits

- n = 5 models per design per orthologue. ipTM in the tables is the mean over the five; the best of
  five is carried separately in `metrics_full.csv`.
- The threshold rests on **one** correctly predicted molecule out of five with deposited structures.
  That is a single calibration point and is treated as such.
- Pose dispersion is reported for every design and gated for none, because the campaign's
  pre-registered 6.0 Å gate excludes 4 of those same 5 deposited molecules on this oracle.
- Chai-1 numbers from the search are in `metrics_full.csv` as `search_iptm` for provenance. They are
  not comparable to the boltz-2 column and were not used in the ranking.
