-- =========================================================================
-- SEED DATA KONTEKS LOKAL EKSTENSI (master_school_local_context)
-- Menghubungkan secara dinamis menggunakan NPSN UPT SDI Bonerate No. 85
-- =========================================================================
INSERT INTO master_school_local_context (
    id, 
    school_id, 
    local_dominant_occupations, 
    local_income_level, 
    local_language_nuance, 
    local_geographic_type, 
    local_natural_resources, 
    local_environmental_issues, 
    local_cultural_heritage, 
    local_umkm_potential, 
    is_vector_synced,
    created_at,
    updated_at
)
SELECT 
    uuid_generate_v4(), 
    id, 
    'Mayoritas utama adalah nelayan tangkap (tradisional dan modern), petani kelapa/kopra, buruh angkut pelabuhan di Dermaga Bonerate, pengrajin perahu kayu, dan sebagian kecil pelaku UMKM perdagangan antar-pulau.',
    'Pedesaan kepulauan terluar berbasis agraris-maritim dengan tingkat pendapatan musiman (sangat bergantung pada fluktuasi harga kopra dunia dan musim angin laut).',
    'Bahasa Bonerate (dialek khas perpaduan unsur Bajo dan Bugis-Makassar) serta Bahasa Indonesia sebagai bahasa pengantar formal. Kosakata lokal seperti ''mabar'' digunakan khusus untuk ''fun games'' dalam interaksi komunitas.',
    'Kawasan pulau terluar (Kepulauan sub-cluster Selayar bagian selatan), didominasi pesisir pantai berpasir putih, ekosistem karang atol (dekat kawasan Taka Bonerate), serta perbukitan rendah di Desa Majapahit.',
    'Kelapa kering (kopra), ikan sunu, ikan kerapu, ikan cakalang, lobster, rumput laut, dan kerajinan anyaman sabut kelapa.',
    'Abrasi pantai di pesisir Desa Lamantu (Pantai Bangke), penumpukan sampah plastik musiman akibat arus laut global di sepanjang pantai Bonerate, serta keterbatasan air bersih siap minum saat musim kemarau panjang.',
    'Tradisi Adu Kuda Jantan (hiburan rakyat Pasimarannu), ritual Mandi Syafar (tolak bala bersama di laut), perayaan Maulid Nabi dengan hiasan telur (maudu), serta upacara adat Ambasa (syukuran sebelum musim melaut atau panen emping laut).',
    'Kelompok pengrajin kopra rumahan, pengeringan ikan asin tradisional di pesisir, industri pembuatan shuttlecock lokal (lini SNAR), dan penyedia penginapan rumah (homestay) kemitraan pariwisata bahari.',
    false,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
FROM master_school 
WHERE npsn = '40304877'
ON CONFLICT (school_id) DO NOTHING;


-- =========================================================================
-- SEED DATA KONTEKS SEKOLAH EKSTENSI (master_school_context_ext)
-- Menghubungkan secara dinamis menggunakan NPSN UPT SDI Bonerate No. 85
-- =========================================================================
INSERT INTO master_school_context_ext (
    id, 
    school_id, 
    school_vision_core, 
    school_distinctive_values, 
    school_location_setting, 
    school_facilities_list, 
    school_digital_adoption_level, 
    school_teacher_profile_matrix, 
    school_external_partners, 
    school_parental_involvement_type, 
    is_vector_synced,
    created_at,
    updated_at
)
SELECT
    uuid_generate_v4(),
    id,
    'Berakhlak Mulia, Cerdas, Tangguh, dan Berwawasan Lingkungan Bahari.',
    'Satuan pendidikan inti kepulauan yang mengintegrasikan kesadaran ekologi pesisir ke dalam Kurikulum Merdeka (Project P5) guna membentuk resiliensi (daya juang) murid terhadap tantangan geografis terluar.',
    'Berada di poros Jalan Majapahit No. 312, Desa Bonerate. Berdekatan dengan pusat aktivitas maritim dermaga transit utama, pemukiman komunal padat pantai, dan area komoditas kelapa.',
    ARRAY[
        'Memiliki 12 Ruang Kelas (8 Baik, 4 Rusak Ringan)',
        'Tidak memiliki ruang laboratorium komputer fisik terpisah',
        'Tidak memiliki ruang perpustakaan fisik terpisah',
        'Pembelajaran berbasis IT dijalankan secara hibrida menggunakan perangkat pribadi guru/gawai komunal',
        'Ruang perpustakaan dioptimalkan melalui pojok baca kelas'
    ],
    'LOW',
    'Memiliki 20 Guru dan 4 Tendik (Total 24 PTK). Rasio guru terhadap rombel sangat ideal (1.67) dan rasio guru terhadap murid sangat intensif (1:12.55). Pendidik didominasi oleh perpaduan guru senior yang kaya pemahaman kultural lokal dan guru muda yang adaptif terhadap implementasi Kurikulum Merdeka.',
    'Puskesmas Pasimarannu, Pemerintah Desa Bonerate, Komunitas Nelayan Lokal, Yayasan Membangun Kultur Negeri (Yayasan Kultur Juara Indonesia) untuk potensi olahraga/badminton.',
    'AKTIF_KOLABORATIF',
    false,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
