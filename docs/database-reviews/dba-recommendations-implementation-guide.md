# DBA Recommendations Implementation Guide

**Document Information**
* **Created:** 2026-05-28
* **Related:** DBA Review Report (dba-review-backend-20260528.md)
* **Status:** In Progress
* **Migration:** 000013_dba_performance_optimizations.up.sql

---

## Overview

This document provides implementation guidance for the Senior DBA recommendations from the database review. The database-level optimizations have been implemented in migration 000013, while infrastructure and operations tasks require separate implementation.

---

## Completed Tasks (Migration 000013)

The following tasks have been completed and are ready for deployment via migration 000013:

### ✅ TSK-02: Add Partial Indexes for Soft Deletes (Priority: HIGH)
**Status:** Completed in migration 000013

**Implementation:**
- Created partial indexes on 48 tables with `deleted_at` columns
- All indexes use `CREATE INDEX CONCURRENTLY` to avoid locking
- Index format: `CREATE INDEX CONCURRENTLY idx_table_active_soft_delete ON table(id) WHERE deleted_at IS NULL`

**Tables Covered:**
- Auth Domain: auth_user
- Master Data: school, teacher, student, parent, classroom, grade, phase, subject, academic_year
- Transaction Domain: attendance, assessment, teaching_module, report, ppdb_applicant
- Assessment Tables: sd_assessment_criteria, di_strategy, module_differentiation, student_di_need, etc.

**Expected Impact:**
- 50-90% reduction in index size for soft-delete tables
- Significant performance improvement for active record queries
- Prevents full table scans as deleted rows accumulate

**Deployment Notes:**
- Safe to run in production with CONCURRENTLY
- No downtime required
- Monitor index creation progress via `pg_stat_progress_create_index`

---

### ✅ TSK-03: Tune Autovacuum Parameters (Priority: HIGH)
**Status:** Completed in migration 000013

**Implementation:**
- Configured autovacuum for 7 high-traffic tables
- Set `autovacuum_vacuum_scale_factor = 0.1` (default is 0.2)
- Set `autovacuum_analyze_scale_factor = 0.05` (default is 0.1)
- Set fillfactor = 90 for frequently updated tables

**Tables Covered:**
- auth_user (autovacuum + fillfactor)
- master_student (autovacuum + fillfactor)
- master_teacher (autovacuum + fillfactor)
- trx_attendance (autovacuum)
- trx_assessment (autovacuum)
- trx_teaching_module (autovacuum)
- audit_logs (autovacuum)

**Expected Impact:**
- 2x more frequent vacuuming on high-traffic tables
- Better statistics accuracy with more frequent analysis
- Reduced page splits with lower fillfactor
- Prevention of dead tuple accumulation

**Deployment Notes:**
- Changes take effect immediately
- Monitor autovacuum activity via `pg_stat_user_tables`
- Adjust parameters based on dead tuple metrics

---

### ✅ TSK-04: Add GIN Indexes for JSONB Columns (Priority: MEDIUM)
**Status:** Completed in migration 000013

**Implementation:**
- Created GIN indexes on 8 JSONB columns across 7 tables
- All indexes use `CREATE INDEX CONCURRENTLY`
- Index format: `CREATE INDEX CONCURRENTLY idx_table_column_gin ON table USING gin(jsonb_column)`

**Tables and Columns:**
- master_sd_assessment_criteria.rubric_elements
- trx_student_di_need.recommended_strategies
- master_rubric.template_structure
- master_portfolio_template.template_structure
- trx_student_portfolio.profile_data
- trx_intelligence_assessment.result_data
- trx_offline_conflict.local_data
- trx_offline_conflict.remote_data

**Expected Impact:**
- 10-100x performance improvement for JSONB containment queries
- Efficient `@>`, `?`, `?&`, `?|` operators
- Supports complex JSONB query patterns

