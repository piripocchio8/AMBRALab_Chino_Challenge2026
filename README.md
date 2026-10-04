# AMBRALab_Chino_Challenge2026

Submission package for the 2026 protein-design challenge.

**Target.** A pH-switchable binder to the protonated histidine at residue 25 of a 161-residue
protein target: the design is intended to engage the imidazolium through both ring nitrogens, so
that binding is stronger at low pH than at neutral pH.

## Layout

```
README.md                      this file
docs/methods.md                methods white paper
scripts/make_submission_csv.py builds a ranked submission CSV from candidate records
Target_1/micro/                designs shorter than 40 residues
Target_1/mini/                 designs of 40-100 residues
Target_1/large/                designs longer than 100 residues
```

Each size-band directory holds the submitted designs and their structure models, plus the ranked
CSV for that band. See `docs/methods.md` for the design and validation protocol and for the
metrics reported.
