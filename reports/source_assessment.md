# Source assessment

Data retrieved on 2026-07-16.

## Queries tested

- `organism_name:Legionella AND protein_name:effector` — **804** records (`protein_name_effector`).
- `organism_name:Legionella AND "Dot/Icm"` — **2096** records (`dot_icm`).
- `organism_name:Legionella AND "type IV secretion"` — **828** records (`type_iv_secretion`).
- `organism_name:Legionella AND (gene:RavZ OR protein_name:RavZ OR gene:SidM OR protein_name:SidM OR gene:DrrA OR protein_name:DrrA OR gene:SidC OR protein_name:SidC OR gene:AnkB OR protein_name:AnkB OR gene:LegK2 OR protein_name:LegK2 OR gene:LubX OR protein_name:LubX OR gene:SidH OR protein_name:SidH OR gene:SidD OR protein_name:SidD OR gene:SdeA OR protein_name:SdeA OR gene:SidE OR protein_name:SidE OR gene:SetA OR protein_name:SetA OR gene:MavE OR protein_name:MavE OR gene:RalF OR protein_name:RalF OR gene:LidA OR protein_name:LidA OR gene:LepA OR protein_name:LepA OR gene:LepB OR protein_name:LepB OR gene:VipD OR protein_name:VipD OR gene:RomA OR protein_name:RomA OR gene:LegAS4 OR protein_name:LegAS4 OR gene:Lgt1 OR protein_name:Lgt1 OR gene:Lgt2 OR protein_name:Lgt2 OR gene:Lgt3 OR protein_name:Lgt3 OR gene:SidJ OR protein_name:SidJ OR gene:SdjA OR protein_name:SdjA OR gene:LotA OR protein_name:LotA OR gene:MavC OR protein_name:MavC)` — **628** records (`known_names`).

## Coverage and overlap

Pathogens3D contains **368** rows and **368** non-empty UniProt accessions. UniProt resolved **368** to active records; **0** accession(s) are inactive/deleted and are noted in the transient fetch log.

Across the exploratory queries, **69** accessions overlap Pathogens3D, **299** Pathogens3D accessions are not recovered by those queries, and **3403** UniProt query hits are absent from Pathogens3D.

The complete row-level comparison, including query provenance, is generated locally as `reports/source_comparison.tsv` and intentionally ignored by Git.

## Missing and additional records

Pathogens3D-only accessions (299): `P37033`, `Q5ZR83`, `Q5ZR84`, `Q5ZRA8`, `Q5ZRD0`, `Q5ZRE6`, `Q5ZRH0`, `Q5ZRH1`, `Q5ZRJ3`, `Q5ZRJ6`, `Q5ZRJ7`, `Q5ZRK2`, `Q5ZRK7`, `Q5ZRL9`, `Q5ZRM1`, `Q5ZRN6`, `Q5ZRP8`, `Q5ZRQ2`, `Q5ZRQ4`, `Q5ZRR5`, `Q5ZRR7`, `Q5ZRS4`, `Q5ZRS6`, `Q5ZRW4`, `Q5ZRW7`, `Q5ZRX6`, `Q5ZS00`, `Q5ZS25`, `Q5ZS27`, `Q5ZS41`, … (269 more in the locally generated comparison TSV).

UniProt-only effector-like records retained in the catalogue (0): none.

## Ambiguity and false positives

The broad searches returned **3403** UniProt-only records that were not retained. Prominent false positives are structural Dot/Icm/type-IV secretion apparatus proteins; text mentioning a secretion system is not evidence that the protein is a translocated effector. Other unreviewed records are plausible homologues but only automatically annotated, so their evidence category must not be upgraded merely because a query matched.

## Source decision

The established master catalogue currently contains **368** records. Pathogens3D is the evidence-bearing seed because its repertoire was compiled from reported Dot/Icm-dependent translocation evaluations. UniProt supplies current sequences, taxonomy, identifiers, review status, comments, cross-references, and publications. Broad UniProt text-query hits remain discovery candidates and are not added automatically.

## Useful UniProt fields inspected

The JSON responses expose `primaryAccession`, `entryType`, `proteinDescription`, `genes` (including ordered locus names/ORF names), `organism` and `taxonId`, `sequence` and length, `comments`, `uniProtKBCrossReferences`, `references`, and `proteinExistence`. The builder uses the stable tabular subset in the master file and retains raw JSON snapshots for deeper inspection.

## Evidence interpretation

The established reference uses `experimentally_supported` for the Pathogens3D repertoire because its source study compiled proteins from reported genome-wide Dot/Icm-dependent translocation evaluations. This describes translocation evidence, not necessarily a known molecular function. Automatic UniProt query hits are excluded from the primary catalogue.
