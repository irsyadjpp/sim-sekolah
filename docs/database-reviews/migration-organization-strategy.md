# Strategi Pembagian Database Migration Scripts

**Document Information**
* **Created:** 2026-05-28
* **Author:** Irsyad Jamal Pratama Putra (Senior PostgreSQL DBA)
* **Current State:** 62 migration files (highly fragmented)
* **Target State:** Organized, maintainable migration structure

---

## 1. Analisis Struktur Migration Saat Ini

### Current Structure
```
backend/migrations/
├── 000001_init_schema.up.sql (34KB - 43 tabel dasar)
├── 000002_seed_master_data.up.sql (8KB)
├── 000003_seed_auth.up.sql (738B)
├── 000004_add_context_extensions.up.sql (6KB)
├── 000005_seed_context_extensions.up.sql (8KB)
├── 000006_add_curriculum.up.sql (3KB)
├── 000007_add_schedule_and_daily_attendance.up.sql (1.5KB)
├── ... (60+ additional migration files)
├── 000090_phase4_advanced_features.up.sql
├── 000091_fix_backend_alignment_critical.up.sql (BARU)
└── 000092_fix_backend_alignment_standardization.up.sql (BARU)
```

### Current Issues
1. **Over-fragmentation:** 60+ files untuk sistem yang sebenarnya bisa konsolidasi
2. **Inconsistent granularity:** Beberapa file 1 baris, beberapa 34KB
3. **Difficult rollback:** Terlalu banyak file untuk di-rollback secara efektif
4. **Deployment complexity:** 60+ migrations = lebih lama dan lebih kompleks
5. **Maintenance difficulty:** Sulit melacak evolution dari satu fitur

---

## 2. Pendekatan Pembagian Migration Script (Best Practices)

### 2.1. Pendekatan A: Single Monolithic Migration
**Pola:** 1 file besar untuk semua CREATE TABLE, 1 file untuk semua ALTER TABLE

**Struktur:**
```
migrations/
├── 000001_create_all_tables.up.sql
├── 000001_create_all_tables.down.sql
├── 000002_add_all_constraints.up.sql
├── 000002_add_all_constraints.down.sql
├── 000003_seed_all_data.up.sql
├── 000003_seed_all_data.down.sql
└── 000004_create_all_indexes.up.sql
```

**Kelebihan:**
- ✅ Simple dan mudah di-maintain
- ✅ Deployment cepat (hanya 3-4 migrations)
- ✅ Mudah rollback
- ✅ Semua CREATE TABLE dalam satu file (vision lengkap)

**Kekurangan:**
- ❌ Tidak cocok untuk production yang sudah ada data
- ❌ Sulit untuk incremental update
- ❌ Tidak mendukung evolution gradual
- ❌ Risky untuk production deployment besar

**Cocok untuk:** Development environment baru, fresh installation

---

### 2.2. Pendekatan B: Feature-Based Migration
**Pola:** 1 migration per feature/domain

**Struktur:**
```
migrations/
├── 000001_init_core_schema.up.sql        # Auth, User, School dasar
├── 000002_init_curriculum.up.sql        # Semua curriculum tables
├── 000003_init_master_data.up.sql       # Semua master data
├── 000004_init_transactions.up.sql      # Semua transaction tables
├── 000005_init_assessment.up.sql        # Semua assessment tables
├── 000006_init_reporting.up.sql         # Semua reporting tables
├── 000007_seed_reference_data.up.sql    # Seed semua reference data
├── 000008_add_constraints.up.sql        # Semua FK constraints
├── 000009_add_performance_indexes.up.sql # Semua indexes
└── 000010_add_optimizations.up.sql      # Autovacuum, dll
```

**Kelebihan:**
- ✅ Logical grouping by domain
- ✅ Moderate jumlah migrations (~10)
- ✅ Evolution yang terstruktur
- ✅ Mudah rollback per domain
- ✅ Cocok untuk incremental development

**Kekurangan:**
- ⚠️ Masih cukup banyak file
- ⚠️ Perlu planning yang baik
- ⚠️ Dependency management antar features

**Cocok untuk:** Sistem yang sedang berkembang, environment dengan data existing

---

### 2.3. Pendekatan C: Phase-Based Migration
**Pola:** 1 migration per development phase/release

