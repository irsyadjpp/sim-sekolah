# Fitur Gap Analysis: Deep Learning & Kurikulum Merdeka
## UPT SDI Bonerate No. 85 Kepulauan Selayar (SD Only)

---

## 🔍 METODOLOGI ANALISIS

**Scope:** Sekolah Dasar (SD) - Fase A (Kelas 1-2), Fase B (Kelas 3-4), Fase C (Kelas 5-6)
**Focus:** Functionality gaps (bukan data seeding)
**Basis:** Pembelajaran Mendalam PDF + Kurikulum Merdeka PDF
**Current System Status:** FITUR SUDAH ADA vs FITUR BELUM ADA

---

## 📊 CURRENT FEATURE STATUS

### ✅ **FITUR SUDAH DIIMPLEMENTASIKAN**

#### Backend Modules (Lengkap dengan Handler/Service):
1. ✅ **Academic Year** - Manajemen tahun ajaran
2. ✅ **Assessment** - Sistem penilaian lengkap (formatif/sumatif, P5, absensi)
3. ✅ **Auth** - Autentikasi dan autorisasi
4. ✅ **Classroom** - Manajemen kelas
5. ✅ **CP (Capaian Pembelajaran)** - CP dengan elemen dan TP
6. ✅ **Curriculum** - Dokumen kurikulum
7. ✅ **Enrollment** - Pendaftaran siswa
8. ✅ **Grade** - Manajemen tingkat/kelas
9. ✅ **Local Context** - Konteks lokal sekolah
10. ✅ **Phase** - Fase pembelajaran (A, B, C)
11. ✅ **Profile Dimension** - Dimensi profil lulusan
12. ✅ **School** - Data sekolah
13. ✅ **SPMB** - Penerimaan siswa baru
14. ✅ **Student** - Data siswa
15. ✅ **Subject** - Mata pelajaran
16. ✅ **Teacher** - Data guru
17. ✅ **Teaching Assignment** - Penugasan mengajar

#### Learning & Deep Learning Related (Partial):
1. ✅ **Learning Module** - ATP, Teaching Module, Module Activities
2. ✅ **Deep Learning Reference** - Elemen desain, tahapan kognitif, tingkat asesmen
3. ✅ **Project Module (P5)** - Modul projek P5 dengan dimensi profil

#### Frontend Pages:
1. ✅ **Academic Pages** - Curriculum, subjects, phases, deep-learning reference, dimensions
2. ✅ **Learning Pages** - Modules, projects, character
3. ✅ **Assessment Pages** - Evaluation, KSP
4. ✅ **Student Pages** - Records, presence, guidance, details
5. ✅ **Report Pages** - Gradebook, progress
6. ✅ **System Pages** - Academic years, access, grades

---

### ❌ **FITUR BELUM DIIMPLEMENTASIKAN (GAP ANALYSIS)**

## 🔴 **PRIORITY 1: KRITICAL - DEEP LEARNING FRAMEWORK**

### 1.1 Learning Aspects (4 Olah) - **MISSING COMPLETELY**
**Status:** TIDAK ADA SAMA SEKALI
**Impact:** Fundamental framework Deep Learning tidak tercakup
**PDF Requirement:** Halaman 10-11 (Olah Pikir, Olah Hati, Olah Rasa, Olah Raga)

#### Backend Features Needed:
```
backend/internal/olah_aspect/
├── model.go              # 4 olah aspects dengan definisi lengkap
├── repository.go         # CRUD operations
├── service.go            # Business logic
├── handler.go            # HTTP handlers
├── dto.go               # Data transfer objects
└── routes.go            # API endpoints
```

**Required API Endpoints:**
- GET /api/v1/olah-aspect - Get all 4 olah aspects
- GET /api/v1/olah-aspect/:id - Get specific olah aspect
- POST /api/v1/olah-aspect - Create olah aspect (admin only)
- PUT /api/v1/olah-aspect/:id - Update olah aspect (admin only)

**Database Schema:**
```sql
CREATE TABLE master_olah_aspect (
    id UUID PRIMARY KEY,
    aspect_code VARCHAR(10) UNIQUE NOT NULL,  -- OLAH_PIKIR, OLAH_HATI, OLAH_RASA, OLAH_RAGA
    aspect_name VARCHAR(50) NOT NULL,
    definition TEXT NOT NULL,
    indicators TEXT[],  -- Array of indicators for each aspect
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    deleted_at TIMESTAMPTZ
);
```

**Integration Points:**
- Link to TeachingModule activities
- Link to Assessment questions
- Link to Project modules (P5)
- Student olah aspect development tracking

#### Frontend Features Needed:
```
frontend/src/pages/app/academic/olah-aspects/
├── page.tsx              # List all 4 olah aspects
├── detail/
│   └── page.tsx          # Detail per olah aspect dengan indikator
└── components/
    ├── OlahAspectCard.tsx
    └── IndicatorList.tsx
```

**UI Components:**
- Visual representation of 4 olah aspects
- Indicator breakdown per aspect
- Integration with module creation (select olah aspects)
- Student development dashboard per olah aspect

---

### 1.2 Learning Principles (3 Prinsip) - **MISSING COMPLETELY**
**Status:** TIDAK ADA SAMA SEKALI
**Impact:** Prinsip pembelajaran tidak termonitor
**PDF Requirement:** Halaman 15-16 (Berkesadaran, Bermakna, Menggembirakan)

