import csv
import datetime as dt
from collections import Counter, defaultdict

from .config import DATA, KNOWN_NAMES, MASTER_FIELDS, QUERIES, RAW, REPORTS
from .io_utils import dump_json, load_json, read_tsv, sequence_hash, write_tsv
from .normalize import normalize_uniprot, record_text
from .sources import fetch_pathogens3d, fetch_uniprot, fetch_uniprot_accessions

FAILURE_FIELDS = ("source", "record", "operation", "error", "retrieval_date")
COMPARISON_FIELDS = (
    "uniprot_accession", "canonical_name", "in_uniprot_queries", "in_pathogens3d",
    "included_in_master", "uniprot_query_names", "pathogens3d_gene", "pathogens3d_locus",
    "pathogens3d_annotation", "comparison_status",
)


def today():
    return dt.datetime.now(dt.timezone.utc).date().isoformat()


def fetch():
    RAW.mkdir(parents=True, exist_ok=True)
    failures = []
    date = today()
    for name, query in QUERIES.items():
        try:
            dump_json(RAW / f"uniprot_{name}.json", fetch_uniprot(query))
        except Exception as exc:
            failures.append({"source": "UniProt", "record": name, "operation": "query", "error": str(exc), "retrieval_date": date})
    try:
        p3d = fetch_pathogens3d()
        write_tsv(RAW / "pathogens3d.tsv", p3d, list(p3d[0]) if p3d else ["Uniprot"])
    except Exception as exc:
        failures.append({"source": "Pathogens3D", "record": "Legionella table", "operation": "download", "error": str(exc), "retrieval_date": date})
        p3d = []

    accessions = {row.get("Uniprot", "").strip() for row in p3d}
    try:
        accession_records = fetch_uniprot_accessions(accessions)
        dump_json(RAW / "uniprot_pathogens3d_accessions.json", accession_records)
        for record in accession_records:
            if record.get("entryType") == "Inactive":
                failures.append({
                    "source": "UniProt", "record": record.get("primaryAccession", ""),
                    "operation": "resolve Pathogens3D accession",
                    "error": record.get("inactiveReason", {}).get("deletedReason", "inactive accession"),
                    "retrieval_date": date,
                })
    except Exception as exc:
        failures.append({"source": "UniProt", "record": "Pathogens3D accessions", "operation": "lookup", "error": str(exc), "retrieval_date": date})
    write_tsv(DATA / "fetch_failures.tsv", failures, FAILURE_FIELDS)
    return failures


def load_sources():
    query_records = {}
    for name in QUERIES:
        path = RAW / f"uniprot_{name}.json"
        query_records[name] = load_json(path) if path.exists() else []
    accession_path = RAW / "uniprot_pathogens3d_accessions.json"
    accession_records = load_json(accession_path) if accession_path.exists() else []
    return query_records, accession_records, read_tsv(RAW / "pathogens3d.tsv")


def _is_effector(record):
    text = record_text(record)
    genes = {part.lower() for part in normalize_uniprot(record, "")["gene_names"].split(";")}
    return (
        "effector" in text
        or "dot/icm substrate" in text
        or bool(genes & {name.lower() for name in KNOWN_NAMES})
    ) and "effector cell" not in text


def _merge_rows(rows):
    by_accession = {}
    by_hash = {}
    for row in rows:
        accession = row["uniprot_accession"]
        digest = sequence_hash(row["sequence"])
        existing = by_accession.get(accession) or (by_hash.get(digest) if digest else None)
        if existing:
            for field in ("gene_names", "locus_tag", "source", "source_record"):
                values = [x for part in (existing[field], row[field]) for x in part.split(";") if x]
                existing[field] = ";".join(dict.fromkeys(values))
            if accession and accession != existing["uniprot_accession"]:
                existing["source_record"] = ";".join(dict.fromkeys(
                    [*existing["source_record"].split(";"), f"UniProt:{accession}"]
                ))
            if row["evidence_category"] == "experimentally_supported":
                existing["evidence_category"] = row["evidence_category"]
            continue
        by_accession[accession] = row
        if digest:
            by_hash[digest] = row
    return list(by_accession.values())


