# Methods

Everything below was run on a CentOS 7 / glibc 2.17 cluster with no container runtime, which
constrains every tool version; `protocol/envs/` carries the exact pins and `protocol/envs/tool-commits.txt`
the tool commits.

## 0. Target preparation

| item | value |
|---|---|
| construct | human EGFR ectodomain, mature 1–621 = **UniProt P00533 25–645** |
| structure | `protocol/inputs/EGFR_ecto_A.pdb` (621 res, chain A) |
| co-folding target | domain III only, mature **311–480** = UniProt 335–504 (170 aa) |
| target MSA | `protocol/inputs/EGFR_domIII_311_480_msa.a3m` (2603 seqs, ColabFold server, cached) |
| cross-species target | mouse Egfr domain III, mature 335–504 |

The binder chain is always folded with `msa: empty` because it is de novo.

## 1. Motif definition (the pH switch)

Two target residues define the motif: **His433** (UniProt; mature 409) as the protonation switch and
**Asp460** (UniProt; mature 436) as a fixed anchor. The binder must present a carboxylate to His433
and a histidine to Asp460. Candidate geometries were enumerated from PDB-derived His–carboxylate
pairs, filtered on the real C(acid)->N(His) distance, and emitted as RFdiffusion3 contigs of the form

```
<flank>,<acid>,<linker>,<His>,<flank>,/0,A311-480
```

with the linker length computed per pair from the measured gap, `ceil((gap - 1.33) / 3.3)`.
Scripts: `protocol/scripts/campaign/c0_emit_inputs.py`.

## 2. Backbone generation — RFdiffusion3

`rc-foundry` 0.2.0 (`rfd3`), bf16 AMP, one V100 per shard.

```
rfd3 design out_dir=$OUT inputs=$IN ckpt_path=$CKPT \
     n_batches=$NB diffusion_batch_size=20 \
     inference_sampler.step_scale=3 inference_sampler.gamma_0=0.2 \
     prevalidate_inputs=True skip_existing=True
```

`diffusion_batch_size=20` is the measured optimum; `skip_existing=True` makes retries resumable.
**RFD3 samples variable segment lengths once per batch, not per design.** Binder length is set by the
flank window: flank 37–70 gives 80–150 aa, which outperformed flank 20–35 (46–80 aa) by **6.6x** on
founder rate while ipSAE was blind to the difference (p = 0.52).

Output caveat: RFD3 renumbers, so the binder is chain A and the target comes back as chain B
starting at 1. Each design's JSON carries `diffused_index_map`; use it or distances are measured to
the wrong residues.

## 3. Sequence design — soluble ProteinMPNN

Driven as a Python API (`MPNNInferenceEngine`), not the CLI, so the checkpoint loads once for a list
of structures. Soluble weights `soluble_v_48_020.pt` with `--is_legacy_weights True`. True
negative-log-likelihood recovered via a forward hook on `decoder_features.log_probs`, masked by
`mask_for_loss` so only designed positions count.

**MPNN-internal scores do not predict downstream success.** Four separate proxies failed, including
the true NLL (significant at n = 2789 but only 1.08x enrichment). We therefore do not filter on them;
we fold more sequences and let ipSAE decide.

## 3b. Surface/core polarity optimisation (rounds 3-4 only; applied to 5 of those 14)

Five designs carry a sequence optimised to bring alanine content and apolarity into the range
occupied by experimentally confirmed all-alpha EGFR binders (alanine 4.5-10.4%, hydrophobic fraction
0.329-0.442). The nine others were already inside that range or could not be brought into it without
losing the fold or the interface.

Positions are partitioned from the cycle-3 structure and treated differently, so that binding and the
pH-switch mechanism cannot be affected:

| class | definition | alphabet |
|---|---|---|
| fixed | the designed motif His/acid, the termini, and every residue within 8 A of the target | not designed |
| surface | relative side-chain SASA >= 0.25, >= 8 A from the target | polar/charged only (apolar omitted) |
| core | relative side-chain SASA < 0.25, >= 8 A from the target | Ala/Gly/Pro/Cys omitted |

