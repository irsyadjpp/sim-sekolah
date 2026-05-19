-- Revert the view back to its original state (without school_id)
CREATE OR REPLACE VIEW public.vw_dashboard_operator_kelengkapan_data AS
 SELECT sch.school_name,
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
  GROUP BY sch.school_name, sch.vision, sch.mission;

-- Drop Curriculum tables
DROP TABLE IF EXISTS trx_curriculum_chapter CASCADE;
DROP TABLE IF EXISTS trx_curriculum_document CASCADE;

-- Recreate old KSP tables
CREATE TABLE trx_ksp_document (
    id uuid DEFAULT uuid_generate_v4() NOT NULL,
    academic_year_id uuid NOT NULL,
    school_id uuid NOT NULL,
    status varchar(20) DEFAULT 'DRAFT' NOT NULL,
    created_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
    updated_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
    CONSTRAINT trx_ksp_document_pkey PRIMARY KEY (id)
);

CREATE TABLE trx_ksp_chapter (
    id uuid DEFAULT uuid_generate_v4() NOT NULL,
    ksp_document_id uuid NOT NULL,
    chapter_number int2 NOT NULL,
    title varchar(100) NOT NULL,
    content text NULL,
    updated_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
    CONSTRAINT trx_ksp_chapter_pkey PRIMARY KEY (id)
);
