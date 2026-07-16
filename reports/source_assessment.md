# Source assessment

Data retrieved on 2026-07-16.

## Queries tested

- `organism_name:Legionella AND protein_name:effector` — **804** records (`protein_name_effector`).
- `organism_name:Legionella AND "Dot/Icm"` — **2096** records (`dot_icm`).
- `organism_name:Legionella AND "type IV secretion"` — **828** records (`type_iv_secretion`).
- `organism_name:Legionella AND (gene:RavZ OR protein_name:RavZ OR gene:SidM OR protein_name:SidM OR gene:DrrA OR protein_name:DrrA OR gene:SidC OR protein_name:SidC OR gene:AnkB OR protein_name:AnkB OR gene:LegK2 OR protein_name:LegK2 OR gene:LubX OR protein_name:LubX OR gene:SidH OR protein_name:SidH OR gene:SidD OR protein_name:SidD OR gene:SdeA OR protein_name:SdeA OR gene:SidE OR protein_name:SidE OR gene:SetA OR protein_name:SetA OR gene:MavE OR protein_name:MavE OR gene:RalF OR protein_name:RalF OR gene:LidA OR protein_name:LidA OR gene:LepA OR protein_name:LepA OR gene:LepB OR protein_name:LepB OR gene:VipD OR protein_name:VipD OR gene:RomA OR protein_name:RomA OR gene:LegAS4 OR protein_name:LegAS4 OR gene:Lgt1 OR protein_name:Lgt1 OR gene:Lgt2 OR protein_name:Lgt2 OR gene:Lgt3 OR protein_name:Lgt3 OR gene:SidJ OR protein_name:SidJ OR gene:SdjA OR protein_name:SdjA OR gene:LotA OR protein_name:LotA OR gene:MavC OR protein_name:MavC)` — **628** records (`known_names`).

## Coverage and overlap

Pathogens3D contains **368** rows and **368** non-empty UniProt accessions. UniProt resolved **367** to active records; **1** accession(s) are inactive/deleted and are noted in the transient fetch log.

Across the exploratory queries, **69** accessions overlap Pathogens3D, **299** Pathogens3D accessions are not recovered by those queries, and **3403** UniProt query hits are absent from Pathogens3D.

The complete, row-level result (including query provenance) is in `reports/source_comparison.tsv`.

## Missing and additional records

Pathogens3D-only accessions (299): `A0A077GS41`, `A0A3N9YH02`, `P37033`, `Q5ZR83`, `Q5ZR84`, `Q5ZRA8`, `Q5ZRD0`, `Q5ZRE6`, `Q5ZRH0`, `Q5ZRH1`, `Q5ZRJ3`, `Q5ZRJ6`, `Q5ZRJ7`, `Q5ZRK2`, `Q5ZRK7`, `Q5ZRL9`, `Q5ZRM1`, `Q5ZRN6`, `Q5ZRP8`, `Q5ZRQ2`, `Q5ZRQ4`, `Q5ZRR5`, `Q5ZRR7`, `Q5ZRS4`, `Q5ZRS6`, `Q5ZRW4`, `Q5ZRW7`, `Q5ZRX6`, `Q5ZS00`, `Q5ZS25`, … (269 more; see `reports/source_comparison.tsv`).

UniProt-only effector-like records retained in the catalogue (940): `A0A078KRP0`, `A0A078KSH7`, `A0A078KT24`, `A0A078KTT6`, `A0A078KU50`, `A0A078KU91`, `A0A078KU98`, `A0A078KVA7`, `A0A078KVE2`, `A0A078KWF2`, `A0A078KWJ9`, `A0A078KXW4`, `A0A078KY31`, `A0A078KYW7`, `A0A078KZ92`, `A0A078L125`, `A0A078L477`, `A0A078L4W6`, `A0A078L595`, `A0A078L5S6`, `A0A078L5T4`, `A0A098FZC7`, `A0A098FZF3`, `A0A098G267`, `A0A098G2B2`, `A0A098G3L6`, `A0A098G4F0`, `A0A098G4M8`, `A0A098G4X0`, `A0A098G522`, … (910 more; see `reports/source_comparison.tsv`).

## Ambiguity and false positives

The broad searches returned **2463** UniProt-only records that were not retained. Prominent false positives are structural Dot/Icm/type-IV secretion apparatus proteins; text mentioning a secretion system is not evidence that the protein is a translocated effector. Other unreviewed records are plausible homologues but only automatically annotated, so their evidence category must not be upgraded merely because a query matched.

## Source decision

The master catalogue currently contains **1303** records. UniProt remains the sequence, taxonomy, identifier, review-status, cross-reference, publication, and evidence backbone. Pathogens3D remains a secondary source because it recovers query-missed accessions and contributes concise functional notes and domain architecture that are not consistently represented as equivalent UniProt fields. Its accessions are resolved back through UniProt so sequences and current identifiers still come from the primary service.

## Useful UniProt fields inspected

The JSON responses expose `primaryAccession`, `entryType`, `proteinDescription`, `genes` (including ordered locus names/ORF names), `organism` and `taxonId`, `sequence` and length, `comments`, `uniProtKBCrossReferences`, `references`, and `proteinExistence`. The builder uses the stable tabular subset in the master file and retains raw JSON snapshots for deeper inspection.

## Evidence interpretation

Reviewed UniProt entries are labelled `curated_annotation`; unreviewed entries are `automated_annotation`. `experimentally_supported` is reserved for an explicit manual assertion backed by literature, and `ambiguous_candidate` is available for deliberately included uncertain records. Neither a Pathogens3D row nor an automatic effector name alone is treated as experimental validation.