#### Backend Features Needed:
```
backend/internal/learning_principle/
├── model.go              # 3 learning principles
├── repository.go         # CRUD operations
├── service.go            # Business logic
├── handler.go            # HTTP handlers
├── dto.go               # Data transfer objects
└── routes.go            # API endpoints
```

**Required API Endpoints:**
- GET /api/v1/learning-principles - Get all 3 principles
- GET /api/v1/learning-principles/:id - Get specific principle
- POST /api/v1/learning-principles - Create principle (admin only)

**Database Schema:**
```sql
CREATE TABLE master_learning_principle (
    id UUID PRIMARY KEY,
    principle_code VARCHAR(10) UNIQUE NOT NULL,  -- BERKESADARAN, BERMAKNA, MENGENGIRAKAN
    principle_name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    key_characteristics TEXT[],  -- Key characteristics per principle
    implementation_examples TEXT[],
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    deleted_at TIMESTAMPTZ
);

-- Link teaching modules to learning principles
CREATE TABLE trx_module_principle_mapping (
    module_id UUID REFERENCES trx_teaching_module(id),
    principle_id UUID REFERENCES master_learning_principle(id),
    PRIMARY KEY (module_id, principle_id)
);
```

**Integration Points:**
- TeachingModule must specify which principles are applied
- Assessment should evaluate principle adherence
- Teacher self-assessment on principle usage

#### Frontend Features Needed:
```
frontend/src/pages/app/academic/learning-principles/
├── page.tsx              # List all 3 principles
├── detail/
│   └── page.tsx          # Detail per principle
└── components/
    ├── PrincipleCard.tsx
    └── PrincipleSelector.tsx  # Multi-select untuk module creation
```

**UI Components:**
- Principle explanation cards
- Principle selector in module creation
- Principle adherence checklist for teachers
- Principle coverage dashboard

---

### 1.3 Learning Experience Phases (3 Tahap) - **MISSING COMPLETELY**
**Status:** TIDAK ADA SAMA SEKALI
**Impact:** Progression learning tidak tertrack
**PDF Requirement:** Halaman 17-18 (Memahami, Mengaplikasi, Merefleksi)

#### Backend Features Needed:
```
backend/internal/learning_experience/
├── model.go              # 3 experience phases
├── repository.go         # CRUD operations
├── service.go            # Business logic + progression tracking
├── handler.go            # HTTP handlers
──── dto.go               # Data transfer objects
└── routes.go            # API endpoints
```

**Required API Endpoints:**
- GET /api/v1/learning-experiences - Get all 3 experience phases
- GET /api/v1/learning-experiences/:id - Get specific phase
- GET /api/v1/students/:studentId/experience-progression - Track student progression
- POST /api/v1/activities/:activityId/experience-phase - Link activity to experience phase

**Database Schema:**
```sql
CREATE TABLE master_learning_experience (
    id UUID PRIMARY KEY,
    experience_code VARCHAR(10) UNIQUE NOT NULL,  -- MEMAHAMI, MENAPLIKASI, MEREFLEKSI
    experience_name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    sequence_order INT NOT NULL,  -- 1, 2, 3
    key_indicators TEXT[],
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    deleted_at TIMESTAMPTZ
);

-- Link activities to experience phases
CREATE TABLE trx_activity_experience_mapping (
    activity_id UUID REFERENCES trx_teaching_module_activity(id),
    experience_id UUID REFERENCES master_learning_experience(id),
    PRIMARY KEY (activity_id, experience_id)
);

-- Track student progression through experiences
CREATE TABLE trx_student_experience_progression (
    id UUID PRIMARY KEY,
    student_id UUID REFERENCES auth_user(id),
    subject_id UUID REFERENCES master_subject(id),
    experience_id UUID REFERENCES master_learning_experience(id),
    mastery_level DECIMAL(3,2),  -- 0.00 to 1.00
    last_assessed_at TIMESTAMPTZ,
    notes TEXT,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
);
```

**Integration Points:**
- Each ModuleActivity must specify experience phase
- Track student mastery progression through phases
- Experience phase readiness for next level
- Learning pathway recommendations

#### Frontend Features Needed:
```
frontend/src/pages/app/academic/learning-experiences/
├── page.tsx              # List all 3 experience phases
├── student-progression/
│   ├── page.tsx          # Student progression dashboard
│   └── components/
│       ├── ProgressionChart.tsx
│       └── ExperienceMasteryCard.tsx
└── components/
    ├── ExperiencePhaseCard.tsx
    └── ExperienceSelector.tsx  # For activity creation
```

**UI Components:**
- Experience phase progression charts
- Student mastery dashboard per experience
- Experience selector in activity creation
- Readiness indicators for phase transitions

---

### 1.4 Profile Dimensions Update (8 Dimensi) - **CRITICAL UPDATE NEEDED**
**Status:** ADA TAPI SALAH REFERENSI (Pancasila, bukan Deep Learning 8 Dimensions)
**Impact:** Profil lulusan tidak sesuai framework
**PDF Requirement:** Halaman 14-15 (8 Dimensi Profil Lulusan)

