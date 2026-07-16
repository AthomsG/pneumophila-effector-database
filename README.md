# Legionella effector catalogue

[![Refresh catalogue](https://github.com/AthomsG/pneumophila-effector-database/actions/workflows/refresh.yml/badge.svg)](https://github.com/AthomsG/pneumophila-effector-database/actions/workflows/refresh.yml)

A compact, refreshable reference catalogue of established *Legionella pneumophila* Dot/Icm effectors. The primary FASTA contains proteins backed by reported Dot/Icm-dependent translocation evaluations; broad text matches and embedding-neighborhood candidates are not added automatically.

## Sources and selection

Pathogens3D is the evidence-bearing seed source. Its 368-protein repertoire was assembled from previously reported genome-wide evaluations of Dot/Icm-dependent translocation. UniProtKB supplies current accessions, sequences, names, taxonomy, review status, comments, cross-references, and publications.

[Pathogens3D](https://proteins.pathogens3d.org/data/data.legionella-effectors.tsv) accessions are validated and resolved through UniProt. Known incorrect or obsolete source mappings are repaired in `curation/source_accession_corrections.tsv`, while the original source accession remains in provenance. Its concise annotations and domain architectures are retained in the catalogue.

The fetch step still measures broad UniProt searches for “effector,” “Dot/Icm,” “type IV secretion,” and known names. These searches are useful for literature follow-up and source assessment, but their results include apparatus proteins, other secretion systems, housekeeping name collisions, and automatically inferred homologues. They do not enter the established reference automatically. See the [initial catalogue audit](reports/catalogue_quality_audit.md) and [embedding-cluster assessment](reports/embedding_cluster_assessment.md).

## Evidence categories

- `experimentally_supported`: reported Dot/Icm-dependent translocation evidence with a supporting source. This does not imply that molecular function has been experimentally determined.
- `curated_annotation`: a reviewed UniProtKB/Swiss-Prot effector annotation.
- `automated_annotation`: an unreviewed UniProtKB/TrEMBL annotation or homology-based name.
- `ambiguous_candidate`: deliberately retained despite uncertainty.

The established output uses `experimentally_supported`. Other categories remain available for diagnostics and future candidate outputs, but automated or ambiguous records are excluded from the primary FASTA. “Reviewed” means expert-curated and is separate from translocation evidence.

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

Add a row to `curation/manual_additions.tsv` using the master-table columns. A primary-reference addition must include a stable accession, sequence where possible, `experimentally_supported`, a precise explanation in `evidence_note`, and a DOI/PMID or publication URL in `evidence_reference`. Exact sequence hashes and UniProt accessions are used for deduplication; aliases and source provenance are merged.

To suppress a record, add its accession (preferred) or canonical name to `curation/manual_exclusions.tsv`, plus a reason and reference. Manual files are intentionally small and reviewable.

## Scheduled refresh

The GitHub Actions workflow runs on the first day of each month and by manual dispatch. It runs fixture tests, fetches current sources, rebuilds every output, writes a diff summary, and uses `peter-evans/create-pull-request` to open or update a pull request. If the tracked outputs did not change, that action creates no pull request.

## Limitations

The reference is centred on the reported *L. pneumophila* translocation repertoire and is not an exhaustive catalogue of inferred effector homologues across every *Legionella* species. Experimental support refers to secretion/translocation, not necessarily biochemical function. New literature-supported effectors require manual review before inclusion. For machine-learning use, homologous sequences should be clustered before train/test splitting to prevent leakage; embedding proximity or automated product names must not be treated as ground-truth positives.
