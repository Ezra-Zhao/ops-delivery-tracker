# Integration Diagram

> DESIGN ASSUMPTIONS ONLY. No interface in this diagram is a real
> integration. Nothing in this repository connects to any external system.
> Each external interface below is labelled with its assumption status.

## System context (Mermaid)

```mermaid
flowchart LR
    subgraph ODT["ops-delivery-tracker (this demo, implemented)"]
        DB[("SQLite portfolio DB<br/>site / milestone / risk / decision / ticket")]
        WF["Handover sign-off<br/>state machine"]
        GOV["Controlled document<br/>register"]
        RPT["Reporting engine<br/>sql/queries.sql"]
        DB --> WF
        DB --> GOV
        DB --> RPT
    end
    TKT["Ticketing system of record<br/>ASSUMPTION: external system exists;<br/>tickets are imported, not created here"]
    BI["Executive reporting surface<br/>ASSUMPTION: the generated markdown<br/>is pasted or published to an internal page"]
    DOC["Document storage<br/>ASSUMPTION: documents live in an<br/>external store; only the register lives here"]
    TKT -. "ticket export (assumed CSV/API, not built)" .-> DB
    RPT -. "weekly markdown (manual publish, not built)" .-> BI
    GOV -. "doc_code + version reference only (not built)" .-> DOC
```

## Interface inventory

| Interface | Direction | Status | Assumption being made |
|---|---|---|---|
| Ticket intake | Ticketing system -> tracker | DESIGN ASSUMPTION, not implemented | A ticketing tool can export id, priority, SLA target, created/resolved timestamps in a stable shape |
| Executive report distribution | Tracker -> reporting surface | DESIGN ASSUMPTION, not implemented | The generated one-page markdown is the artifact; distribution is a human or scheduler step outside this demo |
| Controlled document storage | Register -> document store | DESIGN ASSUMPTION, not implemented | Documents themselves live elsewhere; this system governs registration, version, approval, and obsolescence metadata only |
| Seed / demo data load | Local script -> SQLite | IMPLEMENTED | scripts/build_db.py and the in-memory seed path used by tests and report generation |

## Why the assumptions are drawn this way

- Ticketing stays the system of record for ticket work; the tracker consumes
  timestamps for SLA/MTTR rather than duplicating ticket workflow. That keeps
  one source of truth for operations and one for portfolio governance.
- The document register is deliberately metadata-only: governance (who owns
  it, which version is current, what was retired and why) is the part that
  was missing in discovery, not file storage.
