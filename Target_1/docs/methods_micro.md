# Methods: designing a pH-switchable binder to a protonated histidine

Challenge 2026, Target 1. Written for challenge reviewers and for other designers who may want to
reuse or criticise the protocol. Every number quoted here was measured by us; where a quantity was
not measured it is said so rather than estimated.

> ### A note on what is and is not disclosed here
>
> The design engine behind the micro series — a population-based evolutionary optimiser that scores
> candidate sequences directly against the structure oracle, coupled to an interaction-preserving
> inverse-folding refinement — is **the subject of a manuscript in preparation**. Its internal
> machinery (the objective's term set and weights, the population scheme and its operators, the
> acceptance and re-grounding logic) is therefore described here in principle rather than in
> reproducible detail, **ahead of publication**.
>
> Nothing needed to *evaluate these designs* is withheld. The sequences, the predicted structures,
> every per-model measurement, the selection criteria, the gates and their thresholds, the failures
> and the designs we rejected are all in this repository, and every number quoted can be recomputed
> from the files beside it. The restraints given to the oracle, the hydrogen-bond criteria, the
> validation protocol and the ranking are stated in full. What is held back is how the candidate
> sequences were *generated*, not how they were *judged*.
>
> We will release the engine and its parameters with the publication, and are glad to discuss the
> method in confidence with the organisers in the meantime.

---

## 1. The design problem

The target is a 161-residue protein carrying a histidine at **residue 25** that is protonated at the
pH of interest. It also carries histidines at 37, 85 and 100, so every restraint we declare names
residue 25 explicitly.

A neutral histidine has one ring N-H and can donate one hydrogen bond. A **protonated**
histidine is an imidazolium: it carries an N-H on *both* ring nitrogens, formal charge +1, and can
donate two. A binder that engages both ring nitrogens is therefore bound appreciably more tightly at
low pH than at neutral pH, and that difference in affinity *is* the switch. A binder that engages
only one nitrogen captures much less of it, because the singly-engaged arrangement is available to
the neutral tautomer as well.

So the design objective is not "bind near histidine 25". It is "present two hydrogen-bond acceptors,
one to each ring nitrogen, simultaneously".

### 1.1 How rare that motif is

We ran a full geometric census of the PDB to find out how much precedent exists for this
arrangement, because the answer bears directly on whether a structure predictor can be expected to
produce it. The census is not a sample: it covers a 30 % sequence-identity non-redundant set of
**6,798 X-ray entries at 1.50 Å resolution or better**, containing **56,786 histidines**, of which
**53,400** remain after excluding metal-ligating ones.

| motif | count | denominator | frequency |
|---|---|---|---|
| ND1 **and** NE2 each accept from a distinct true C=O | **243** | 53,400 | **0.455 %, 1 in 220** |
| exactly one ring N accepting from a true C=O | 12,640 | 53,400 | 23.7 % |
| entries carrying at least one such histidine | 170 | 6,798 | 2.5 %, 1 entry in 40 |

"True C=O" means a backbone carbonyl O, an Asn OD1 or a Gln OE1. Serine, threonine and tyrosine
hydroxyls and waters are not carbonyls and were not counted.

Three properties of those 243 shaped the whole design campaign.

**It is overwhelmingly a backbone motif.** Of the 243, **178 are backbone carbonyl plus backbone
carbonyl**, 58 are amide plus backbone, and 7 are amide plus amide. The motif does not need
particular side chains; it needs particular backbone geometry. Of the 486 donor carbonyls, 312 come
from residues more than four positions apart in sequence, 140 from four or fewer, and 34 from another
chain.

**It is a buried-core feature.** Using protein heavy atoms within 8 Å of the imidazole centroid as a
burial proxy, with waters removed, the 243 have a median of **96** against **74** for a random
metal-free histidine control (n = 3,978). A buried imidazolium has no water with which to share its
+1 and pays for it with two strong buried hydrogen bonds. This is not a surface decoration, and it
argues against retreating to the shortest allowed binder length.

**The rarity is specifically in demanding a carbonyl on both sides.** Admit an Asp or Glu
carboxylate oxygen as one of the two acceptors and the count rises to 1,468, or 2.75 %, which is
about **six times more common** than the strict double-carbonyl motif. This is the single most
useful prediction the census gave us: if a structure predictor is going to be plausibly-but-wrongly
confident at our designed site, the most likely failure is that it reaches for the common
carboxylate-assisted arrangement instead of the rare double-carbonyl one. Section 5 reports that
this is exactly what happened.

An orthogonal control, on a quantity the census never selected on: of the 9,543 histidines in
entries that model hydrogens, 26.9 % have both HD1 and HE2 modelled (n = 8,960 metal-free
background), against **66.0 %** of the strict bidentate set (31 of 47). The purely geometric call is
2.5x enriched for histidines that the depositors' own refinement independently treated as
imidazolium.

### 1.2 The geometry the two acceptors have to present

Measured over the 181 histidines that have at least one backbone-only donor pair. That count is
three higher than the 178 above, and the two are consistent rather than in conflict: both describe
the same 243 histidines, and they differ only in which donor pair is counted. The 178 classifies
each histidine by the first qualifying pair found, whereas the 181 asks whether a backbone-only pair
exists at all — three histidines whose first qualifying pair includes an amide also possess a
backbone-only pair, and the geometry below is measured over the backbone pairs.

| | n | median | P10 to P90 | range |
|---|---|---|---|---|
| CA(donor 1) to CA(donor 2) | 181 | 9.9 Å | 8.1 to 11.2 | 5.6 to 12.7 |
| **O(donor 1) to O(donor 2)** | 181 | **7.4 Å** | **6.7 to 8.2** | 5.6 to 8.7 |

The oxygen-oxygen separation is the invariant, and it does not depend on sequence separation at all:
binning the donor pairs by sequence separation into 10 to 20, 21 to 60 and 61 or more gives O-O
medians of 7.3 to 7.6 Å throughout. The geometric target is therefore two carbonyl oxygens about
7.4 Å apart, each 2.8 to 3.0 Å from its own ring nitrogen, bridging a ring roughly 4.5 Å wide from
opposite edges.

Two subsets are directly relevant to a short cyclic binder:

- **Short-stretch templates** (same chain, donor sequence separation 9 or less; 19 cases). The
  observed separations are 3 (five times), 4, 5 (four), 6 (three), 7 (four) and 9 (twice), and
  **never 1 or 2**. O-O median 7.42 Å, CA-CA median 9.20 Å. A designed acceptor separation of 1 or 2
  asks for an arrangement that does not occur in this set.
