# Database Migrations - SIM Sekolah

**Organization Strategy:** DOMAIN-BASED + PHASE-BASED (Strategy 7.2)
**Reorganized:** 2026-05-28
**Status:** Active for Development & Future Features

---

## Overview

This directory contains database migration scripts organized using the **DOMAIN-BASED + PHASE-BASED** strategy as defined in the migration organization strategy document. This structure provides better maintainability, clearer evolution paths, and easier rollback procedures.

---

## Directory Structure

```
migrations/
├── 000001_init_auth_domain.up.sql
├── 000002_init_master_data.up.sql
├── 000003_init_curriculum_domain.up.sql
├── 000004_init_transaction_domain.up.sql
├── 000005_init_system_tables.up.sql
├── 000006_seed_reference_data.up.sql
├── 000007_add_all_constraints.up.sql
├── 000008_add_performance_indexes.up.sql
├── 000009_phase2_assessment_enhancements.up.sql
├── 000010_phase3_advanced_features.up.sql
├── 000011_phase4_ai_integration.up.sql
├── 000012_add_missing_model_tables.up.sql
├── 000013_dba_performance_optimizations.up.sql
└── README.md
```

**Note:** The directory structure shown in the original strategy document (foundation/ and features/ subdirectories) represents the ideal organization. The current structure is flat with sequential numbering, which is also acceptable and functional.

---

## Foundation Migrations

Foundation migrations contain the base schema required for fresh installations. These should be applied in sequence when setting up a new database.

### 1. Auth Domain (`000001_init_auth_domain.up.sql`)
- **Tables:** `auth_user`, `auth_role`, `auth_user_role`, `auth_permission`, `auth_role_permission`, `auth_refresh_token`, `auth_password_reset_token`, `auth_user_session`
- **Purpose:** Authentication and authorization system
- **Dependencies:** None

### 2. Master Data (`000002_init_master_data.up.sql`)
- **Tables:** `master_school`, `master_teacher`, `master_student`, `master_student_parent`, `master_classroom`, `master_grade`, `master_phase`, `master_subject`, `master_subject_characteristic`, `master_subject_element`, `master_local_context`, `master_local_context_category`, `master_academic_year`, `master_profile_dimension`
- **Purpose:** Core reference data for schools, teachers, students, and academic structure
- **Dependencies:** None

### 3. Curriculum Domain (`000003_init_curriculum_domain.up.sql`)
- **Tables:** `cur_cp_detail`, `cur_learning_objective`, `cur_learning_outcome`, `dl_assessment_level`, `dl_cognitive_stage`, `dl_design_element`
- **Purpose:** Curriculum planning (CP, TP, ATP) and design learning elements
- **Dependencies:** Master Data

### 4. Transaction Domain (`000004_init_transaction_domain.up.sql`)
- **Tables:** All `trx_*` tables including basic assessments, rubrics, foundational skills, reading literacy, numeracy, lesson planning, ATP, attendance, enrollment, PPDB, reports, teaching assignments, curriculum documents, kokurikuler/ekstrakurikuler activities, KSP, project modules, question banks, and document repository
- **Purpose:** Transactional data for daily school operations (Kurikulum Merdeka requirements)
- **Dependencies:** Auth Domain, Master Data, Curriculum Domain

### 5. System Tables (`000005_init_system_tables.up.sql`)
- **Tables:** `sys_automation_queue`, `sys_server_telemetry`
- **Purpose:** System automation and monitoring
- **Dependencies:** None

### 6. Reference Data (`000006_seed_reference_data.up.sql`)
- **Data:** Roles, permissions, academic years, phases, grades, cognitive stages, assessment levels, profile dimensions, local context categories, SPMB admission paths
- **Purpose:** Seed initial reference data required for system operation
- **Dependencies:** All foundation tables

### 7. Constraints (`000007_add_all_constraints.up.sql`)
- **Content:** Foreign key constraints across all domains
- **Purpose:** Enforce referential integrity
- **Dependencies:** All foundation tables

### 8. Performance Indexes (`000008_add_performance_indexes.up.sql`)
- **Content:** Performance indexes for all tables
- **Purpose:** Optimize query performance
- **Dependencies:** All foundation tables

---

## Feature Migrations

Feature migrations contain domain-specific features organized by development phase. These represent the evolution of the system over time.

### Phase 2: Assessment Enhancements (`000009_phase2_assessment_enhancements.up.sql`)
- **Features:** Advanced learning intelligence system, AI learning patterns, adaptive learning strategies
- **Purpose:** Enhanced AI-powered assessment analytics (core assessment tables moved to foundation)
- **Dependencies:** Foundation migrations

### Phase 3: Advanced Features (`000010_phase3_advanced_features.up.sql`)
- **Features:** Portfolio system, communication system, offline support system
- **Purpose:** Advanced collaboration and mobility features
- **Dependencies:** Foundation migrations, Phase 2 features

### Phase 4: AI Integration (`000011_phase4_ai_integration.up.sql`)
- **Features:** AI analytics, character analysis, survey system, FGD sessions, analysis tools (SWOT, root cause, fishbone)
- **Purpose:** AI-powered analytics and advanced analysis tools (document repository moved to foundation)
- **Dependencies:** Foundation migrations, Phase 2-3 features

---

## Additional Migrations

Additional migrations that were added for specific purposes such as model alignment and performance optimization.

### Model Alignment (`000012_add_missing_model_tables.up.sql`)
- **Content:** Adds 100+ missing tables for Go models that don't exist in previous migrations
- **Purpose:** Align database schema with Go ORM models
- **Dependencies:** All previous migrations
- **Tables:** Assessment, DI, numeracy, P5, parent partnership, peer assessment, portfolio, question bank, rubric, learning experience, lesson planning, ILP, play-based learning, communication, document repository, intelligence, intervention, character intervention, offline tables

