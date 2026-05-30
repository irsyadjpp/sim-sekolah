# Database Review Document: SIM Sekolah Backend

**Document Information**
* **Review Date:** 2026-05-28
* **Reviewer:** Irsyad Jamal Pratama Putra
* **Target System/Module:** SIM Sekolah Backend
* **Schema Version:** Migration Scripts (000001-000012)
* **Status:** APPROVED WITH COMMENTS

---

## 1. Executive DBA Summary

The SIM Sekolah backend database demonstrates a solid foundation with proper PostgreSQL practices including UUID primary keys, soft-delete patterns, and comprehensive audit trails. The migration scripts are well-structured and follow a logical progression from authentication to transaction domains. However, several critical PostgreSQL optimization opportunities exist that could significantly impact production performance and scalability.

**MCP Sync Status:** Unable to perform physical database validation due to MCP PostgreSQL server transport errors. Review is based on migration scripts and Go ORM models only. Physical schema drift validation could not be completed.

**Production Readiness Assessment:** The database design is production-ready for small to medium-scale deployments but requires optimization for high-traffic scenarios (1000+ concurrent users). Connection pooling, indexing strategy, and MVCC health management need attention before large-scale production deployment.

---

## 2. Critical PostgreSQL Red Flags (Blockers)

* **🚨 Missing Connection Pooler:** No PgBouncer or Pgpool-II configured. Direct database connections with MaxOpenConns=100 may cause connection exhaustion under high traffic. This is a critical scalability risk.
* **🚨 Soft Delete Without Partial Index:** The `deleted_at` soft-delete pattern is used extensively (via GORM's DeletedAt) but lacks partial indexes on `WHERE deleted_at IS NULL`. This will cause full table scans on active record queries as deleted rows accumulate.
* **🚨 UUID v4 Fragmentation Risk:** Heavy insert tables using `uuid_generate_v4()` may experience index fragmentation and poor cache locality. Consider UUID v7 or sequential UUIDs for high-throughput tables.
* **🚨 No Autovacuum Tuning:** No evidence of autovacuum configuration tuning in the migration scripts or configuration. Default settings may be insufficient for tables with heavy UPDATE/DELETE workloads.

---

## 3. Detailed Findings (Schema, MVCC, Indexing)

### 3.1. Architecture & Table Structure

**Strengths:**
- **Primary Keys:** All tables use UUID primary keys with proper `uuid_generate_v4()` defaults
- **Foreign Keys:** Comprehensive foreign key relationships defined in Go models and migration scripts
- **Naming Conventions:** Consistent snake_case naming for all database objects
- **Audit Trail:** Excellent `Auditable` base struct with `created_at`, `updated_at`, `deleted_at`, `created_by`, `updated_by`, `deleted_by`
- **Data Types:** Appropriate use of PostgreSQL-specific types (UUID, TIMESTAMPTZ, JSONB, NUMERIC)

**Concerns:**
- **UUID Strategy:** Using `uuid_generate_v4()` for all tables. For high-insert tables (e.g., `trx_attendance`, `trx_assessment`), consider UUID v7 or sequential UUIDs to reduce index fragmentation
- **JSONB Usage:** JSONB is used appropriately for semi-structured data (e.g., medical history in student records), but ensure GIN indexes are created for JSONB query patterns
- **Soft Delete Pattern:** GORM's `DeletedAt` pattern is used but lacks partial indexes for active records optimization

**Schema Drift Risk:** Unable to validate due to MCP connection issues. Recommend manual schema comparison before production deployment.

### 3.2. MVCC & Bloat Health

**Current State:**
- **Autovacuum:** No custom autovacuum configuration detected in migration scripts. Relying on PostgreSQL defaults.
- **Dead Tuples Risk:** High. The soft-delete pattern with `deleted_at` will cause massive dead tuple accumulation without proper cleanup strategy.
- **Fillfactor:** No fillfactor tuning detected. Default fillfactor (100) may cause page splits on tables with heavy UPDATE workloads.
- **Bloat Strategy:** No evidence of `pg_repack` or periodic REINDEX strategy in the codebase.

**Recommendations:**
- Implement autovacuum tuning for tables with high UPDATE/DELETE rates
- Lower fillfactor to 90-95 for tables with frequent UPDATEs (e.g., `auth_user`, `master_student`)
- Establish monthly bloat monitoring and REINDEX strategy
- Consider `pg_repack` for production maintenance windows

### 3.3. Performance & Indexing

**B-Tree Indexes:**
- **Foreign Keys:** Most foreign keys have corresponding indexes (good practice)
- **Unique Constraints:** Proper unique indexes on email, username, NISN, NIK
- **Composite Indexes:** Some composite indexes exist but could be expanded for common query patterns

**GIN Indexes:**
- **Full-Text Search:** GIN indexes created for `trx_question_bank.question`, `trx_project_module.title`, `master_school.school_name` (excellent)
- **JSONB:** No GIN indexes detected for JSONB columns. If JSONB queries exist, GIN indexes are required

**Partial Indexes:**
- **Critical Gap:** No partial indexes on `WHERE deleted_at IS NULL` for soft-delete tables. This is a major performance risk.
- **Active Records:** Partial index on `auth_user` for `WHERE is_enabled = true AND account_non_locked = true` exists (good)

**Expression Indexes:**
- **Case-Insensitive Search:** No expression indexes on `lower(email)` or `lower(username)` for case-insensitive lookups

**BRIN Indexes:**
- **Time-Series:** No BRIN indexes detected. Consider BRIN for append-only tables like `trx_attendance`, `sys_server_telemetry`, `audit_logs`

**Index Issues Found:**
- Migration 000008 had 6 index creation errors that were fixed by commenting out problematic indexes
- Missing indexes on `dl_design_element.element_name` (column doesn't exist)
- Missing indexes on `master_student.current_classroom_id` and `is_active` (columns don't exist)

---

## 4. Recommendations & Action Plan

### 4.1. Immediate Actions (Before Production)

1. **Implement PgBouncer Connection Pooler**
   - Deploy PgBouncer in transaction pooling mode
   - Configure max connections to 200-500
   - Update application to connect via PgBouncer
   - **Zero-downtime strategy:** Deploy PgBouncer alongside direct connections, then gradually migrate

2. **Add Partial Indexes for Soft Deletes**
   - Create partial indexes on all tables with `deleted_at`: `CREATE INDEX CONCURRENTLY idx_table_active ON table(id) WHERE deleted_at IS NULL`
   - This is safe to run in production with `CONCURRENTLY`

3. **Tune Autovacuum Parameters**
   - Set `autovacuum_vacuum_scale_factor = 0.1` for high-traffic tables
   - Set `autovacuum_analyze_scale_factor = 0.05` for better statistics
   - Monitor dead tuple accumulation

### 4.2. Short-term Optimizations (1-2 weeks)

4. **Add GIN Indexes for JSONB**
   - Identify JSONB query patterns in the codebase
   - Create GIN indexes: `CREATE INDEX CONCURRENTLY idx_table_jsonb ON table USING gin(jsonb_column)`

5. **Implement Expression Indexes**
   - Add `lower(email)` and `lower(username)` indexes for case-insensitive authentication
   - `CREATE INDEX CONCURRENTLY idx_auth_user_email_lower ON auth_user(lower(email))`

6. **Add BRIN Indexes for Time-Series**
   - For `trx_attendance`, `sys_server_telemetry`: `CREATE INDEX CONCURRENTLY idx_table_created_brin ON table USING brin(created_at)`

### 4.3. Long-term Strategy (1-3 months)

7. **UUID Migration Strategy**
   - Evaluate UUID v7 or sequential UUIDs for high-insert tables
   - Plan migration strategy for existing data
   - Consider `pgcrypto` or custom UUID generation functions

8. **Bloat Monitoring & Maintenance**
   - Implement `pg_stat_statements` monitoring
   - Set up monthly bloat reports
   - Schedule quarterly `pg_repack` during maintenance windows

9. **Query Performance Monitoring**
   - Enable `pg_stat_statements` extension
   - Set up slow query logging (> 1 second)
   - Implement EXPLAIN ANALYZE for critical queries

---

## 5. Task Breakdown (Jira/Linear Format)

| Task ID | Type | Priority | Title | Description | Acceptance Criteria |
|---|---|---|---|---|---|
| TSK-01 | Infra | High | Deploy PgBouncer Connection Pooler | Deploy PgBouncer in transaction pooling mode with 200-500 max connections. Update application configuration to connect via PgBouncer. | PgBouncer deployed and running, application successfully connecting via pooler, connection count monitoring shows reduced direct connections |
| TSK-02 | Perf | High | Add Partial Indexes for Soft Deletes | Create partial indexes on all tables with deleted_at column using CONCURRENTLY to avoid locks. | All partial indexes created successfully, query performance tests show improvement for active record queries |
| TSK-03 | Perf | High | Tune Autovacuum Parameters | Configure autovacuum_vacuum_scale_factor and autovacuum_analyze_scale_factor for high-traffic tables. | Autovacuum configuration updated, dead tuple accumulation reduced, monitoring shows improved vacuum performance |
| TSK-04 | Perf | Medium | Add GIN Indexes for JSONB | Identify JSONB query patterns and create appropriate GIN indexes. | JSONB query patterns identified, GIN indexes created, JSONB query performance improved |
| TSK-05 | Perf | Medium | Implement Expression Indexes | Add lower(email) and lower(username) indexes for case-insensitive authentication. | Expression indexes created, authentication queries use case-insensitive lookups efficiently |
| TSK-06 | Perf | Medium | Add BRIN Indexes for Time-Series | Create BRIN indexes for append-only tables like trx_attendance and sys_server_telemetry. | BRIN indexes created, time-series query performance improved, index size reduced compared to B-Tree |
| TSK-07 | Arch | Low | Evaluate UUID Migration Strategy | Evaluate UUID v7 or sequential UUIDs for high-insert tables and plan migration strategy. | UUID strategy evaluation complete, migration plan documented, risk assessment completed |
| TSK-08 | Ops | Low | Implement Bloat Monitoring | Set up pg_stat_statements monitoring and monthly bloat reports. | Monitoring dashboard configured, monthly bloat reports automated, alert thresholds defined |
| TSK-09 | Ops | Low | Enable Query Performance Monitoring | Enable pg_stat_statements extension and slow query logging. Implement EXPLAIN ANALYZE for critical queries. | pg_stat_statements enabled, slow query logging configured, critical query performance baseline established |
| TSK-10 | Validation | High | Physical Schema Validation | Perform manual schema comparison between migration scripts and physical database to identify drift. | Schema comparison report generated, any drift documented and remediated |

---

## 6. Final Approval Decision

**Decision:** APPROVED WITH COMMENTS

**Reasoning:** The database architecture demonstrates solid PostgreSQL fundamentals with proper primary keys, foreign keys, audit trails, and naming conventions. The migration scripts are comprehensive and well-structured. However, critical performance and scalability issues must be addressed before production deployment:

1. **Connection Pooling (BLOCKER):** PgBouncer deployment is mandatory for production scalability
2. **Partial Indexes (HIGH):** Soft-delete optimization is required for acceptable query performance
3. **Autovacuum Tuning (HIGH):** MVCC health management is critical for long-term stability
4. **Index Strategy (MEDIUM):** GIN, BRIN, and expression indexes will significantly improve performance

The database is approved for development and staging environments with the understanding that the HIGH priority tasks must be completed before production deployment. The MCP sync validation could not be completed due to technical issues, so manual schema validation is strongly recommended.
