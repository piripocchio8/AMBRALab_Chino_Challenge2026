# Target 5 — submission narrative

Twenty de novo binders against the KRAS **G12D** neoantigen decamer VVVGADGVGK presented on
HLA-A\*11:01, designed to discriminate it from the wild-type decamer VVVGAGGVGK, which differs at
one position.

The designs were produced by forward-folding search with a declared restraint table, then
**re-predicted with no restraints at all** — four chains, nothing declared — on both peptides.
Selection is on the unrestrained arm, because a design scored under its own restraint table is
being asked whether the restraint table works.

Designs were ranked on four criteria in this order: that the binder lands on the α1/α2 groove
unrestrained; that it induces the neoantigen aspartate to engage HLA Arg114, the 2.95 Å contact
seen in the deposited structure 7OW6; that it folds on its own; and that it separates the two
peptides. The second criterion is tested against a measured null rather than a threshold we chose:
the same groove with no binder reaches that contact in **0 of 50** predictions, the therapeutic TCR
of 7OW6 in **42 of 50**, and a published de novo minibinder of a different pMHC transplanted onto
this groove in **0 of 25**. A design is credited only where its count is separated from zero by a
one-sided Fisher exact test at p < 0.05.

Eight of the twenty meet that bar; twelve are deposited on the remaining three criteria and are, on
the aspartate contact, not distinguishable from an empty groove. The per-design files say which is
which, carry the full ensemble rather than a single model, and report the three systematic
behaviours of the predictor that bear on how the numbers should be read. All results are predicted
structures; no experiment was performed.
