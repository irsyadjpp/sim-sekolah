-- Revert Domisili to Zonasi
UPDATE trx_ppdb_admission_path SET name = 'Zonasi' WHERE name = 'Domisili';

-- Enable Prestasi
UPDATE trx_ppdb_admission_path SET is_active = true WHERE name = 'Prestasi';

-- Remove family_card_issue_date
ALTER TABLE trx_ppdb_applicant DROP COLUMN IF EXISTS family_card_issue_date;
