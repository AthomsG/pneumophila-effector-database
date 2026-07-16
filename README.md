# Legionella effector catalogue

[![Refresh catalogue](https://github.com/AthomsG/pneumophila-effector-database/actions/workflows/refresh.yml/badge.svg)](https://github.com/AthomsG/pneumophila-effector-database/actions/workflows/refresh.yml)

A compact, refreshable catalogue of known and candidate *Legionella* Dot/Icm effectors. The repository deliberately separates source retrieval from evidence interpretation: matching a broad text query does not establish experimental validation.

## Sources and selection

UniProtKB is the primary source for accessions, sequences, names, taxonomy, review status, comments, cross-references, publications, and protein-existence evidence. The fetch step tests four search strategies: protein names containing “effector”, free-text “Dot/Icm”, free-text “type IV secretion”, and a growing list of established names such as RavZ, SidM/DrrA, SidC, AnkB, LegK2, LubX, SidH, and SidD.

[Pathogens3D](https://proteins.pathogens3d.org/data/data.legionella-effectors.tsv) is retained as a secondary discovery/evidence source. Its accessions are resolved through UniProt; its concise annotations and domain architectures remain useful for source assessment. The measured source overlap and current rationale are in [reports/source_assessment.md](reports/source_assessment.md).

Broad query results include Dot/Icm apparatus components and automatically named homologues. The builder retains records with explicit effector wording, explicit Dot/Icm-substrate wording, a known effector gene name, or a Pathogens3D accession. It does not treat every query hit as a catalogue member.

## Evidence categories

- `experimentally_supported`: explicitly asserted through a manual addition with a supporting reference.
- `curated_annotation`: a reviewed UniProtKB/Swiss-Prot effector annotation.
- `automated_annotation`: an unreviewed UniProtKB/TrEMBL annotation or homology-based name.
- `ambiguous_candidate`: deliberately retained despite uncertainty.

These categories are conservative. “Reviewed” means expert-curated, not necessarily that translocation or function was directly demonstrated for every strain-specific record. Pathogens3D membership alone is not upgraded to experimental support.

## Running the pipeline

Python 3.10 or newer is sufficient; the runtime uses only the standard library. The examples use [uv](https://docs.astral.sh/uv/) for reproducible environment management.

```bash
uv run python -m legionella_effectors fetch
uv run python -m legionella_effectors compare
uv run python -m legionella_effectors build
uv run python -m legionella_effectors all
```

`fetch` writes ignored raw source snapshots and a transient failure log under `data/raw/`. A genuine retrieval failure exits non-zero, making the Actions badge red; an obsolete source accession is recorded but does not abort an otherwise valid refresh. `compare` produces the row-level source comparison under `reports/`. `build` creates the master TSV and FASTA from already-fetched snapshots. `all` runs retrieval and the complete rebuild. Tests use only local fixtures:

```bash
uv run --with pytest pytest
```

The `data/` directory contains only the two primary deliverables: `master_effectors.tsv` and `all_effector_sequences.faa`. FASTA headers include the accession, canonical name, gene aliases, locus tag, full protein name, organism, taxonomy ID, review status, evidence category, sources, and available functional annotation. Source-comparison diagnostics live under `reports/`.

## Manual additions and exclusions

Add a row to `curation/manual_additions.tsv` using the master-table columns. Supply a stable accession when one exists, a sequence where possible, a provenance string in `source_record`, and do not use `experimentally_supported` without a literature reference in the provenance. Exact sequence hashes and UniProt accessions are used for deduplication; aliases and source provenance are merged.

To suppress a record, add its accession (preferred) or canonical name to `curation/manual_exclusions.tsv`, plus a reason and reference. Manual files are intentionally small and reviewable.

## Scheduled refresh

The GitHub Actions workflow runs on the first day of each month and by manual dispatch. It runs fixture tests, fetches current sources, rebuilds every output, writes a diff summary, and uses `peter-evans/create-pull-request` to open or update a pull request. If the tracked outputs did not change, that action creates no pull request.

## Limitations

Text search is sensitive to annotation wording and can miss effectors described only as “uncharacterized protein.” Conversely, secretion-system queries retrieve machinery proteins that are not effectors. Gene names are reused across strains, automated annotations propagate by homology, and Pathogens3D is centred on structurally interpreted records rather than exhaustive strain coverage. The catalogue is therefore a transparent, reproducible starting point—not a claim of complete or uniformly experimental coverage.
