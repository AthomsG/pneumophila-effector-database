import re


def _full_name(record):
    desc = record.get("proteinDescription", {})
    recommended = desc.get("recommendedName", {})
    value = recommended.get("fullName", {}).get("value")
    if value:
        return value
    submitted = desc.get("submissionNames") or []
    return submitted[0].get("fullName", {}).get("value", "") if submitted else ""


def _genes(record):
    values = []
    locus = []
    for gene in record.get("genes", []):
        for key in ("geneName", "synonyms", "orfNames", "orderedLocusNames"):
            item = gene.get(key, [])
            item = [item] if isinstance(item, dict) else item
            for entry in item:
                value = entry.get("value", "")
                if value and value not in values:
                    values.append(value)
                if key in ("orfNames", "orderedLocusNames") and value not in locus:
                    locus.append(value)
    return values, locus


def strain_from_organism(name):
    match = re.search(r"\((?:strain\s+)?(.+?)\)$", name or "", re.I)
    return match.group(1) if match else ""


def normalize_uniprot(record, retrieval_date):
    genes, locus = _genes(record)
    protein_name = _full_name(record)
    sequence = record.get("sequence", {}).get("value", "")
    organism = record.get("organism", {}).get("scientificName", "")
    canonical = genes[0] if genes else re.sub(r"^(?:putative\s+)?(?:effector protein\s+)?", "", protein_name, flags=re.I)
    return {
        "uniprot_accession": record.get("primaryAccession", ""),
        "canonical_name": canonical,
        "gene_names": ";".join(genes),
        "locus_tag": ";".join(locus),
        "organism": organism,
        "strain": strain_from_organism(organism),
        "taxonomy_id": record.get("organism", {}).get("taxonId", ""),
        "reviewed": str(record.get("entryType", "").startswith("UniProtKB reviewed")).lower(),
        "protein_name": protein_name,
        "sequence": sequence,
        "sequence_length": record.get("sequence", {}).get("length", len(sequence)),
        "evidence_category": "curated_annotation" if record.get("entryType", "").startswith("UniProtKB reviewed") else "automated_annotation",
        "source": "UniProt",
        "source_record": record.get("primaryAccession", ""),
        "retrieval_date": retrieval_date,
    }


def record_text(record):
    return " ".join((
        _full_name(record),
        " ".join(x.get("value", "") for g in record.get("genes", []) for x in [g.get("geneName", {})]),
        str(record.get("comments", [])),
        str(record.get("uniProtKBCrossReferences", [])),
    )).lower()

