from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RAW = DATA / "raw"
REPORTS = ROOT / "reports"
CURATION = ROOT / "curation"

UNIPROT_URL = "https://rest.uniprot.org/uniprotkb/search"
PATHOGENS3D_URL = "https://proteins.pathogens3d.org/data/data.legionella-effectors.tsv"

KNOWN_NAMES = (
    "RavZ", "SidM", "DrrA", "SidC", "AnkB", "LegK2", "LubX", "SidH", "SidD",
    "SdeA", "SidE", "SetA", "MavE", "RalF", "LidA", "LepA", "LepB", "VipD",
    "RomA", "LegAS4", "Lgt1", "Lgt2", "Lgt3", "SidJ", "SdjA", "LotA", "MavC",
)

QUERIES = {
    "protein_name_effector": "organism_name:Legionella AND protein_name:effector",
    "dot_icm": 'organism_name:Legionella AND "Dot/Icm"',
    "type_iv_secretion": 'organism_name:Legionella AND "type IV secretion"',
    "known_names": "organism_name:Legionella AND (" + " OR ".join(
        f"gene:{name} OR protein_name:{name}" for name in KNOWN_NAMES
    ) + ")",
}

MASTER_FIELDS = (
    "uniprot_accession", "canonical_name", "gene_names", "locus_tag", "organism",
    "strain", "taxonomy_id", "reviewed", "protein_name", "annotation", "sequence", "sequence_length",
    "evidence_category", "evidence_note", "evidence_reference", "source", "source_record", "retrieval_date",
)
