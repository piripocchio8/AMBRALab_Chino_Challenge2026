# What each column of `submission.csv` means

The twenty rows share one schema so the two series can be read side by side. Not every column is
filled for every row: the two series were produced by different pipelines and measured with
different tools, and a blank means *not measured*, never *measured as zero*.

## Identity

| column | meaning |
|---|---|
| `name` | the submitted identifier |
| `sequence` | the binder sequence, as submitted |
| `molecule_class` | `protein` for every row |
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

## Expressibility

`net_charge_pH70`, `net_charge_pH74`, `pI`, `gravy`, `n_cys`, `frac_hydrophobic_AVILMFWY` and
`risk_flags` are computed from sequence alone and are reported, not optimised. A convincing design
is allowed to be awkward to make.

## The honest reading

Every number here describes a **prediction**. None of these designs has been measured. The micro
series reproducibly places a binder main-chain carbonyl in hydrogen-bonding geometry on the target
imidazolium; the double engagement that would make that binding sharply pH-dependent appears in
about 1 % of predicted models and is **not** an established property of any submitted design.