**Deployment Notes:**
- GIN indexes are larger than B-Tree indexes
- Monitor index size vs query performance benefits
- Consider `gin_pending_list_limit` for write-heavy workloads

---

### ✅ TSK-05: Implement Expression Indexes (Priority: MEDIUM)
**Status:** Completed in migration 000013

**Implementation:**
- Created expression indexes for case-insensitive authentication
- All indexes use `CREATE INDEX CONCURRENTLY`
- Index format: `CREATE INDEX CONCURRENTLY idx_auth_user_email_lower ON auth_user(lower(email))`

**Indexes Created:**
- idx_auth_user_email_lower (basic)
- idx_auth_user_username_lower (basic)
- idx_auth_user_email_lower_enabled (partial with is_enabled = true)
- idx_auth_user_username_lower_enabled (partial with is_enabled = true)

**Expected Impact:**
- Efficient case-insensitive authentication lookups
- No need for `LOWER()` function calls in queries
- Supports application-level case-insensitive authentication

**Deployment Notes:**
- Application must use `LOWER(email)` or `LOWER(username)` in queries
- Consider adding application-level validation for email format
- Monitor authentication query performance

---

### ✅ TSK-06: Add BRIN Indexes for Time-Series Data (Priority: MEDIUM)
**Status:** Completed in migration 000013

**Implementation:**
- Created BRIN indexes on 23 time-series/append-only tables
- All indexes use `CREATE INDEX CONCURRENTLY`
- Index format: `CREATE INDEX CONCURRENTLY idx_table_created_brin ON table USING brin(created_at)`

**Tables Covered:**
- Transaction tables: trx_attendance, trx_assessment, trx_teaching_module
- Assessment results: trx_numeracy_result, trx_p5_result, trx_peer_assessment
- Learning data: trx_learning_experience, trx_lesson_plan, trx_ilp
- Communication: trx_communication_log
- Intelligence: trx_intelligence_assessment, trx_student_intervention
- Character: trx_character_intervention
- Offline: trx_offline_sync, trx_offline_conflict
- Audit: audit_logs

**Expected Impact:**
- 99% reduction in index size compared to B-Tree
- Efficient for time-range queries on append-only data
- Minimal storage overhead for large time-series tables

**Deployment Notes:**
- BRIN indexes are best for physically ordered data
- Consider `pages_per_range` parameter (default: 128)
- Monitor query performance; switch to B-Tree if range queries are slow

---

## Remaining Tasks (Infrastructure/Operations)

The following tasks require infrastructure deployment, monitoring setup, or manual validation and cannot be implemented via database migrations.

---

## 🚧 TSK-01: Deploy PgBouncer Connection Pooler (Priority: HIGH)

**Status:** Not Started - Infrastructure Task

**Description:** Deploy PgBouncer in transaction pooling mode with 200-500 max connections. Update application configuration to connect via PgBouncer.

### Implementation Steps

#### 1. Install PgBouncer
```bash
# Ubuntu/Debian
sudo apt-get install pgbouncer

# CentOS/RHEL
sudo yum install pgbouncer

# Docker
docker run -d --name pgbouncer \
  -p 6432:6432 \
  -e PGHOST=postgres \
  -e PGPORT=5432 \
  -e PGDATABASE=sim_sekolah \
  -e PGUSER=postgres \
  -e PGPASSWORD=your_password \
  edoburu/pgbouncer
```

#### 2. Configure PgBouncer
Create `/etc/pgbouncer/pgbouncer.ini`:

```ini
[databases]
sim_sekolah = host=localhost port=5432 dbname=sim_sekolah

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 200
reserve_pool_size = 50
reserve_pool_timeout = 3
server_lifetime = 3600
server_idle_timeout = 600
log_connections = 1
log_disconnections = 1
log_pooler_errors = 1
stats_period = 60
```

#### 3. Configure Authentication
Create `/etc/pgbouncer/userlist.txt`:
```
"postgres" "md5password_hash"
"sim_sekolah_user" "md5password_hash"
```

