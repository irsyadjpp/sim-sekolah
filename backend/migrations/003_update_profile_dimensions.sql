-- Migration: Update profile dimensions from Pancasila to Deep Learning 8 dimensions
-- Description: Migrate existing profile dimensions to the 8 standard dimensions according to Deep Learning framework
-- Created: 2024-05-24

-- Delete existing dimensions (will be recreated with correct data)
DELETE FROM master_profile_dimension;

-- Insert the 8 standard dimensions according to Deep Learning framework
INSERT INTO master_profile_dimension (dimension_code, dimension_name, description, is_active, created_at, updated_at) VALUES
('DIM_KEIMANAN', 'Keimanan dan Ketakwaan terhadap Tuhan YME', 'Individu yang memiliki keyakinan teguh akan keberadaan Tuhan YME dan menghayati serta mengamalkan nilai-nilai spiritual dalam kehidupan sehari-hari.', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('DIM_KEWARGAAN', 'Kewargaan', 'Individu yang memiliki rasa cinta tanah air serta menghargai keberagaman budaya, mentaati aturan dan norma sosial dalam kehidupan bermasyarakat, memiliki kepedulian dan tanggung jawab sosial, serta berkomitmen untuk menyelesaikan masalah nyata yang berkaitan dengan keberlanjutan kehidupan, lingkungan, dan harmoni antarbangsa dalam konteks kebhinekaan global.', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('DIM_PENALARAN', 'Penalaran Kritis', 'Individu yang mampu berpikir secara logis, analitis, dan reflektif dalam memahami, mengevaluasi, serta memproses informasi untuk menyelesaikan masalah.', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('DIM_KREATIVITAS', 'Kreativitas', 'Individu yang mampu berpikir secara inovatif, fleksibel, dan orisinal dalam mengolah ide atau informasi untuk menciptakan solusi yang unik dan bermanfaat.', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('DIM_KOLABORASI', 'Kolaborasi', 'Individu yang mampu bekerja sama secara efektif dengan orang lain secara gotong royong untuk mencapai tujuan bersama melalui pembagian peran dan tanggung jawab.', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('DIM_KEMANDIRIAN', 'Kemandirian', 'Individu yang mampu bertanggung jawab atas proses dan hasil belajarnya sendiri dengan menunjukkan kemampuan untuk mengambil inisiatif, mengatasi hambatan, dan menyelesaikan tugas secara tepat tanpa bergantung pada orang lain.', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('DIM_KESEHATAN', 'Kesehatan', 'Individu yang memiliki fisik yang prima, bugar, sehat, dan mampu menjaga keseimbangan kesehatan mental dan fisik untuk mewujudkan kesejahteraan lahir dan batin (well-being).', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('DIM_KOMUNIKASI', 'Komunikasi', 'Individu yang memiliki kemampuan komunikasi intrapribadi untuk melakukan refleksi dan antarpribadi untuk menyampaikan ide, gagasan, dan informasi baik lisan maupun tulisan serta berinteraksi secara efektif dalam berbagai situasi.', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Update comment on the table
COMMENT ON TABLE master_profile_dimension IS 'Master table for 8 profile dimensions according to Deep Learning framework: Keimanan dan Ketakwaan, Kewargaan, Penalaran Kritis, Kreativitas, Kolaborasi, Kemandirian, Kesehatan, Komunikasi';
