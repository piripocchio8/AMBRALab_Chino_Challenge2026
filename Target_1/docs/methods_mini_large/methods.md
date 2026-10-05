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

## 3b. Surface/core polarity optimisation (applied to 5 of the 14)

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

## 4. Three-cycle refinement with restraint release

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

## 6. Acceptance gate

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

## 8. Reproducing this

```bash
source scripts/env.sh                     # redirects all caches to scratch; raises ulimit -u
conda activate rfd3                       # backbones + MPNN
conda activate boltz2                     # co-folding
conda activate pyros                      # pH / pKa work
bash protocol/scripts/campaign/run_campaign.sh    # 7-stage driver
```

Environment exports in `protocol/envs/`. Note `scripts/env.sh` must be sourced first: PyRosetta and
JAX both need it, and the default `ulimit -u` of 100 on every node otherwise kills anything that forks.