#### 4. Start PgBouncer
```bash
sudo systemctl enable pgbouncer
sudo systemctl start pgbouncer
```

#### 5. Update Application Configuration
Update backend configuration to connect via PgBouncer:

```yaml
# config/database.yaml or environment variables
database:
  host: localhost
  port: 6432  # PgBouncer default port
  database: sim_sekolah
  user: sim_sekolah_user
  password: your_password
  max_open_conns: 50  # Reduced from 100
  max_idle_conns: 10
```

#### 6. Verify Connection
```bash
# Test PgBouncer connection
psql -h localhost -p 6432 -U sim_sekolah_user -d sim_sekolah

# Check PgBouncer stats
psql -h localhost -p 6432 -U pgbouncer -d pgbouncer
SHOW STATS;
```

### Zero-Downtime Deployment Strategy
1. Deploy PgBouncer alongside direct connections
2. Configure application to use both connection pools
3. Gradually shift traffic from direct connections to PgBouncer
4. Monitor connection counts and performance
5. Once stable, disable direct connections

### Monitoring
- Monitor `pgbouncer` stats: `SHOW STATS;`
- Monitor connection pool utilization
- Set up alerts for pool exhaustion
- Track connection wait times

---

## 🚧 TSK-07: Evaluate UUID Migration Strategy (Priority: LOW)

**Status:** Not Started - Architecture Task

**Description:** Evaluate UUID v7 or sequential UUIDs for high-insert tables and plan migration strategy.

### Analysis Required

#### Current State
- All tables use `uuid_generate_v4()` (random UUIDs)
- High-insert tables: trx_attendance, trx_assessment, trx_teaching_module
- Risk: Index fragmentation and poor cache locality

#### UUID v7 Benefits
- Time-ordered UUIDs
- Better cache locality
- Reduced index fragmentation
- Monotonically increasing for same-millisecond inserts
- Still UUID format (128-bit)

#### Implementation Options

**Option A: UUID v7 (Recommended)**
```sql
-- Install uuid-ossp extension
CREATE EXTENSION IF NOT EXISTS uuid_ossp;

-- Or use uuidv7 function if available
CREATE OR REPLACE FUNCTION uuid_generate_v7()
RETURNS UUID AS $$
SELECT encode(
    (
        (CURRENT_TIMESTAMPTZ::bigint)::bit(64) ||
        (random() * (2^52 - 1))::bigint::bit(52) ||
        (random() * (2^12 - 1))::bigint::bit(12)
    )::bigint, 
    'hex'
)::uuid;
$$ LANGUAGE SQL;
```

**Option B: Sequential UUIDs**
```sql
-- Use UUID v1 or custom sequential function
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
SELECT uuid_generate_v1();  -- Time-based but includes MAC address
```

**Option C: Keep UUID v4 with Monitoring**
- Current approach
- Monitor index fragmentation
- Implement periodic REINDEX if needed

### Migration Strategy
1. **Phase 1:** Add UUID v7 function to database
2. **Phase 2:** Test on non-production tables
3. **Phase 3:** Evaluate performance impact
4. **Phase 4:** Plan migration for existing data (complex)
5. **Phase 5:** Gradual migration or new table strategy

### Recommendation
- **Short-term:** Keep UUID v4 for stability
- **Medium-term:** Test UUID v7 on new tables
- **Long-term:** Consider migration if fragmentation becomes problematic

---

## 🚧 TSK-08: Implement Bloat Monitoring (Priority: LOW)

**Status:** Not Started - Operations Task

**Description:** Set up pg_stat_statements monitoring and monthly bloat reports.

### Implementation Steps

