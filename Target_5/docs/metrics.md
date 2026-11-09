# What each column means

Every column of `metrics_full.csv` is reproduced in each design's `metrics.json`, with the
per-model values that the summary was taken over. Distances are Å; RMSD is on Cα unless stated.

## Identity

| column | meaning |
|---|---|
| `name` | the submitted identifier, `AMBRA_T5_01` … `_20`, in rank order |
| `design_id` | the internal identifier of the design run, kept so a number can be traced |
| `lineage` | the parent design this one descends from; several entries share a parent |
| `generation` | *delivered* = as the search produced it; *redesign* = its sequence re-sampled inside its own complex with the interface held fixed; *elong+redesign* = the same after extending one terminus by ten residues |
| `binder_length` | residues in the submitted chain |

## The selection criteria, in the order they were applied

`priorities_met` prints one character per criterion, its number when met and `-` when missed.

1. **Lands on the groove, unrestrained** — `on_groove` ≥ 60 % of models place the binder with most
   of its HLA contacts on the α1/α2 groove helices (residues 57–84 and 138–180) while touching the
   decamer, with no restraint table. `engaged` counts models touching the decamer at all.
2. **Induces the IN state, unrestrained** — `IN_unrestrained` of `n_models_unrestrained` models put
   the Asp6 carboxylate (OD1/OD2) within 4 Å of the Arg114 guanidinium (NH1/NH2/NE). Met when a
   one-sided Fisher exact test against the binder-free control (0 of 50) gives p < 0.05.
   `IN_95CI_low/high` is the Wilson interval on that fraction.
3. **Folds alone** — `alone_plddt` ≥ 70, `alone_vs_bound_A` ≤ 2.0, and the spread among the
   unbound models ≤ 2.0. This is the campaign's gate F, unchanged.
4. **Tells G12D from wild type** — `margin_unrestrained` ≥ +0.035, the margin the therapeutic TCR
   itself shows unrestrained, or `margin_restrained` ≥ +0.10.

## The two arms, which are different measurements

| column | arm | meaning |
|---|---|---|
| `iptm_G12D`, `iptm_WT` | unrestrained | median binder-vs-decamer ipTM over the ensemble, on each peptide |
| `margin_unrestrained` | unrestrained | `iptm_G12D` − `iptm_WT`. Negative means the binder prefers wild-type KRAS |
| `iptm_restrained`, `margin_restrained`, `IN_restrained` | restrained | the same quantities measured with the design's own declared restraint table in place |
| `campaign_gates` | restrained | the delivery gates: **E** cold ipTM ≥ 0.40, **F** folds alone, **S** G12D ≥ WT by sign, **I** IN in ≥ 3 of 5. A `.` is a fail |

The within-cell standard deviation of the margin is 0.0295, so a margin of +0.035 is about one
standard deviation from zero and +0.10 is more than three. The sign alone carries little.

## Geometry reported as a check, not ranked on

| column | meaning |
|---|---|
| `d6_deposited_model_A` | Asp6–Arg114 in the coordinate file in this directory; `d6_all_models_A` in `metrics.json` places it in its ensemble |
| `d6_min_A` | the closest approach over the ensemble |
| `peptide_register_rmsd_A` | decamer Cα RMSD to the 7OW6 peptide after superposing the groove helices. It separates a binder that holds Asp6 against Arg114 from one that slid the peptide until Asp6 happened to be there. All twenty sit between 0.72 and 1.99 Å, so none is doing the latter |
| `closest_contact_A` | tightest heavy-atom approach between binder and pMHC. Read it against the deposited crystal (2.69 Å) and against the oracle's own models of that same TCR (1.14–2.57 Å, median 2.19 over 75 models). Sub-2 Å is the oracle's signature across the board, so nothing is ranked on it |
| `term_rmsd_A`, `core_rmsd_A`, `iface_rmsd_A` | bound-minus-unbound displacement split at the first and last four residues, the rest, and the residues contacting the decamer. A design over 2 Å on core but at or under 1 Å on iface keeps its binding face and loosens elsewhere, which is a different object from one that rearranges the face |
| `free_terminal_residues` | residues at the two termini touching nothing at all in the bound pose |

