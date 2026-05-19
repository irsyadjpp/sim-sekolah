-- Update Zonasi to Domisili
UPDATE trx_ppdb_admission_path SET name = 'Domisili' WHERE name = 'Zonasi';

-- Disable Prestasi
UPDATE trx_ppdb_admission_path SET is_active = false WHERE name = 'Prestasi';

-- Add family_card_issue_date
ALTER TABLE trx_ppdb_applicant ADD COLUMN family_card_issue_date DATE;
