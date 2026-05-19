-- Revert trx_spmb_admission_path to trx_ppdb_admission_path
ALTER TABLE trx_spmb_admission_path RENAME TO trx_ppdb_admission_path;

-- Revert trx_spmb_applicant to trx_ppdb_applicant
ALTER TABLE trx_spmb_applicant RENAME TO trx_ppdb_applicant;

-- Revert trx_spmb_document to trx_ppdb_document
ALTER TABLE trx_spmb_document RENAME TO trx_ppdb_document;

-- Revert trx_spmb_parent to trx_ppdb_parent
ALTER TABLE trx_spmb_parent RENAME TO trx_ppdb_parent;

-- Revert trx_spmb_verification_log to trx_ppdb_verification_log
ALTER TABLE trx_spmb_verification_log RENAME TO trx_ppdb_verification_log;

-- Revert index idx_trx_spmb_parent_applicant_id to idx_trx_ppdb_parent_applicant_id
ALTER INDEX idx_trx_spmb_parent_applicant_id RENAME TO idx_trx_ppdb_parent_applicant_id;