#### Backend Changes Needed:
```
backend/internal/profile_dimension/
├── model.go              # UPDATE: Change comment from Pancasila to Deep Learning
├── repository.go         # UPDATE: Add validation for 8 standard dimensions
├── service.go            # UPDATE: Add dimension-specific logic
└── seeder.go            # NEW: Seed with correct 8 dimensions
```

**Required Updates:**
```sql
-- Update existing data or migrate to correct 8 dimensions:
-- 1. Keimanan dan Ketakwaan terhadap Tuhan YME
-- 2. Kewargaan
-- 3. Penalaran Kritis
-- 4. Kreativitas
-- 5. Kolaborasi
-- 6. Kemandirian
-- 7. Kesehatan
-- 8. Komunikasi

UPDATE master_profile_dimension SET 
    dimension_code = 'DIM_KEIMANAN',
    dimension_name = 'Keimanan dan Ketakwaan terhadap Tuhan YME',
    description = 'Individu yang memiliki keyakinan teguh akan keberadaan Tuhan YME dan menghayati serta mengamalkan nilai-nilai spiritual dalam kehidupan sehari-hari.'
WHERE dimension_name LIKE '%Pancasila%' OR dimension_name ILIKE '%ketuhanan%';

-- Add remaining dimensions...
```

**Integration Points:**
- CP must link to profile dimensions (already exists in CPDetail.element_id)
- P5 projects must specify target dimensions (already exists in ProjectModule.Dimensions)
- Student assessment per dimension
- Dimension development tracking

#### Frontend Changes Needed:
```
frontend/src/pages/app/academic/dimensions/
├── page.tsx              # UPDATE: Show correct 8 dimensions
└── components/
    ├── DimensionCard.tsx  # UPDATE: Correct dimension info
    └── DimensionMatrix.tsx  # NEW: Visual matrix of 8 dimensions
```

---

### 1.5 Deep Learning Framework Elements (4 Elemen) - **PARTIAL, NEED UPDATE**
**Status:** ADA ELEMEN DESAIN TAPI TIDAK SPESIFIK 4 FRAMEWORK ELEMENTS
**Impact:** Framework elements tidak sesuai standar Deep Learning
**PDF Requirement:** Halaman 13 (4 Kerangka Pembelajaran)

#### Backend Changes Needed:
```
backend/internal/deep_learning/elemen_desain/
├── model.go              # UPDATE: Add framework_element_type field
├── service.go            # UPDATE: Add framework-specific logic
└── seeder.go            # NEW: Seed with correct 4 framework elements
```

**Required Updates:**
```sql
-- Add framework classification to existing design elements
ALTER TABLE dl_design_element 
ADD COLUMN framework_element_type VARCHAR(50);

-- Values should be:
-- 1. PRAKTIK_PEDAGOGIS (Pedagogical Practices)
-- 2. KEMITRAAN_PEMBELAJARAN (Learning Partnerships) 
-- 3. LINGKUNGAN_PEMBELAJARAN (Learning Environment)
-- 4. PEMANFAATAN_DIGITAL (Digital Utilization)

-- Update existing elements and classify them correctly
UPDATE dl_design_element SET 
    framework_element_type = 'PRAKTIK_PEDAGOGIS'
WHERE design_element_name ILIKE '%pedagogik%' OR design_element_name ILIKE '%metode%';

-- Add new elements for missing framework categories
INSERT INTO dl_design_element (design_element_name, description, framework_element_type) VALUES
('Kemitraan Guru-Siswa', 'Kolaborasi aktif antara guru dan siswa dalam proses pembelajaran', 'KEMITRAAN_PEMBELAJARAN'),
('Kemitraan Siswa-Siswa', 'Kerja sama dan kolaborasi antar siswa', 'KEMITRAAN_PEMBELAJARAN'),
('Kemitraan Sekolah-Komunitas', 'Keterlibatan komunitas dan orang tua dalam pembelajaran', 'KEMITRAAN_PEMBELAJARAN'),
('Lingkungan Kelas yang Kondusif', 'Pengaturan ruang kelas yang mendukung pembelajaran', 'LINGKUNGAN_PEMBELAJARAN'),
('Lingkungan Sosial yang Positif', 'Budaya kelas yang saling menghargai', 'LINGKUNGAN_PEMBELAJARAN'),
('Pemanfaatan Media Digital', 'Penggunaan teknologi digital dalam pembelajaran', 'PEMANFAATAN_DIGITAL'),
('Pemanfaatan Platform Pembelajaran', 'Penggunaan LMS dan platform edukasi', 'PEMANFAATAN_DIGITAL');
```

#### Frontend Changes Needed:
```
frontend/src/pages/app/academic/deep-learning/
├── page.tsx              # UPDATE: Group by framework element type
└── components/
    ├── FrameworkElementTab.tsx  # NEW: Tabs per framework element
    └── ElementMatrix.tsx        # NEW: Visual matrix of elements
```

---

## 🟠 **PRIORITY 2: HIGH - KURIKULUM MERDEKA SD SPECIFICS**

### 2.1 SD-Only Phase Validation - **URGENT FIX**
**Status:** ADA FASE D, E, F (SALAH - UNTUK SMP/SMA)
**Impact:** Sistem mencakup fase yang tidak relevan untuk SD
**PDF Requirement:** Kurikulum Merdeka SD hanya Fase A, B, C