def build():
    query_sets, accession_records, p3d = load_sources()
    date = today()
    p3d_by_accession = {r.get("Uniprot", "").strip(): r for r in p3d if r.get("Uniprot", "").strip()}
    records = {}
    from_query = set()
    for values in query_sets.values():
        for record in values:
            accession = record.get("primaryAccession", "")
            records[accession] = record
            if _is_effector(record):
                from_query.add(accession)
    for record in accession_records:
        records[record.get("primaryAccession", "")] = record

    rows = []
    for accession in sorted(from_query | set(p3d_by_accession)):
        record = records.get(accession)
        if not record:
            continue
        row = normalize_uniprot(record, date)
        if accession in p3d_by_accession:
            p = p3d_by_accession[accession]
            row["source"] = "UniProt;Pathogens3D"
            row["source_record"] = f"{accession};Pathogens3D:{p.get('Locus name') or p.get('Gene name') or accession}"
            p_alias = p.get("Gene name", "").strip()
            if p_alias:
                aliases = [*row["gene_names"].split(";"), *p_alias.replace("/", ";").split(";")]
                row["gene_names"] = ";".join(dict.fromkeys(x for x in aliases if x))
            if accession not in from_query and not _is_effector(record):
                row["evidence_category"] = "ambiguous_candidate"
            if record.get("entryType") == "Inactive":
                row["source"] = "Pathogens3D"
        rows.append(row)

    rows.extend(read_tsv(DATA / "manual_additions.tsv"))
    exclusions = read_tsv(DATA / "manual_exclusions.tsv")
    excluded_accessions = {r.get("uniprot_accession", "") for r in exclusions}
    excluded_names = {r.get("canonical_name", "").lower() for r in exclusions if r.get("canonical_name")}
    rows = [r for r in rows if r.get("uniprot_accession", "") not in excluded_accessions and r.get("canonical_name", "").lower() not in excluded_names]
    rows = sorted(_merge_rows(rows), key=lambda r: (r["canonical_name"].lower(), r["uniprot_accession"]))
    write_tsv(DATA / "master_effectors.tsv", rows, MASTER_FIELDS)
    _write_fasta(rows)
    compare(rows)
    return rows


def _write_fasta(rows):
    lines = []
    for row in rows:
        if not row["sequence"]:
            continue
        header = row["uniprot_accession"] or sequence_hash(row["sequence"])[:12]
        lines.append(f">{header} {row['canonical_name']} | {row['organism']}")
        lines.extend(row["sequence"][i:i + 60] for i in range(0, len(row["sequence"]), 60))
    (DATA / "all_effector_sequences.faa").write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def compare(master=None):
    query_sets, accession_records, p3d = load_sources()
    master = master if master is not None else read_tsv(DATA / "master_effectors.tsv")
    query_names = defaultdict(list)
    query_records = {}
    for name, values in query_sets.items():
        for record in values:
            accession = record.get("primaryAccession", "")
            query_records[accession] = record
            query_names[accession].append(name)
    p3d_by = {r.get("Uniprot", "").strip(): r for r in p3d if r.get("Uniprot", "").strip()}
    master_by = {r.get("uniprot_accession", ""): r for r in master}
    all_accessions = sorted(set(query_records) | set(p3d_by))
    rows = []
    for accession in all_accessions:
        p = p3d_by.get(accession, {})
        m = master_by.get(accession, {})
        in_u, in_p = accession in query_records, accession in p3d_by
        status = "overlap" if in_u and in_p else "uniprot_query_only" if in_u else "pathogens3d_only"
        rows.append({
            "uniprot_accession": accession,
            "canonical_name": m.get("canonical_name", p.get("Gene name", "")),
            "in_uniprot_queries": str(in_u).lower(),
            "in_pathogens3d": str(in_p).lower(),
            "included_in_master": str(accession in master_by).lower(),
            "uniprot_query_names": ";".join(query_names[accession]),
            "pathogens3d_gene": p.get("Gene name", ""),
            "pathogens3d_locus": p.get("Locus name", ""),
            "pathogens3d_annotation": p.get("Annotation", ""),
            "comparison_status": status,
        })
    write_tsv(DATA / "source_comparison.tsv", rows, COMPARISON_FIELDS)
    _write_report(query_sets, p3d, accession_records, rows, master)
    return rows


