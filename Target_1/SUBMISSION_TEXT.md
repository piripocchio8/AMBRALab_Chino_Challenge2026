# Text for the submission form's description box

*(Paste as-is. The attachable file is `Target_1/DESIGN_STRATEGY.md` in the repository.)*

---

**pH-selective EGFR domain III binders — AMBRA group, Chino lab, University of Naples Federico II**

We optimised for **pH selectivity**, not affinity: binding that differs between tumour pH (~6.5) and
blood pH (7.4), built on a histidine of the target whose imidazole is protonated at the lower pH. We
submit **two independent series, against two different histidines, by two different chemistries,
from pipelines that share no code**. Neither can take the other down.

**Micro — 8 disulfide-cyclised peptides, 12–39 aa, engaging His358.** Binder main-chain carbonyls
accept from the protonated imidazolium. **This histidine was chosen because the target already
supplies a charge partner for it:** Glu11 sits adjacent to the conserved Asn355–Lys357–His358 cluster
and is identical in position in both orthologs, so a binder holding that cluster also holds the
target's own carboxylate against the protonated ring — the same physics the scaffolded series
engineers onto its binders, reached from the opposite side. Glu11 was deliberately never declared as
a restraint, so whether the pair forms is the binder's doing: it ranges from **2.9 to 18.1 Å across
the shortlist**, and the leading design holds it under 4 Å in **76 % of human and 100 % of mouse**
models.

Sequences were optimised **directly against a structure oracle** by an evolutionary algorithm, then
refined by **interaction-preserving inverse folding (CARBonAra)**: the hydrogen bonds, charge pairs
and stacking coordinated to the histidine were held fixed while the rest of the binder was repacked.
This reached what the standard RFdiffusion3→ProteinMPNN route did not — that pipeline produced
nothing below 60 residues and could not target His358, a site whose double-carbonyl motif occurs in
~0.455 % of PDB histidines, about six times rarer than the carboxylate-bridged alternative. They take
the same cell-free route from synthetic DNA as every other entry, and at 12–39 aa they sit at the
favourable end of the strongest *negative* expression term in this competition's own 800-design EGFR
dataset — length. That cuts the other way for *binding*, and we state it plainly below.

**Mini and large — 12 scaffolded proteins, 94–129 aa, engaging His433 by a reciprocal two-point
motif.** This is the concept the series exists to test. Most pH-switch designs hang the effect on a
single titratable contact; these build **two His–carboxylate salt bridges pointing in opposite
directions**, both switching on as the pH falls. The *switch* pair takes the target's **His433**,
protonated at pH 6.5, to an engineered **carboxylate** on the binder. The *anchor* pair runs the
other way: the binder's **own engineered histidine** to the target's **Asp460**. Because both
histidines titrate across the same window, the two bridges engage together going from blood pH to
tumour pH — the protonation dependence is doubled rather than carried by one contact, and the second
pair fixes the register of the interface rather than merely adding affinity.

That makes the binder's anchor histidine a **design variable, not a passive clamp**: its pKa is set
by the electrostatic environment built around it, and the campaign shows this rather than asserting
it — substituting an apolar residue for a serine in that network costs **1.8–4.9 REU** of pH-switch
ΔΔG while being free on every interface metric. Selectivity and affinity are separable here, and the
design optimises the former explicitly.

Built from motif-scaffolded RFdiffusion3 on nine enumerated anchor geometries, soluble ProteinMPNN
and Boltz-2 co-folding. A fifth round enforced an **amino-acid composition envelope taken from
experimentally confirmed sub-µM α-helical EGFR binders *before* any folding** (11 of 12 inside it),
and a later pass removed 18 unpaired buried cysteines, so **all 12 ship with zero free thiols**.
Acceptance required both bridges to re-form **without restraints in two independent seeds** — the
salt bridge replicates across folds at only ρ = +0.36, so a bridge seen once is not evidence; of 98
founders, 84 failed on **bridge-geometry realism alone**. They carry ipSAE **0.833–0.912 human /
0.794–0.891 mouse**, binder pLDDT 0.915–0.965, His433 bridge 2.64–3.34 Å, and PyRosetta pH-mode ΔΔG
for 7 of them (0.47–5.98 REU favouring the acidic form).

