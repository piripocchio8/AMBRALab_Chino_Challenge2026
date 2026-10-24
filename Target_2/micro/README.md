# Target 2 — micro band

**Twenty disulfide-cyclised peptides of 39 residues that bind one protomer of a TNF-family
homotrimer near a lysine pair, designed so that protonating their own histidines would release
them.**

This is the only band in this target. Every candidate in the pool is 39 residues, so there is nothing
to put in a `mini/` or a `large/` directory; `micro/` here uses **Target 1's** size definition (under
40 residues) and not a Target-2 category we have been able to verify. See the band note in
[`../README.md`](../README.md).

> **The design word is *designed*, not *observed*.** No protonation state was varied anywhere in
> this campaign; the oracles are heavy-atom only and have no concept of one. Nothing in this
> directory is evidence of a pH effect in either direction.

## The mechanism, as an objective

The target protomer presents **Lys57 and Lys104** (human) / **Lys57 and Lys103** (mouse — position
104 is a proline there, so the site is derived per species rather than copied). A lysine ammonium
carries its positive charge at every pH of interest. A histidine does not.

Each design carries **two or three histidines at interfacial positions**, and was optimised to seat
them within **5–7 Å** of that pair on **one** protomer. At blood pH those histidines would be
neutral beside a permanent cation; as the pH falls each would become an imidazolium — a cation
beside a cation — and the complex would be destabilised. **The prediction is a direction: weaker
binding at acidic pH.** A flat or inverted result refutes the design hypothesis outright, which is
more useful than an unexplained binder.

**What is designed is proximity, not a bond.** Coulombic destabilisation does not need a specific
hydrogen bond, and requiring one would specify a geometry the mechanism does not need. A 3.5 Å
hydrogen-bond test is kept as a separate readout and is never the criterion.

**Both histidines must land on the same protomer**, because the designed epitope spans about 15 Å on
one subunit while a cross-subunit arrangement asks for about 29 Å. Scoring that minimises each
histidine over protomers independently cannot see the difference; the instrument used in the
previous round picks the protomer that minimises the **worse** of the two distances, so the pair is
scored jointly or not at all.

**How close this band gets.** On the delivered 20, primary oracle, human arm: the binder's closest
heavy atom reaches **2.46–4.85 Å** of Lys57 NZ — under an 8 Å pocket restraint on Lys57 — and
**3.53–11.10 Å** of Lys104 NZ, median 7.81 Å, with only 7 of 20 inside 7 Å. The unrestrained half of
the designed pair is not engaged. The joint two-histidine seating criterion itself was **not
computed for this band**; it belonged to the previous round's instrument, and we name that gap
rather than fill the column from a different arm.

## What is in this directory

Thirty directories — `AMBRA_T2_micro_01` … `AMBRA_T2_micro_20` for the submitted band and
`AMBRA_T2_micro_21` … `AMBRA_T2_micro_30` for the ten designs that are documented and **not**
submitted — each holding:

| file | what it is |
|---|---|
| `human_model_0.cif` … `human_model_4.cif` | the five primary-oracle models of the human complex that every human figure for this design is a median or a count over |
| `mouse_model_0.cif` … `mouse_model_4.cif` | the same five for the mouse complex |
| `restraints.csv` | the restraint file as given to the oracle — one row, an 8 Å pocket on Lys57 |
| `sequence.fasta` | the binder sequence under its deposited name |
| `metrics.json` | every number quoted for that design, field names matching `../metrics_full.csv` |

**No design directory carries a "selected" model.** Every figure is a median or a count over the
five, because the primary oracle is nondeterministic on this system and the best of *n* draws is a
property of *n*. The second and third oracles' coordinates are not deposited; their per-design
numbers are in `../metrics_full.csv`.

The deposited names are assigned in the delivered order, which is **the worse of the two orthologs'
interface ipTM**, descending — never the mean, never the maximum, never the difference between them.
**That order is not a claim** — see the band note below and `../README.md`. `AMBRA_T2_micro_21`
through `_30` carry a `status` and no `submission_rank`: each clears every criterion and is simply
below the line in a qualifying pool of 30. The internal campaign identifiers are deliberately not
carried into this directory; `parent_family` groups designs that share a backbone, and
`design_origin` says whether a design is a family's original or an inverse-folding repack of it —
**20 repacks, no originals, 10 families**, because no family original cleared the fold floor on both
orthologs.

## Limits

- **Nothing here has been measured.** Every number is a property of a structure prediction — no
  binding data, no pH titration, no expression or synthesis result.