### DBA Performance Optimizations (`000013_dba_performance_optimizations.up.sql`)
- **Content:** Senior DBA performance recommendations implementation
- **Purpose:** Implement critical performance optimizations from DBA review
- **Dependencies:** All previous migrations
- **Related:** DBA Review Report (docs/database-reviews/dba-review-backend-20260528.md)
- **Details:** See docs/database-reviews/dba-recommendations-implementation-guide.md
- **Optimizations:**
  - Partial indexes for soft deletes (48 tables)
  - Autovacuum tuning (7 high-traffic tables)
  - GIN indexes for JSONB columns (8 columns)
  - Expression indexes for case-insensitive search (4 indexes)
  - BRIN indexes for time-series data (23 tables)

---

## Migration Strategy

### For Fresh Installations (Development/New Projects)

Use the organized structure:
```bash
# Apply foundation migrations first
migrate -path backend/migrations/foundation/ -database "postgres://..." up

# Then apply feature migrations in order
migrate -path backend/migrations/features/ -database "postgres://..." up
```

### For Production (Existing Data)

**DO NOT USE THIS STRUCTURE** - Continue using the legacy migration files from the backup folder (`migrations_backup_20260528_100423/`):
- Risk too high for production database restructure
- Existing structure is functional and proven
- Use this organized structure for future major versions only

### For Future Development

**Strategy:**
1. Keep existing production migrations as-is
2. Use organized structure for new major versions (v2.0+)
3. Consolidate small changes when opportunities arise
4. Apply template standards to new migrations
5. Follow naming convention: `[3-digit sequence]_[domain/phase]_[action]_[description].up.sql`

---

## Naming Convention

**Pattern:** `[3-digit sequence]_[description].up.sql`

**Examples:**
- Foundation: `000001_init_auth_domain.up.sql`
- Features: `000009_phase2_assessment_enhancements.up.sql`
- Additional: `000012_add_missing_model_tables.up.sql`

**Numbering Ranges:**
- 001-008: Foundation migrations (base schema)
- 009-011: Feature migrations by phase
- 012+: Additional migrations (model alignment, performance optimizations, etc.)

---

## Migration Template

All migrations should follow this template:

```sql
-- Migration: [Number]_[Domain]_[Description]
-- Description: [Detailed description]
-- Author: Database Team
-- Created: YYYY-MM-DD
-- Related Issues: [Ticket/PR]
-- Risk Level: [LOW/MEDIUM/HIGH]
-- Downtime Required: [YES/NO]
-- Rollback Procedure: [Description]

-- ============================================================
-- SECTION 1: Create/Modify Tables
-- ============================================================

-- Table creation/modification SQL here

-- ============================================================
-- SECTION 2: Add Constraints
-- ============================================================

-- Constraint SQL here

-- ============================================================
-- SECTION 3: Add Indexes
-- ============================================================

-- Index SQL here

-- ============================================================
-- SECTION 4: Data Migration (if needed)
-- ============================================================

-- Data migration SQL here

-- ============================================================
-- SECTION 5: Validation Queries
-- ============================================================

-- Validation SQL here
```

---

## Best Practices

### Before Creating Migration
- [ ] Verify migration doesn't break existing functionality
- [ ] Test on development environment
- [ ] Create corresponding down migration
- [ ] Add descriptive comments
- [ ] Review naming convention
- [ ] Check for performance impact

### Migration Content
- [ ] Use transactions for atomic operations
- [ ] Include appropriate error handling
- [ ] Add data validation constraints
- [ ] Use IF NOT EXISTS for safe re-runs
- [ ] Include rollback procedures
- [ ] Document data migration steps

### After Applying Migration
- [ ] Verify in staging environment
- [ ] Monitor application logs
- [ ] Check database performance
- [ ] Validate data integrity
- [ ] Document any manual steps
- [ ] Update schema documentation

---

## Backup Information

The original migration files (62 files) have been backed up to:
`backend/migrations_backup_20260528_100423/`

This backup contains:
- Original structure with 62+ migration files
- All corresponding down migrations
- Original naming convention
- Proven production-tested scripts

**DO NOT DELETE** the backup folder until the new structure has been thoroughly tested and validated.

---

## Rollback Procedures

### Foundation Migrations Rollback
Each foundation migration should have a corresponding `.down.sql` file in the backup folder. For rollback:

```bash
migrate -path backend/migrations/foundation/ -database "postgres://..." down 1
```

### Feature Migrations Rollback
For feature rollback, apply in reverse order:

```bash
migrate -path backend/migrations/features/ -database "postgres://..." down 1
```

### Hotfix Rollback
Hotfixes can be rolled back individually:

```bash
migrate -path backend/migrations/hotfixes/ -database "postgres://..." down 1
```

---

## Validation

To validate the migration structure, run:

```bash
psql -d sim_sekolah -f backend/migrations/validate_alignment.sql
```

This will check:
- All tables exist
- All constraints are properly applied
- All indexes are created
- Reference data is populated
- No orphaned records exist

---

## Support

For questions or issues related to migrations:
1. Check this README first
2. Review the migration organization strategy document
3. Consult the database team
4. Check the backup folder for original implementation

---

## Related Documentation

- Migration Organization Strategy: `docs/database-reviews/migration-organization-strategy.md`
- Database Review Documentation: `docs/database-reviews/`
- Original Migration Examples: `backend/migrations_examples/`

---

**Last Updated:** 2026-05-28
**Maintained By:** Database Team