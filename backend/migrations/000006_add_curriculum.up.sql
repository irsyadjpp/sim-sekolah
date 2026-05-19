-- 0. Drop old KSP tables if they exist
DROP TABLE IF EXISTS trx_ksp_chapter CASCADE;
DROP TABLE IF EXISTS trx_ksp_document CASCADE;

-- 1. Table Header: School Curriculum Document
-- Represents the core curriculum document per academic year for a school
CREATE TABLE trx_curriculum_document (
    id uuid DEFAULT uuid_generate_v4() NOT NULL,
    academic_year_id uuid NOT NULL,
    school_id uuid NOT NULL,
    status varchar(20) DEFAULT 'DRAFT' NOT NULL, -- 'DRAFT', 'REVIEW', 'FINAL'
    created_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
    updated_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
    
    CONSTRAINT trx_curriculum_document_pkey PRIMARY KEY (id),
    CONSTRAINT fk_curriculum_doc_academic_year FOREIGN KEY (academic_year_id) REFERENCES master_academic_year(id),
    CONSTRAINT fk_curriculum_doc_school FOREIGN KEY (school_id) REFERENCES master_school(id) ON DELETE CASCADE,
    -- Business Validation: Only 1 curriculum document allowed per school per academic year
    CONSTRAINT uni_curriculum_school_year UNIQUE (academic_year_id, school_id),
    CONSTRAINT chk_curriculum_status CHECK (status IN ('DRAFT', 'REVIEW', 'FINAL'))
);
CREATE INDEX idx_curriculum_doc_status ON trx_curriculum_document (status);

-- 2. Table Detail: School Curriculum Chapter
-- Stores the HTML content for each chapter (Bab I s.d Bab V) compiled by the system or edited by user
CREATE TABLE trx_curriculum_chapter (
    id uuid DEFAULT uuid_generate_v4() NOT NULL,
    curriculum_document_id uuid NOT NULL,
    chapter_number int2 NOT NULL, -- 1 = Characteristics, 2 = Vision & Mission, 3 = Learning Structure, 4 = Classroom Planning, 5 = System Evaluation
    title varchar(150) NOT NULL,
    content text NULL, -- Stores rich text/HTML format
    updated_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
    
    CONSTRAINT trx_curriculum_chapter_pkey PRIMARY KEY (id),
    CONSTRAINT fk_curriculum_chapter_doc FOREIGN KEY (curriculum_document_id) REFERENCES trx_curriculum_document(id) ON DELETE CASCADE,
    -- Business Validation: Chapter number must be unique within a single curriculum document
    CONSTRAINT uni_curriculum_doc_chapter UNIQUE (curriculum_document_id, chapter_number),
    CONSTRAINT chk_chapter_number CHECK (chapter_number BETWEEN 1 AND 5)
);

-- 3. Update vw_dashboard_operator_kelengkapan_data to include school_id
DROP VIEW IF EXISTS public.vw_dashboard_operator_kelengkapan_data;
CREATE VIEW public.vw_dashboard_operator_kelengkapan_data AS
 SELECT sch.id AS school_id,
        sch.school_name,
        CASE
            WHEN ((sch.vision IS NOT NULL) AND (sch.mission IS NOT NULL)) THEN 100
            ELSE 0
        END AS persentase_profil_dasar,
        CASE
            WHEN (count(DISTINCT t.id) > 0) THEN 100
            ELSE 0
        END AS persentase_data_guru,
        CASE
            WHEN (count(DISTINCT s.id) > 0) THEN 100
            ELSE 0
        END AS persentase_data_siswa,
        CASE
            WHEN (count(DISTINCT lc.id) > 0) THEN 100
            ELSE 0
        END AS persentase_karakteristik_lokal
   FROM (((public.master_school sch
     LEFT JOIN public.master_teacher t ON ((sch.id = t.school_id)))
     LEFT JOIN public.master_student s ON ((sch.id = s.school_id)))
     LEFT JOIN public.master_local_context lc ON (((sch.id)::text = lc.school_id)))
  GROUP BY sch.id, sch.school_name, sch.vision, sch.mission;
