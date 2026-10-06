# What each column of `metrics_full.csv` means

> `submission.csv` is the file submitted to the challenge and carries **only** the three columns
> the template defines — `name`, `sequence`, `molecule_class` — with `molecule_class` =
> `single_chain` for every design. Everything measured here lives beside it in
> `metrics_full.csv`, keyed by the same `name`, so the submission stays in the required format
> while nothing is lost.

The twenty rows share one schema so the two series can be read side by side. Not every column is
filled for every row: the two series were produced by different pipelines and measured with
different tools, and a blank means *not measured*, never *measured as zero*.

## Identity

| column | meaning |
|---|---|
| `name` | the submitted identifier |
| `sequence` | the binder sequence, as submitted |
| `molecule_class` | `single_chain` for every row — the upload form accepts `single_chain`, `nanobody`, `scfv`, `fab_kappa`, `fab_lambda` |
| `submission_rank` | 1 is the entry we would most like tested |
| `binder_length` | residues |
| `series` | `micro`, `mini` or `large` |
| `target_histidine_uniprot` | which histidine this design engages, in UniProt P00533 numbering |
| `mechanism` | how it engages it |

## Prediction confidence

| column | meaning |
|---|---|
| `interface_iptm` | interface predicted TM-score. Note it is **not** comparable across predictors, and it carries no information about whether the binder is at the intended site - one design scored 0.918 while sitting 18 Å away |
| `ipsae` | interface pSAE, the stricter interface score; for the mini/large rows this is the minimum over three independent folds. **The two series are not comparable on this number**: the micro peptides score 0.03-0.41 and the scaffolded designs 0.89-0.91, which is what a 12-39 residue binder burying a fraction of the surface of a 110-residue one looks like, not a measure of which is more likely to work |
| `lis` | local interaction score: the mean of (1 - PAE/12) over inter-chain pairs below 12 Å, so a small confident interface is not averaged away by a large uncertain one |
| `pdockq` | pDockQ from interface pLDDT and contact count (Bryant 2022 constants, untuned) |
| `plddt_binder`, `plddt_complex` | mean pLDDT, 0-1 |
| `shape_complementarity` | interface shape complementarity estimate |
| `bsa_A2` | buried surface area, Å² |
| `n_interchain_hbonds`, `interface_contacts_5A` | interface size |

## The pH-switch measurements (micro series)

These are the columns the micro designs were actually selected on. Each is a count over **all**
predicted models of that design, pooled across both oracle settings, so the denominator is the
evidence base rather than a single lucky draw.

| column | meaning |
|---|---|
| `human_engaged_models` | models where any acceptor reaches a ring nitrogen in hydrogen-bonding geometry |
| `human_binder_bond_models` | models where **the binder** supplies that acceptor. This is the headline number |
| `human_bidentate_models` | models where **both** ring nitrogens are satisfied by two different acceptors - the arrangement that would make binding sharply pH-dependent |
| `inverse_direction_models` | models where the binder **donates into** a ring nitrogen instead. This is an inverted switch: it requires the ring deprotonated, so it favours pH 7.4 over 6.5. Lower is better |
| `mouse_bidentate_models` | the same count on the mouse ortholog, which is what the search optimised against |
| `rg_ratio` | radius of gyration over the compact expectation for that length; above about 1.3 the chain is extended |

## Reproducibility: does the same thing happen every time?

A single predicted complex says what the oracle produced once. These columns say what it produces
*repeatedly*, over many independent refolds of the same sequence, and they are the properties the
final ranking is built on. Two different failures are separated here, because a design can fold
consistently and still dock somewhere different each time.

| column | meaning |
|---|---|
| `n_refolds_human`, `n_refolds_mouse` | how many independent models the rates below are computed from. Read these first: a rate over five models is not a rate |
| `pose_rmsd_human_A` | median backbone RMSD of the binder to its own best pose, after superposing the two structures on the **target**. This asks whether the peptide docks in the same place every time |
| `pose_reproducible_human` | fraction of refolds landing within 2 Å of that best pose |
| `rmsf_human_A` | mean spread of each binder residue about its average position across refolds |
| `fold_spread_human_A`, `fold_spread_mouse_A` | median pairwise RMSD of the binder to itself within one species, superposing binder on binder. This asks whether it is one structure, independently of where it sits |
| `cross_species_rmsd_A` | best agreement between a human-bound and a mouse-bound conformation. A large value means the peptide adopts genuinely different structures against the two orthologs |
| `ipsae_human`, `ipsae_mouse` | median ipSAE over **all** models of that species, computed per token (the residue-aggregated form collapses its d0 on atom-tokenised residues) |
| `iptm_human`, `iptm_mouse` | median of the **binder-target** entry of the per-chain-pair ipTM matrix, not the global ipTM — on a 161-residue target the global figure is dominated by the target's own confidence |
| `frac_extended` | fraction of models with `rg_ratio` above 1.25, i.e. not folded |
| `apo_rmsd_A` | RMSD between the binder folded **alone** and its bound conformation. Small means the peptide already holds the binding-competent fold; large means the target has to fold it |