- **Nothing here tests protonation.** The two orthologs differ in sequence and length, not in pH,
  and no protonation state was varied. The predicted-pKa column runs −1.39 to +0.68 over the band
  with a median of −0.27 and only 2 of 20 positive, so it does not support the mechanism either.
- **Unaided engagement of the epitope has not been demonstrated**, and this band has no
  restraint-free arm of its own. In the previous round the designs with such data missed Lys57 by
  6.5–17.7 Å, and the designed two-histidine arrangement appeared in 4 of 36 systems by the primary
  oracle and 0 of 36 by the second. The binders find the face; they do not yet reproduce the
  arrangement without help.
- **The folds this band was cut on carry an 8 Å pocket on Lys57.** That states where the binder
  goes, not the interaction being measured — and it is far weaker than the previous round's explicit
  5–7 Å histidine-to-lysine rows — but it is not nothing. On this arm it was strong enough to make
  the 5 Å Lys57 gate inert: 99.1 % of 325 passed it and nine deciles sit between 2.4 and 3.7 Å.
- **This is a set, not an order.** Both halves of the rule reproduce across independent draws of
  the primary oracle: all 17 delivered designs with re-draw data still clear the 0.65 binder-pLDDT
  floor on **both** orthologs at a different seed, and the worse-ortholog ranking key returns at
  ρ = +0.9447 [+0.7970, +0.9897] with 17 of 17 staying in the re-drawn top 20 of the same pool. But
  reproducing is not discriminating: eleven of the twenty sit inside 0.0467 on the key, and the
  first design cut from the pool is 0.0060 below the lowest delivered one. `submission_rank` exists
  because the upload form reads a ranking from the top row down.
- **The objective is that BOTH orthologs are bound — not selectivity, and not preference.** The
  band is gated on a binder-pLDDT floor of 0.65 applied to the human arm **and** the mouse arm, and
  ranked on the **worse** of the two orthologs' interface ipTM, so a design that binds one well and
  the other poorly ranks low by construction. 34 of 325 clear the floor on both arms, 30 of those
  clear every primary-oracle gate, and the band is the top 20 of those 30. The full argument is in
  `../docs/methods_micro.md` §4.4.1.
- **The human-minus-mouse difference is reported and is not a criterion.** It gates nothing, orders
  nothing, and runs −0.3404 to +0.3836 over the band, positive for 8 designs and negative for 12.
  **No ortholog preference is claimed.** The measured reason it is not used: it reproduces inside
  the primary oracle (**ρ = +0.948 [+0.926, +0.964], n = 325**, both orthologs re-drawn) and no
  second oracle confirms it (ρ = +0.0533 [−0.0569, +0.1580], **8.3 %** of attainable, interval
  containing zero), so it is a property of *(design, oracle)*.
- **For five designs the two orthologs are closer together than the measurement's own
  draw-to-draw spread**, so which one is the worse is **not established** for them. They are marked
  with a dagger in the band table of `../docs/methods_micro.md` §8.
- **The three oracles disagree about which designs bind.** The agreement rule is defined on the
  50-design replicate pool and ranks each oracle on its **human** arm, which is not this band's key;
  three delivered designs sit outside the pool, so the denominator is 17. The second oracle places
  6 of those 17 in its own top 20 of the same 50 and the third places 10, with 3 in both, against
  6.8 and 2.7 expected by chance. They agree about folding and not about binding.
- **The second oracle's quality gate was relaxed for this band.** It applied the same four gates to
  its own models, and 53 of the 148 designs clearing the primary oracle's gates were demoted for
  failing one of its — mostly its binder-pLDDT gate. That demotion built the 50-design pool; it does
  **not** gate this band. `boltz_state` is reported per design, and three submitted designs carry
  `fail`: `AMBRA_T2_micro_03`, `AMBRA_T2_micro_09` and `AMBRA_T2_micro_11`.
- **The magnitude of the pH effect is not computed**, only its intended direction. No free energy of
  the protonated against the neutral complex exists, and the predicted-pKa axis cannot supply one.
- **One of the two originally designed histidines had no consistent partner** in the previous round
  — it hydrogen-bonds in 63 % of folds with three distinct partners across twenty designs. That
  measurement is why the current bar asks for *any* two interfacial histidines rather than two named
  positions, and why the histidine positions in this band vary from design to design
  (`his_positions` in each `metrics.json`).

Selection, metrics and the bars are in [`../docs/methods_micro.md`](../docs/methods_micro.md) and
[`../docs/metrics.md`](../docs/metrics.md).