- **Intermolecular analogues** (donors not in the histidine's own chain; 21 cases), the closest
  existing precedent for what we are designing. O-O 7.06 to 7.87 Å, CA-CA 7.8 to 11.5 Å, donor
  oxygen to ring nitrogen 2.54 to 3.22 Å.

Same-chain donor pairs have a median sequence separation of **33** and reach 452, so in natural
proteins the two carbonyls usually meet through tertiary packing rather than along a local stretch.

The natural single reference structure, if restraints are to be derived from a real structure rather
than invented, is **1MFM chain A residue 43**, a monomeric human superoxide dismutase mutant at
1.02 Å, the highest-resolution example in the set: HIS120.O to ND1 at 2.74 Å and THR39.O to NE2 at
2.63 Å. 1OAL A 42 and 8IMD A/B 116 are further Cu/Zn SOD examples. In all three these are the buried
beta-barrel histidines, not the metal-ligating ones, which are excluded from the census by
construction.

---

## 2. The structure oracle

All structure prediction in this work uses **Chai-1** as a **forward-folding oracle**. The design
loop proposes a sequence, Chai-1 predicts the structure of the binder-target complex, and the
prediction is measured. No gradients are taken through the predictor and no part of it is retrained
or fine-tuned; it is treated strictly as a black-box scoring function over candidate sequences.

One property of the oracle governs the entire methodology and should be stated plainly:

> **Chai-1 is heavy-atom only. It has no hydrogens and no concept of protonation state.**

There is no way to ask it for "the protonated form of histidine 25". Consequently **protonation can
only ever be expressed, and measured, as geometry**. Everything downstream follows from that
constraint:

- the design hypothesis has to be encoded as a geometric arrangement of heavy atoms (section 3);
- the acceptance criterion has to be a heavy-atom geometric test built on an *inferred* N-H
  direction (section 4.2);
- and any claim that a design engages an imidazolium is an inference from heavy-atom positions, of
  exactly the same kind as the census inference in section 1.1, with the same caveat.

The inferred N-H direction we use throughout is the exocyclic in-plane bisector at the ring
nitrogen: for ND1, the negated normalised sum of the unit vectors from ND1 to CG and from ND1 to
CE1, and correspondingly for NE2 from CD2 and CE1. Since a carbonyl oxygen has no polar hydrogen and
can only accept, a ring nitrogen with a carbonyl oxygen at hydrogen-bond distance in good N-H
geometry must be the donor, hence protonated. The deposited-hydrogen control in section 1.1 is the
evidence that this inference is usually right.

Compute was a local two-GPU workstation plus an institutional HPC cluster. A single structure
evaluation inside the design loop costs roughly 36 to 68 s depending on GPU generation; a full
five-model validation fold of the 161-residue target with a short binder takes about 2 to 3.5 min.

---

## 3. Design strategies

Two families of strategy were run. The first is a non-canonical scaffolding trick, reported here
because it produced the strongest geometries in the campaign and because its honest result is a
negative one. The second is what the current and recommended generation uses.

Candidate sequences were explored by **an evolutionary algorithm for global optimization** driving
**an objective function** over candidate sequences. The objective is a weighted combination of fold
confidence, interface quality, shape complementarity, restraint satisfaction and a geometric
hydrogen-bond term. Binders are cyclic, closed by a real disulfide between the first and last
residue rather than by a head-to-tail amide.

### 3.1 The "jig" strategy (non-canonical, run first, reported as a negative)

Because the oracle cannot represent an N-H, we attempted to impose the interaction geometrically by
building a covalent stand-in for the hydrogen bond. Each binder acceptor site carried an
**N-methyl asparagine** (chemical component code `MEN`, atoms `N CA C O CB CG OD1 ND2 CE2`), and its
N-methyl carbon `CE2` was **declared as a covalent bond to a ring nitrogen** of histidine 25. The
substitution being made is:

```
real:  His N - H    ...  O = C          the acceptor is the carbonyl OXYGEN
jig:   His N - CE2 - ND2 - CG = OD1     CE2 takes the H's place, ND2 takes the O's place
```

Two such bonds reproduce the 1,3-disubstitution pattern of a protonated ring, and the amide nitrogen
`ND2` behind each bridging carbon stands in for the sp2 oxygen that would accept the hydrogen bond
in the real molecule. We call this a **jig**: a temporary fixture that holds the chain in the pose we
want to test, and that is not part of the molecule we would make.

The bridging topology was chosen by measurement, not by taste. Three candidate topologies were
embedded in RDKit (80 embeddings each, lowest MMFF conformer):

| topology | acceptor to ring N | acceptor out of ring plane | acceptor separation |
|---|---|---|---|
| bonded through the bridging **carbon** | **2.37 Å** | 1.35 Å | **6.49 Å** |
| acceptor heteroatom bonded **directly** to the ring N | 1.56 Å | 0.00 Å | 5.13 Å |
| oxygen bonded directly to the ring N | 1.43 Å | 0.11 Å | 4.83 Å |

A real imidazolium N-H...O puts the acceptor 2.8 to 3.0 Å from the ring nitrogen. Bonding the
acceptor heteroatom straight to the ring nitrogen puts it at 1.4 to 1.6 Å, which is where the
*hydrogen* sits, not the acceptor, so the perfect coplanarity of those two rows is an artefact of
occupying the wrong site. The carbon bridge is still about 0.5 Å short but it is in the right
regime, and its 6.49 Å acceptor separation is consistent with the 6.7 to 8.2 Å interdecile range the
census reports for real donor pairs. The cost of the bridge is planarity: the bridging methylene is
sp3, so the amide rotates about 1.35 Å out of the ring plane in the free minimum, and an imidazolium
N-H points *along* the ring plane. A coplanarity restraint was therefore carried alongside the jigs.

Two variants were run:

- **`twojig`**: `MEN` at both acceptor positions, each `CE2` declared bonded to one ring nitrogen.
- **`jigcontact`**: `MEN` at the first position only. The second position is left free and is given
  a *residue-level* proximity restraint to histidine 25, so that its main-chain carbonyl can find
  the other ring nitrogen on its own. This variant exists because **a covalent bond to a backbone
  carbonyl does not work**: over 25 delivered structures a declared main-chain bond sat at a 4.90 Å
  median against a 1.43 Å declaration, while a side-chain bond hit 1.49 Å. The oracle refuses to make
  that bond, and it is right to, because the arrangement does not exist in the PDB. So this variant
  asks only for proximity and leaves the hydrogen bond free to appear or not.

**Two mandatory implementation details.** First, the canonical target histidine must be
**force-atomized**, i.e. represented atom-by-atom rather than as a single residue token. The oracle
addresses restraints by token, and a canonical residue is one token whose representative atom sits
near the backbone; there is no token at ND1 or NE2 for a bond to attach to, so the bond is accepted
into the topology and then has nothing to act on. It is reported as resolved and is silently not
enforced. Measured on the same configuration and seed, bridging carbon to its ring nitrogen against
a declared 1.45 Å:

| | min | median | max |
|---|---|---|---|
| canonical target, as-is | 3.89 Å | 7.85 Å | 14.47 Å |
| the same run, residue 25 atomized | **1.30 Å** | **1.38 Å** | **1.44 Å** |

Second, atomization has a price: it retypes the residue, so the oracle stops applying
histidine-specific ideal geometry. Over ten evaluations of the same cell the ring stayed flat
(0.005 Å to 0.006 Å RMS out-of-plane deviation) but ring bonds drifted by up to 0.096 Å (CD2-CG
1.343 to 1.446 Å against an ideal 1.35; CE1-NE2 1.315 to 1.385 Å against 1.32) and the CB-CG linker
stretched 0.225 Å (1.490 to 1.725 Å against 1.50), a 15 % error that displaces the whole imidazole
relative to the backbone. **Jigged, atomized runs are therefore a search scaffold, not publishable
geometry.**

**What the jigs delivered, and the honest finding.** Scored on the correct atoms, which for a jigged
fold means the `ND2`...N(ring) distance and not an incidental oxygen elsewhere in the chain, the jigs
largely worked as fixtures. Of 53 delivered cells with measurable declared jigs, **46 held every
declared jig** (bridging carbon within 1.75 Å) with `ND2` within 3.4 Å at every site, 1 held
partially and 6 failed; **12 `twojig` cells engaged both ring nitrogens**, with acceptor-stand-in
distances of 2.11 to 2.92 Å. The 6 failures all came from the earliest run, four of them by drifting
onto the *other* nitrogen, which is why the pairing must be read from the declaration and never
inferred as "whichever nitrogen it ended up nearest".

But the jigged pose is optimised against covalent bonds that do not exist in the molecule we would
make, and the design has to be accepted on a jig-free refold with canonical residues. **Those are
not the same quantity, and the pose does not survive.** For 14 gen-1 delivered designs the jig-free
validation folds gave **0 bidentate engagements**, 2 single hydrogen bonds (NE2 from Asn10 OD1 at
2.73 Å / 33.2°, and NE2 from Asp3 backbone O at 2.64 Å / 39.1°) and 12 with nothing at all. For the
one 40-mer that produced a genuine incidental backbone bidentate on the jigged scaffold
(ND1 from the main-chain O of residue 28 at 2.99 Å / 39.6°, NE2 from residue 30 at 2.60 Å / 17.4°,
in 1 of 5 models at ipTM 0.244), a dedicated 20-model jig-free refold with the non-canonical residue
swapped to Asp produced **0 of 20** models with even a single hydrogen bond, the nearest binder
acceptor to either ring nitrogen being 6.5 to 21.5 Å away.

The campaign's corrected total is **one** genuine bidentate engagement on a jigged scaffold, not
reproduced in 40 jig-free models across two validation protocols. A second apparent bidentate was
withdrawn on inspection: it came from a pre-campaign pull whose target residue was a histidine
methylated on NE2, so the reported NE2 bond was physically impossible, the methyl occupying exactly
the position the donated proton would need. Our scoring code tests both ring nitrogens
unconditionally and cannot see what is attached to them; the present target is deliberately a plain
histidine partly for this reason.

### 3.2 The jig-free strategy (current, recommended)

The current generation removes the fixture entirely and closes the gap between what is optimised and
what is accepted, by scoring during the search exactly the quantity the validation measures.

- **No jigs, no covalent stand-ins, no force-atomization, no non-canonical residues.** The target is
  a plain canonical histidine. **The delivered sequence is the molecule we would make.**
- The site is stated, and only the site: a residue-level proximity restraint from each intended
  acceptor position to histidine 25, plus a chain-level pocket on histidine 25 and the real
  disulfide that cyclises the binder. Nothing names a donor atom, an acceptor atom or a bond.
- The hydrogen-bond geometry of section 4.2 is **measured**, made continuous so that the search has
  a gradient to climb, and enters the objective as the geometric hydrogen-bond term. It requires the
  two ring nitrogens to be served by two **different** acceptor atoms.
- Because the census says the rare motif is the double-carbonyl one and that offering a carboxylate
  is offering the common answer, the current arm **excludes Asp and Glu** at and around the acceptor
  positions and pays only for a main-chain carbonyl reaching a ring nitrogen.

Design axes in the current generation are binder length and random seed. Based on section 5 the
recommended region is length 28 to 40 with an acceptor separation of 3 to 7, which is the window the
census observes for short-stretch donor pairs.

Expressibility (GRAVY, net charge, histidine count, longest hydrophobic run, aromatic fraction) is
computed as a **filter and reported, not optimised**: a convincing hit is allowed to be awkward to
make. For reference, every candidate examined so far passes with no flags raised, so nothing is
currently being traded away for makeability. Where a non-canonical design is assessed this way it is
assessed on its expressible swap, since the non-canonical residue is not something a ribosome makes.

### 3.3 Interaction-preserving repacking of the selected designs

The designs that survive selection are refined once more, by rebuilding the parts of the sequence
that are not carrying the binding and leaving the parts that are.

For each candidate, the interactions worth preserving are identified from its own predicted
structure, by geometry rather than by inspection:

- every residue within 5 Å of the target histidine, whatever it is doing, because the whole design
  turns on that residue;
- hydrogen bonds across the interface, taken as a nitrogen/oxygen donor-acceptor pair between 2.5
  and 3.4 Å;
- salt bridges, a carboxylate oxygen within 4.0 Å of a cationic nitrogen;
- aromatic stacking, ring centroids within 5.5 Å either face to face below 30° or edge to face above
  60°;
- the two cysteines of the disulfide, which define the cyclic molecule rather than the interface.

**Plain hydrophobic contact is deliberately not preserved.** A leucine packed against a valine is
worth about as much as any other aliphatic residue of similar size, so holding its identity
constrains the rebuild without protecting anything specific. The point of the exercise is to free
the generic positions and hold the ones whose chemistry *is* the interaction.

Those positions are then held fixed while **CARBonAra**, a context-aware all-atom inverse-folding
model, rebuilds the rest, conditioned on the target chain as fixed context. The target sequence cannot change and is
verified unchanged in the output. Cysteine is excluded from the rebuilt positions so that no third
cysteine can scramble the disulfide.

Two hold policies are run for every candidate and judged against each other rather than chosen in
advance: one holds the specific interactions *and* the histidine shell, the other holds only the
specific interactions, freeing residues that merely sit near the site without doing anything
chemical. Which is right is an empirical question, and the refold answers it.

Inverse-folding output is filtered before anything is folded. CARBonAra has a measured tendency to
return low-complexity, alanine-rich sequences when few positions are free, so each candidate is
required to carry at least 2.0 bits of Shannon entropy over its rebuilt positions with no single
residue type taking more than 40 % of them. On the 12-residue designs, where only four or five
positions are free, this discards 14 to 20 of every 88 sequences generated; on the 39-residue
designs it discards almost none.

Surviving sequences are refolded under their parent's own restraint file, unchanged, so that parent
and variant are compared like for like and any difference is a property of the sequence rather than
of how it was held. Because the oracle is not deterministic, each parent is refolded three times to
establish its own run-to-run spread, and a variant is accepted only if it clears that spread. The
acceptance order is fixed and is not a weighted sum: engagement of the target imidazolium first,
reproducibility across the five predicted models second, fold quality third, and confidence scores
last. A variant that loses the hydrogen bond is rejected however good its confidence looks.

---

## 4. Validation protocol and acceptance criteria

### 4.1 The jig-free refold

A design is accepted or rejected on a **jig-free refold** that carries exactly two restraint rows:

1. the **real disulfide** that cyclises the binder, and
2. a **chain-level pocket on the target histidine at 10 Å**.

Nothing else. No jigs, no atomization, no non-canonical residues, no atom-level restraint, no
statement about any hydrogen bond.

**Why a pocket at all, and why 10 Å.** Our first attempt passed no restraints whatsoever, and the
result was void twice over: without the disulfide the cycle folded linear, which is not the molecule
we would make, and without any site information the oracle had to find the epitope on a 161-residue
target unaided. All 14 folds landed 20 to 33 Å from residue 25 at ipTM 0.21 to 0.26, which is a blind
global dock failing, and says nothing about the hypothesis under test. Those folds are kept as the
no-site-information control.

A 10 Å chain-level pocket is **a statement of WHERE and not a statement of the interaction**. Which
surface of a target a binder occupies is a legitimate input to complex prediction, of the same kind
as an epitope being known experimentally. At 10 Å it is about three times the length of a hydrogen
bond, so it constrains the neighbourhood while leaving the interaction being measured entirely free
to form or not to form. A pocket at 3 Å would be handing the fold its answer, and no number produced
under one would mean anything.

**The long-chain amendment.** The two-row protocol is sound for a short binder and insufficient for a
long one, and we found this the hard way. A 10 Å chain-level pocket on an 11-mer effectively forces
proximity, because the whole peptide is about that wide. On a 40-mer the same restraint is
satisfiable without ever engaging the named residue, because there is enough chain to bury a large
interface in the neighbourhood and ignore the ring. Measured: 40-mer refolds buried 1,922 to
2,278 Å<sup>2</sup> with 49 to 55 residue contacts and binder pTM 0.267, against 625 to 1,430 Å<sup>2</sup>, 17 to 40
contacts and binder pTM 0.07 to 0.10 for the 11-mers. The long chain was binding, and binding near
the histidine, while presenting nothing at all to the ring.

Long-chain validation therefore adds **one** further row: a **residue-level site contact** from the
design's own intended acceptor position to the target histidine at 6 to 9 Å. The justification is
exactly the pocket's, applied at residue rather than chain resolution: 9 Å is still about three times
a hydrogen bond, so it states the site and not the interaction. The amendment did what it was added
to do and changed the character of the failure rather than hiding it. With the site contact, the
nearest acceptor to either ring nitrogen moved from 6.47 to 20.43 Å down to 3.44 to 18.91 Å, mostly
3.4 to 5.5 Å, and **distance became the sole remaining failure in every near miss** while direction,
ring clearance and planarity frequently passed. The best single model fails on distance alone, by
0.27 Å: ND1 from a main-chain O at 3.67 Å, 26° off the N-H vector, 4.10 Å clear of the nearest ring
carbon and 0.25 Å out of the ring plane.

We also record which residues arrive. The site contact named residue 28 and the jigged bidentate had
come from the carbonyls of 28 and 30, but what actually approaches the ring under the amended
protocol is residue 27, and sometimes 20, 24 or 31. The site contact steers the right *region* of the
chain into place without reproducing the specific backbone arrangement the jig had produced.

Validation folds are run over multiple seeds with five models per seed, and every model is scored
independently. A restraint-emitting step is pinned by a test and the job aborts before taking a GPU
if an expected restraint row is missing from the emitted restraint file, because a validation fold
that silently loses a restraint is a mistake this campaign has already made twice.

### 4.2 An independent second oracle

Confidence from a single predictor is one model's opinion. Final candidates are therefore also folded
with **Boltz-2**, which is independent of Chai-1 in training data and architecture, using a
multiple-sequence alignment for the target chain computed once and reused (the target is identical in
every prediction) and no alignment for the de-novo binder, which has no homologues. Boltz-2 reports
per-chain pTM directly, so binder-only confidence is read rather than reconstructed.

Two findings from that cross-check are worth stating, because both are traps:

- **The second oracle must be given the site.** Folded with no restraints, Boltz-2 placed one
  candidate 24.7 Å from the target histidine, against a different histidine entirely, and reported
  interface ipTM 0.883 and binder pTM 0.904 for it. The prediction was confident and internally
  consistent; it was simply about an interaction nobody asked for. Supplied with the same two
  statements the Chai-1 refold carries — the binder's disulfide and a pocket on the target histidine
  — the same sequence moved to 5.96 Å of the intended residue, formed its own disulfide at 1.61 Å,
  became compact (radius of gyration 1.02 against the expectation for its length) and scored higher
  still. A site restraint makes the right answer reachable; it does not make a wrong answer
  impossible, so every prediction is scored for *where* the binder landed, never on confidence alone.

- **The two predictors are not given the same information, and that governs how the comparison
  reads.** The Chai-1 refold carries *residue-level* restraints naming which binder positions sit at
  the site (each intended acceptor position to the target histidine at 4-6 Å). The second oracle is
  given only the chain-level pocket, so it is told the neighbourhood and left to find the pose. Under
  those terms Boltz-2 predicts the peptide bound at the target histidine, compact and with high
  confidence, but does not reproduce the binder-to-imidazolium hydrogen bond Chai-1 reports.

  That is **not** evidence of disagreement about the mechanism, and is not reported as such: an
  oracle that was never told which residue should reach the ring cannot be said to have failed to
  confirm it. The weaker and correct statement is that the *association* is supported by two
  independent predictors, while the hydrogen-bond geometry has so far been demonstrated only under
  restraints that name the participating residues. The pocket-only run is kept as the primary
  cross-check precisely because it is the one that leaves the pose to the predictor; a matched run
  carrying the same residue-level contacts is reported alongside it, as a measurement of what those
  restraints are worth rather than as a second vote.

Protenix was evaluated as a third predictor and not adopted; the optimized builds we assessed require
a GPU compute capability the available hardware does not provide.

### 4.3 Hydrogen-bond acceptance criteria

A contact between a ring nitrogen of the target histidine and a candidate acceptor oxygen counts as a
hydrogen bond only if **all four** of the following hold:

| criterion | bound | why |
|---|---|---|
| N...O distance | **2.5 to 3.4 Å** | the range for a charged N-H...O |
| angle off the in-plane N-H vector | **at most 45°** | the oxygen must lie along the N-H |
| distance to the nearest ring carbon (CG, CD2, CE1) | **at least 2.9 Å** | no collision with the ring edge |
| displacement from the ring plane | **at most 1.2 Å** | an imidazolium N-H lies in the ring plane |

A design is **bidentate** only when both ring nitrogens are each satisfied by a **different**
acceptor atom.

The 45° bound is calibrated rather than chosen. It is stated at the donor, and at N-H 1.02 Å with
N...O 2.90 Å it corresponds to a conventional D-H...A angle of 117°, against the usual bar of 120°.
It is therefore slightly *more* permissive than the standard criterion, and a rejection by direction
is not an artefact of a tight threshold.

**Distance alone is not enough, and this is not a theoretical worry.** Our original scoring took the
closest acceptor oxygen to each ring nitrogen and called a short distance a hydrogen bond. A
delivered two-jig design duly reported 3.30 Å to ND1 and 2.75 Å to NE2, apparently the bidentate hit
the entire screen was for. Both numbers came from the **same** backbone oxygen, which was sitting
**2.13 Å from the ring carbon CE1**. C...O van der Waals contact is about 3.2 Å, so that oxygen was
jammed into the edge of the ring, where neither N-H can reach it. One acceptor cannot serve both
nitrogens in any case: the two N-H vectors of an imidazolium diverge by more than 60°. The ring-carbon
clearance and distinct-acceptor rules exist because of that one structure.

A note on how to read the two uses of these criteria. The continuous form used inside the search
combines the four factors as a geometric mean, which preserves the "every criterion must hold"
character, including the veto, while keeping the scale usable by a search; a plain product scored the
best real bond in our validation set at 0.10, which no weight can make a search feel. The continuous
value is **for searching, not for judging**: a partial score on a contact 49° off the N-H is credit
for a near miss, not a hydrogen bond. **The verdict always comes from the four booleans above.** The
earlier distance-only scorer is retained only for comparison and is not used to decide anything.

---

## 5. What has been achieved, measured on real histidines

Reported separately from the protocol, because these are results and not methods.

**Single-nitrogen engagement is now routine on the expressible molecule.** Of 26 delivered jig-free
designs, folded against a real canonical histidine with no jig and no atomization, **9 engage one
ring nitrogen** by all four criteria:

| length | bond | distance / angle |
|---|---|---|
| 10 | NE2 from main-chain O of residue 5 | 3.17 Å / 22° |
| 11 | ND1 from main-chain O of residue 6 | 2.87 Å / 36° |
| 12 | NE2 from main-chain O of residue 6 | 2.80 Å / 24° |
| 18 | ND1 from main-chain O of residue 7 | 2.80 Å / 25° |
| 12 | NE2 from main-chain O of residue 4 | 3.11 Å / 20° |
| 12 | ND1 from main-chain O of residue 5 | 3.11 Å / 40° |
| 10 | NE2 from main-chain O of residue 4 | 2.90 Å / 21° |
| 11 | ND1 from Asp OD2 of residue 5 | 3.36 Å / 42° |
| 18 | NE2 from main-chain O of residue 8 | 3.08 Å / 34° |

**Eight of the nine donate from a main-chain carbonyl**, not from the designed Asp or Glu side chain,
which is the mechanism the census says dominates in nature (178 of 243 cases) and which needs no
non-canonical chemistry at all. ND1 is engaged four times, where across the 14 gen-1 jig-free
validation refolds it had never been engaged once. Confidence remains low throughout (ipTM 0.16 to
0.35, binder pLDDT 0.50 to 0.66). **None of the nine is bidentate.**

**One bidentate engagement on a real histidine, obtained under guidance.** The four designs that held
every declared jig and reached binder pTM above 0.6 were refolded with the non-canonical residues
swapped to Asp or Asn in all three assignments, two seeds each and five models each: 12
configurations, 120 models. Restraints were the real disulfide, the 10 Å chain-level pocket, and a
4 to 8 Å residue contact from each former acceptor position to histidine 25.

**This was a guided feasibility test, not a validation.** The contacts state which residues sit at
the site; they name no atom, no donor and no bond, and the hydrogen bond is still measured rather
than restrained. But the fold is being helped, and no number from it is evidence that a design finds
the arrangement unaided. The jig-free runs above are what answer that question, and the answer there
is still no.

Of the 120 models, **7 make a hydrogen bond to a ring nitrogen and one is bidentate**: a 40-mer in
which ND1 accepts from Asn17 OD1 at **2.65 Å / 26°** and NE2 from Asp23 OD1 at **2.99 Å / 23°**, both
passing all four criteria, on a plain canonical histidine with no jig and no atomization. Binder pTM
on that model is 0.396, so the structure around it is not confident, and it is 1 of 120 draws.

**It is the carboxylate-assisted variant, exactly as the census predicted.** Asn OD1 is a genuine
amide carbonyl, but Asp23 OD1 is a carboxylate, so this is the amide-plus-carboxylate arrangement
that the census puts at 2.75 %, six times more common than the strict double-carbonyl motif at
0.455 %. The prediction, made before the run, was that left to itself the model would reach for the
common carboxylate-assisted geometry rather than the rare double-carbonyl one, and that is what it
did when Asp and Asn were placed at the acceptor positions.

Three splits of those 120 models are informative and all are coherent with the census:

| split | models | with a bond | bidentate |
|---|---|---|---|
| length 11 | 60 | **0** | 0 |
| length 40 | 60 | **7** | **1** |
| length 40, acceptor separation 6 (inside the observed window) | 30 | 4 | 1 |
| length 40, acceptor separation 14 (outside it) | 30 | 3 | 0 |
| Asn at the ND1 site, Asp at NE2 | 40 | **4** | **1** |
| Asp at ND1, Asn at NE2 | 40 | 2 | 0 |
| Asp at both | 40 | 1 | 0 |

1. **Length is decisive.** Not one length-11 model makes a bond, under the same restraints that got
   the 40-mers there. This matches the burial finding: the motif sits in a pocket with a median 96
   protein heavy atoms within 8 Å of the ring, and an 11-mer cannot build one.
2. **The short binders do not merely miss, they collide.** Four of the twelve length-11
   configurations put an acceptor oxygen **under 2.5 Å** of a ring nitrogen, down to 2.15 Å, inside
   the clash floor. A 4 to 8 Å residue contact on a chain only about 10 Å wide jams the acceptor into
   the ring rather than presenting it to it.
3. **Acceptor separation matters in the direction the census predicts.** Separation 6 is inside the
   observed short-stretch window of 3 to 9 and produced the bidentate; separation 14 is outside it
   and did not.

The next design generation is therefore specified by data rather than by sweeping: binder length in
the 28 to 40 range, acceptor separation 3 to 7, binder-only fold confidence in place of global
confidence in the objective, and acceptor positions that are **not** Asp or Glu if the goal is
genuinely the rare double-carbonyl motif, because offering a carboxylate is offering the common
answer.

---

## 6. Metrics reported, and what they mean here

The submission CSV (see `scripts/make_submission_csv.py`) carries the following. Each is reported
because the obvious alternative is misleading on this particular system.

**Interface (pair) ipTM, not global ipTM.** The complex is a 161-residue target plus a binder of 10
to 40 residues. A global ipTM averaged over all chain pairs on such an asymmetric complex is
dominated by the target and compresses exactly the variation we care about. We report the ipTM of the
**binder-target pair**.

**ipSAE.** The interface-localised score of Dunbrack and co-workers, which we report with its
conventional 10 Å PAE cutoff. On this system it is frequently **exactly 0.000**, and that is a real
statement rather than a bug: the score returns 0 when no inter-chain residue pair falls below the
cutoff, and in 11 of our 14 gen-1 validation folds not one residue pair in the entire interface
reaches 10 Å PAE. Relaxing the cutoff to 15 Å or 20 Å does not rescue it (values move only to about
0.005 to 0.064). One caveat for any reader recomputing it on a non-canonical or atomized design: the
residue-aggregated form's length normalisation collapses on atom-tokenized residues, and the
token-level form must be used there. Fully canonical folds are unaffected, since token and residue
coincide.

**Binder-only pTM, not global pTM.** Global pTM on a 161 + L complex is dominated by the target's own
confidence, which the binder does not influence, and it is actively misleading. Over 82 delivered
designs the global pTM ranged 0.833 to 0.950 with a standard deviation of 0.029, while the binder's
own pTM ranged 0.058 to 0.736 with a standard deviation of 0.178, and the two are **anti-correlated,
Pearson r = -0.304**. The mechanism is dilution: a longer binder that is itself better predicted
drags the global average down. Length 10 designs gave global pTM 0.923 to 0.942 with binder pTM
0.088 to 0.137, while length 40 designs gave global pTM 0.833 to 0.906 with binder pTM 0.270 to
0.717, so the best binders had the worst global scores. We therefore report and rank on the binder
chain's own pTM, and also report binder pLDDT.

**Shape complementarity and buried surface area**, plus inter-chain atom contact counts, as the
packing-quality complement to the confidence metrics. A design can satisfy every geometric criterion
at the ring while burying nothing.

**Hydrogen-bond columns**: the count of qualifying bonds, a bidentate flag, and for each ring
nitrogen the donor atom, the N...O distance and the angle off the inferred N-H vector, so that a
reviewer can apply the section 4.2 criteria independently and see the near misses.

**One measurement caveat that applies to all interface metrics.** Interface metrics on any design
containing non-canonical residues, or against an atomized target residue, **must be computed with
those residues retained**. Our scoring initially kept only residues whose three-letter name was one
of the canonical twenty, which on this campaign silently deleted *both* sides of the interaction
under study, the binder's non-canonical acceptors and the retyped target histidine; a delivered
11-mer was measured as a 9-mer. A second filter sat behind the first: non-canonical residues are
written as `HETATM`, and the solvent-accessibility library skips `HETATM` by default, so buried
surface area stayed blind to them even after the first fix. Correcting both moved inter-chain atom
contacts by +30 to +120 %, buried surface area by +100 to +250 Å<sup>2</sup> and shape complementarity by up to
0.3, **enough to reorder the ranking**, and two designs went from zero inter-chain hydrogen bonds to
one. Any number recomputed from our deposited models should be recomputed with non-canonical
residues retained.

---

## 7. Limitations


**The target carries a free cysteine, and these binders are closed by a disulfide.** The target's
Cys4 and Cys29 form a disulfide in every predicted structure (1.90 Å), but **Cys137 is unpaired** and
33 Å from any partner. A disulfide-cyclised peptide incubated with a protein presenting a free
surface thiol can undergo thiol-disulfide exchange, which would open the cycle and could tether the
peptide covalently at the wrong place. This is not predicted in any of our complexes — across 200
predicted models no binder sulfur comes within 4 Å of a target sulfur, since the designed epitope is
roughly 30 Å from Cys137 — but it was observed once, in an unrestrained fold by the second oracle,
which cross-linked a binder cysteine to Cys137 at 2.00 Å and scored that adduct highly. It is a real
consideration at the bench rather than a modelling artifact: it argues for a redox-controlled
assay, a blocked Cys137, or a non-disulfide cyclisation if these designs are taken forward.

Stated plainly, because several of them are load-bearing.

1. **Model confidence on the delivered designs is low.** The jig-free designs that engage a ring
   nitrogen sit at ipTM 0.16 to 0.35 and binder pLDDT 0.50 to 0.66; the one bidentate engagement on a
   real histidine has binder pTM 0.396. These are correct geometries inside structures the oracle is
   not confident about, and they should be read that way.

2. **The strongest bidentate geometries in this work were obtained on jigged scaffolds, which are not
   molecules.** Twelve designs engage both ring nitrogens under the covalent stand-in. Those
   structures contain declared bonds that no synthesisable compound has. They are a search scaffold
   and a hallucination inducer, not a result, and we do not submit them as designs.

3. **The jigged pose does not survive a jig-free refold.** 0 bidentate engagements in 14 gen-1
   refolds; 0 of 20 models for the one 40-mer bidentate, across two validation protocols.

4. **Coverage of the jigged set is incomplete.** Of 56 delivered jigged scaffolds only 14 have any
   jig-free refold at all; **42 have never been validated**, including the both-nitrogen engagements
   at lengths 28 and 40, which have never been tested as molecules. Absence of a reported failure for
   those is absence of a test.

5. **The single bidentate on a real histidine was obtained under guidance**, with residue-level
   contacts placing the acceptor positions at the site, and it is 1 of 120 draws. It is a feasibility
   result. No design in this work has found the bidentate arrangement unaided.

6. **It is also the wrong variant.** That engagement is the carboxylate-assisted arrangement, which
   the census puts at six times the frequency of the double-carbonyl motif the campaign is aimed at.

7. **No design in this work has been tested experimentally.** There are no binding data, no pH
   titration and no structure. Every number here is a prediction or a geometric measurement on a
   prediction.

8. **Protonation is never modelled, only inferred.** The oracle is heavy-atom only, so "imidazolium"
   is a geometric inference throughout, in the designs exactly as in the census.

9. **Census caveats.** 196 of the 243 reference cases have no modelled hydrogens; the deposited-H
   control agrees 66 % against a 27 % background, which is good and not perfect. The census covers
   the deposited asymmetric unit only, so 243 should be treated as a floor (9.7 % of metal-free
   histidines have a symmetry-image oxygen within 3.4 Å of a ring nitrogen). It is a non-redundant
   high-resolution subset, so **the percentages transfer but the absolute 243 does not**; scaling
   2.5 % of entries to the whole PDB is not valid. The angular criteria are thresholds rather than a
   potential and **no sensitivity sweep was run**, which is the most useful follow-up if the number
   has to be defended in print. Only unmodified `HIS` was counted.

10. **Our hydrogen-bond scorer tests both ring nitrogens unconditionally** and cannot see a
    substituent blocking one. On a methylated-histidine target it will score a blocked nitrogen as a
    donor, which is how one apparent bidentate entered and then left our records. It is not an issue
    for the present target, which is a plain histidine, but anyone reusing the criteria on a modified
    histidine must gate on what occupies each ring nitrogen.

11. **Some compaction restraints used in the long-chain runs are generic length-scaled pins, not
    derived from any real structure.** They did not prevent the designed interaction in any cell that
    held its fixture, but they impose an arbitrary topology. Deriving such restraints from a real
    structure, and sanity-checking them in that structure, is the better discipline and is what we
    would do again; 1MFM A 43 is the natural reference.

12. **Resolved.** The campaign is finished and the selection is made. The eight submitted designs,
    their sequences, their predicted structures and every per-model measurement behind them are in
    `../micro/`, with `../submission.csv` (the challenge template: name, sequence, molecule_class)
    and `../metrics_full.csv` (the same designs with all metrics) at the target root. Section 10
    describes how the eight were chosen, and names the designs that were rejected and why.

---

## 8. Reproducing the measurements in this document

The census of section 1 is a direct geometric census over downloaded mmCIF files, with every search
API call, its body, URL and response retained alongside the per-histidine records. It deliberately
does not use the RCSB `strucmotif` service, which cannot express the query: `strucmotif` matches
residue *arrangements* under distance and RMSD tolerance and has no hydrogen-bond or atom-level
predicate, and its residue-exchange list is capped at 4 identities per position (8, 10, 16 and 20 all
return HTTP 400), while the motif requires "any residue whose backbone carbonyl is here", i.e. all
20. The inflation is itself the proof: loosening two positions of a three-residue reference
arrangement to four identities each returns 9,364 entries, 1.4x the entire working set. The Erebus
atom-level motif server, which does have the predicate `strucmotif` lacks, no longer resolves and
appears to be decommissioned.

Structure prediction uses Chai-1 at its released weights with five diffusion samples per fold and no
retraining, run on a local two-GPU workstation and an institutional HPC cluster. Scoring code for the
hydrogen-bond criteria of section 4.2, the interface metrics of section 6 and the submission CSV
format is the authors' own.

---

## 9. Selection on engagement rate alone (superseded by section 10)

> **This section records an earlier ranking and the three findings that shaped it. The submitted
> band is no longer chosen this way** — ranking on engagement rate alone admitted designs that make
> the hydrogen bond from an inconsistent pose, designs with interfaces too small for the oracle to
> believe, and one design that is extended against the mouse ortholog. Section 10 describes the
> measurements that replaced it and what they changed. The findings below still hold and are the
> reason several of those measurements exist.

The eight micro designs were first chosen on measurements made against the **human** target, pooled
over two oracles, after three findings changed what the earlier ranking was worth.

**The search optimised against the wrong ortholog.** The design campaign ran against the *mouse*
sequence (UniProt Q01279 334–494); the competition target is human (P00533 334–494). The two are
90.7 % identical and the epitope is conserved residue for residue — Asn355, Lys357 and **His358**
are identical — but the orthologs differ at 15 other positions and the designs did not transfer.
Of the first sixteen refolded on human, **one kept a double engagement** where the best of them
reached six models in fifteen on mouse. The whole pool was therefore refolded against human, and
every number reported here comes from those folds. The nearest substitution to the site is three
residues away (mouse Tyr → human Asn at local 28), which removes packing surface immediately beside
the histidine.

Note also that the human construct carries **five** histidines to the mouse construct's four: local
50 is His in human and Arg in mouse. The search never saw that competing site.

**Both hydrogen-bond directions are now measured, and they mean opposite things.** The campaign
scored only the designed direction, in which a protonated ring nitrogen **donates** to an acceptor.
The reverse — a binder donor giving into a deprotonated ring nitrogen, which the ring **accepts** —
was never counted. Across 1200 models it occurs in about one model in eleven, with the binder
supplying the donor in 9 %. This is not a bonus: a bond in that direction requires the ring to be
*deprotonated*, so a design relying on it binds more tightly at pH 7.4 than at pH 6.5 — the switch
running backwards. Designs are therefore reported with both counts, and the inverse direction is
penalised in the ranking rather than ignored.

**The two oracle settings disagree about individual designs.** Folding with a multiple-sequence
alignment for the target and with none changes which designs score: of thirty-six designs run both
ways, several move from three double engagements to zero and others in the opposite direction. The
overall rate is essentially unchanged — 0.9 % against 1.5 % of models — so the alignment does not
rescue the second hydrogen bond, but it does make any single-oracle ranking unstable. The submitted
eight were selected on **agreement**: each scores under both settings, ranked by the rate of
binder-supplied hydrogen bonds across all thirty models, penalised by the inverse direction, with a
usable fold required and at most two designs drawn from any one lineage, so that a single bad
scaffold cannot carry the whole submission.

The honest summary of what is claimed: on the human target these designs reproducibly place a
binder main-chain carbonyl in hydrogen-bonding geometry on the target imidazolium. **The double
engagement that would make the interaction sharply pH-dependent is observed in roughly 1 % of
predicted models, and is not an established property of any submitted design.**

### The ranking, on the evidence as it finally stood

Every candidate was refolded on the human target until it carried **55 to 60 predicted models**,
pooled across both oracle settings, before any of them was ranked against the others. That mattered:
an earlier ordering built on 15 to 30 models put six designs in the submission that the fuller
evidence does not support, and only two of those eight survive here. The designs were not wrong
then; there was less of them measured.

Ranking is on the rate at which **the binder itself** donates a hydrogen bond to the target
imidazolium, penalised by the rate of the inverse direction, with the double engagement as a
tiebreak rather than a driver - on human it is too rare to rank on. A fold that is extended is
excluded, and at most two designs are taken from any one lineage, so a single bad scaffold cannot
carry the submission.

| rank | binder-supplied bond | double engagement | inverse direction | Rg ratio |
|---|---|---|---|---|
| 1 | 40/60 | 0/60 | 0 | 1.153 |
| 2 | 29/60 | 0/60 | 1 | 1.165 |
| 3 | 28/60 | 0/60 | 1 | 1.01 |
| 4 | 23/55 | 0/55 | 0 | 1.048 |
| 5 | 25/60 | 5/60 | 12 | 1.101 |
| 6 | 21/60 | 1/60 | 1 | 0.986 |
| 7 | 20/60 | 0/60 | 0 | 1.066 |
| 8 | 22/60 | 0/60 | 6 | 0.984 |

Three things are worth stating because they are not what the campaign set out to find.

**The best design engages in two models out of three and never doubly.** It donates a binder
main-chain carbonyl to the imidazolium in **40 of 60 models**, with not one model showing the
inverse direction, and shows the double engagement in none. It is the most reproducible single
hydrogen bond measured anywhere in this work, and it is a one-bond interaction. *It is also the
design section 10.2 removes from the submission: it is extended in every one of its mouse models.*

**It came from refinement, not from search.** It is an inverse-folding repack of a backbone the
search had found but could not encode in a sequence - the backbone folded compactly only while an
explicit restraint held it, and the repack produced a sequence that holds it unaided. The design
ranked second by that route is of the same kind. The search waves that ran against this site
produced nothing that survives into the top three.

**Across all eight, the double engagement appears in 6 of 465 predicted models, about 1 %.** It is
reported where it occurs and claimed for nothing. What this submission asserts is a reproducibly
placed single hydrogen bond from the binder to the target imidazolium, which is a weaker claim than
the campaign set out to make and is the one the measurements support.

## 10. The final ranking: reproducibility, both orthologs, and a pKa

The ranking in section 9 was built on one quantity — how often the binder donates a hydrogen bond to
the target imidazolium. That is necessary but not sufficient, and three further properties were
measured before the submission was fixed. Each is a separate way for a design to be worthless while
scoring well on the others.

### 10.1 Does it dock in the same place every time?

Every refold of a design was superposed on the **target** chain, and the binder's deviation from the
design's own best pose measured. This is a different question from whether the peptide folds
consistently: a peptide can hold one structure and still bind a different patch each time, and the
complex metrics report that as a good interface either way.

The spread is reported as the median pose RMSD to the best pose, the fraction of refolds within
2 Å of it, and the RMSF — the spread of each binder residue about its mean position. The leading
design docks within a median 1.03 Å in 45 of 45 independent human refolds, with an RMSF of 0.80 Å.
Most designs do not: of the shortlist, pose RMSDs run from 1.03 Å to 21.8 Å, and several designs
with respectable bond rates turn out to be making those bonds from inconsistent positions.

### 10.2 Is it one structure, in both species?

Binder-on-binder superposition gives the fold spread within each species, and the best agreement
between a human-bound and a mouse-bound conformation gives the cross-species difference.

This test removed the design that had led the previous ranking. It is compact in **all 45** of its
human models (median Rg ratio 1.01) and extended in **all 5** of its mouse models (median 1.62) —
two different structures, 9.9 Å apart, one per ortholog. Pooled across both species that reads as
"14 % of models extended", which is how it survived an earlier filter. Per species it is a design
with no folded conformation against one of the two orthologs, and for a submission judged on
cross-reactivity that is disqualifying rather than cosmetic. Extension is therefore taken from the
**worse** species, never pooled.

Where a design was also folded alone, the RMSD between the free binder and its bound conformation is
reported. A peptide that already holds the binding-competent fold is a better bet than one the
target has to fold for it.

### 10.3 Comparable denominators

An engagement rate over 45 human models and 5 mouse ones is not a comparison, and the first version
of this ranking made exactly that mistake. The mouse side was refolded up to roughly 20–25 models
per design, under **each design's own restraint file** — recovered from the queue that originally ran
it, so the restraints are identical between the two species and the two rates mean the same thing.
Designs whose restraint file could not be identified were left out of the top-up rather than refolded
under a reconstructed one, and every rate in `metrics_full.csv` carries its own *n*.

Cross-reactivity is then scored as the **lower** of the two rates. An average lets a design that
works on one ortholog and fails on the other look mid-table, which is the opposite of what the
property means.

### 10.4 pH sensitivity: why it is read from geometry, and why propka is not scored

**The structure states the protonation.** Neutral imidazole carries one N–H; the other ring nitrogen
holds a lone pair. A model in which **both** ring nitrogens donate hydrogen bonds to acceptors is
therefore not merely consistent with the protonated ring — it is only constructible *given* it. That
makes the bidentate geometry the strongest statement about protonation that a structure can make,
and it is what the pH axis is ranked on, together with whether the acceptor is a **carboxylate**
(a charge–charge interaction) rather than a neutral carbonyl.

**propka was run, tested, and found unable to represent that constraint.** It is reported in the CSV
for transparency and does not enter the score. The reason is specific, not a general complaint.

A stratified test was run: 18 models per class, propka on identical coordinates with and without the
binder.

| what engages the ring | n | median ΔpKa | fraction > 0 |
|---|---|---|---|
| nothing | 18 | −1.31 | 0.00 |
| one main-chain carbonyl | 18 | −0.74 | 0.00 |
| **both ring N, two carbonyls** | 18 | −0.54 | 0.00 |
| **binder carboxylate** | 18 | −0.28 | 0.28 |

The trend is monotonic, so propka is **not blind** to the interaction — it does credit the hydrogen
bonds. The problem is the magnitude it assigns them relative to burial. Its own term breakdown for a
bidentate model (binder Leu19 O → ND1, target Asn5 O → NE2):

| | free target | with binder |
|---|---|---|
| His25 pKa | 5.83 | 4.99 |
| buried | 24 % | 66 % |
| desolvation term | −0.99 | **−2.27** |
| hydrogen-bond terms | +0.44 | +0.44, **+0.55** |

Both bonds are counted, at **+0.44 and +0.55** pKa units. Burial of the histidine moves desolvation
by **−1.28** over the same step, and decides the sign. So an additive empirical model returns a net
*negative* shift for a geometry that cannot exist without the cation. That is not noise to be
averaged away and not a reason to distrust propka generally — it is a model whose hydrogen-bond term
is capped near half a pKa unit being asked a question where the right answer is "whatever it takes".

Reporting those numbers as this submission's pH evidence would therefore have been wrong in the
direction that matters: it would have said the designs favour the neutral ring when the geometry
they were selected for requires the protonated one. The shift stays in the CSV so the judgement can
be checked; the ranking uses the geometry.

**What the carboxylate result adds.** The only positive shifts anywhere in the test are in the
carboxylate stratum (28 % of them, up to +1.80). Even on a model that understates hydrogen bonding,
a *charged* acceptor on the ring can overcome the burial penalty where a neutral carbonyl cannot.
That is a design lever, and three designs in the pool present a binder Asp/Glu to His358 in a
substantial fraction of models — one of them in both orthologs.

### 10.5 How the four combine

`overall_score` is a weighted sum of four sub-scores, each on 0–1 and each reported beside it:
cross-reactivity 0.30, pH sensitivity and bond strength 0.25 (bidentate rate 0.45, carboxylate rate 0.35, vina 0.20), binding consistency 0.25, fold consistency 0.20. The
weights are a judgement; the components are measurements, and are published so the weighting can be
disagreed with without redoing the work.

### 10.6 The submitted band, on these measurements

<!-- GENERATED:RANKING -->
| # | design | overall | cross (H/M bond rate) | pH (bidentate, carboxylate H/M) | binding (pose, repro) | fold (extended H/M, H↔M Å) | refolds H/M |
|---|---|---|---|---|---|---|---|
| 1 | `AMBRA_T1_micro_01` | **0.500** | 0.48 (0.22/0.31) | 0.59 (0.07, 0.00/0.00) | 0.07 (3.41 Å, 0.24) | 0.95 (0.00/0.00, 0.25) | 45/35 |
| 2 | `AMBRA_T1_micro_02` | **0.412** | 0.40 (0.00/0.40) | 0.37 (0.00, 0.00/0.00) | 0.04 (5.07 Å, 0.20) | 0.94 (0.00/0.00, 0.24) | 15/15 |
| 3 | `AMBRA_T1_micro_03` | **0.363** | 0.46 (0.36/0.23) | 0.21 (0.00, 0.00/0.00) | 0.00 (1.34 Å, 0.89) | 0.86 (0.00/0.00, 0.32) | 45/35 |
| 4 | `AMBRA_T1_micro_04` | **0.358** | 0.20 (0.36/0.37) | 0.53 (0.04, 0.33/0.20) | 0.00 (3.41 Å, 0.22) | 0.83 (0.00/0.00, 0.69) | 45/35 |
| 5 | `AMBRA_T1_micro_05` | **0.334** | 0.27 (0.58/0.17) | 0.31 (0.00, 0.58/0.17) | 0.00 (3.37 Å, 0.20) | 0.88 (0.00/0.00, 0.65) | 45/35 |
| 6 | `AMBRA_T1_micro_06` | **0.262** | 0.13 (0.60/0.23) | 0.31 (0.00, 0.60/0.00) | 0.00 (3.82 Å, 0.20) | 0.71 (0.00/0.00, 1.73) | 45/30 |
| 7 | `AMBRA_T1_micro_07` | **0.252** | 0.26 (0.00/0.20) | 0.06 (0.00, 0.00/0.00) | 0.00 (3.46 Å, 0.27) | 0.79 (0.00/0.00, 0.66) | 15/15 |
| 8 | `AMBRA_T1_micro_08` | **0.189** | 0.07 (0.44/0.09) | 0.12 (0.00, 0.00/0.00) | 0.02 (5.50 Å, 0.07) | 0.66 (0.00/0.00, 1.85) | 45/35 |

Read the refold counts first: a rate is only as good as its denominator. Rows where a value
is missing were not measured, which is not the same as measuring zero.
<!-- /GENERATED:RANKING -->