#### 1. Enable pg_stat_statements Extension
```sql
-- postgresql.conf
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.track = all
pg_stat_statements.max = 10000

-- Restart PostgreSQL
sudo systemctl restart postgresql

-- Create extension
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

#### 2. Create Bloat Monitoring View
```sql
CREATE OR REPLACE VIEW pg_bloat_summary AS
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) AS table_size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) AS indexes_size,
    pg_stat_get_dead_tuples(c.oid) AS dead_tuples,
    pg_stat_get_live_tuples(c.oid) AS live_tuples,
    round(100.0 * pg_stat_get_dead_tuples(c.oid) / (pg_stat_get_dead_tuples(c.oid) + pg_stat_get_live_tuples(c.oid)), 2) AS dead_tuple_ratio
FROM
    pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE
    c.relkind = 'r'
    AND n.nspname NOT IN ('pg_catalog', 'information_schema');
```

#### 3. Create Bloat Report Function
```sql
CREATE OR REPLACE FUNCTION generate_bloat_report()
RETURNS TABLE (
    tablename TEXT,
    total_size TEXT,
    dead_tuples BIGINT,
    live_tuples BIGINT,
    dead_tuple_ratio NUMERIC,
    recommendation TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        b.tablename,
        b.total_size,
        b.dead_tuples,
        b.live_tuples,
        b.dead_tuple_ratio,
        CASE
            WHEN b.dead_tuple_ratio > 20 THEN 'HIGH: Consider VACUUM FULL or pg_repack'
            WHEN b.dead_tuple_ratio > 10 THEN 'MEDIUM: Monitor autovacuum effectiveness'
            WHEN b.dead_tuple_ratio > 5 THEN 'LOW: Normal range'
            ELSE 'OK: No action needed'
        END AS recommendation
    FROM pg_bloat_summary b
    WHERE b.dead_tuple_ratio > 5
    ORDER BY b.dead_tuple_ratio DESC;
END;
$$ LANGUAGE plpgsql;
```

#### 4. Set Up Monthly Reporting
```bash
# Create cron job for monthly bloat reports
crontab -e

# Add: Run on 1st of every month at 2 AM
0 2 1 * * psql -U postgres -d sim_sekolah -c "SELECT * FROM generate_bloat_report();" > /var/log/postgresql/bloat_report_$(date +\%Y\%m).txt
```

#### 5. Monitoring Dashboard Setup
- Use Grafana + Prometheus for visualization
- Create dashboard for:
  - Dead tuple ratio
  - Autovacuum frequency
  - Table/index sizes
  - Query performance (via pg_stat_statements)

### Alert Thresholds
- **CRITICAL:** dead_tuple_ratio > 20%
- **WARNING:** dead_tuple_ratio > 10%
- **INFO:** dead_tuple_ratio > 5%

---

## 🚧 TSK-09: Enable Query Performance Monitoring (Priority: LOW)

**Status:** Not Started - Operations Task

**Description:** Enable pg_stat_statements extension and slow query logging. Implement EXPLAIN ANALYZE for critical queries.

### Implementation Steps

#### 1. Configure Slow Query Logging
```ini
# postgresql.conf
log_min_duration_statement = 1000  # Log queries > 1 second
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '
log_duration = on
log_statement = 'none'  # Don't log statement text, just duration
```

#### 2. Enable pg_stat_statements
```sql
-- Already enabled in TSK-08, but verify:
SELECT * FROM pg_extension WHERE extname = 'pg_stat_statements';

-- Check top queries by total time
SELECT
    query,
    calls,
    total_time,
    mean_time,
    stddev_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;

-- Check top queries by calls
SELECT
    query,
    calls,
    total_time,
    mean_time
FROM pg_stat_statements
ORDER BY calls DESC
LIMIT 10;
```

#### 3. Create Performance Monitoring View
```sql
CREATE OR REPLACE VIEW query_performance_summary AS
SELECT
    pg_database.datname AS database_name,
    pg_stat_statements.calls AS total_calls,
    pg_stat_statements.total_time / 1000 AS total_time_seconds,
    pg_stat_statements.mean_time / 1000 AS mean_time_seconds,
    pg_stat_statements.stddev_time / 1000 AS stddev_time_seconds,
    pg_stat_statements.rows AS total_rows,
    pg_stat_statements.query
FROM
    pg_stat_statements
    JOIN pg_database ON pg_database.oid = pg_stat_statements.dbid
WHERE
    pg_stat_statements.calls > 100  -- Ignore frequently executed one-off queries
ORDER BY
    pg_stat_statements.total_time DESC;
```

#### 4. Implement EXPLAIN ANALYZE for Critical Queries
Create a testing script for critical paths:

```bash
#!/bin/bash
# test_query_performance.sh

# Test authentication query
psql -U postgres -d sim_sekolah -c "EXPLAIN ANALYZE SELECT * FROM auth_user WHERE email = 'test@example.com';"

# Test attendance query
psql -U postgres -d sim_sekolah -c "EXPLAIN ANALYZE SELECT * FROM trx_attendance WHERE student_id = 'uuid' AND date >= CURRENT_DATE - INTERVAL '7 days';"

# Test assessment query
psql -U postgres -d sim_sekolah -c "EXPLAIN ANALYZE SELECT * FROM trx_assessment WHERE classroom_id = 'uuid' ORDER BY created_at DESC LIMIT 10;"
```

#### 5. Set Up Performance Alerts
Monitor and alert on:
- Mean query time > 500ms for frequently executed queries
- Total time increase > 50% week-over-week
- New queries appearing in top 10 slow queries
- Sequential scan on large tables

---

## 🚧 TSK-10: Physical Schema Validation (Priority: HIGH)

**Status:** Not Started - Validation Task

**Description:** Perform manual schema comparison between migration scripts and physical database to identify drift.

### Implementation Steps

#### 1. Generate Physical Schema Dump
```bash
# Dump current database schema
pg_dump -U postgres -d sim_sekolah --schema-only --no-owner --no-privileges > physical_schema.sql

# Or use pg_dump with specific format
pg_dump -U postgres -d sim_sekolah --schema-only --file=physical_schema_dump.sql
```

#### 2. Compare with Migration Scripts
```bash
# Create expected schema from migrations
# (This requires running all migrations on a fresh database)

# Compare schemas
diff -u expected_schema.sql physical_schema.sql > schema_drift_report.txt
```

#### 3. Use Schema Comparison Tools
```bash
# Install schemacrawler (or similar tool)
wget https://github.com/schemacrawler/SchemaCrawler/releases/download/v16.20.1/schemacrawler-16.20.1-distribution.zip

# Generate schema diagrams and differences
schemacrawler.sh -c config.properties -command schema -outputformat svg -outputfile schema_diagram.svg
```

#### 4. Manual Validation Checklist
- [ ] All tables in migrations exist in physical database
- [ ] All columns match between migrations and physical database
- [ ] All foreign keys exist and are valid
- [ ] All indexes are present
- [ ] All constraints are present
- [ ] No orphaned tables/columns in physical database
- [ ] Data types match exactly
- [ ] Default values match
- [ ] NOT NULL constraints match

#### 5. Create Validation Report
```sql
-- Missing tables in physical database
SELECT m.table_name
FROM (
    -- Extract table names from migration scripts
    -- This requires parsing migration files
) m
WHERE NOT EXISTS (
    SELECT 1 FROM information_schema.tables t 
    WHERE t.table_name = m.table_name
);

-- Extra tables in physical database
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
AND table_name NOT IN (
    -- Extract table names from migration scripts
);
```

#### 6. Remediation Plan
If schema drift is detected:
1. Document differences
2. Determine root cause (manual changes, failed migrations, etc.)
3. Create remediation migration
4. Test on non-production
5. Apply to production

### Recommended Schedule
- **Pre-production:** Complete validation before first production deployment
- **Post-deployment:** Run validation after major migrations
- **Quarterly:** Regular validation to catch accidental changes

---

## Migration Deployment Procedure

### Pre-Deployment Checklist
- [ ] Review migration 000013 content
- [ ] Test on staging environment
- [ ] Verify no conflicts with existing indexes
- [ ] Ensure sufficient disk space for index creation
- [ ] Notify stakeholders of deployment
- [ ] Schedule maintenance window (optional, CONCURRENTLY should be safe)

### Deployment Steps
```bash
# 1. Backup database
pg_dump -U postgres -d sim_sekolah -F c -f backup_before_000013.dump

# 2. Run migration
psql -U postgres -d sim_sekolah -f backend/migrations/000013_dba_performance_optimizations.up.sql

# 3. Monitor index creation
# In another terminal:
psql -U postgres -d sim_sekolah
SELECT * FROM pg_stat_progress_create_index;

# 4. Verify index creation
SELECT indexname, indexdef 
FROM pg_indexes 
WHERE indexname LIKE '%_active_soft_delete' 
   OR indexname LIKE '%_gin' 
   OR indexname LIKE '%_lower' 
   OR indexname LIKE '%_brin';

# 5. Verify autovacuum settings
SELECT relname, autovacuum_vacuum_scale_factor, autovacuum_analyze_scale_factor, fillfactor
FROM pg_class
JOIN pg_namespace ON pg_namespace.oid = pg_class.relnamespace
WHERE relname IN ('auth_user', 'master_student', 'trx_attendance');

# 6. Run performance tests
# (Use existing test suite or manual queries)
```

### Post-Deployment Verification
- [ ] All indexes created successfully
- [ ] Autovacuum parameters updated
- [ ] No error messages in PostgreSQL logs
- [ ] Application performance baseline established
- [ ] Query performance tests pass
- [ ] Monitor dead tuple accumulation over next week

### Rollback Procedure
If issues arise:
```bash
# Run down migration
psql -U postgres -d sim_sekolah -f backend/migrations/000013_dba_performance_optimizations.down.sql

# Restore from backup if needed
pg_restore -U postgres -d sim_sekolah -c backup_before_000013.dump
```

---

## Monitoring and Maintenance

### Ongoing Monitoring
- **Index Usage:** Monitor index usage statistics
- **Dead Tuples:** Track dead tuple ratios weekly
- **Autovacuum:** Monitor autovacuum frequency and duration
- **Query Performance:** Track slow queries and execution times
- **Connection Pool:** Monitor PgBouncer pool utilization (when deployed)

### Monthly Maintenance
- Review bloat reports
- Check index fragmentation
- Analyze slow query logs
- Review autovacuum effectiveness
- Update performance baselines

### Quarterly Maintenance
- Consider REINDEX for fragmented indexes
- Review and adjust autovacuum parameters
- Evaluate UUID migration strategy
- Comprehensive performance review

---

## Summary

**Completed (Migration 000013):**
- ✅ Partial indexes for soft deletes (48 tables)
- ✅ Autovacuum tuning (7 tables)
- ✅ GIN indexes for JSONB (8 columns)
- ✅ Expression indexes for case-insensitive search (4 indexes)
- ✅ BRIN indexes for time-series data (23 tables)

**Remaining (Infrastructure/Operations):**
- 🚧 PgBouncer deployment (TSK-01)
- 🚧 UUID migration strategy evaluation (TSK-07)
- 🚧 Bloat monitoring setup (TSK-08)
- 🚧 Query performance monitoring (TSK-09)
- 🚧 Physical schema validation (TSK-10)

**Next Steps:**
1. Deploy migration 000013 to staging
2. Test and validate performance improvements
3. Deploy to production with monitoring
4. Implement remaining infrastructure/operations tasks
5. Establish ongoing monitoring and maintenance procedures

---

**Contact:** Database Team
**Last Updated:** 2026-05-28
**Document Version:** 1.0