#### Backend Changes Needed:
```
backend/internal/phase/
├── repository.go         # UPDATE: Remove Fase D, E, F from seeding
├── service.go            # NEW: Add SD-only validation
└── validation.go         # NEW: SD phase validation logic
```

**Required Changes:**
```go
// In repository.go - Update Seed function
func (r *phaseRepository) Seed(ctx context.Context) error {
    seeds := []struct {
        Code string
        Name string
        Desc string
    }{
        {"FAS-A", "Fase A", "Kelas 1-2 SD/Sederajat"},
        {"FAS-B", "Fase B", "Kelas 3-4 SD/Sederajat"},
        {"FAS-C", "Fase C", "Kelas 5-6 SD/Sederajat"},
        // REMOVE Fase D, E, F - not relevant for SD
    }
    // ... rest of seeding logic
}

// Add validation service
func (s *phaseService) ValidateSDPhase(phaseCode string) error {
    validSDPhases := map[string]bool{
        "FAS-A": true,
        "FAS-B": true, 
        "FAS-C": true,
    }
    
    if !validSDPhases[phaseCode] {
        return errors.New("fase ini tidak relevan untuk Sekolah Dasar")
    }
    return nil
}
```

#### Frontend Changes Needed:
```
frontend/src/pages/app/academic/phases/
├── page.tsx              # UPDATE: Only show Fase A, B, C
└── components/
    ├── PhaseSelector.tsx  # UPDATE: SD-only options
    └── PhaseInfoCard.tsx   # UPDATE: SD-specific information
```

---

### 2.2 Foundational Skills Assessment (Literasi-Numerasi Dasar) - **MISSING**
**Status:** TIDAK ADA SAMA SEKALI
**Impact:** Tidak ada tracking kemampuan dasar kritis untuk Fase A
**PDF Requirement:** Kurikulum Merdeka emphasizes literasi-numerasi dasar for Fase A

#### Backend Features Needed:
```
backend/internal/foundational_skills/
├── model.go              # Foundational skills tracking
├── repository.go         # CRUD operations
├── service.go            # Assessment logic
├── handler.go            # HTTP handlers
├── dto.go               # Data transfer objects
└── routes.go            # API endpoints
```

**Required API Endpoints:**
- GET /api/v1/foundational-skills/standards - Get literacy/numerasi standards
- POST /api/v1/foundational-skills/assessment - Create assessment
- GET /api/v1/students/:studentId/foundational-skills - Get student progress
- PUT /api/v1/foundational-skills/:id - Update assessment results

**Database Schema:**
```sql
CREATE TABLE master_foundational_skill_standard (
    id UUID PRIMARY KEY,
    skill_type VARCHAR(20) NOT NULL,  -- LITERASI, NUMERASI
    skill_code VARCHAR(20) NOT NULL,
    skill_name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    phase_id UUID REFERENCES master_phase(id),  -- Fase A focused
    indicators TEXT[],
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
);

CREATE TABLE trx_foundational_skill_assessment (
    id UUID PRIMARY KEY,
    student_id UUID REFERENCES auth_user(id),
    skill_standard_id UUID REFERENCES master_foundational_skill_standard(id),
    assessment_date DATE NOT NULL,
    mastery_level VARCHAR(20) NOT NULL,  -- BELUM, SEDANG, MENGUASAI
    score DECIMAL(5,2),
    notes TEXT,
    teacher_id UUID REFERENCES auth_user(id),
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
);
```

#### Frontend Features Needed:
```
frontend/src/pages/app/academic/foundational-skills/
├── page.tsx              # Foundational skills dashboard
├── assessment/
│   ├── page.tsx          # Assessment creation
│   └── components/
│       ├── SkillChecklist.tsx
│       └── MasteryRubric.tsx
└── student-progress/
    ├── page.tsx          # Per-student progress
    └── components/
        ├── LiterasiProgressChart.tsx
        └── NumerasiProgressChart.tsx
```

---

### 2.3 Reading Literacy Progression - **MISSING**
**Status:** TIDAK ADA SAMA SEKALI
**Impact:** Tidak ada tracking kemampuan membaca (kritis untuk Fase A-B)
**PDF Requirement:** Reading literacy is foundational for SD success

#### Backend Features Needed:
```
backend/internal/reading_literacy/
├── model.go              # Reading literacy tracking
├── repository.go         # CRUD operations
├── service.go            # Progression logic
├── handler.go            # HTTP handlers
├── dto.go               # Data transfer objects
└── routes.go            # API endpoints
```

**Required API Endpoints:**
- GET /api/v1/reading-literacy/levels - Get reading level standards
- POST /api/v1/reading-literacy/assessment - Assess student reading
- GET /api/v1/students/:studentId/reading-literacy - Get student progression
- GET /api/v1/classrooms/:classroomId/reading-literacy - Class overview

**Database Schema:**
```sql
CREATE TABLE master_reading_level (
    id UUID PRIMARY KEY,
    level_code VARCHAR(10) UNIQUE NOT NULL,  -- LEVEL_0 to LEVEL_6
    level_name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    phase_id UUID REFERENCES master_phase(id),
    indicators TEXT[],
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ
);

CREATE TABLE trx_reading_literacy_assessment (
    id UUID PRIMARY KEY,
    student_id UUID REFERENCES auth_user(id),
    reading_level_id UUID REFERENCES master_reading_level(id),
    assessment_date DATE NOT NULL,
    words_per_minute INT,
    comprehension_score DECIMAL(5,2),
    fluency_rating VARCHAR(20),
    notes TEXT,
    teacher_id UUID REFERENCES auth_user(id),
    created_at TIMESTAMPTZ
);
```