## pH sensitivity, as a number

| column | meaning |
|---|---|
| `dpka_his_human`, `dpka_his_mouse` | the predicted pKa of the target histidine **with** the binder minus the same quantity **without** it, computed by propka on the same coordinates so that conformation cannot account for the difference, and taken as the median over the five best-engaged models of that species. **Positive** means the binder stabilises the protonated ring and therefore prefers acidic pH, which is the behaviour the challenge asks for; **negative** means it stabilises the neutral ring, an inverted switch favouring pH 7.4 |
| `dpka_his_human_spread`, `dpka_his_human_usable` | how far the shift moves between the five models, and whether it was stable enough to score. A shift that varies by several pH units between models of the same design is not a measurement of that design, so it is treated as **unmeasured** rather than as a large negative - otherwise designs would be ranked by how noisy their propka runs were |
| `vina_kcal_human` | AutoDock Vina interaction energy of the predicted pose, scored in place without docking or minimisation. An independent opinion on whether the interface is worth anything, from a function unrelated to the model that built it. More negative is better |

Burial and hydrogen bonding pull `dpka` in opposite directions: putting a histidine into an
interface lowers its pKa, while accepting a hydrogen bond from it raises the pKa. For most designs
burial wins, and only a few show a net shift in the direction the mechanism intends.

## Two gates applied before scoring

A weighted sum lets a design that fails badly on one axis be carried by the other three, so two
disqualifications are applied as gates rather than penalties:

- **extended in either species** (`frac_extended` above half for human or mouse) — not a folded
  binder against that ortholog, whatever the other numbers say;
- **median pose RMSD above 6 Å** from the design's own best pose — it is not binding one site.

Designs rejected by a gate are named in `docs/methods_micro.md` with the reason, rather than quietly
dropped.

## The overall score

`overall_score` combines four sub-scores, each already on 0 to 1 and each reported beside it, so the
ranking can be argued with rather than taken on trust:

| component | weight | what it is |
|---|---|---|
| `score_cross` | 0.30 | computed per species from the interface confidence (ipSAE and the binder-target ipTM) **and** the engagement rate, then taken as the **lower** of the two species — never the average, because a design that works on one ortholog and not the other is not cross-reactive and an average hides exactly that. Both halves must hold: a 12-mer can make the hydrogen bond in 40 % of models with an ipSAE of 0.03, which is an interface too small to believe |
| `score_ph` | 0.25 | bond direction, number and energy together: half the propka shift in the intended direction, a quarter the rate of double engagement, a quarter the vina interaction energy |
| `score_binding` | 0.25 | pose reproducibility, discounted by the per-residue spread |
| `score_fold` | 0.20 | one structure, **in both species** (extension taken from the worse one, never pooled) and - where measured - unaided |

Cross-reactivity and pH sensitivity are what the challenge is judged on, so they carry half the
weight between them. The two consistency axes decide between designs making the same claim, by
asking whether that claim survives being refolded from scratch.

## The second predictor

Four columns report an independent co-folding model given the same two statements as the primary
oracle - the binder's disulfide and a pocket on the target histidine.

| column | meaning |
|---|---|
| `boltz_iptm`, `boltz_binder_ptm` | its confidence in the complex and in the binder |
| `boltz_dist_to_His25_A` | **the distance from the binder to the target histidine in its prediction** |
| `boltz_ring_engaged` | ring nitrogens it finds engaged, by the same four criteria |

Read the distance column first. The second predictor places five of the eight within 8 Å of the
target histidine and the other three 11.8 to 15.4 Å away, while reporting interface confidences of
0.55 to 0.90 regardless - the highest-confidence case among all designs tested sat 18 Å from the
site. **Its confidence carries no information about whether the binder is in the right place**, so
it is reported beside a measured distance and never instead of one. It is also a model trained
largely on natural complexes with alignments on both chains, and a designed peptide with no
homologues is outside that distribution, so its disagreement with the primary oracle is weak
evidence either way.

## Expressibility

`net_charge_pH70`, `net_charge_pH74`, `pI`, `gravy`, `n_cys`, `frac_hydrophobic_AVILMFWY` and
`risk_flags` are computed from sequence alone and are reported, not optimised. A convincing design
is allowed to be awkward to make.

## The honest reading

Every number here describes a **prediction**. None of these designs has been measured. The micro
series reproducibly places a binder main-chain carbonyl in hydrogen-bonding geometry on the target
imidazolium; the double engagement that would make that binding sharply pH-dependent appears in
about 1 % of predicted models and is **not** an established property of any submitted design.
