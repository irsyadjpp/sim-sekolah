-- =========================================================================
-- 1. TABEL KONTEKS LOKAL (master_school_local_context)
-- HUBUNGAN: 1-to-1 dengan master_school untuk mendefinisikan karakteristik area sekitar
-- =========================================================================
CREATE TABLE IF NOT EXISTS master_school_local_context (
    id uuid DEFAULT uuid_generate_v4() NOT NULL,
    school_id uuid NOT NULL,
    
    -- A. Demografi & Kependudukan
    local_dominant_occupations text NOT NULL, -- Contoh: "Nelayan, Petani Rumput Laut, Pengrajin"
    local_income_level text NOT NULL,        -- Contoh: "Pesisir Menengah ke Bawah"
    local_language_nuance text NOT NULL,     -- Contoh: "Bahasa Selayar, Dialek Bonerate"
    
    -- B. Monografi & Geografis
    local_geographic_type text NOT NULL,     -- Contoh: "Pesisir Pantai dan Pulau Terluar"
    local_natural_resources text NOT NULL,    -- Contoh: "Kelapa, Ikan Laut, Terumbu Karang"
    local_environmental_issues text NOT NULL, -- Contoh: "Abrasi Pantai, Sampah Plastik Pesisir"
    
    -- C. Sosio-Kultural & Ekonomi Lokal
    local_cultural_heritage text NULL,       -- Contoh: "Tradisi Bahari, Pembuatan Perahu"
    local_umkm_potential text NULL,          -- Contoh: "Warung Olahan Ikan Kering, Kerajinan Batok Kelapa"
    
    -- Status Sinkronisasi Mesin Otomasi (RAG)
    is_vector_synced bool DEFAULT false NULL,
    created_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
    updated_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
    
    CONSTRAINT master_school_local_context_pkey PRIMARY KEY (id),
    CONSTRAINT fk_local_context_school FOREIGN KEY (school_id) REFERENCES master_school(id) ON DELETE CASCADE,
    CONSTRAINT uni_local_context_school UNIQUE (school_id)
);
CREATE INDEX IF NOT EXISTS idx_local_context_synced ON master_school_local_context (is_vector_synced);


-- =========================================================================
-- 2. TABEL KONTEKS SEKOLAH - EKSTENSI PRAKTIK MENDALAM (master_school_context_ext)
-- HUBUNGAN: 1-to-1 dengan master_school untuk parameter operasional kelas
-- =========================================================================
CREATE TABLE IF NOT EXISTS master_school_context_ext (
    id uuid DEFAULT uuid_generate_v4() NOT NULL,
    school_id uuid NOT NULL,
    
    -- A. Visi Misi & Karakteristik Unik
    school_vision_core text NOT NULL,          -- Contoh: "Berwawasan Lingkungan Bahari"
    school_distinctive_values text NOT NULL,   -- Contoh: "Sekolah Pesisir Tangguh Bencana"
    school_location_setting text NOT NULL,     -- Contoh: "Dekat dengan garis pantai Desa Bonerate"
    
    -- B. Kapasitas & Sumber Daya Physical/Digital
    school_facilities_list text[] NOT NULL,    -- Menggunakan Array Postgres untuk daftar fasilitas harian
    school_digital_adoption_level varchar(20) NOT NULL, -- 'LOW', 'MEDIUM', 'HIGH'
    school_teacher_profile_matrix text NOT NULL, -- Kondisi riil kompetensi para pendidik
    
    -- C. Kemitraan Ekosistem
    school_external_partners text NULL,        -- Contoh: "Puskesmas Pasimarannu, Pemerintah Desa Bonerate"
    school_parental_involvement_type varchar(50) NOT NULL, -- 'AKTIF_KOLABORATIF', 'PASIF_INFORMATIF'
    
    -- Status Sinkronisasi Mesin Otomasi (RAG)
    is_vector_synced bool DEFAULT false NULL,
    created_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
    updated_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
    
    CONSTRAINT master_school_context_ext_pkey PRIMARY KEY (id),
    CONSTRAINT fk_school_context_ext_school FOREIGN KEY (school_id) REFERENCES master_school(id) ON DELETE CASCADE,
    CONSTRAINT uni_school_context_ext_school UNIQUE (school_id),
    CONSTRAINT chk_digital_level CHECK (school_digital_adoption_level IN ('LOW', 'MEDIUM', 'HIGH')),
    CONSTRAINT chk_parental_type CHECK (school_parental_involvement_type IN ('AKTIF_KOLABORATIF', 'PASIF_INFORMATIF'))
);
CREATE INDEX IF NOT EXISTS idx_school_context_synced ON master_school_context_ext (is_vector_synced);


-- =========================================================================
-- 3. TABEL KONTEKS PERSONAL SISWA (master_student_context_ext)
-- HUBUNGAN: 1-to-1 dengan master_student untuk penegakan Belajar Berdiferensiasi
-- =========================================================================
CREATE TABLE IF NOT EXISTS master_student_context_ext (
    id uuid DEFAULT uuid_generate_v4() NOT NULL,
    student_id uuid NOT NULL,
    
    -- A. Identitas & Latar Belakang Personal
    student_family_background text NULL,
    student_home_language varchar(50) NULL,    -- Contoh: "Bahasa Daerah Bonerate"
    
    -- B. Profil Akademik & Riwayat Belajar (Kognitif & Metakognitif)
    student_prior_knowledge_level varchar(30) NOT NULL, -- 'BELUM_BERKEMBANG', 'LAYAK', 'CAKAP', 'MAHIR'
    student_literacy_numeracy_status text NOT NULL,     -- Diagnostik riil tingkat literasi anak
    student_learning_pace varchar(30) NOT NULL,         -- 'CEPAT_BERNALAR', 'RATA_RATA', 'BUTUH_BIMBINGAN'
    student_metacognitive_awareness text NULL,          -- Tingkat regulasi mandiri anak
    
    -- C. Aspek Non-Kognitif & Sosial-Emosional
    student_dominant_interest text NOT NULL,            -- Contoh: "Aktivitas Fisik, Olahraga Sepak Bola"
    student_social_interaction_style text NULL,         -- Karakter pergaulan di kelas
    student_well_being_status text NULL,                -- Kondisi kesehatan fisik & mental umum
    
    -- Status Sinkronisasi Mesin Otomasi (RAG)
    is_vector_synced bool DEFAULT false NULL,
    created_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
    updated_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
    
    CONSTRAINT master_student_context_ext_pkey PRIMARY KEY (id),
    CONSTRAINT fk_student_context_ext_student FOREIGN KEY (student_id) REFERENCES master_student(id) ON DELETE CASCADE,
    CONSTRAINT uni_student_context_ext_student UNIQUE (student_id),
    CONSTRAINT chk_prior_level CHECK (student_prior_knowledge_level IN ('BELUM_BERKEMBANG', 'LAYAK', 'CAKAP', 'MAHIR')),
    CONSTRAINT chk_learning_pace CHECK (student_learning_pace IN ('CEPAT_BERNALAR', 'RATA_RATA', 'BUTUH_BIMBINGAN'))
);
CREATE INDEX IF NOT EXISTS idx_student_context_synced ON master_student_context_ext (is_vector_synced);