FROM master_school
WHERE npsn = '40304877'
ON CONFLICT (school_id) DO NOTHING;


-- =========================================================================
-- SEED DATA KONTEKS LOKAL INDIVIDUAL (master_local_context)
-- Menghubungkan secara dinamis menggunakan NPSN UPT SDI Bonerate No. 85
-- =========================================================================

-- 1. Demografi & Kependudukan (Category: SOSIAL)
INSERT INTO master_local_context (
    id,
    school_id,
    category_id,
    title,
    description,
    location,
    scope_type,
    is_active,
    created_at,
    updated_at
)
SELECT 
    'd78b1cf6-5384-48f8-b3d4-4f4094ab4711',
    s.id::text,
    c.id,
    'Demografi & Kependudukan Kecamatan Pasimarannu',
    'Mayoritas utama adalah nelayan tangkap (tradisional dan modern), petani kelapa/kopra, buruh angkut pelabuhan di Dermaga Bonerate, pengrajin perahu kayu, dan sebagian kecil pelaku UMKM perdagangan antar-pulau. Profil ekonomi area pedesaan kepulauan terluar berbasis agraris-maritim dengan tingkat pendapatan musiman. Bahasa Bonerate (dialek khas perpaduan Bajo dan Bugis-Makassar) serta bahasa Indonesia digunakan, dengan kosakata lokal seperti ''mabar'' untuk fun games.',
    'Kecamatan Pasimarannu, Kepulauan Selayar',
    'Kecamatan',
    true,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
FROM master_school s
CROSS JOIN master_local_context_category c
WHERE s.npsn = '40304877' AND c.category_code = 'SOSIAL'
ON CONFLICT (id) DO NOTHING;

-- 2. Monografi & Geografis/Lingkungan (Category: BAHARI)
INSERT INTO master_local_context (
    id,
    school_id,
    category_id,
    title,
    description,
    location,
    scope_type,
    is_active,
    created_at,
    updated_at
)
SELECT 
    'd78b1cf6-5384-48f8-b3d4-4f4094ab4712',
    s.id::text,
    c.id,
    'Geografis dan Isu Lingkungan Pantai Bonerate & Lamantu',
    'Kawasan pulau terluar (Kepulauan sub-cluster Selayar bagian selatan), didominasi pesisir pantai berpasir putih, ekosistem karang atol (dekat kawasan Taka Bonerate), serta perbukitan rendah di Desa Majapahit. Sumber daya alam meliputi kelapa kering (kopra), ikan sunu, ikan kerapu, ikan cakalang, lobster, rumput laut, dan kerajinan anyaman sabut kelapa. Isu lingkungan meliputi abrasi pantai di pesisir Desa Lamantu (Pantai Bangke), penumpukan sampah plastik musiman akibat arus laut global di sepanjang pantai Bonerate, serta keterbatasan air bersih.',
    'Desa Bonerate, Lamantu, dan Majapahit',
    'Desa',
    true,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
FROM master_school s
CROSS JOIN master_local_context_category c
WHERE s.npsn = '40304877' AND c.category_code = 'BAHARI'
ON CONFLICT (id) DO NOTHING;

-- 3. Sosio-Kultural & Ekonomi Lokal (Category: BUDAYA)
INSERT INTO master_local_context (
    id,
    school_id,
    category_id,
    title,
    description,
    location,
    scope_type,
    is_active,
    created_at,
    updated_at
)
SELECT 
    'd78b1cf6-5384-48f8-b3d4-4f4094ab4713',
    s.id::text,
    c.id,
    'Warisan Budaya dan Potensi UMKM Pasimarannu',
    'Tradisi Adu Kuda Jantan (hiburan rakyat Pasimarannu), ritual Mandi Syafar (tolak bala bersama di laut), perayaan Maulid Nabi dengan hiasan telur (maudu), serta upacara adat Ambasa (syukuran sebelum musim melaut atau panen emping laut). Potensi UMKM meliputi kelompok pengrajin kopra rumahan, pengeringan ikan asin tradisional di pesisir, industri pembuatan shuttlecock lokal (lini SNAR), dan penyedia homestay kemitraan pariwisata bahari.',
    'Kecamatan Pasimarannu',
    'Kecamatan',
    true,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
FROM master_school s
CROSS JOIN master_local_context_category c
WHERE s.npsn = '40304877' AND c.category_code = 'BUDAYA'
ON CONFLICT (id) DO NOTHING;