**Struktur:**
```
migrations/
├── 000001_phase1_core_infrastructure.up.sql    # Auth, master data dasar
├── 000002_phase1_curriculum_basic.up.sql       # Curriculum tables
├── 000003_phase2_assessment_system.up.sql     # Assessment features
├── 000004_phase2_advanced_features.up.sql     # Advanced features
├── 000005_phase3_reporting_analytics.up.sql   # Reporting & analytics
├── 000006_phase3_ai_integration.up.sql        # AI features
├── 000007_phase4_optimization_security.up.sql # Performance & security
└── 000008_phase4_document_repository.up.sql  # Document system
```

**Kelebihan:**
- ✅ Sangat cocok untuk project-based development
- ✅ Jumlah migrations terkontrol (~8)
- ✅ Clear evolution path
- ✅ Mudah planning per phase
- ✅ Cocok untuk multi-stage deployment

**Kekurangan:**
- ⚠️ Perlu strict phase discipline
- ⚠️ Cross-phase dependencies kompleks
- ⚠️ Tidak flexible untuk small changes

**Cocok untuk:** Proyek dengan clear development phases ( seperti SIM Sekolah Anda)

---

### 2.4. Pendekatan D: Domain-Based with Incremental Updates (RECOMMENDED)
**Pola:** Kombinasi domain-based dengan incremental updates

**Struktur:**
```
migrations/
├── 000001_init_core_auth.up.sql           # Auth domain: user, role, permission
├── 000002_init_master_data.up.sql         # Master data: school, teacher, student
├── 000003_init_curriculum.up.sql          # Curriculum domain: CP, TP, ATP
├── 000004_init_assessment.up.sql          # Assessment domain
├── 000005_init_transaction.up.sql         # Transaction domain
├── 000006_init_reporting_views.up.sql      # Views & reporting
├── 000007_seed_reference_data.up.sql      # Seed data
├── 000008_add_constraints_indexes.up.sql   # All FK + indexes
├── 000009_phase2_assessment_enhancements.up.sql  # Phase 2 updates
├── 000010_phase3_advanced_features.up.sql         # Phase 3 updates
├── 000011_phase4_ai_integration.up.sql            # Phase 4 updates
└── 000091_fix_alignment_critical.up.sql          # Hotfixes
```

**Kelebihan:**
- ✅ Balance antara granularity dan maintainability
- ✅ Domain grouping logical
- ✅ Support incremental evolution
- ✅ Moderate jumlah migrations (~12-15)
- ✅ Flexible untuk hotfixes

**Kekurangan:**
- ⚠️ Perlu consistent naming convention
- ⚠️ Cross-domain dependencies perlu management

**Cocok untuk:** Sistem seperti SIM Sekolah yang sudah kompleks dan akan terus berkembang

---

## 3. Rekomendasi untuk SIM Sekolah

### 3.1. Strategi Hybrid: Domain-Based + Phase-Based

**Alasan:** SIM Sekolah Anda memiliki clear domain separation dan development phases

**Struktur Rekomendasi:**

#### Foundation (Base Schema)
```
migrations/
├── 000001_init_auth_domain.up.sql       # Auth tables (5 tables)
├── 000002_init_master_data.up.sql       # Master tables (12 tables)
├── 000003_init_curriculum_domain.up.sql # Curriculum tables (3 tables)
├── 000004_init_transaction_domain.up.sql # Transaction tables (25 tables)
├── 000005_init_system_tables.up.sql     # System tables (2 tables)
```

#### Core Infrastructure
```
├── 000006_seed_reference_data.up.sql    # Seed semua reference data
├── 000007_add_constraints.up.sql        # Semua FK constraints
├── 000008_add_performance_indexes.up.sql # Semua indexes
```

#### Phase-Based Evolution
```
├── 000009_phase2_assessment_enhancements.up.sql  # Phase 2 features
├── 000010_phase3_advanced_features.up.sql         # Phase 3 features
├── 000011_phase4_ai_integration.up.sql            # Phase 4 AI features
├── 000012_phase4_document_repository.up.sql       # Phase 4 documents
```

#### Optimization & Fixes
```
├── 000020_performance_optimization.up.sql       # Autovacuum, tuning
├── 000021_security_enhancements.up.sql          # Security features
├── 000091_hotfix_backend_alignment.up.sql       # Hotfixes (separate numbering)
└── 000092_hotfix_constraint_enhancement.up.sql   # Hotfixes
```

### 3.2. Naming Convention Rekomendasi

**Pattern:** `[3-digit sequence]_[phase_or_domain]_[description].up.sql`