#### Frontend Features Needed:
```
frontend/src/pages/app/academic/reading-literacy/
├── page.tsx              # Reading literacy dashboard
├── assessment/
│   ├── page.tsx          # Reading assessment tool
│   └── components/
│       ├── ReadingLevelIndicator.tsx
│       └── FluencyAssessment.tsx
└── progression/
    ├── page.tsx          # Student progression
    └── components/
        ├── ReadingProgressChart.tsx
        └── LevelMilestoneTracker.tsx
```

---

### 2.4 Age-Appropriate Assessment Types - **PARTIAL**
**Status:** ADA TAPI TIDAK DIKLASIFIKASIKAN MENURUT USIA
**Impact:** Tidak ada asesmen yang sesuai dengan perkembangan kognitif SD
**PDF Requirement:** Different assessment approaches for different phases

#### Backend Changes Needed:
```
backend/internal/assessment/
├── model.go              # ADD: age_appropriate_type field
├── service.go            # ADD: Age-appropriate validation
└── assessment_type.go    # NEW: SD assessment type definitions
```

**Required Changes:**
```sql
-- Add age-appropriate classification
ALTER TABLE trx_assessment 
ADD COLUMN age_appropriate_type VARCHAR(30);

-- Values:
-- FASE_A_OBSERVATION (Observation-based, play-based)
-- FASE_A_PORTFOLIO (Portfolio assessment)
-- FASE_B_PERFORMANCE (Performance tasks)
-- FASE_B_PROJECT (Simple projects)
-- FASE_C_PROJECT_COMPLEX (Complex projects)
-- FASE_C_COLLABORATIVE (Collaborative assessment)
-- FASE_C_PEER_ASSESSMENT (Peer assessment)

-- Add SD-specific assessment criteria
CREATE TABLE master_sd_assessment_criteria (
    id UUID PRIMARY KEY,
    assessment_type VARCHAR(30) NOT NULL,
    phase_id UUID REFERENCES master_phase(id),
    criteria_name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    rubric_elements JSONB,
    is_active BOOLEAN DEFAULT true
);
```

#### Frontend Changes Needed:
```
frontend/src/pages/app/academic/evaluation/
├── create/
│   ├── page.tsx          # UPDATE: Add phase-specific assessment types
│   └── components/
│       ├── AssessmentTypeSelector.tsx  # NEW: Phase-aware selector
│       └── PhaseSpecificCriteria.tsx    # NEW: Phase-specific criteria
└── templates/
    ├── fase-a-observation.tsx  # NEW: Fase A template
    ├── fase-b-performance.tsx  # NEW: Fase B template
    └── fase-c-project.tsx       # NEW: Fase C template
```

---

### 2.5 Curriculum Type Classification - **MISSING**
**Status:** TIDAK ADA KLASIFIKASI KURIKULUM
**Impact:** Tidak ada pembagian intra/co/extra-curricular
**PDF Requirement:** Kurikulum Merdeka requires clear classification

#### Backend Changes Needed:
```
backend/internal/curriculum/
├── model.go              # ADD: curriculum_type field
├── service.go            # ADD: Type-based logic
└── curriculum_type.go    # NEW: Type definitions and validation
```

**Required Changes:**
```sql
-- Add curriculum type classification
ALTER TABLE trx_curriculum_document 
ADD COLUMN curriculum_type VARCHAR(20) NOT NULL DEFAULT 'INTRAKURIKULER';

-- Values:
-- INTRAKURIKULER (Intra-curricular)
-- KOKURIKULER (Co-curricular)
-- EKSTRAKURIKULER (Extra-curricular)

-- Add co-curricular module tracking
CREATE TABLE trx_kokurikuler_activity (
    id UUID PRIMARY KEY,
    curriculum_document_id UUID REFERENCES trx_curriculum_document(id),
    activity_name VARCHAR(100) NOT NULL,
    linked_subject_id UUID REFERENCES master_subject(id),
    description TEXT,
    schedule TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ
);

-- Add extra-curricular module tracking
CREATE TABLE trx_ekstrakurikuler_activity (
    id UUID PRIMARY KEY,
    curriculum_document_id UUID REFERENCES trx_curriculum_document(id),
    activity_name VARCHAR(100) NOT NULL,
    activity_category VARCHAR(50),  -- OLAHRAGA, SENI, ORGANISASI, LAINNYA
    description TEXT,
    schedule TEXT,
    instructor_id UUID REFERENCES auth_user(id),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ
);
```

#### Frontend Features Needed:
```
frontend/src/pages/app/academic/curriculum/
├── create/
│   ├── page.tsx          # UPDATE: Add curriculum type selection
│   └── components/
│       ├── CurriculumTypeSelector.tsx  # NEW
│       └── TypeSpecificForm.tsx           # NEW
├── kokurikuler/
│   ├── page.tsx          # NEW: Co-curricular management
│   └── components/
│       ├── KokurikulerCard.tsx
│       └── SubjectLinker.tsx
└── ekstrakurikuler/
    ├── page.tsx          # NEW: Extra-curricular management
    └── components/
        ├── EkstrakurikulerCard.tsx
        └── CategoryFilter.tsx
```