## ipSAE

| column | meaning |
|---|---|
| `ipsae_binder_target` | ipSAE between the binder and all target chains taken together |
| `ipsae_binder_peptide` | ipSAE between the binder and the decamer alone — the designed interaction |
| `ipsae_binder_hla` | ipSAE between the binder and the HLA heavy chain |
| `apo_ipsae_binder_target` | the same, in the peptide-free arm |
| `n_models_ipsae` | models behind these values (5) |
| `ipsae_method` (in `metrics.json`) | every parameter used, written out |

ipSAE is computed from predicted aligned error, which the campaign's earlier waves did not store,
so **a dedicated 5-model ensemble was folded for all twenty** under the unrestrained G12D
condition with PAE saved. That ensemble is used for ipSAE **and for nothing else**: it is not
pooled with the ensembles behind the IN counts and the ranking, which have their own *n*. The two
should not be averaged together.

Parameters, pinned because published implementations differ: PAE cutoff **10.0** (strict),
L floor **27**, d0 minimum **1.0**, d0 = max(1.0, 1.24·(max(27, n_valid) − 15)^(1/3) − 1.8) per
residue, term 1/(1 + (PAE/d0)²) applied to the **PAE value**, mean over PAE-valid partners only,
max over residues, larger of the two chain directions.

Across the twenty, `ipsae_binder_target` has a median of **0.583** and a range of 0.000–0.813;
`ipsae_binder_peptide` is lower throughout (median 0.200), as expected for a ten-residue partner.
**Four designs score at or below 0.02** — `AMBRA_T5_09`, `_17`, `_18`, `_19`. For `AMBRA_T5_09`
this is not a rounding artefact: in that ensemble **no** binder–target residue pair has a PAE below
the cutoff at all (minimum inter-chain PAE 15.0). That design is in the first ten for what it does
under the single declared Asp6–Ile97 contact, and its unrestrained interface is weak by every
measure we have — on-groove in 15 of 20, the lowest binder–HLA ipTM in the set (0.209), and now
ipSAE 0.000. The deposit does not hide this.

## The peptide-free arm, and the two screens added for the selection process

| column | meaning |
|---|---|
| `apo_hla_iptm` | median binder↔HLA chain-pair ipTM with **no peptide in the groove** — three chains (binder, HLA heavy chain, β2-microglobulin), no restraint table, 5 models. This is challenge goal (b), measured directly |
| `g12d_hla_iptm` | the same quantity in the G12D complex, so the comparison is like for like. The campaign's ranking axis is binder↔**decamer** ipTM (`iptm_G12D`), which has no counterpart in a peptide-free fold |
| `apo_minus_g12d_hla_iptm` | the difference. Negative means the design is less confident of the HLA when the peptide is gone |
| `n_models_apo` | models behind the apo numbers (5) |
| `mean_kd_hydropathy` | Kyte & Doolittle 1982 scale, unweighted mean over the whole submitted chain. Lower is more hydrophilic |

A peptide-free class I heterodimer is not a physiological species and the oracle has seen very few,
so an empty groove may attract a binder for reasons that have nothing to do with this target. The
apo arm is reported as a screen against goal (b), not as a verdict on it, and nothing was re-ranked
on it: it was folded after the twenty were fixed.

## A measurement that was withdrawn

An earlier version of this analysis reported a peptide Val3 backbone state (ψ3) on which the oracle
separated TCR+G12D from TCR+WT 25 of 25 against 2 of 25. The deposited structures refute it: 7OW6
gives ψ3 = 155° and 7OW5 gives 153°, both in the same basin. The switch is the oracle's and not the
receptor's, and the column is not reported.