def _write_report(query_sets, p3d, accession_records, comparison, master):
    counts = Counter(r["comparison_status"] for r in comparison)
    p3d_accessions = {r.get("Uniprot", "").strip() for r in p3d if r.get("Uniprot", "").strip()}
    resolved = {r.get("primaryAccession", "") for r in accession_records if r.get("entryType") != "Inactive"}
    inactive = {r.get("primaryAccession", "") for r in accession_records if r.get("entryType") == "Inactive"}
    missing = [r for r in comparison if r["comparison_status"] == "pathogens3d_only"]
    query_only_included = [r for r in comparison if r["comparison_status"] == "uniprot_query_only" and r["included_in_master"] == "true"]
    query_only_rejected = [r for r in comparison if r["comparison_status"] == "uniprot_query_only" and r["included_in_master"] == "false"]
    def preview(rows, limit=30):
        values = ", ".join(f"`{r['uniprot_accession']}`" for r in rows[:limit]) or "none"
        return values + (f", … ({len(rows) - limit} more; see `data/source_comparison.tsv`)" if len(rows) > limit else "")

    lines = [
        "# Source assessment", "", f"Data retrieved on {today()}.", "", "## Queries tested", "",
    ]
    for name, query in QUERIES.items():
        lines.append(f"- `{query}` — **{len(query_sets[name])}** records (`{name}`).")
    lines += [
        "", "## Coverage and overlap", "",
        f"Pathogens3D contains **{len(p3d)}** rows and **{len(p3d_accessions)}** non-empty UniProt accessions. "
        f"UniProt resolved **{len(resolved & p3d_accessions)}** to active records; **{len(inactive)}** accession(s) are inactive/deleted and appear in `data/fetch_failures.tsv`.",
        "",
        f"Across the exploratory queries, **{counts['overlap']}** accessions overlap Pathogens3D, "
        f"**{counts['pathogens3d_only']}** Pathogens3D accessions are not recovered by those queries, and "
        f"**{counts['uniprot_query_only']}** UniProt query hits are absent from Pathogens3D.",
        "", "The complete, row-level result (including query provenance) is in `data/source_comparison.tsv`.",
        "", "## Missing and additional records", "",
        f"Pathogens3D-only accessions ({len(missing)}): " + preview(missing) + ".",
        "",
        f"UniProt-only effector-like records retained in the catalogue ({len(query_only_included)}): "
        + preview(query_only_included) + ".",
        "", "## Ambiguity and false positives", "",
        f"The broad searches returned **{len(query_only_rejected)}** UniProt-only records that were not retained. "
        "Prominent false positives are structural Dot/Icm/type-IV secretion apparatus proteins; text mentioning a secretion system is not evidence that the protein is a translocated effector. "
        "Other unreviewed records are plausible homologues but only automatically annotated, so their evidence category must not be upgraded merely because a query matched.",
        "", "## Source decision", "",
        f"The master catalogue currently contains **{len(master)}** records. UniProt remains the sequence, taxonomy, identifier, review-status, cross-reference, publication, and evidence backbone. "
        "Pathogens3D remains a secondary source because it recovers query-missed accessions and contributes concise functional notes and domain architecture that are not consistently represented as equivalent UniProt fields. "
        "Its accessions are resolved back through UniProt so sequences and current identifiers still come from the primary service.",
        "", "## Useful UniProt fields inspected", "",
        "The JSON responses expose `primaryAccession`, `entryType`, `proteinDescription`, `genes` (including ordered locus names/ORF names), `organism` and `taxonId`, `sequence` and length, `comments`, `uniProtKBCrossReferences`, `references`, and `proteinExistence`. "
        "The builder uses the stable tabular subset in the master file and retains raw JSON snapshots for deeper inspection.",
        "", "## Evidence interpretation", "",
        "Reviewed UniProt entries are labelled `curated_annotation`; unreviewed entries are `automated_annotation`. `experimentally_supported` is reserved for an explicit manual assertion backed by literature, and `ambiguous_candidate` is available for deliberately included uncertain records. "
        "Neither a Pathogens3D row nor an automatic effector name alone is treated as experimental validation.", "",
    ]
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "source_assessment.md").write_text("\n".join(lines), encoding="utf-8")


def run_all():
    fetch()
    return build()