Because no designed position lies within 8 A of the target, the interface is untouched by
construction. soluble ProteinMPNN generates 200 sequences per design under those per-position
restrictions (`--designed_residues`, `--omit_per_residue`), and proposals are then required to land
inside the binder envelope rather than merely to improve: hydrophobic fraction 0.329-0.42, alanine
0.02-0.158, net charge -19.3 to -5.0, charge per residue -0.12 to -0.05, pI 4.60-5.00, charged
fraction 0.30-0.42. The floor on hydrophobic fraction is as important as the ceiling -- minimising
apolarity produces sequences that satisfy the composition targets while having no hydrophobic core.

Surviving proposals are threaded onto the parent backbone and screened for steric clashes with
PyRosetta (whole-pose repack, backbone+sidechain minimisation), then **re-folded unconstrained
against both the human and mouse targets** and required to keep, in both arms: ipSAE within 0.05 of
the parent's worst-of-three, binder pLDDT >= 0.80, self-consistency RMSD < 2.0 A, both anchor salt
bridges <= 4.0 A, and native-like bridge geometry. The motif identity is asserted rather than
assumed -- the binder acid must still be Asp/Glu and the binder His still His.

Note that threading onto a *fixed* backbone measures backbone-adaptation strain, not foldability, so
PyRosetta is used here only as a clash screen; whether a sequence folds is decided by the refold.

## 4. Three-cycle refinement with restraint release (rounds 3-4)

| cycle | restraints | purpose |
|---|---|---|
| 1 | Boltz-2 contact restraints on both salt bridges | get the motif formed |
| 2 | restrained | refine |
| **3** | **UNCONSTRAINED** | the only evidence that counts |

Restraints are `constraints: - contact: {token1, token2, max_distance: 3.5, force: true}`. Polymer-token
contacts expand to a Cartesian product aggregated by a soft minimum, which makes this a genuine
closest-heavy-atom salt-bridge restraint. The driver asserts the constraint state by counting
`constraints:` blocks on disk before each cycle and aborts on mismatch — cycle 3 must carry zero.

**Selection happens at cycle 1, and that is where the leverage is.** Gating cycle 1 on
pDockQ >= 0.30, worst bridge <= 5.5 A, binder pLDDT >= 0.85, scRMSD < 2.0 was worth **11.6x** over
ranking by a composite score, at no extra compute. Thresholds are the loosest value observed across
known-good founders, with margin — calibrating from per-axis medians instead silently dropped 3 of 5.

## 5. Validation — three independent unconstrained folds

Boltz-2 2.2.1 on one V100, `--output_format mmcif --write_full_pae`, seed 7919, target MSA cached so
no MSA-server calls are made.

1. human replicate at a different seed
2. mouse domain III ortholog (cross-species specificity)
3. the cycle-3 fold itself

Both arms are submitted in **one** job because this cluster has ~2x node-to-node variance and the
arms must not be confounded by it.

Scoring: **ipSAE** (Dunbrack), computed explicitly from the Boltz-2 PAE plus the CIF at cutoffs
15/15. ipSAE writes its output next to the *input* files, not the working directory.

Two checks that are not optional:
- grep the Boltz log for `Failed to process` and confirm `manifest.json` `records` is non-empty. A
  single trailing NUL byte in a cached `.a3m` once made every record fail while the job still exited 0.
- export a per-shard `NUMBA_CACHE_DIR`; concurrent shards otherwise race on Boltz's `@njit(cache=True)`.

## 6. Acceptance gate (rounds 3-4; round 5 uses the stricter gate in 7b)

Applied to **all three** folds independently:

```
binder pLDDT >= 0.80   AND   scRMSD vs backbone < 2.0 A   AND   ipSAE >= 0.50
```

plus both designed salt bridges <= 4.0 A, and bridge geometry within the native envelope
(`realism_dev <= 2.5`; the native reference deviates from its own median by 3.39 at p95).

> **A high ipSAE does not mean the binder hit the intended epitope.** In earlier work only 3 of 15
> refolds docked where the backbone was designed to dock, and one scored 0.79 while binding a
> different face with the intended hotspots 11–20 A away. The epitope is therefore verified
> geometrically after every refold, never inferred from confidence.