**Convention:**
- **Foundation:** `001_init_*` untuk initial schema
- **Core Infrastructure:** `006_seed_*`, `007_add_*` untuk infrastructure
- **Phase-Based:** `009_phase*_*` untuk feature phases
- **Hotfixes:** `091_hotfix_*` untuk production fixes (using 90+ range)
- **Rollbacks:** Every `.up.sql` must have corresponding `.down.sql`

---

## 4. Contoh Implementasi Restructuring

### 4.1. Konsolidasi Foundation Migrations

**Current:** 43 tabel ter分散 di multiple files
**Target:** 5 domain-based files

#### 000001_init_auth_domain.up.sql
```sql
-- Migration: Initialize Authentication Domain
-- Description: Create all authentication and authorization tables
-- Tables: auth_user, auth_role, auth_user_role, auth_permission, auth_role_permission,
--          auth_refresh_token, auth_password_reset_token, auth_user_session

-- CREATE TABLE statements untuk semua auth tables
-- Include PRIMARY KEY, default values, dan basic indexes
-- FK constraints ditambah di migration terpisah (000007)
```

#### 000002_init_master_data.up.sql
```sql
-- Migration: Initialize Master Data Domain
-- Description: Create all master/reference data tables
-- Tables: master_school, master_teacher, master_student, master_student_parent,
--          master_classroom, master_grade, master_phase, master_subject,
--          master_subject_characteristic, master_subject_element,
--          master_local_context, master_local_context_category,
--          master_academic_year, master_profile_dimension

-- CREATE TABLE statements untuk semua master tables
-- Include PRIMARY KEY, default values
-- FK constraints ditambah di migration terpisah
```

#### 000003_init_curriculum_domain.up.sql
```sql
-- Migration: Initialize Curriculum Domain
-- Description: Create all curriculum-related tables
-- Tables: cur_cp_detail, cur_learning_objective, cur_learning_outcome,
--          trx_curriculum_document, trx_curriculum_chapter,
--          trx_kokurikuler_activity, trx_ekstrakurikuler_activity

-- CREATE TABLE statements untuk semua curriculum tables
-- Include comments untuk domain-specific logic
```

#### 000004_init_transaction_domain.up.sql
```sql
-- Migration: Initialize Transaction Domain
-- Description: Create all transactional/operational tables
-- Tables: trx_assessment, trx_assessment_score, trx_attendance, trx_daily_attendance,
--          trx_academic_score, trx_atp, trx_atp_detail, trx_enrollment,
--          trx_teaching_assignment, trx_teaching_module, dll (25+ tables)

-- CREATE TABLE statements untuk semua transaction tables
-- Organized by functional sub-domains (assessment, attendance, teaching, dll)
```

#### 000005_init_system_tables.up.sql
```sql
-- Migration: Initialize System Tables
-- Description: Create system-level tables
-- Tables: sys_automation_queue, sys_server_telemetry, audit_logs

-- CREATE TABLE statements untuk system tables
-- Include monitoring and audit trail tables
```

### 4.2. Infrastructure Migrations

#### 000006_seed_reference_data.up.sql
```sql
-- Migration: Seed Reference Data
-- Description: Insert initial reference data for all domains
-- Content: Default roles, basic curriculum data, assessment levels,
--          cognitive stages, academic years, phases, dll

-- INSERT statements untuk semua reference data
-- Use ON CONFLICT DO NOTHING untuk safe re-runs
```

#### 000007_add_constraints.up.sql
```sql
-- Migration: Add All Foreign Key Constraints
-- Description: Add FK constraints to all relationship tables
-- Content: 25+ FK constraints dengan appropriate CASCADE rules

-- Organized by domain:
-- Auth domain FKs
-- Master data FKs
-- Curriculum FKs
-- Transaction FKs
```

#### 000008_add_performance_indexes.up.sql
```sql
-- Migration: Add All Performance Indexes
-- Description: Add indexes for query optimization
-- Content: 30+ indexes (FK column indexes, query optimization indexes,
--          partial indexes, composite indexes)

-- Organized by type:
-- Foreign key indexes
-- Query pattern indexes
-- Partial indexes for active records
-- Composite indexes for complex queries
```

### 4.3. Phase-Based Feature Migrations

#### 000009_phase2_assessment_enhancements.up.sql
```sql
-- Migration: Phase 2 - Assessment Enhancements
-- Description: Add Phase 2 assessment features
-- Phase: Fase B dan C assessment types
-- Tables: master_sd_assessment_criteria, rubric tables
-- Changes: ALTER TABLE additions, new tables

-- Phase 2 specific tables and modifications
```