**The two series together give the pH switch a control, and it works.** Running propka on a
scaffolded complex and on the same coordinates with the binder deleted: the target's His433 goes from
pKa **6.26 free to 6.89 bound** — 36.5 % → 71.1 % protonated at pH 6.5 against 6.8 % → 23.6 % at
pH 7.4, widening the selectivity window from 0.298 to 0.474. The term breakdown shows the binder's
engineered carboxylate contributing **+1.60 (H-bond) and +1.52 (coulombic) against −2.73 of
desolvation** at 100 % burial. The micro series' neutral main-chain carbonyls contribute +0.44 and
+0.55 against −1.28 and come out negative. Same tool, same protein, opposite sign, and the only
difference is whether the acceptor carries a charge — which is why the micro series' pH evidence is
read from geometry while the scaffolded series' is supported by propka directly. It also confirms the
free target histidine titrates normally (6.8 % protonated at pH 7.4), so there is a real window to
exploit rather than a histidine already saturated before the binder arrives.

**The mechanism commits to a direction.** Neutral imidazole carries one N–H, so a geometry with both
ring nitrogens donating is only constructible on the **imidazolium**. That predicts tighter binding
at acidic pH; a flat or inverted result refutes the hypothesis outright, which is more informative
than an unexplained binder.

**Selection rested on 5,849 predicted structures.** Every micro design was refolded to 45 models
against human and 30–35 against mouse under its own restraints, so the two rates mean the same
thing; nothing is ranked on a best model. Four axes — cross-reactivity (ipSAE and binder–target ipTM
with engagement rate, taken from the *worse* species, never the average), pH sensitivity (read from
geometry), binding consistency, fold consistency. Three disqualifications are mechanism failures and
cannot be waived: extended in either species; a binder that **lands somewhere different on every
refold**, measured as the average RMSD between its poses with every model superposed on the target
alone — reference-free, because deviation from a design's own best pose flatters a scattered set; and
a binder lysine or arginine held against the imidazolium, which pushes the histidine's pKa the wrong
way and works against our own switch. The leading micro design has **equal interface confidence on human and mouse** (ipSAE
0.368/0.390), is the **same structure in both** (0.25 Å), and **already holds its bound conformation
unaided** (0.37 Å between the free peptide and its bound form). The micro campaign ran against the
**mouse** ortholog and was evaluated on human without re-optimisation — transfer, not a fit to the
scored sequence, and the same molecules are directly testable in mouse models.

**Independently validated, including where that disagrees with us.** All micro designs were refolded
by **Boltz-2** and **Protenix** on the same restraints. All three oracles converge on the same
conformation (fold spread 0.21–0.35 Å), but they are **less convinced about the hydrogen bond** than
the oracle the designs were optimised against (engagement 0.00–0.60 ours, 0.10–0.40 Boltz, 0.00–0.30
Protenix). We report that rather than only the model that agrees with us. A predicted pKa shift is
published but deliberately **not scored**: propka credits each hydrogen bond at ~0.5 pKa units while
burial of the histidine costs more than 1, so it returns a negative shift for a geometry that cannot
exist without the cation.

**The length risk, from your own data.** Length helps expression and hurts binding, and the second
effect is the one that should worry you here: that same dataset gives a 3.4 % hit rate at ≤30 aa and
**0 % at 31–45 aa**, and six of these eight are 39 aa. We submit them because that prior comes from
campaigns optimising affinity while this one optimises selectivity; because the site forces the size
(the scaffolded route could not reach His358 at all); and because those bins are small enough that
the regime is closer to untested than to excluded. The two 12-mers sit in the better bin.

Four of the eight micro designs share one backbone, five lineages in all — a stated concentration risk: it
is the only lineage with equal interface confidence on both orthologs and the only one all three
oracles return as a single conformation. The design engine behind the micro series is the subject of
a manuscript in preparation and is described in principle ahead of publication; every sequence,
structure, per-model measurement, restraint file and command line needed to evaluate the designs is
public at **github.com/piripocchio8/AMBRALab_Chino_Challenge2026**.