## 7. pH-selectivity assessment (PyRosetta + PROPKA)

PyRosetta pH mode (`-pH_mode true -value_pH X`, `e_pH` weighted during packing only) lets the packer
choose HIS / HIS_D / HIS_P; dG is then scored with a clean ref2015. pKa from **PROPKA 3.5.1**.

Measurement protocol, with five guards each of which was learned from a failure:
- evaluation is **whole-pose**, never a local shell (a local repack freezes other titratable His and
  collapses the measurement)
- minimisation includes **backbone**, not only chi (mutate+repack alone cannot relieve clashes and
  produced up to +429 REU of noise)
- **every** His in the complex is reported, target included (the switch anchor is on the target)
- null substitutions are detected and labelled, not silently averaged in
- `structurally_broken` is flagged at parent + 25 REU
- >= 8 replicates; effect sizes quoted as absolute REU, never fold-changes (the parent's own
  baseline is near zero, so ratios are unstable)

**pKa is protocol-dependent by ~0.7 units, far more than replicate noise**: the same variant gives
6.88 +- 0.30 under a local relax and 7.58 +- 0.01 whole-pose. Always relax whole-pose before PROPKA.

## 7b. Round 5 — composition-first redesign (9 of the 23 designs)

Rounds 3-4 produced designs whose predicted interfaces were good but whose **amino-acid composition
sat outside the envelope of experimentally confirmed sub-uM all-alpha EGFR binders** (8 of 14
outside). Section 3b resurfaced five of them after the fact and recovered only those five. Round 5
moved the constraint upstream.

**Envelope enforced** (observed range of the experimentally confirmed sub-uM all-alpha binders of
the previous round; derivation and limits in `analysis/composition_envelope.md`):
alanine <= 0.104, hydrophobic AVILMFWY 0.329-0.42, net charge pH7 -19.3..-5.0, pI 4.60-5.00.
The hydrophobic **floor** is enforced as well as the ceiling: minimising apolarity produces
serine-core proteins, so the objective is closeness to the binder centroid (0.085 / 0.376), not
minimisation.

**Pipeline as run** (`protocol/scripts/round5/`):

| stage | what | scale |
|---|---|---|
| backbones | RFdiffusion3, same 9 anchor pairs as round 4, two length arms (86-146 and 179-245 aa) | 8640 designs |
| sequences | soluble ProteinMPNN with an **alanine bias of -2.0** | 37312 sequences |
| composition gate | the envelope above, applied **before any folding** | 3157 candidates |
| fold 1 | Boltz-2 with the two contact constraints, `force: true` | 2370 folds |
| founder gate | pDockQ >= 0.20, both bridges <= 5.5 A, binder pLDDT >= 0.85, scRMSD <= 2.0 A, bridge realism_dev <= 2.5 | 98 founders |
| verification | Boltz-2 **unconstrained**, two independent seeds (7919, 20261005) | 196 folds |
| acceptance | every mechanism criterion in **both** seeds; confidence criteria on the **worst** seed | **11 accepted, 9 submitted** |
| cross-species | mouse domain III unconstrained fold | 11 folds |
| pH | PyRosetta pH mode, whole-pose, 8 replicates, pH 6.5 vs 7.4 | 11 designs |

Two of the 11 accepted designs are **not** submitted: `R5_01` (187 aa, excluded on length -- our
cell-free expression evidence covers only 60-134 aa) and `R5_11` (collapsed on the mouse ortholog,
ipSAE 0.094). Both are retained in `metrics/round5_*`. See README section 3.

The alanine bias is the whole intervention: it moved the composition-gate pass rate from 4.7% to
49.2%, alanine from 0.157 to 0.072 and hydrophobic fraction from 0.452 to 0.367. All 11 accepted
designs -- and all 9 submitted -- are inside the envelope on every axis.