---

## 🟡 **PRIORITY 3: MEDIUM - ENHANCEMENT FEATURES**

### 3.1 Individual Learning Plans (SD-Appropriate) - **MISSING**
**Status:** TIDAK ADA SAMA SEKALI
**Impact:** Tidak ada pembelajaran personal untuk siswa SD
**PDF Requirement:** Student-centered learning approach

#### Backend Features Needed:
```
backend/internal/individual_learning_plan/
├── model.go              # ILP structure
├── repository.go         # CRUD operations
├── service.go            # ILP logic
├── handler.go            # HTTP handlers
├── dto.go               # Data transfer objects
└── routes.go            # API endpoints
```

**Required API Endpoints:**
- GET /api/v1/students/:studentId/ilp - Get student ILP
- POST /api/v1/students/:studentId/ilp - Create ILP
- PUT /api/v1/students/:studentId/ilp/:id - Update ILP
- GET /api/v1/ilp/templates - Get SD-appropriate ILP templates

**Database Schema:**
```sql
CREATE TABLE trx_individual_learning_plan (
    id UUID PRIMARY KEY,
    student_id UUID REFERENCES auth_user(id),
    academic_year_id UUID REFERENCES master_academic_year(id),
    title VARCHAR(150) NOT NULL,
    goals TEXT[],  -- Learning goals
    strategies TEXT[],  -- Learning strategies
    accommodations TEXT[],  -- Special accommodations
    parent_notes TEXT,
    teacher_notes TEXT,
    status VARCHAR(20) DEFAULT 'ACTIVE',  -- ACTIVE, COMPLETED, ARCHIVED
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
);

CREATE TABLE trx_ilp_milestone (
    id UUID PRIMARY KEY,
    ilp_id UUID REFERENCES trx_individual_learning_plan(id),
    milestone_name VARCHAR(100) NOT NULL,
    target_date DATE,
    achieved BOOLEAN DEFAULT false,
    achieved_date DATE,
    notes TEXT
);
```

#### Frontend Features Needed:
```
frontend/src/pages/app/students/
├── details/
│   ├── ilp/
│   │   ├── page.tsx          # ILP management per student
│   │   └── components/
│   │       ├── ILPForm.tsx
│   │       ├── MilestoneTracker.tsx
│   │       └── GoalProgressCard.tsx
│   └── ...
└── templates/
    └── ilp-templates.tsx    # SD-appropriate templates
```

---

### 3.2 Differentiated Instruction Tracking - **MISSING**
**Status:** TIDAK ADA SAMA SEKALI
**Impact:** Tidak ada tracking pembelajaran berbeda untuk kebutuhan berbeda
**PDF Requirement:** Inclusive education requirements

#### Backend Features Needed:
```
backend/internal/differentiated_instruction/
├── model.go              # DI tracking
├── repository.go         # CRUD operations
├── service.go            # DI logic
├── handler.go            # HTTP handlers
├── dto.go               # Data transfer objects
└── routes.go            # API endpoints
```

**Required API Endpoints:**
- GET /api/v1/differentiated-instruction/strategies - Get DI strategies
- POST /api/v1/teaching-modules/:moduleId/differentiation - Add DI to module
- GET /api/v1/students/:studentId/differentiation-needs - Get student DI needs

**Database Schema:**
```sql
CREATE TABLE master_di_strategy (
    id UUID PRIMARY KEY,
    strategy_code VARCHAR(20) UNIQUE NOT NULL,
    strategy_name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    applicability TEXT[],  -- When to use this strategy
    examples TEXT[],
    is_active BOOLEAN DEFAULT true
);

CREATE TABLE trx_module_differentiation (
    id UUID PRIMARY KEY,
    module_id UUID REFERENCES trx_teaching_module(id),
    strategy_id UUID REFERENCES master_di_strategy(id),
    target_students UUID[],  -- Students who need this differentiation
    modifications TEXT,
    resources TEXT,
    created_at TIMESTAMPTZ
);
```

#### Frontend Features Needed:
```
frontend/src/pages/app/learning/modules/
├── drafts/
│   ├── page.tsx          # UPDATE: Add DI section
│   └── components/
│       ├── DifferentiationPanel.tsx  # NEW
│       ├── StrategySelector.tsx      # NEW
│       └── StudentNeedAssessment.tsx # NEW
└── strategies/
    ├── page.tsx          # NEW: DI strategies reference
    └── components/
        └── StrategyCard.tsx
```

---

### 3.3 Local Context Integration - **PARTIAL**
**Status:** ADA LOCAL CONTEXT MODULE TAPI BELUM TERINTEGRASI PENUH
**Impact:** Konteks lokal kepulauan belum dimanfaatkan optimal
**PDF Requirement:** Contextual learning for SD

#### Backend Changes Needed:
```
backend/internal/local_context/
├── model.go              # UPDATE: Add integration fields
├── service.go            # ADD: Integration logic
└── integration/
    ├── subject_linker.go  # NEW: Link context to subjects
    └── activity_linker.go # NEW: Link context to activities
```

