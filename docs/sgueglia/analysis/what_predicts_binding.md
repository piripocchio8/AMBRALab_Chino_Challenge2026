# What actually predicts binding, measured on experimental data

All numbers here are computed on experimentally tested designs, not on our own predictions. Two
datasets: a 3027-design / 32-target harvest from Proteinbase, and the 800-design EGFR subset of it
(126 binders, 15.8%), which is larger than the 599-design cut used in the published Adaptyv analysis.

## Nothing in sequence composition generalises across targets

Variance explained in binding outcome: **target identity eta^2 = 0.208**, design method 0.118, and
every sequence feature below 0.014 (length 0.013, entropy 0.008, %Ala 0.007, %hydrophobic 0.004).
Directions reverse between targets — binders are significantly *less* hydrophobic on DERF7/FGF-R1/MDM2
and significantly *more* on MZB1/PD-L1. **Composition filters must be derived from the target's own
cohort, never imported.**

## On EGFR specifically

**Length is bimodal, and the effect survives method stratification.**

| length | hit rate |
|---|---|
| <= 30 aa | 3.4% |
| 31–45 | 0% |
| 45–60 | 24.6% |
| 60–100 | 4.5% |
| 100–140 | 9.6% |
| 140–200 | 10.9% |
| **200+** | **34.7%** |

The 45–60 aa peak is a method artefact (ProtRL, 41.8%). The long-length effect is not: within the
single largest method group, >= 200 aa gives 26.9% against 9.8% at 100–200 aa, **Fisher p = 0.00086,
OR 3.40**. A median comparison misses this entirely — medians for binders and non-binders are both
100 aa (p = 0.073).

**Alanine discriminates in aggregate but is a scaffold-class artefact.** Monotonic 24.8% (Ala 0–5%)
down to 2.6% (>20%), p = 7.9e-07. But stratified by length it vanishes: 60–100 aa p = 0.65,
**100–140 aa p = 1.00**, 140–250 aa p = 0.07. The aggregate signal comes from the 45–60 aa
low-alanine EGF-domain mimetics. Alanine does **not** affect expression (p = 0.47).

**Charged fraction: the published expression guideline is harmful for binding.** The source recommends
D+E+K+R = 0.30–0.40 as the strongest positive expression term. Against binding: <0.22 -> 21.4%,
0.22–0.30 -> 14.4%, **0.30–0.40 -> 7.3%**, >0.40 -> 7.8%. Both endpoints are real; the conflict is
not flagged in the source.

**In the 100–140 aa de novo regime nothing predicts binding** (n = 250, 9.6% baseline): Ala p = 0.37,
charged fraction p = 0.40, net charge p = 0.11, Gly p = 0.44, hydrophobic p = 0.09, Cys p = 0.95,
His p = 0.27. Only length at p = 0.030, for a 1.5-residue difference — significance without consequence.

**What does transfer:** interface size (buried area, interface residue count) discriminates at
AUC 0.78 / 0.61; H-bond counts never do; ranking by PAE-interaction lifts hit rate 14% -> 26% (1.85x).

## Expression is a much easier target than binding

Fitting the expression model on our 800 designs, only two of six published terms replicate, and they
are the strong ones: **length (-1.119, p < 0.0001)** and **charged fraction (+11.22, p = 0.0028)**.
Gly and net charge do not replicate; alanine and GRAVY are null in both.

Two-term model: **AUC 0.809**, well calibrated at the high end. Designs matching our envelope
(60–134 aa, charged fraction >= 0.25) expressed **143/144 = 99.3%** against 91.3% outside
(Fisher p = 0.0001).

> **Caveat that matters: this is cell-free expression**, a <0.02 ug/mL translation-yield cutoff, not
> E. coli or mammalian secretion. Cell-free bypasses inclusion bodies, proteolysis, toxicity and
> secretion QC. Treat ~98% as an upper bound for a cellular host.

There is an uncomfortable symmetry: short and highly charged predicts expression, and is
neutral-to-negative for binding. Designs optimised for solubility score well on the easy filter.
