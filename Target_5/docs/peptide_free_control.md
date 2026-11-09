# The peptide-free arm — challenge goal (b)

Goal (b) of this run asks for **no binding to the same HLA and β2-microglobulin with no peptide**.
The campaign had never measured it for a design: the binder-free control that the IN counts are
read against (0 of 50) is the *groove without a binder*, which answers a different question. So all
twenty deposited designs were re-predicted for this submission as **three chains — binder, HLA
heavy chain, β2-microglobulin — with the peptide record deleted and no restraint table**, five
models each, through the same code path and seed as every other unrestrained fold. The hypotheses
were written down before the folds existed.

## What was measured

| quantity | why |
|---|---|
| `apo_hla_iptm` vs `g12d_hla_iptm` | binder↔**HLA** chain-pair ipTM in both arms. The campaign's ranking axis is binder↔decamer ipTM, which has no counterpart when there is no decamer, so the HLA pair is the only like-for-like comparison |
| `apo_binder_atoms_in_peptide_seat` | the apo model superposed on the G12D model by HLA Cα, then binder heavy atoms counted within 4 Å of where the decamer sits. Confidence says how sure the oracle is; this says **where the chain went** |
| `apo_groove_helix_frac` | share of the binder's HLA contacts lying on the α1/α2 helices (57–84, 138–180), measured identically in both arms |
| `apo_binder_plddt` vs `binder_plddt` | mean pLDDT of the binder chain itself in each arm. A chain modelled into a pose the oracle cannot commit to loses pLDDT, independently of any interface score |

## Result

**Confidence falls for every design.** All twenty have a lower binder↔HLA ipTM without the peptide:
median **−0.207**, range −0.015 to −0.551. Not one design is more confident of the empty
heterodimer than of the G12D complex.

**But the binders do not leave the groove.** They stay on the α1/α2 helices (groove-helix fraction
0.59–1.00 in apo, against 0.80–1.00 with the peptide present), they contact *more* HLA residues
than before (median **+6**), and **19 of 20 occupy the seat the peptide vacated** — a median of
**47.5** binder heavy atoms within 4 Å of the decamer's position, in 5 of 5 models for 17 of them.

**The binder itself is modelled worse there.** Binder pLDDT falls in **20 of 20** designs without
the peptide, median **−7.7** (range −1.9 to −16.6), and the apo median sits at **71.3** against **81.3**
with the peptide present, both read by the one script so the pair is comparable. So the oracle is not quietly confident about an alternative pose: the
interface score falls, and the chain's own confidence falls with it.

**One design is the exception.** `AMBRA_T5_12` puts **0** atoms in that seat in its median model
(1 of 5 models reaches 10), its groove-helix fraction falls to 0.59, and its ipTM drops 0.477. It
is the only design in this set with positive structural evidence for goal (b).

## What this does and does not support

It does **not** support a claim of peptide-free non-binding, and we do not make one. The honest
reading is that the oracle is less confident of the empty heterodimer in every case — in the
interface score **and** in the binder's own pLDDT — while the designed chain nonetheless stays on
the groove and fills the empty channel. A design selected to engage a side chain in the middle of
a groove has no reason to refuse the groove when that side chain is absent, and we did not select
against it: goal (b) was never an objective of the search.

**The pose the oracle produces in this arm is not a realizable state.** A peptide-free class I
heavy chain is not a stable species: without peptide the heterodimer does not hold its fold, which
is why empty HLA is loaded in the ER rather than found waiting on the surface. The structure
returned here is a model of a complex that does not persist, so a binder "occupying the groove" in
it describes what the predictor does with an empty channel, not an interaction that could be
measured at the bench. The two confidence drops — interface and binder pLDDT, both 20 of 20 — are
consistent with exactly that: the oracle fills the hole and is less sure of everything it writes
while doing so.

Two further cautions, stated rather than discovered:

1. **The construct itself is not physiological**, as above, and the oracle has seen very few empty
   grooves. This arm is a **screen**, not a verdict.
2. **No peptide-free positive control was run**, so the −0.207 median drop has no external
   yardstick. We can say every design moves in the expected direction; we cannot say by how much it
   *should* move.

Nothing was re-ranked on this measurement. It was folded after the twenty and their order were
fixed, and it is reported because the organizers ask for goal (b) and this is what we can honestly
say about it. The designs with the strongest evidence here, in order, are `AMBRA_T5_12` (ranked
12th on the campaign's own criteria), then `AMBRA_T5_04`, `AMBRA_T5_03` and `AMBRA_T5_01`; the
weakest are `AMBRA_T5_06`, `AMBRA_T5_10`, `AMBRA_T5_20` and `AMBRA_T5_07`, which keep an apo ipTM
of 0.60–0.70.