**Required Changes:**
```sql
-- Add local context linkage to subjects
ALTER TABLE master_subject 
ADD COLUMN local_context_ids UUID[];

-- Add local context linkage to teaching modules
ALTER TABLE trx_teaching_module
ADD COLUMN local_context_ids UUID[];

-- Add context utilization tracking
CREATE TABLE trx_local_context_utilization (
    id UUID PRIMARY KEY,
    context_id UUID REFERENCES master_local_context(id),
    subject_id UUID REFERENCES master_subject(id),
    module_id UUID REFERENCES trx_teaching_module(id),
    utilization_type VARCHAR(30),  -- EXAMPLE, CASE_STUDY, PROJECT_BASE, RESOURCE
    description TEXT,
    created_at TIMESTAMPTZ
);
```

#### Frontend Features Needed:
```
frontend/src/pages/app/local-context/
├── page.tsx              # UPDATE: Add integration dashboard
├── integration/
│   ├── page.tsx          # NEW: Context integration management
│   └── components/
│       ├── SubjectContextLinker.tsx
│       ├── ModuleContextSelector.tsx
│       └── ContextUtilizationChart.tsx
└── kepulauan-specific/
    └── page.tsx          # NEW: Kepulauan Selayar specific contexts
```

---

### 3.4 Play-Based Learning Tracking (Fase A) - **MISSING**
**Status:** TIDAK ADA SAMA SEKALI
**Impact:** Tidak ada tracking pembelajaran berbasis bermain untuk kelas 1-2
**PDF Requirement:** Fase A should be play-based learning

#### Backend Features Needed:
```
backend/internal/play_based_learning/
├── model.go              # Play-based activity tracking
├── repository.go         # CRUD operations
── service.go            # Play-based learning logic
├── handler.go            # HTTP handlers
├── dto.go               # Data transfer objects
└── routes.go            # API endpoints
```

**Required API Endpoints:**
- GET /api/v1/play-based-activities/templates - Get play-based templates
- POST /api/v1/play-based-activities - Create play-based activity
- GET /api/v1/teaching-modules/:moduleId/play-based-elements - Get play elements

**Database Schema:**
```sql
CREATE TABLE master_play_activity_type (
    id UUID PRIMARY KEY,
    activity_code VARCHAR(20) UNIQUE NOT NULL,
    activity_name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    learning_outcomes TEXT[],  -- What students learn
    materials_needed TEXT[],
    is_active BOOLEAN DEFAULT true
);

CREATE TABLE trx_play_based_activity (
    id UUID PRIMARY KEY,
    module_id UUID REFERENCES trx_teaching_module(id),
    activity_type_id UUID REFERENCES master_play_activity_type(id),
    activity_name VARCHAR(100) NOT NULL,
    duration_minutes INT,
    social_interaction_type VARCHAR(30),  -- INDIVIDUAL, PAIR, GROUP, CLASS
    physical_activity_level VARCHAR(20),  -- LOW, MEDIUM, HIGH
    learning_goals TEXT[],
    created_at TIMESTAMPTZ
);
```

#### Frontend Features Needed:
```
frontend/src/pages/app/learning/
├── fase-a-specific/
│   ├── play-based/
│   │   ├── page.tsx          # NEW: Play-based learning management
│   │   └── components/
│   │       ├── PlayActivityTemplate.tsx
│   │       ├── SocialInteractionSelector.tsx
│   │       └── LearningOutcomeMapper.tsx
│   └── observation/
│       └── page.tsx          # NEW: Play-based observation tool
```

---

## 🟢 **PRIORITY 4: LOW - ENHANCEMENT FEATURES**

### 4.1 Parent-Teacher Partnership Tracking - **MISSING**
**Status:** TIDAK ADA SAMA SEKALI
**Impact:** Tidak ada tracking kolaborasi home-school (penting untuk SD)
**PDF Requirement:** Parent involvement is crucial for SD success

#### Backend Features Needed:
```
backend/internal/parent_partnership/
├── model.go              # Partnership tracking
├── repository.go         # CRUD operations
├── service.go            # Partnership logic
├── handler.go            # HTTP handlers
├── dto.go               # Data transfer objects
└── routes.go            # API endpoints
```

#### Frontend Features Needed:
```
frontend/src/pages/app/students/
├── details/
│   ├── parent-partnership/
│   │   ├── page.tsx          # NEW: Partnership management
│   │   └── components/
│   │       ├── CommunicationLog.tsx
│   │       ├── MeetingScheduler.tsx
│   │       └── PartnershipDashboard.tsx
```

---

### 4.2 Character Intervention System - **MISSING**
**Status:** ADA P5 ASSESSMENT TAPI TANPA SISTEM INTERVENSI
**Impact:** Tidak ada rekomendasi tindakan follow-up karakter
**PDF Requirement**: Character development requires actionable interventions

#### Backend Features Needed:
```
backend/internal/character_intervention/
├── model.go              # Intervention tracking
├── service.go            # Recommendation logic
└── recommendation_engine.go  # Generate intervention recommendations
```

---

### 4.3 Self & Peer Assessment (Simplified for SD) - **MISSING**
**Status:** TIDAK ADA SAMA SEKALI
**Impact:** Tidak ada asesmen mandiri dan teman sebaya
**PDF Requirement:** Assessment should include self and peer components

