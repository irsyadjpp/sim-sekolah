SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;
COMMENT ON SCHEMA public IS '';
CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;
COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';
SET default_tablespace = '';
SET default_table_access_method = heap;
CREATE TABLE public.auth_password_reset_token (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id text,
    token text,
    expired_at timestamp with time zone,
    created_at timestamp with time zone
);
CREATE TABLE public.auth_refresh_token (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id text,
    token text,
    expired_at timestamp with time zone,
    created_at timestamp with time zone
);
CREATE TABLE public.auth_role (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    role_name text,
    created_at timestamp with time zone
);
CREATE TABLE public.auth_user (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    teacher_id uuid,
    student_id uuid,
    full_name text,
    username text,
    email text,
    password_hash text,
    account_non_expired boolean DEFAULT true,
    account_non_locked boolean DEFAULT true,
    credentials_non_expired boolean DEFAULT true,
    is_enabled boolean DEFAULT true,
    last_login timestamp with time zone,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    theme_color text DEFAULT 'theme-purple'::text,
    theme_mode text DEFAULT 'system'::text,
    content_type text DEFAULT 'boxed'::text,
    left_menu_type text DEFAULT 'comfort'::text,
    two_factor_enabled boolean DEFAULT false,
    email_notifications boolean DEFAULT true,
    push_notifications boolean DEFAULT true
);
CREATE TABLE public.auth_user_role (
    user_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    role_id uuid DEFAULT public.uuid_generate_v4() NOT NULL
);
CREATE TABLE public.cur_cp_detail (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    learning_outcome_id uuid,
    element_id uuid,
    sub_code text,
    detail_text text,
    sequence_no bigint DEFAULT 1,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    created_by text,
    updated_by text,
    deleted_by text
);
CREATE TABLE public.cur_learning_objective (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    learning_outcome_id uuid NOT NULL,
    description text NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    created_by text,
    updated_by text,
    deleted_by text
);
CREATE TABLE public.cur_learning_outcome (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    phase_id uuid,
    subject_id uuid,
    cp_code text,
    outcome_text text,
    year_sk text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    created_by text,
    updated_by text,
    deleted_by text
);
CREATE TABLE public.dl_assessment_level (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    level_code text NOT NULL,
    description text NOT NULL,
    pisa_level text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    created_by text,
    updated_by text,
    deleted_by text
);
CREATE TABLE public.dl_cognitive_stage (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    stage_order bigint NOT NULL,
    stage_name text NOT NULL,
    operational_verbs text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    created_by text,
    updated_by text,
    deleted_by text
);
CREATE TABLE public.dl_design_element (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    design_element_name text NOT NULL,
    description text,
    is_active boolean DEFAULT true,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    created_by text,
    updated_by text,
    deleted_by text
);
CREATE TABLE public.master_academic_year (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    year_name character varying(20) NOT NULL,
    semester character varying(10) NOT NULL,
    is_active boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE public.master_classroom (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    school_id uuid NOT NULL,
    academic_year_id uuid NOT NULL,
    grade_id uuid NOT NULL,
    classroom_name character varying(50) NOT NULL,
    homeroom_teacher_id uuid,
    class_characteristics text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    phase_id uuid NOT NULL,
    max_quota smallint DEFAULT 28
);
CREATE TABLE public.master_grade (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    phase_id uuid NOT NULL,
    grade_level smallint NOT NULL,
    grade_name character varying(20) NOT NULL
);
CREATE TABLE public.master_local_context (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    school_id text,
    category_id uuid,
    title text,
    description text,
    location text,
    scope_type text,
    is_active boolean DEFAULT true,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    created_by text,
    updated_by text,
    deleted_by text
);
CREATE TABLE public.master_local_context_category (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    category_code text,
    category_name text,
    description text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    created_by text,
    updated_by text,
    deleted_by text
);
CREATE TABLE public.master_phase (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    phase_code text,
    phase_name text,
    description text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    created_by text,
    updated_by text,
    deleted_by text
);
CREATE TABLE public.master_profile_dimension (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    dimension_code text NOT NULL,
    dimension_name text NOT NULL,
    description text,
    is_active boolean DEFAULT true,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    created_by text,
    updated_by text,
    deleted_by text
);
CREATE TABLE public.master_school (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    npsn character varying(20),
    school_name character varying(255) NOT NULL,
    address text,
    phone character varying(30),
    email character varying(100),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    electricity_capacity bigint,
    signal_status character varying(50),
    vision text,
    mission text,
    district character varying(100),
    regency character varying(100),
    province character varying(100),
    status character varying(20),
    accreditation character varying(5),
    principal_name character varying(255),
    operator_name character varying(255),
    operating_hours character varying(255),
    latitude numeric(10,8),
    longitude numeric(11,8),
    total_students bigint,
    male_students bigint,
    female_students bigint,
    total_teachers bigint,
    male_teachers bigint,
    female_teachers bigint,
    curriculum character varying(100),
    water_source character varying(100),
    internet_access character varying(100),
    bos_status character varying(100),
    infrastructure_summary text,
    vision_meaning text,
    goal text,
    graduation_data character varying(255),
    teacher_pns_count bigint,
    teacher_honor_count bigint,
    teacher_certified_count character varying(50),
    teacher_qualified_count character varying(50),
    classroom_count bigint,
    classroom_good_count bigint,
    classroom_damaged_count bigint,
    library_count bigint,
    toilet_student_count bigint,
    toilet_teacher_count bigint,
    student_religion character varying(100),
    student_ratio character varying(100),
    education_form character varying(100),
    country character varying(100),
    total_staff bigint,
    lab_count bigint,
    rombel_count bigint,
    sync_system character varying(255),
    sync_compliance character varying(255)
);
CREATE TABLE public.master_student (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    school_id uuid NOT NULL,
    full_name character varying(255) NOT NULL,
    nis character varying(20),
    nisn character varying(20),
    gender character(1),
    birth_place character varying(100),
    birth_date date,
    religion character varying(20),
    nationality character varying(50) DEFAULT 'WNI'::character varying,
    child_order smallint DEFAULT 1,
    siblings smallint DEFAULT 0,
    photo_url text,
    nik character varying(20),
    family_card_number character varying(20),
    birth_certificate character varying(50),
    k_ip_number character varying(30),
    full_address text,
    rtrw character varying(10),
    village character varying(100),
    district character varying(100),
    regency character varying(100),
    province character varying(100),
    postal_code character varying(10),
    coordinates character varying(50),
    enrollment_year smallint,
    curriculum character varying(50),
    student_status character varying(20) DEFAULT 'Aktif'::character varying,
    entry_path character varying(50),
    previous_school character varying(255),
    exam_number character varying(30),
    blood_type character varying(5),
    height numeric(5,2) DEFAULT 0,
    weight numeric(5,2) DEFAULT 0,
    medical_history text,
    disability character varying(100),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE public.master_student_parent (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    student_id uuid NOT NULL,
    parent_type character varying(10) NOT NULL,
    full_name character varying(255),
    nik character varying(20),
    education character varying(20),
    occupation character varying(100),
    income bigint DEFAULT 0,
    phone character varying(30)
);
CREATE TABLE public.master_subject (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    subject_code character varying(20) NOT NULL,
    subject_name character varying(255) NOT NULL,
    rational text,
    goals text,
    characteristics text,
    is_active boolean DEFAULT true,
    level text,
    abbreviation text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    created_by text,
    updated_by text,
    deleted_by text
);
CREATE TABLE public.master_subject_characteristic (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    subject_id uuid,
    description text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    created_by text,
    updated_by text,
    deleted_by text
);
CREATE TABLE public.master_subject_element (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    subject_id uuid,
    point_id uuid,
    element_name text,
    abbreviation text,
    element_code text,
    description text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    created_by text,
    updated_by text,
    deleted_by text
);
CREATE TABLE public.master_teacher (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    school_id uuid NOT NULL,
    full_name character varying(255) NOT NULL,
    gender character(1),
    birth_place character varying(100),
    birth_date date,
    nik character varying(20),
    nuptk character varying(20),
    niynigk character varying(30),
    religion character varying(20),
    nationality character varying(50) DEFAULT 'WNI'::character varying,
    photo_url text,
    full_address text,
    hamlet character varying(100),
    rtrw character varying(10),
    village character varying(100),
    district character varying(100),
    regency character varying(100),
    province character varying(100),
    postal_code character varying(10),
    phone character varying(30),
    email character varying(100),
    n_ip character varying(30),
    employment_status character varying(20),
    start_teaching_date date,
    appointment_decree character varying(100),
    salary_source character varying(50),
    teaching_subject character varying(255),
    additional_position character varying(100),
    teaching_hours smallint DEFAULT 0,
    is_active boolean DEFAULT true,
    last_education character varying(20),
    major character varying(100),
    university_name character varying(255),
    graduation_year smallint,
    is_certified boolean DEFAULT false,
    certificate_number character varying(50),
    teaching_preference text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE public.sys_automation_queue (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    task_type character varying(50) NOT NULL,
    reference_id uuid NOT NULL,
    user_id uuid NOT NULL,
    status character varying(20) DEFAULT 'ANTREAN'::character varying NOT NULL,
    error_log text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE public.sys_server_telemetry (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    cpu_usage_percent numeric(5,2) NOT NULL,
    ram_usage_percent numeric(5,2) NOT NULL,
    storage_free_gb numeric(10,2) NOT NULL,
    server_temperature_c numeric(4,1),
    engine_status character varying(20) DEFAULT 'RUNNING'::character varying NOT NULL,
    logged_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE public.trx_academic_score (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    student_id uuid NOT NULL,
    question_id uuid NOT NULL,
    assessment_type character varying(20) NOT NULL,
    score numeric(5,2) DEFAULT 0,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    created_by text,
    updated_by text,
    deleted_by text
);
CREATE TABLE public.trx_assessment (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    teaching_assignment_id uuid NOT NULL,
    assessment_name character varying(100) NOT NULL,
    assessment_type character varying(20) NOT NULL,
    assessment_date date NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE public.trx_assessment_p5 (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    student_id uuid NOT NULL,
    project_id uuid NOT NULL,
    dimension_id uuid NOT NULL,
    capaian character varying(50) NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    created_by text,
    updated_by text,
    deleted_by text
);
CREATE TABLE public.trx_assessment_score (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    assessment_id uuid NOT NULL,
    student_id uuid NOT NULL,
    score numeric(5,2) DEFAULT 0,
    notes text
);
CREATE TABLE public.trx_atp (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    classroom_id uuid NOT NULL,
    subject_id uuid NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    created_by text,
    updated_by text,
    deleted_by text
);
CREATE TABLE public.trx_atp_detail (
    atp_id uuid NOT NULL,
    objective_id uuid NOT NULL,
    sequence bigint NOT NULL
);
CREATE TABLE public.trx_attendance (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    student_id uuid NOT NULL,
    classroom_id uuid NOT NULL,
    semester character varying(10) NOT NULL,
    sick bigint DEFAULT 0,
    permission bigint DEFAULT 0,
    unexcused bigint DEFAULT 0,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    created_by text,
    updated_by text,
    deleted_by text
);
CREATE TABLE public.trx_enrollment (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    classroom_id uuid NOT NULL,
    student_id uuid NOT NULL,
    enrollment_date date DEFAULT CURRENT_DATE
);
CREATE TABLE public.trx_ksp_chapter (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    ksp_document_id uuid NOT NULL,
    chapter_number smallint NOT NULL,
    title character varying(100) NOT NULL,
    content text,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE public.trx_ksp_document (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    academic_year_id uuid NOT NULL,
    school_id uuid NOT NULL,
    status character varying(20) DEFAULT 'DRAFT'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE public.trx_module_element_mapping (
    teaching_module_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    design_element_id uuid DEFAULT public.uuid_generate_v4() NOT NULL
);
CREATE TABLE public.trx_ppdb_admission_path (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name character varying(50) NOT NULL,
    description text,
    is_active boolean DEFAULT true
);
CREATE TABLE public.trx_ppdb_applicant (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    registration_no character varying(50) NOT NULL,
    school_year_id uuid NOT NULL,
    admission_path_id uuid NOT NULL,
    full_name character varying(150) NOT NULL,
    nik character varying(16) NOT NULL,
    nisn character varying(20),
    birth_place character varying(100) NOT NULL,
    birth_date date NOT NULL,
    gender character varying(1) NOT NULL,
    religion character varying(20) NOT NULL,
    address text NOT NULL,
    village character varying(100),
    district character varying(100),
    regency character varying(100),
    province character varying(100),
    postal_code character varying(10),
    distance_to_school_km numeric(5,2),
    status character varying(50) DEFAULT 'Submitted'::character varying,
    accepted_at timestamp without time zone,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE public.trx_ppdb_document (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    applicant_id uuid NOT NULL,
    document_type character varying(50) NOT NULL,
    file_path text NOT NULL,
    uploaded_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE public.trx_ppdb_parent (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    applicant_id uuid NOT NULL,
    father_name character varying(150),
    father_nik character varying(16),
    father_occupation character varying(100),
    mother_name character varying(150),
    mother_nik character varying(16),
    mother_occupation character varying(100),
    phone_number character varying(20) NOT NULL
);
CREATE TABLE public.trx_ppdb_verification_log (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    applicant_id uuid NOT NULL,
    verified_by uuid,
    status_changed_to character varying(50) NOT NULL,
    notes text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE public.trx_project_dimension_mapping (
    project_module_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    profile_dimension_id uuid DEFAULT public.uuid_generate_v4() NOT NULL
);
CREATE TABLE public.trx_project_module (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    title character varying(150) NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    created_by text,
    updated_by text,
    deleted_by text
);
CREATE TABLE public.trx_question_bank (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    module_id uuid NOT NULL,
    question text NOT NULL,
    level_id uuid NOT NULL,
    tingkat character varying(10) NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    created_by text,
    updated_by text,
    deleted_by text
);
CREATE TABLE public.trx_report (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    classroom_id uuid NOT NULL,
    student_id uuid NOT NULL,
    semester character varying(10) NOT NULL,
    homeroom_notes text,
    student_reflection text,
    is_finalized boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    academic_narrative_ai text,
    character_narrative_ai text,
    status character varying(20) DEFAULT 'DRAFT'::character varying
);
CREATE TABLE public.trx_report_attendance (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    report_id uuid NOT NULL,
    sick bigint DEFAULT 0,
    permission bigint DEFAULT 0,
    unexcused bigint DEFAULT 0
);
CREATE TABLE public.trx_report_deep_learning (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    report_id uuid NOT NULL,
    aspect character varying(100) NOT NULL,
    observation_notes text
);
CREATE TABLE public.trx_report_extracurricular (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    report_id uuid NOT NULL,
    activity_name character varying(255) NOT NULL,
    predicate character varying(50),
    description text
);
CREATE TABLE public.trx_report_p5 (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    report_id uuid NOT NULL,
    theme character varying(255) NOT NULL,
    description text,
    predicate character varying(50)
);
CREATE TABLE public.trx_report_score (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    report_id uuid NOT NULL,
    subject_id uuid NOT NULL,
    final_score numeric(5,2) DEFAULT 0,
    competency_achieved text,
    competency_needs_improvement text
);
CREATE TABLE public.trx_teaching_assignment (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    classroom_id uuid NOT NULL,
    teacher_id uuid NOT NULL,
    subject_id uuid NOT NULL,
    assigned_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE public.trx_teaching_module (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    atp_id uuid NOT NULL,
    title character varying(150) NOT NULL,
    status character varying(20) DEFAULT 'DRAFT'::character varying,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    created_by text,
    updated_by text,
    deleted_by text
);
CREATE TABLE public.trx_teaching_module_activity (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    module_id uuid NOT NULL,
    stage_id uuid NOT NULL,
    description text NOT NULL
);
CREATE VIEW public.vw_dashboard_guru_modul_compliance AS
 SELECT tm.id AS teaching_module_id,
    tm.title AS judul_modul,
    t.full_name AS nama_guru,
    sub.subject_name,
    count(DISTINCT tma.stage_id) AS jumlah_tahap_terpenuhi,
        CASE
            WHEN (count(DISTINCT tma.stage_id) >= 3) THEN 'PATUH'::text
            ELSE 'BELUM LENGKAP (Wajib Refleksi)'::text
        END AS status_kepatuhan
   FROM ((((((public.trx_teaching_module tm
     JOIN public.trx_atp atp ON ((tm.atp_id = atp.id)))
     JOIN public.master_classroom c ON ((atp.classroom_id = c.id)))
     JOIN public.trx_teaching_assignment ta ON (((c.id = ta.classroom_id) AND (atp.subject_id = ta.subject_id))))
     JOIN public.master_teacher t ON ((ta.teacher_id = t.id)))
     JOIN public.master_subject sub ON ((atp.subject_id = sub.id)))
     LEFT JOIN public.trx_teaching_module_activity tma ON ((tm.id = tma.module_id)))
  GROUP BY tm.id, tm.title, t.full_name, sub.subject_name;
CREATE VIEW public.vw_dashboard_guru_pantauan_siswa AS
 SELECT s.id AS student_id,
    s.full_name AS nama_siswa,
    c.classroom_name,
    ((COALESCE(att.sick, (0)::bigint) + COALESCE(att.permission, (0)::bigint)) + COALESCE(att.unexcused, (0)::bigint)) AS total_absen,
    round(avg(ascore.score), 2) AS rata_rata_akademik,
        CASE
            WHEN ((((COALESCE(att.sick, (0)::bigint) + COALESCE(att.permission, (0)::bigint)) + COALESCE(att.unexcused, (0)::bigint)) >= 5) OR (avg(ascore.score) < (65)::numeric)) THEN 'PERLU INTERVENSI'::text
            ELSE 'AMAN'::text
        END AS status_peringatan
   FROM ((((public.master_student s
     JOIN public.trx_enrollment e ON ((s.id = e.student_id)))
     JOIN public.master_classroom c ON ((e.classroom_id = c.id)))
     LEFT JOIN public.trx_attendance att ON (((s.id = att.student_id) AND (c.id = att.classroom_id))))
     LEFT JOIN public.trx_academic_score ascore ON ((s.id = ascore.student_id)))
  WHERE (c.academic_year_id = ( SELECT master_academic_year.id
           FROM public.master_academic_year
          WHERE (master_academic_year.is_active = true)
         LIMIT 1))
  GROUP BY s.id, s.full_name, c.classroom_name, att.sick, att.permission, att.unexcused;
CREATE VIEW public.vw_dashboard_operator_kelengkapan_data AS
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
CREATE VIEW public.vw_dashboard_pimpinan_kognitif AS
 SELECT c.id AS classroom_id,
    c.classroom_name,
    sub.subject_name,
    qb.tingkat AS tingkat_kognitif,
    round(avg(ascore.score), 2) AS rata_rata_nilai,
    count(ascore.id) AS total_sampel_jawaban
   FROM (((((public.trx_academic_score ascore
     JOIN public.trx_question_bank qb ON ((ascore.question_id = qb.id)))
     JOIN public.trx_teaching_module tm ON ((qb.module_id = tm.id)))
     JOIN public.trx_atp atp ON ((tm.atp_id = atp.id)))
     JOIN public.master_classroom c ON ((atp.classroom_id = c.id)))
     JOIN public.master_subject sub ON ((atp.subject_id = sub.id)))
  WHERE (c.academic_year_id = ( SELECT master_academic_year.id
           FROM public.master_academic_year
          WHERE (master_academic_year.is_active = true)
         LIMIT 1))
  GROUP BY c.id, c.classroom_name, sub.subject_name, qb.tingkat;
CREATE VIEW public.vw_dashboard_pimpinan_ksp AS
 SELECT kd.id AS ksp_document_id,
    ay.year_name,
    ay.semester,
    kd.status AS status_dokumen,
    count(kc.id) AS jumlah_bab_terisi,
    round((((count(kc.id))::numeric / 5.0) * (100)::numeric), 2) AS persentase_selesai
   FROM ((public.trx_ksp_document kd
     JOIN public.master_academic_year ay ON ((kd.academic_year_id = ay.id)))
     LEFT JOIN public.trx_ksp_chapter kc ON ((kd.id = kc.ksp_document_id)))
  GROUP BY kd.id, ay.year_name, ay.semester, kd.status;
CREATE VIEW public.vw_dashboard_pimpinan_profil_p5 AS
 SELECT pd.dimension_name,
    ap5.capaian AS predikat_rubrik,
    count(ap5.id) AS jumlah_siswa
   FROM (public.trx_assessment_p5 ap5
     JOIN public.master_profile_dimension pd ON ((ap5.dimension_id = pd.id)))
  GROUP BY pd.dimension_name, ap5.capaian;
ALTER TABLE ONLY public.auth_password_reset_token
    ADD CONSTRAINT auth_password_reset_token_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.auth_refresh_token
    ADD CONSTRAINT auth_refresh_token_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.auth_role
    ADD CONSTRAINT auth_role_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.auth_user_role
    ADD CONSTRAINT auth_user_role_pkey PRIMARY KEY (user_id, role_id);
ALTER TABLE ONLY public.cur_cp_detail
    ADD CONSTRAINT cur_cp_detail_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.cur_learning_objective
    ADD CONSTRAINT cur_learning_objective_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.cur_learning_outcome
    ADD CONSTRAINT cur_learning_outcome_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.dl_assessment_level
    ADD CONSTRAINT dl_assessment_level_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.dl_cognitive_stage
    ADD CONSTRAINT dl_cognitive_stage_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.dl_design_element
    ADD CONSTRAINT dl_design_element_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.master_academic_year
    ADD CONSTRAINT master_academic_year_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.master_classroom
    ADD CONSTRAINT master_classroom_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.master_grade
    ADD CONSTRAINT master_grade_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.master_local_context_category
    ADD CONSTRAINT master_local_context_category_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.master_local_context
    ADD CONSTRAINT master_local_context_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.master_phase
    ADD CONSTRAINT master_phase_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.master_profile_dimension
    ADD CONSTRAINT master_profile_dimension_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.master_school
    ADD CONSTRAINT master_school_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.master_student_parent
    ADD CONSTRAINT master_student_parent_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.master_student
    ADD CONSTRAINT master_student_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.master_subject_characteristic
    ADD CONSTRAINT master_subject_characteristic_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.master_subject_element
    ADD CONSTRAINT master_subject_element_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.master_subject
    ADD CONSTRAINT master_subject_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.master_teacher
    ADD CONSTRAINT master_teacher_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.sys_automation_queue
    ADD CONSTRAINT sys_automation_queue_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.sys_server_telemetry
    ADD CONSTRAINT sys_server_telemetry_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_academic_score
    ADD CONSTRAINT trx_academic_score_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_assessment_p5
    ADD CONSTRAINT trx_assessment_p5_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_assessment
    ADD CONSTRAINT trx_assessment_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_assessment_score
    ADD CONSTRAINT trx_assessment_score_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_atp_detail
    ADD CONSTRAINT trx_atp_detail_pkey PRIMARY KEY (atp_id, objective_id);
ALTER TABLE ONLY public.trx_atp
    ADD CONSTRAINT trx_atp_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_attendance
    ADD CONSTRAINT trx_attendance_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_enrollment
    ADD CONSTRAINT trx_enrollment_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_ksp_chapter
    ADD CONSTRAINT trx_ksp_chapter_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_ksp_document
    ADD CONSTRAINT trx_ksp_document_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_module_element_mapping
    ADD CONSTRAINT trx_module_element_mapping_pkey PRIMARY KEY (teaching_module_id, design_element_id);
ALTER TABLE ONLY public.trx_ppdb_admission_path
    ADD CONSTRAINT trx_ppdb_admission_path_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_ppdb_applicant
    ADD CONSTRAINT trx_ppdb_applicant_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_ppdb_document
    ADD CONSTRAINT trx_ppdb_document_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_ppdb_parent
    ADD CONSTRAINT trx_ppdb_parent_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_ppdb_verification_log
    ADD CONSTRAINT trx_ppdb_verification_log_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_project_dimension_mapping
    ADD CONSTRAINT trx_project_dimension_mapping_pkey PRIMARY KEY (project_module_id, profile_dimension_id);
ALTER TABLE ONLY public.trx_project_module
    ADD CONSTRAINT trx_project_module_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_question_bank
    ADD CONSTRAINT trx_question_bank_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_report_attendance
    ADD CONSTRAINT trx_report_attendance_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_report_deep_learning
    ADD CONSTRAINT trx_report_deep_learning_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_report_extracurricular
    ADD CONSTRAINT trx_report_extracurricular_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_report_p5
    ADD CONSTRAINT trx_report_p5_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_report
    ADD CONSTRAINT trx_report_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_report_score
    ADD CONSTRAINT trx_report_score_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_teaching_assignment
    ADD CONSTRAINT trx_teaching_assignment_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_teaching_module_activity
    ADD CONSTRAINT trx_teaching_module_activity_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.trx_teaching_module
    ADD CONSTRAINT trx_teaching_module_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.auth_role
    ADD CONSTRAINT uni_auth_role_role_name UNIQUE (role_name);
ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT uni_auth_user_email UNIQUE (email);
ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT uni_auth_user_username UNIQUE (username);
ALTER TABLE ONLY public.master_local_context_category
    ADD CONSTRAINT uni_master_local_context_category_category_code UNIQUE (category_code);
ALTER TABLE ONLY public.trx_ppdb_admission_path
    ADD CONSTRAINT uni_trx_ppdb_admission_path_name UNIQUE (name);
ALTER TABLE ONLY public.trx_ppdb_applicant
    ADD CONSTRAINT uni_trx_ppdb_applicant_nik UNIQUE (nik);
ALTER TABLE ONLY public.trx_ppdb_applicant
    ADD CONSTRAINT uni_trx_ppdb_applicant_registration_no UNIQUE (registration_no);
CREATE UNIQUE INDEX idx_active_homeroom ON public.master_classroom USING btree (academic_year_id, homeroom_teacher_id);
CREATE UNIQUE INDEX idx_app_doc ON public.trx_ppdb_document USING btree (applicant_id, document_type);
CREATE UNIQUE INDEX idx_assessment_student ON public.trx_assessment_score USING btree (assessment_id, student_id);
CREATE UNIQUE INDEX idx_attendance ON public.trx_attendance USING btree (student_id, classroom_id, semester);
CREATE INDEX idx_cur_cp_detail_deleted_at ON public.cur_cp_detail USING btree (deleted_at);
CREATE INDEX idx_cur_learning_objective_deleted_at ON public.cur_learning_objective USING btree (deleted_at);
CREATE UNIQUE INDEX idx_cur_learning_outcome_cp_code ON public.cur_learning_outcome USING btree (cp_code);
CREATE INDEX idx_cur_learning_outcome_deleted_at ON public.cur_learning_outcome USING btree (deleted_at);
CREATE INDEX idx_cur_learning_outcome_phase_id ON public.cur_learning_outcome USING btree (phase_id);
CREATE INDEX idx_cur_learning_outcome_subject_id ON public.cur_learning_outcome USING btree (subject_id);
CREATE INDEX idx_cur_learning_outcome_year_sk ON public.cur_learning_outcome USING btree (year_sk);
CREATE INDEX idx_dl_assessment_level_deleted_at ON public.dl_assessment_level USING btree (deleted_at);
CREATE UNIQUE INDEX idx_dl_assessment_level_level_code ON public.dl_assessment_level USING btree (level_code);
CREATE INDEX idx_dl_cognitive_stage_deleted_at ON public.dl_cognitive_stage USING btree (deleted_at);
CREATE UNIQUE INDEX idx_dl_cognitive_stage_name ON public.dl_cognitive_stage USING btree (stage_name);
CREATE INDEX idx_dl_design_element_deleted_at ON public.dl_design_element USING btree (deleted_at);
CREATE UNIQUE INDEX idx_dl_design_element_name ON public.dl_design_element USING btree (design_element_name);
CREATE UNIQUE INDEX idx_enrollment ON public.trx_enrollment USING btree (classroom_id, student_id);
CREATE UNIQUE INDEX idx_ksp_chapter ON public.trx_ksp_chapter USING btree (ksp_document_id, chapter_number);
CREATE UNIQUE INDEX idx_ksp_year ON public.trx_ksp_document USING btree (academic_year_id);
CREATE INDEX idx_master_local_context_category_deleted_at ON public.master_local_context_category USING btree (deleted_at);
CREATE INDEX idx_master_local_context_deleted_at ON public.master_local_context USING btree (deleted_at);
CREATE UNIQUE INDEX idx_master_phase_code ON public.master_phase USING btree (phase_code);
CREATE INDEX idx_master_phase_deleted_at ON public.master_phase USING btree (deleted_at);
CREATE UNIQUE INDEX idx_master_phase_name ON public.master_phase USING btree (phase_name);
CREATE INDEX idx_master_profile_dimension_deleted_at ON public.master_profile_dimension USING btree (deleted_at);
CREATE UNIQUE INDEX idx_master_profile_dimension_dimension_code ON public.master_profile_dimension USING btree (dimension_code);
CREATE UNIQUE INDEX idx_master_school_npsn ON public.master_school USING btree (npsn);
CREATE UNIQUE INDEX idx_master_student_nik ON public.master_student USING btree (nik);
CREATE UNIQUE INDEX idx_master_student_nisn ON public.master_student USING btree (nisn);
CREATE INDEX idx_master_subject_characteristic_deleted_at ON public.master_subject_characteristic USING btree (deleted_at);
CREATE INDEX idx_master_subject_characteristic_subject_id ON public.master_subject_characteristic USING btree (subject_id);
CREATE INDEX idx_master_subject_deleted_at ON public.master_subject USING btree (deleted_at);
CREATE INDEX idx_master_subject_element_deleted_at ON public.master_subject_element USING btree (deleted_at);
CREATE INDEX idx_master_subject_element_point_id ON public.master_subject_element USING btree (point_id);
CREATE INDEX idx_master_subject_element_subject_id ON public.master_subject_element USING btree (subject_id);
CREATE UNIQUE INDEX idx_master_subject_subject_code ON public.master_subject USING btree (subject_code);
CREATE UNIQUE INDEX idx_master_subject_subject_name ON public.master_subject USING btree (subject_name);
CREATE UNIQUE INDEX idx_master_teacher_nik ON public.master_teacher USING btree (nik);
CREATE UNIQUE INDEX idx_master_teacher_nuptk ON public.master_teacher USING btree (nuptk);
CREATE UNIQUE INDEX idx_report_class_student_sem ON public.trx_report USING btree (classroom_id, student_id, semester);
CREATE UNIQUE INDEX idx_report_dl_aspect ON public.trx_report_deep_learning USING btree (report_id, aspect);
CREATE UNIQUE INDEX idx_report_extra_activity ON public.trx_report_extracurricular USING btree (report_id, activity_name);
CREATE UNIQUE INDEX idx_report_p5_theme ON public.trx_report_p5 USING btree (report_id, theme);
CREATE UNIQUE INDEX idx_report_subject ON public.trx_report_score USING btree (report_id, subject_id);
CREATE UNIQUE INDEX idx_single_active_year ON public.master_academic_year USING btree (is_active) WHERE (is_active = true);
CREATE INDEX idx_sys_queue_status ON public.sys_automation_queue USING btree (status);
CREATE INDEX idx_sys_telemetry_logged_at ON public.sys_server_telemetry USING btree (logged_at DESC);
CREATE INDEX idx_trx_academic_score_deleted_at ON public.trx_academic_score USING btree (deleted_at);
CREATE INDEX idx_trx_assessment_p5_deleted_at ON public.trx_assessment_p5 USING btree (deleted_at);
CREATE INDEX idx_trx_atp_deleted_at ON public.trx_atp USING btree (deleted_at);
CREATE INDEX idx_trx_attendance_deleted_at ON public.trx_attendance USING btree (deleted_at);
CREATE UNIQUE INDEX idx_trx_ppdb_parent_applicant_id ON public.trx_ppdb_parent USING btree (applicant_id);
CREATE INDEX idx_trx_project_module_deleted_at ON public.trx_project_module USING btree (deleted_at);
CREATE INDEX idx_trx_question_bank_deleted_at ON public.trx_question_bank USING btree (deleted_at);
CREATE UNIQUE INDEX idx_trx_report_attendance_report_id ON public.trx_report_attendance USING btree (report_id);
CREATE INDEX idx_trx_teaching_module_deleted_at ON public.trx_teaching_module USING btree (deleted_at);
ALTER TABLE ONLY public.auth_user_role
    ADD CONSTRAINT fk_auth_user_role_role FOREIGN KEY (role_id) REFERENCES public.auth_role(id);
ALTER TABLE ONLY public.auth_user_role
    ADD CONSTRAINT fk_auth_user_role_user FOREIGN KEY (user_id) REFERENCES public.auth_user(id);
ALTER TABLE ONLY public.cur_cp_detail
    ADD CONSTRAINT fk_cur_cp_detail_element FOREIGN KEY (element_id) REFERENCES public.master_subject_element(id);
ALTER TABLE ONLY public.cur_cp_detail
    ADD CONSTRAINT fk_cur_learning_outcome_details FOREIGN KEY (learning_outcome_id) REFERENCES public.cur_learning_outcome(id);
ALTER TABLE ONLY public.cur_learning_outcome
    ADD CONSTRAINT fk_cur_learning_outcome_phase FOREIGN KEY (phase_id) REFERENCES public.master_phase(id);
ALTER TABLE ONLY public.cur_learning_outcome
    ADD CONSTRAINT fk_cur_learning_outcome_subject FOREIGN KEY (subject_id) REFERENCES public.master_subject(id);
ALTER TABLE ONLY public.master_classroom
    ADD CONSTRAINT fk_master_classroom_academic_year FOREIGN KEY (academic_year_id) REFERENCES public.master_academic_year(id);
ALTER TABLE ONLY public.master_classroom
    ADD CONSTRAINT fk_master_classroom_grade FOREIGN KEY (grade_id) REFERENCES public.master_grade(id);
ALTER TABLE ONLY public.master_classroom
    ADD CONSTRAINT fk_master_classroom_homeroom FOREIGN KEY (homeroom_teacher_id) REFERENCES public.master_teacher(id);
ALTER TABLE ONLY public.master_classroom
    ADD CONSTRAINT fk_master_classroom_school FOREIGN KEY (school_id) REFERENCES public.master_school(id);
ALTER TABLE ONLY public.master_local_context
    ADD CONSTRAINT fk_master_local_context_category FOREIGN KEY (category_id) REFERENCES public.master_local_context_category(id);
ALTER TABLE ONLY public.master_student_parent
    ADD CONSTRAINT fk_master_student_parents FOREIGN KEY (student_id) REFERENCES public.master_student(id);
ALTER TABLE ONLY public.master_subject_element
    ADD CONSTRAINT fk_master_subject_characteristic_elements FOREIGN KEY (point_id) REFERENCES public.master_subject_characteristic(id);
ALTER TABLE ONLY public.master_subject_characteristic
    ADD CONSTRAINT fk_master_subject_characteristic_points FOREIGN KEY (subject_id) REFERENCES public.master_subject(id);
ALTER TABLE ONLY public.master_subject_element
    ADD CONSTRAINT fk_master_subject_elements FOREIGN KEY (subject_id) REFERENCES public.master_subject(id);
ALTER TABLE ONLY public.trx_academic_score
    ADD CONSTRAINT fk_trx_academic_score_question FOREIGN KEY (question_id) REFERENCES public.trx_question_bank(id);
ALTER TABLE ONLY public.trx_academic_score
    ADD CONSTRAINT fk_trx_academic_score_student FOREIGN KEY (student_id) REFERENCES public.master_student(id);
ALTER TABLE ONLY public.trx_assessment_p5
    ADD CONSTRAINT fk_trx_assessment_p5_student FOREIGN KEY (student_id) REFERENCES public.master_student(id);
ALTER TABLE ONLY public.trx_assessment_score
    ADD CONSTRAINT fk_trx_assessment_score_student FOREIGN KEY (student_id) REFERENCES public.master_student(id);
ALTER TABLE ONLY public.trx_assessment_score
    ADD CONSTRAINT fk_trx_assessment_scores FOREIGN KEY (assessment_id) REFERENCES public.trx_assessment(id);
ALTER TABLE ONLY public.trx_assessment
    ADD CONSTRAINT fk_trx_assessment_teaching_assignment FOREIGN KEY (teaching_assignment_id) REFERENCES public.trx_teaching_assignment(id);
ALTER TABLE ONLY public.trx_atp
    ADD CONSTRAINT fk_trx_atp_classroom FOREIGN KEY (classroom_id) REFERENCES public.master_classroom(id);
ALTER TABLE ONLY public.trx_atp_detail
    ADD CONSTRAINT fk_trx_atp_detail_objective FOREIGN KEY (objective_id) REFERENCES public.cur_learning_objective(id);
ALTER TABLE ONLY public.trx_atp_detail
    ADD CONSTRAINT fk_trx_atp_details FOREIGN KEY (atp_id) REFERENCES public.trx_atp(id);
ALTER TABLE ONLY public.trx_atp
    ADD CONSTRAINT fk_trx_atp_subject FOREIGN KEY (subject_id) REFERENCES public.master_subject(id);
ALTER TABLE ONLY public.trx_enrollment
    ADD CONSTRAINT fk_trx_enrollment_student FOREIGN KEY (student_id) REFERENCES public.master_student(id);
ALTER TABLE ONLY public.trx_ksp_document
    ADD CONSTRAINT fk_trx_ksp_document_academic_year FOREIGN KEY (academic_year_id) REFERENCES public.master_academic_year(id);
ALTER TABLE ONLY public.trx_ksp_chapter
    ADD CONSTRAINT fk_trx_ksp_document_chapters FOREIGN KEY (ksp_document_id) REFERENCES public.trx_ksp_document(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.trx_ksp_document
    ADD CONSTRAINT fk_trx_ksp_document_school FOREIGN KEY (school_id) REFERENCES public.master_school(id);
ALTER TABLE ONLY public.trx_module_element_mapping
    ADD CONSTRAINT fk_trx_module_element_mapping_design_element FOREIGN KEY (design_element_id) REFERENCES public.dl_design_element(id);
ALTER TABLE ONLY public.trx_module_element_mapping
    ADD CONSTRAINT fk_trx_module_element_mapping_teaching_module FOREIGN KEY (teaching_module_id) REFERENCES public.trx_teaching_module(id);
ALTER TABLE ONLY public.trx_ppdb_applicant
    ADD CONSTRAINT fk_trx_ppdb_applicant_admission_path FOREIGN KEY (admission_path_id) REFERENCES public.trx_ppdb_admission_path(id);
ALTER TABLE ONLY public.trx_ppdb_document
    ADD CONSTRAINT fk_trx_ppdb_applicant_documents FOREIGN KEY (applicant_id) REFERENCES public.trx_ppdb_applicant(id);
ALTER TABLE ONLY public.trx_ppdb_parent
    ADD CONSTRAINT fk_trx_ppdb_applicant_parents FOREIGN KEY (applicant_id) REFERENCES public.trx_ppdb_applicant(id);
ALTER TABLE ONLY public.trx_ppdb_applicant
    ADD CONSTRAINT fk_trx_ppdb_applicant_school_year FOREIGN KEY (school_year_id) REFERENCES public.master_academic_year(id);
ALTER TABLE ONLY public.trx_project_dimension_mapping
    ADD CONSTRAINT fk_trx_project_dimension_mapping_profile_dimension FOREIGN KEY (profile_dimension_id) REFERENCES public.master_profile_dimension(id);
ALTER TABLE ONLY public.trx_project_dimension_mapping
    ADD CONSTRAINT fk_trx_project_dimension_mapping_project_module FOREIGN KEY (project_module_id) REFERENCES public.trx_project_module(id);
ALTER TABLE ONLY public.trx_report_attendance
    ADD CONSTRAINT fk_trx_report_attendance FOREIGN KEY (report_id) REFERENCES public.trx_report(id);
ALTER TABLE ONLY public.trx_report
    ADD CONSTRAINT fk_trx_report_classroom FOREIGN KEY (classroom_id) REFERENCES public.master_classroom(id);
ALTER TABLE ONLY public.trx_report_deep_learning
    ADD CONSTRAINT fk_trx_report_deep_learning FOREIGN KEY (report_id) REFERENCES public.trx_report(id);
ALTER TABLE ONLY public.trx_report_extracurricular
    ADD CONSTRAINT fk_trx_report_extracurricular FOREIGN KEY (report_id) REFERENCES public.trx_report(id);
ALTER TABLE ONLY public.trx_report_p5
    ADD CONSTRAINT fk_trx_report_p5 FOREIGN KEY (report_id) REFERENCES public.trx_report(id);
ALTER TABLE ONLY public.trx_report_score
    ADD CONSTRAINT fk_trx_report_score_subject FOREIGN KEY (subject_id) REFERENCES public.master_subject(id);
ALTER TABLE ONLY public.trx_report_score
    ADD CONSTRAINT fk_trx_report_scores FOREIGN KEY (report_id) REFERENCES public.trx_report(id);
ALTER TABLE ONLY public.trx_report
    ADD CONSTRAINT fk_trx_report_student FOREIGN KEY (student_id) REFERENCES public.master_student(id);
ALTER TABLE ONLY public.trx_teaching_assignment
    ADD CONSTRAINT fk_trx_teaching_assignment_subject FOREIGN KEY (subject_id) REFERENCES public.master_subject(id);
ALTER TABLE ONLY public.trx_teaching_assignment
    ADD CONSTRAINT fk_trx_teaching_assignment_teacher FOREIGN KEY (teacher_id) REFERENCES public.master_teacher(id);
ALTER TABLE ONLY public.trx_teaching_module_activity
    ADD CONSTRAINT fk_trx_teaching_module_activities FOREIGN KEY (module_id) REFERENCES public.trx_teaching_module(id);
ALTER TABLE ONLY public.trx_teaching_module_activity
    ADD CONSTRAINT fk_trx_teaching_module_activity_stage FOREIGN KEY (stage_id) REFERENCES public.dl_cognitive_stage(id);

-- =========================================================================
-- 1. TABEL KONTEKS LOKAL (master_school_local_context)
-- HUBUNGAN: 1-to-1 dengan master_school untuk mendefinisikan karakteristik area sekitar
-- =========================================================================
CREATE TABLE public.master_school_local_context (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    school_id uuid NOT NULL,
    local_dominant_occupations text NOT NULL,
    local_income_level text NOT NULL,
    local_language_nuance text NOT NULL,
    local_geographic_type text NOT NULL,
    local_natural_resources text NOT NULL,
    local_environmental_issues text NOT NULL,
    local_cultural_heritage text,
    local_umkm_potential text,
    is_vector_synced boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE ONLY public.master_school_local_context
    ADD CONSTRAINT master_school_local_context_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.master_school_local_context
    ADD CONSTRAINT fk_local_context_school FOREIGN KEY (school_id) REFERENCES public.master_school(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.master_school_local_context
    ADD CONSTRAINT uni_local_context_school UNIQUE (school_id);
CREATE INDEX idx_local_context_synced ON public.master_school_local_context (is_vector_synced);


-- =========================================================================
-- 2. TABEL KONTEKS SEKOLAH - EKSTENSI PRAKTIK MENDALAM (master_school_context_ext)
-- HUBUNGAN: 1-to-1 dengan master_school untuk parameter operasional kelas
-- =========================================================================
CREATE TABLE public.master_school_context_ext (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    school_id uuid NOT NULL,
    school_vision_core text NOT NULL,
    school_distinctive_values text NOT NULL,
    school_location_setting text NOT NULL,
    school_facilities_list text[] NOT NULL,
    school_digital_adoption_level character varying(20) NOT NULL,
    school_teacher_profile_matrix text NOT NULL,
    school_external_partners text,
    school_parental_involvement_type character varying(50) NOT NULL,
    is_vector_synced boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE ONLY public.master_school_context_ext
    ADD CONSTRAINT master_school_context_ext_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.master_school_context_ext
    ADD CONSTRAINT fk_school_context_ext_school FOREIGN KEY (school_id) REFERENCES public.master_school(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.master_school_context_ext
    ADD CONSTRAINT uni_school_context_ext_school UNIQUE (school_id);
ALTER TABLE ONLY public.master_school_context_ext
    ADD CONSTRAINT chk_digital_level CHECK (((school_digital_adoption_level)::text = ANY (ARRAY[('LOW'::character varying)::text, ('MEDIUM'::character varying)::text, ('HIGH'::character varying)::text])));
ALTER TABLE ONLY public.master_school_context_ext
    ADD CONSTRAINT chk_parental_type CHECK (((school_parental_involvement_type)::text = ANY (ARRAY[('AKTIF_KOLABORATIF'::character varying)::text, ('PASIF_INFORMATIF'::character varying)::text])));
CREATE INDEX idx_school_context_synced ON public.master_school_context_ext (is_vector_synced);


-- =========================================================================
-- 3. TABEL KONTEKS PERSONAL SISWA (master_student_context_ext)
-- HUBUNGAN: 1-to-1 dengan master_student untuk penegakan Belajar Berdiferensiasi
-- =========================================================================
CREATE TABLE public.master_student_context_ext (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    student_id uuid NOT NULL,
    student_family_background text,
    student_home_language character varying(50),
    student_prior_knowledge_level character varying(30) NOT NULL,
    student_literacy_numeracy_status text NOT NULL,
    student_learning_pace character varying(30) NOT NULL,
    student_metacognitive_awareness text,
    student_dominant_interest text NOT NULL,
    student_social_interaction_style text,
    student_well_being_status text,
    is_vector_synced boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE ONLY public.master_student_context_ext
    ADD CONSTRAINT master_student_context_ext_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.master_student_context_ext
    ADD CONSTRAINT fk_student_context_ext_student FOREIGN KEY (student_id) REFERENCES public.master_student(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.master_student_context_ext
    ADD CONSTRAINT uni_student_context_ext_student UNIQUE (student_id);
ALTER TABLE ONLY public.master_student_context_ext
    ADD CONSTRAINT chk_prior_level CHECK (((student_prior_knowledge_level)::text = ANY (ARRAY[('BELUM_BERKEMBANG'::character varying)::text, ('LAYAK'::character varying)::text, ('CAKAP'::character varying)::text, ('MAHIR'::character varying)::text])));
ALTER TABLE ONLY public.master_student_context_ext
    ADD CONSTRAINT chk_learning_pace CHECK (((student_learning_pace)::text = ANY (ARRAY[('CEPAT_BERNALAR'::character varying)::text, ('RATA_RATA'::character varying)::text, ('BUTUH_BIMBINGAN'::character varying)::text])));
CREATE INDEX idx_student_context_synced ON public.master_student_context_ext (is_vector_synced);