**Acceptance is stricter than rounds 3-4.** A design is accepted only if the binder re-docks and
*both* designed bridges re-form with no restraint **in both seeds** (<= 5.5 A in both, <= 4.0 A in at
least one), with ipSAE >= 0.50 and binder pLDDT >= 0.85 on the *worst* seed, the fold retained within
2.0 A of the constrained pose, and bridge geometry inside the native envelope. The two-seed
requirement is not redundancy theatre: the designed salt bridge replicates across folds at only
Spearman rho +0.36, so a bridge observed once unconstrained is not evidence.

> **The realism reference rests on 39 contacts.** `metrics/native_bridge_envelope.json` is built from
> 20 crystal and 19 AlphaFold His-carboxylate contacts, and the file's own caveat is that "the
> envelope tails are loosely determined -- widen or replace with a full PDB survey before treating
> the 5th/95th percentiles as hard physical limits". Since realism is the criterion that actually
> decides acceptance, that limitation propagates directly into how many designs pass.

**What actually limits yield.** Of the 98 founders, 84 fail on **bridge-geometry realism** alone;
dropping that single criterion would accept 25 instead of 11, while dropping any other criterion
changes the count by at most one. Interface confidence, docking and fold stability are effectively
free at this stage -- native-like bridge *geometry* is the scarce property. Realism is therefore a
stringency dial, and the value used here (`realism_dev <= 2.5`) is stated so it can be re-applied.

**Two results worth recording for anyone repeating this.**

1. **A `force: true` Boltz contact constraint does not mean the contact forms.** In round 4 the worst
   designed bridge had a median of 16.7 A across constrained folds with both constraints present and
   verified on disk. Any bridge threshold must be calibrated on the *current* round's distribution:
   the round-4-derived gate retained 5 of 1580 round-5 folds, while recalibrating gave 70.
2. **Designed length is a window, not a trend.** 86-146 aa gave a 5.58% founder rate and 10 of the 11
   accepted designs; 179-245 aa gave 1.45% and one -- but that one (`R5_01`, 187 aa) was the best
   round-5 design by ipSAE. Low yield, not a low ceiling. It is excluded from the submission on
   expression grounds, not on quality.

## 7c. Cysteine removal (applied to 9 of the 23 designs)

An audit of the shipped structures found **18 unpaired cysteines across 12 designs**, all of them
buried (relSASA 0.00-0.12), only one genuine disulfide in the set (`pHsel-02`). Cysteine had never
been excluded at ProteinMPNN sampling time. Free thiols are an aggregation and heterogeneity
liability, so they were redesigned away where that cost nothing.

**Only the cysteine positions were designable.** `designed_residues` named exactly those positions,
so MPNN could not touch anything else; CYS was omitted there by construction, and because every site
is core the charged and backbone-disruptive residues were omitted too. Scripts:
`protocol/scripts/cysfix/`.

> **Slice safety.** MPNN returns the whole complex and which end carries the binder depends on chain
> order in the input -- an RFD3 output puts the binder first, a Boltz co-fold puts the target first.
> Guessing wrong silently returns a slice of the TARGET. The binder slice is therefore *discovered*:
> the only acceptable slice is one reproducing the parent sequence at every non-designable position.
> All 41 candidates passed, so nothing outside the cysteine positions changed.

Two MPNN passes were run, the second with an alanine bias of -2.0. The first pass chose alanine 22
times in 40 substitutions, which would have pushed designs past the composition ceilings that round 5
exists to respect; the biased pass supplied Ser/Thr/Val/Asn/Gln alternatives. 192 samples collapsed
to **41 distinct candidates** across the 12 designs.

**Acceptance is relative to the parent**, because a cysteine is a liability rather than a defect and
the bar for replacing one is that the design is no worse. In all three unconstrained folds: ipSAE
within 0.05 of the parent, fold kept within 2.0 A, both designed bridges <= 4.0 A, binder pLDDT
>= 0.80, fewer cysteines, and the composition envelope not worsened. **25 of 41 candidates passed,
covering 9 of the 12 designs.**