#### 000010_phase3_advanced_features.up.sql
```sql
-- Migration: Phase 3 - Advanced Learning Features
-- Description: Add Phase 3 advanced features
-- Phase: Deep learning, ILP, DI, play-based learning
-- Tables: 20+ Phase 3 specific tables
-- Changes: Complex learning-related tables
```

---

## 5. Strategy Implementasi Restructuring

### 5.1. Pendekatan untuk Production yang Sudah Ada Data

**STRATEGI RECOMMENDED: DON'T RESTRUCTURE EXISTING PRODUCTION**

**Alasan:**
- ⚠️ Restrukturisasi migrations di production berisiko tinggi
- ⚠ akan break existing deployment pipeline
- ⚠️ Sulit memprediksi impact pada existing data
- ⚠️ Rollback complexity sangat tinggi

**Solusi:**
1. **Tetap gunakan migration files yang ada untuk production**
2. **Terapkan restructuring untuk FRESH INSTALLATION ONLY**
3. **Gunakan approach baru untuk future development**
4. **Create baseline migration untuk environment baru**

### 5.2. Implementasi untuk Future Development

**Step 1: Create Baseline untuk New Environment**
```
migrations/
├── baseline/                              # Directory untuk fresh installs
│   ├── 000001_init_auth_domain.up.sql
│   ├── 000002_init_master_data.up.sql
│   └── ... (foundation migrations)
└── incremental/                           # Directory untuk updates
    ├── 000001_add_phase5_features.up.sql  # Continue from highest production
    └── 000002_hotfix_alignment.up.sql
```

**Step 2: Update Migration Tool Configuration**
```go
// Configure migration tool to handle new structure
migrate.SetTable("schema_migrations")
migrate.SetSchema("public")
```

**Step 3: Documentation & Guidelines**
- Document migration creation process
- Provide template for new migrations
- Establish code review checklist for migrations

### 5.3. Consolidation untuk Development Environment

**Jika ingin restructure untuk development:**

**Step 1: Export Current Schema**
```bash
pg_dump --schema-only sim_sekolah > current_schema.sql
```

**Step 2: Create New Migration Structure**
```bash
# Create new organized migration files based on current schema
# Use current_schema.sql as reference
```

**Step 3: Test Fresh Installation
```bash
# Drop development database
dropdb sim_sekolah_dev

# Create fresh database
createdb sim_sekolah_dev

# Run new organized migrations
migrate -path migrations_new -database "postgres://..." up
```

**Step 4: Verify Data Consistency**
```sql
-- Compare schema old vs new
-- Verify all tables, columns, constraints match
```

---

## 6. Template Migration Script

### 6.1. Template untuk Domain-Based Migration

```sql
-- Migration: [3-digit sequence]_[domain]_[description]
-- Description: [Detailed description of what this migration does]
-- Author: [Author name]
-- Created: [Date]
-- Related Issues: [Jira/GitHub issue numbers]

-- ============================================================
-- SECTION 1: Create/Modify Tables
-- ============================================================

-- Example: Create new table
CREATE TABLE IF NOT EXISTS example_table (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ
);

-- Example: Alter existing table
ALTER TABLE existing_table 
ADD COLUMN IF NOT EXISTS new_field VARCHAR(50);

-- ============================================================
-- SECTION 2: Add Constraints
-- ============================================================

-- Add primary key
ALTER TABLE example_table 
ADD CONSTRAINT example_table_pkey PRIMARY KEY (id);

-- Add foreign key
ALTER TABLE example_table 
ADD CONSTRAINT fk_example_parent
FOREIGN KEY (parent_id) REFERENCES parent_table(id) ON DELETE CASCADE;

-- Add check constraint
ALTER TABLE example_table 
ADD CONSTRAINT chk_status
CHECK (status IN ('ACTIVE', 'INACTIVE', 'PENDING'));

-- Add unique constraint
ALTER TABLE example_table 
ADD CONSTRAINT uq_example_name
UNIQUE (name, status);

-- ============================================================
-- SECTION 3: Add Indexes
-- ============================================================

-- Basic index
CREATE INDEX idx_example_name ON example_table(name);

-- Composite index
CREATE INDEX idx_example_status_created ON example_table(status, created_at DESC);

-- Partial index
CREATE INDEX idx_example_active ON example_table(status) WHERE status = 'ACTIVE';

-- GIN index for JSONB
CREATE INDEX idx_example_data_gin ON example_table USING GIN(data_jsonb);

-- ============================================================
-- SECTION 4: Data Migration (if needed)
-- ============================================================

-- Example: Migrate existing data
UPDATE example_table 
SET new_field = 'DEFAULT_VALUE'
WHERE new_field IS NULL;

-- Example: Insert reference data
INSERT INTO reference_table (code, name) VALUES
('CODE1', 'Name 1'),
('CODE2', 'Name 2')
ON CONFLICT (code) DO NOTHING;

-- ============================================================
-- SECTION 5: Cleanup (if needed)
-- ============================================================

-- Example: Drop old column (BE CAREFUL in production)
-- ALTER TABLE example_table DROP COLUMN IF EXISTS old_field;

-- ============================================================
-- SECTION 6: Validation Queries
-- ============================================================

-- Verify table exists
SELECT table_name FROM information_schema.tables 
WHERE table_name = 'example_table';

-- Verify constraints
SELECT constraint_name, constraint_type 
FROM information_schema.table_constraints 
WHERE table_name = 'example_table';

-- Verify indexes
SELECT indexname FROM pg_indexes 
WHERE tablename = 'example_table';
```

