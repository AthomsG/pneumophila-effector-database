import json
from pathlib import Path

from legionella_effectors.io_utils import read_tsv, sequence_hash
from legionella_effectors.normalize import normalize_uniprot
from legionella_effectors import pipeline

FIXTURES = Path(__file__).parent / "fixtures"


def test_normalize_uniprot():
    record = json.loads((FIXTURES / "uniprot.json").read_text())[0]
    row = normalize_uniprot(record, "2026-01-02")
    assert row["uniprot_accession"] == "P00001"
    assert row["canonical_name"] == "testA"
    assert row["locus_tag"] == "lpg0001"
    assert row["strain"] == "Test 1"
    assert row["evidence_category"] == "curated_annotation"


def test_effector_filter_rejects_apparatus():
    records = json.loads((FIXTURES / "uniprot.json").read_text())
    assert pipeline._is_effector(records[0])
    assert not pipeline._is_effector(records[1])


def test_exact_sequence_deduplication():
    base = {field: "" for field in pipeline.MASTER_FIELDS}
    first = {**base, "uniprot_accession": "P1", "sequence": "MPEP", "source": "UniProt", "source_record": "P1"}
    second = {**base, "uniprot_accession": "", "sequence": "MPEP", "source": "manual", "source_record": "x"}
    merged = pipeline._merge_rows([first, second])
    assert len(merged) == 1
    assert merged[0]["source"] == "UniProt;manual"
    assert sequence_hash("MPEP")


def test_build_from_local_fixtures(monkeypatch, tmp_path):
    data, raw, reports, curation = tmp_path / "data", tmp_path / "data/raw", tmp_path / "reports", tmp_path / "curation"
    raw.mkdir(parents=True)
    curation.mkdir()
    records = json.loads((FIXTURES / "uniprot.json").read_text())
    for name in pipeline.QUERIES:
        (raw / f"uniprot_{name}.json").write_text(json.dumps(records))
    (raw / "uniprot_pathogens3d_accessions.json").write_text(json.dumps([records[0]]))
    (raw / "pathogens3d.tsv").write_text((FIXTURES / "pathogens3d.tsv").read_text())
    (curation / "manual_additions.tsv").write_text("\t".join(pipeline.MASTER_FIELDS) + "\n")
    (curation / "manual_exclusions.tsv").write_text("uniprot_accession\tcanonical_name\treason\treference\n")
    monkeypatch.setattr(pipeline, "DATA", data)
    monkeypatch.setattr(pipeline, "RAW", raw)
    monkeypatch.setattr(pipeline, "REPORTS", reports)
    monkeypatch.setattr(pipeline, "CURATION", curation)
    rows = pipeline.build()
    assert [r["uniprot_accession"] for r in rows] == ["P00001"]
    assert read_tsv(reports / "source_comparison.tsv")[0]["comparison_status"] == "overlap"
    assert (data / "all_effector_sequences.faa").read_text().startswith(">P00001")
    assert "gene=testA" in (data / "all_effector_sequences.faa").read_text().splitlines()[0]