**pH selectivity is a third criterion where it exists.** For the round-5 designs a fix was also
required not to cost more than 0.5 REU of switch. This proved decisive rather than cosmetic: at the
same positions, different residues swing ddG_bind by up to **3.7 REU** (`pHsel-09`: `C17S;C50S`
+0.85 against `C17M;C50T` -2.81), so these buried cysteines are coupled to the His switch in a way
no interface metric detects. Selecting on interface quality alone would have cost `pHsel-07` 1.66 REU
and `pHsel-08` 2.19 REU; selecting on all three axes instead **gained** `pHsel-07` +3.65 REU, giving
it the strongest switch in the submission.

**Apolar is preferred at a buried position, but not unconditionally.** A buried serine was only
accepted where an apolar alternative was not equal-or-better: of the nine substitutions, five go to
A/V/I/L/M/F. Two considerations limited that. First, all nine introduced polar side chains do find an
H-bond partner in the predicted structure (2.4-3.4 A, usually a local backbone carbonyl), so the
usual buried-unsatisfied-hydroxyl penalty is not in evidence here. Second, and decisively, for the
three round-5 designs the serine is **load-bearing for the pH switch**: replacing it with an apolar
residue costs 1.8-4.9 REU of ddG (`pHsel-07` +5.98 -> +1.06 as C48S;C91A -> C48A;C91V). That is the
same coupling reported above -- these buried cysteines sit in the electrostatic network that sets the
anchor His pKa -- so an apolar swap that looks free on interface metrics is not free on selectivity.

The nine substitutions as shipped:

| design | local_id | substitution | class |
|---|---|---|---|
| `pHsel-01` | `R3_01` | `C85A` | apolar |
| `pHsel-02` | `R4_03` | `C9I` | apolar |
| `pHsel-07` | `R5_05` | `C48S,C91A` | contains a polar residue |
| `pHsel-08` | `R5_08` | `C55S,C107S` | contains a polar residue |
| `pHsel-09` | `R5_07` | `C17S,C50S` | contains a polar residue |
| `pHsel-10` | `R4_07` | `C9S` | contains a polar residue |
| `pHsel-15` | `R3_04` | `C22V,C25V` | apolar |
| `pHsel-19` | `R3_02` | `C50M` | apolar |
| `pHsel-20` | `R4_05` | `C18A` | apolar |

Five are fully apolar. `pHsel-01` (C85A), `pHsel-15` (C22V;C25V) and `pHsel-19` (C50M) were
moved from a polar first choice to an apolar one after the fact, each being equal or better on
ipSAE, bridge distance and composition; none of those three moves pushed a design newly outside
the composition envelope.


`pHsel-14`, `-16` and `-22` keep their cysteines: no candidate held the interface (one broke a
designed bridge at 4.81 A, three collapsed ipSAE by 0.11-0.25). They remain flagged `free-cys:N`.

> **scRMSD is computed independently here.** `protocol/scripts/loop/loop_score.py` picks its reference chain by walking
> A..Z for the first chain whose CA count matches the binder, forcing chain B only when the reference
> path contains "boltz" or "loop". With a reference under `designs/<id>/`, neither token is present,
> so it aligns the binder onto a slice of the 170-residue target and returns a uniform 12-16 A
> artefact -- 15.87 A where the true value is 0.27 A. Every scRMSD in this round is measured with the
> binder chain identified explicitly in both structures.

## 8. Reproducing this

```bash
source scripts/env.sh                     # redirects all caches to scratch; raises ulimit -u
conda activate rfd3                       # backbones + MPNN
conda activate boltz2                     # co-folding
conda activate pyros                      # pH / pKa work
bash protocol/scripts/campaign/run_campaign.sh    # rounds 3-4, 7-stage driver

# round 5: chained SLURM orchestrators (sbatch runs from compute nodes, so each stage
# submits the next with --dependency and a wall-clock guard)
sbatch protocol/scripts/round5/r5_sbatch/r5_orch_a.sbatch   # verify + score the constrained folds
#   -> orch_b gate + 2-seed unconstrained fold + acceptance
#   -> orch_c export + pH;  orch_d mouse;  orch_e batch-2 merge;  orch_f refresh tables
```

Environment exports in `protocol/envs/`. Note `scripts/env.sh` must be sourced first: PyRosetta and
JAX both need it, and the default `ulimit -u` of 100 on every node otherwise kills anything that forks.