#### Backend Features Needed:
```
backend/internal/peer_assessment/
├── model.go              # Peer assessment (simplified for SD)
└── service.go            # SD-appropriate peer assessment logic
```

---

## 📋 **IMPLEMENTATION PRIORITY MATRIX**

### 🔴 **IMMEDIATE (Phase 1 - Weeks 1-4)**

#### Backend:
1. **SD Phase Validation** - Remove Fase D, E, F (URGENT)
2. **Learning Aspects (4 Olah)** - Complete module creation
3. **Learning Principles (3 Prinsip)** - Complete module creation
4. **Profile Dimensions Update** - Migrate to 8 dimensions
5. **Framework Elements Update** - Add 4 framework classification

#### Frontend:
1. **Deep Learning Reference Page** - Update with 4 olah aspects
2. **Learning Principles Page** - New page creation
3. **Profile Dimensions Page** - Update with 8 dimensions
4. **Phase Selector Updates** - SD-only options
5. **Framework Element Tabs** - Group by framework type

### 🟠 **HIGH PRIORITY (Phase 2 - Weeks 5-8)**

#### Backend:
6. **Learning Experience Phases** - Complete module with progression tracking
7. **Foundational Skills Assessment** - Literasi-numerasi dasar
8. **Reading Literacy Progression** - Reading level tracking
9. **Age-Appropriate Assessment Types** - SD-specific classification
10. **Curriculum Type Classification** - Intra/co/extra-curricular

#### Frontend:
6. **Learning Experience Dashboard** - Progression tracking UI
7. **Foundational Skills Assessment** - Assessment tools UI
8. **Reading Literacy Dashboard** - Progress monitoring UI
9. **Phase-Specific Assessment Templates** - Age-appropriate forms
10. **Curriculum Type Management** - Classification UI

### 🟡 **MEDIUM PRIORITY (Phase 3 - Weeks 9-12)**

#### Backend:
11. **Individual Learning Plans** - SD-appropriate ILP system
12. **Differentiated Instruction** - DI tracking system
13. **Local Context Integration** - Full integration with subjects/modules
14. **Play-Based Learning Tracking** - Fase A specific

#### Frontend:
11. **ILP Management Interface** - Per-student ILP
12. **DI Integration in Modules** - Differentiation panel
13. **Context Integration Dashboard** - Utilization tracking
14. **Play-Based Learning Tools** - Fase A specific tools

### 🟢 **LOW PRIORITY (Phase 4 - Weeks 13-16)**

#### Backend:
15. **Parent-Teacher Partnership** - Partnership tracking
16. **Character Intervention System** - Recommendation engine
17. **Simplified Peer Assessment** - SD-appropriate peer assessment

#### Frontend:
15. **Parent Partnership Interface** - Communication tools
16. **Character Intervention Dashboard** - Recommendation UI
17. **Peer Assessment Tools** - Simplified peer assessment UI

---

## 🎯 **SUCCESS CRITERIA PER PHASE**

### Phase 1 Success (Foundation):
- ✅ SD-only phases (A, B, C) validated
- ✅ 4 olah aspects fully implemented and integrated
- ✅ 3 learning principles fully implemented and integrated
- ✅ 8 profile dimensions correctly configured
- ✅ 4 framework elements properly classified

### Phase 2 Success (SD Specifics):
- ✅ Learning experience progression tracked
- ✅ Foundational skills (literasi-numerasi) assessed
- ✅ Reading literacy progression monitored
- ✅ Age-appropriate assessments implemented
- ✅ Curriculum types classified correctly

### Phase 3 Success (Enhancement):
- ✅ Individual learning plans created and tracked
- ✅ Differentiated instruction implemented
- ✅ Local context integrated into learning
- ✅ Play-based learning tracked for Fase A

### Phase 4 Success (Optimization):
- ✅ Parent partnerships tracked and managed
- ✅ Character interventions recommended and tracked
- ✅ Peer assessment tools available

---

## 📊 **RESOURCE ESTIMATION**

### Backend Development:
- **Phase 1:** ~40 hours (5 modules + updates)
- **Phase 2:** ~50 hours (5 complex modules)
- **Phase 3:** ~40 hours (4 enhancement modules)
- **Phase 4:** ~30 hours (3 optimization modules)
- **Total Backend:** ~160 hours

### Frontend Development:
- **Phase 1:** ~30 hours (5 pages/updates)
- **Phase 2:** ~40 hours (5 major UI components)
- **Phase 3:** ~35 hours (4 enhancement interfaces)
- **Phase 4:** ~25 hours (3 optimization interfaces)
- **Total Frontend:** ~130 hours

### Testing & Integration:
- **Unit Testing:** ~20 hours
- **Integration Testing:** ~15 hours
- **UI/UX Testing:** ~10 hours
- **Total Testing:** ~45 hours

### **TOTAL ESTIMATED EFFORT:** ~335 hours (~8-10 weeks with 2 developers)

---

**Analysis Date:** 2024-05-24
**Analyst:** Devin AI Agent
**Document Version:** 1.0
**Scope:** SD Only - UPT SDI Bonerate No. 85 Kepulauan Selayar
**Focus:** Feature gaps and implementation priorities