### 6.2. Template untuk Down Migration

```sql
-- Rollback Migration: [3-digit sequence]_[domain]_[description]
-- Description: Rollback changes from [migration description]

-- ============================================================
-- SECTION 1: Rollback Data Migration
-- ============================================================

-- Reverse data changes
-- UPDATE example_table SET new_field = NULL;

-- ============================================================
-- SECTION 2: Rollback Indexes
-- ============================================================

DROP INDEX IF EXISTS idx_example_name;
DROP INDEX IF EXISTS idx_example_status_created;
DROP INDEX IF EXISTS idx_example_active;

-- ============================================================
-- SECTION 3: Rollback Constraints
-- ============================================================

ALTER TABLE example_table DROP CONSTRAINT IF EXISTS uq_example_name;
ALTER TABLE example_table DROP CONSTRAINT IF EXISTS chk_status;
ALTER TABLE example_table DROP CONSTRAINT IF EXISTS fk_example_parent;

-- ============================================================
-- SECTION 4: Rollback Table Changes
-- ============================================================

-- Rollback ALTER TABLE
ALTER TABLE existing_table DROP COLUMN IF EXISTS new_field;

-- Drop table (BE CAREFUL - DATA LOSS!)
-- DROP TABLE IF EXISTS example_table CASCADE;
```

---

## 7. Rekomendasi Final untuk SIM Sekolah

### 7.1. Untuk Production (Existing Data)

**STRATEGI: MAINTENANCE ONLY**

✅ **Lanjut gunakan structure saat ini untuk production**
- 60+ migration files sudah ada dan terbukti berfungsi
- Risk terlalu tinggi untuk restructure
- Fokus pada improvement per migration ke depan

**Improvement yang bisa dilakukan segera:**
1. **Standardisasi naming** - Gunakan pattern yang konsisten
2. **Add comments** - Setiap migration harus punya deskripsi jelas
3. **Consolidate small changes** - Jangan buat file baru untuk 1 line change
4. **Use transaction blocks** - Wrap migrations dalam transactions

### 7.2. Untuk Development & Future Features

**STRATEGI: DOMAIN-BASED + PHASE-BASED**

Untuk development ke depan, gunakan structure:

```
migrations/
├── foundation/              # Base schema untuk fresh install
│   ├── 000001_init_auth_domain.up.sql
│   ├── 000002_init_master_data.up.sql
│   ├── 000003_init_curriculum_domain.up.sql
│   ├── 000004_init_transaction_domain.up.sql
│   ├── 000005_init_system_tables.up.sql
│   ├── 000006_seed_reference_data.up.sql
│   ├── 000007_add_constraints.up.sql
│   └── 000008_add_performance_indexes.up.sql
├── features/                # Feature-based migrations
│   ├── 000001_phase5_features.up.sql
│   └── 000001_phase6_features.up.sql
└── hotfixes/                # Production hotfixes
    └── 000001_hotfix_[description].up.sql
```

### 7.3. Template untuk Future Migrations

**Gunakan format ini:**
```
[3-digit sequence]_[domain/phase]_[action]_[description].up.sql
```

