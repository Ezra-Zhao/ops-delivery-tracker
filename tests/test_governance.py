import pytest
from odt import governance as G

def test_version_lifecycle_and_obsolescence(conn):
    cur = G.current_version(conn, "OPS-RBK-001")
    assert cur["version"] == 2 and cur["approval_status"] == "approved" and cur["is_obsolete"] == 0
    v1 = conn.execute("SELECT * FROM controlled_document WHERE doc_code='OPS-RBK-001' AND version=1").fetchone()
    assert v1["is_obsolete"] == 1 and "Superseded" in v1["obsolete_reason"]

def test_new_version_must_supersede(conn):
    with pytest.raises(G.GovernanceError):
        G.register_document(conn, "OPS-HOV-002", "Template v2 without supersedes", "tpm-demo", "2026-11-02")

def test_obsolete_cannot_be_approved(conn):
    v1 = conn.execute("SELECT id FROM controlled_document WHERE doc_code='OPS-RBK-001' AND version=1").fetchone()["id"]
    with pytest.raises(G.GovernanceError):
        G.approve_document(conn, v1, "tpm-demo")
    with pytest.raises(G.GovernanceError):
        G.submit_for_review(conn, v1)

def test_draft_review_approve_flow(conn):
    doc_id, version = G.register_document(conn, "OPS-NEW-009", "New procedure", "docs-owner", "2026-11-02")
    assert version == 1
    with pytest.raises(G.GovernanceError):
        G.approve_document(conn, doc_id, "tpm-demo")  # must be in_review first
    G.submit_for_review(conn, doc_id)
    G.approve_document(conn, doc_id, "tpm-demo")
    cur = G.current_version(conn, "OPS-NEW-009")
    assert cur["approval_status"] == "approved"

def test_obsolescence_requires_approved_and_reason(conn):
    doc_id, _ = G.register_document(conn, "OPS-NEW-010", "Draft only doc", "docs-owner", "2026-11-02")
    with pytest.raises(G.GovernanceError):
        G.mark_obsolete(conn, doc_id, "some reason")  # not approved yet
