-- ops-delivery-tracker: canonical reporting queries (SQLite)
-- Convention: each query starts with a marker line of the form
--   -- name: <query_name>
-- reporting.py parses and executes exactly these statements, so every
-- number in the executive report can be re-run by hand against the same DB.
-- Parameters: :as_of is an ISO date (YYYY-MM-DD). All data is SYNTHETIC.

-- name: ticket_counts
SELECT COUNT(*) AS total_tickets,
       SUM(CASE WHEN status IN ('resolved','closed') THEN 1 ELSE 0 END) AS resolved_tickets,
       SUM(CASE WHEN status = 'open' THEN 1 ELSE 0 END) AS open_tickets
FROM ticket;

-- name: sla_attainment
-- SLA attainment over resolved tickets only: resolved within sla_hours.
SELECT COUNT(*) AS resolved_n,
       SUM(CASE WHEN (julianday(resolved_at) - julianday(created_at)) * 24.0 <= sla_hours
                THEN 1 ELSE 0 END) AS sla_met_n,
       ROUND(100.0 * SUM(CASE WHEN (julianday(resolved_at) - julianday(created_at)) * 24.0 <= sla_hours
                              THEN 1 ELSE 0 END) / COUNT(*), 2) AS sla_rate_pct
FROM ticket
WHERE status IN ('resolved','closed') AND resolved_at IS NOT NULL;

-- name: mttr
-- Mean time to resolve, in hours, over resolved tickets.
SELECT ROUND(AVG((julianday(resolved_at) - julianday(created_at)) * 24.0), 2) AS mttr_hours,
       COUNT(*) AS resolved_n
FROM ticket
WHERE status IN ('resolved','closed') AND resolved_at IS NOT NULL;

-- name: mttr_by_priority
SELECT priority,
       COUNT(*) AS resolved_n,
       ROUND(AVG((julianday(resolved_at) - julianday(created_at)) * 24.0), 2) AS mttr_hours
FROM ticket
WHERE status IN ('resolved','closed') AND resolved_at IS NOT NULL
GROUP BY priority ORDER BY priority;

-- name: milestone_achievement
-- Achievement over milestones already due on or before :as_of.
SELECT COUNT(*) AS due_n,
       SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed_n,
       ROUND(100.0 * SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) / COUNT(*), 2) AS achievement_pct
FROM milestone
WHERE due_date <= :as_of;

-- name: milestones_by_site
SELECT s.code AS site_code, s.ownership AS ownership,
       COUNT(m.id) AS milestones,
       SUM(CASE WHEN m.status = 'completed' THEN 1 ELSE 0 END) AS completed
FROM site s LEFT JOIN milestone m ON m.site_id = s.id
GROUP BY s.code, s.ownership ORDER BY s.code;

-- name: open_risks_by_severity
SELECT severity, COUNT(*) AS n FROM risk WHERE status = 'open'
GROUP BY severity ORDER BY n DESC;

-- name: open_tickets_by_priority
SELECT priority, COUNT(*) AS n FROM ticket WHERE status = 'open'
GROUP BY priority ORDER BY priority;