**Examples:**
- `000009_phase5_add_numeracy_assessments.up.sql`
- `000010_phase5_add_parent_portal.up.sql`
- `000011_transaction_add_payment_tracking.up.sql`
- `000091_hotfix_fix_user_role_constraints.up.sql`

---

## 8. Best Practices Checklist

### 8.1. Before Creating Migration
- [ ] Verify migration doesn't break existing functionality
- [ ] Test on development environment
- [ ] Create corresponding down migration
- [ ] Add descriptive comments
- [ ] Review naming convention
- [ ] Check for performance impact

### 8.2. Migration Content
- [ ] Use transactions for atomic operations
- [ ] Include appropriate error handling
- [ ] Add data validation constraints
- [ ] Use IF NOT EXISTS for safe re-runs
- [ ] Include rollback procedures
- [ ] Document data migration steps

### 8.3. After Applying Migration
- [ ] Verify in staging environment
- [ ] Monitor application logs
- [ ] Check database performance
- [ ] Validate data integrity
- [ ] Document any manual steps
- [ ] Update schema documentation

---

## 9. Rekomendasi Spesifik untuk SIM Sekolah

### 9.1. Immediate Actions (Tanpa Restrukturisasi)

**1. Standardisasi naming untuk future migrations:**
```
Current pattern: ✅ KEEP (already quite good)
Pattern: [sequence]_[description].up.sql
Example: 000091_fix_backend_alignment_critical.up.sql
```

**2. Consolidate small changes:**
```
Instead of:
- 000015_add_unique_constraint_to_cp_details.up.sql (607 bytes)
- 000016_add_impersonator_to_audit_logs.up.sql (187 bytes)

Consider consolidating:
- 000015_add_phase2_constraints.up.sql (includes both)
```

**3. Add template comments:**
```sql
-- Migration: [Number]_[Description]
-- Description: [Detailed what/why]
-- Author: [Name]
-- Related Issue: [Ticket/PR]
-- Risk Level: [LOW/MEDIUM/HIGH]
-- Downtime Required: [YES/NO]
-- Rollback Procedure: [Description]
```

### 9.2. Long-term Strategy

**Phase 1: Documentation (Week 1-2)**
- Document existing migration patterns
- Create migration guidelines document
- Establish code review checklist
- Train team on best practices

**Phase 2: Template Implementation (Week 3-4)**
- Create migration template files
- Setup pre-commit hooks for validation
- Implement migration testing in CI/CD
- Create migration approval process

**Phase 3: Gradual Improvement (Ongoing)**
- Consolidate small migrations when opportunities arise
- Improve naming consistency for new migrations
- Add comprehensive comments to all new migrations
- Implement performance monitoring for migrations

---

## 10. Final Recommendation

### Untuk SIM Sekolah saat ini:

**SHORT TERM (0-3 bulan):**
1. ✅ **Keep existing structure for production** (too risky to change)
2. ✅ **Apply migration 000091 & 000092** (fixes yang baru dibuat)
3. ✅ **Standardisasi naming** untuk future migrations
4. ✅ **Add comments & documentation** untuk new migrations

**MEDIUM TERM (3-6 bulan):**
1. 🔄 **Consolidate small migrations** (group 5-10 files into 1)
2. 🔄 **Improve naming consistency**
3. 🔄 **Add performance monitoring**
4. 🔄 **Create migration guidelines**

**LONG TERM (6-12 bulan):**
1. 🎯 **Consider restructuring** untuk next major version
2. 🎯 **Implement domain-based structure** untuk fresh installations
3. 🎯 **Create baseline migrations** untuk new environments
4. 🎯 **Automate migration testing** in CI/CD

### Strategy Summary:

| Environment | Strategy | Timeline |
|-------------|----------|----------|
| **Production (existing)** | Maintenance only, no restructuring | Ongoing |
| **Development (new features)** | Domain-based + consolidated | Immediate |
| **Fresh Installation** | New organized structure | Next major version |
| **Hotfixes** | Separate 09xx numbering | As needed |

---

## Conclusion

**Best approach untuk SIM Sekolah:** HYBRID STRATEGY
- **Production:** Keep existing, improve incrementally
- **Development:** Use domain-based structure moving forward
- **New Features:** Consolidate and organize logically
- **Hotfixes:** Use separate numbering system

**Key principle:** Don't break what works, improve what doesn't, and build better patterns for the future.

**Next Steps:**
1. Review dan approve migration 000091 & 000092
2. Create migration guidelines document
3. Implement code review checklist
4. Setup migration testing in development environment