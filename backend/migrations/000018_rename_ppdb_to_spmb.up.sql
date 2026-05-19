-- Rename trx_ppdb_admission_path to trx_spmb_admission_path
ALTER TABLE trx_ppdb_admission_path RENAME TO trx_spmb_admission_path;

-- Rename trx_ppdb_applicant to trx_spmb_applicant
ALTER TABLE trx_ppdb_applicant RENAME TO trx_spmb_applicant;

-- Rename trx_ppdb_document to trx_spmb_document
ALTER TABLE trx_ppdb_document RENAME TO trx_spmb_document;

-- Rename trx_ppdb_parent to trx_spmb_parent
ALTER TABLE trx_ppdb_parent RENAME TO trx_spmb_parent;

-- Rename trx_ppdb_verification_log to trx_spmb_verification_log
ALTER TABLE trx_ppdb_verification_log RENAME TO trx_spmb_verification_log;

-- Rename index idx_trx_ppdb_parent_applicant_id to idx_trx_spmb_parent_applicant_id
ALTER INDEX idx_trx_ppdb_parent_applicant_id RENAME TO idx_trx_spmb_parent_applicant_id;
