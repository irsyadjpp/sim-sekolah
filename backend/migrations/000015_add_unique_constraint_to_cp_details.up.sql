-- 1. Safely deduplicate any existing active records in cur_cp_detail, leaving only the latest one per (learning_outcome_id, element_id)
DELETE FROM public.cur_cp_detail a
USING public.cur_cp_detail b
WHERE a.id < b.id
  AND a.learning_outcome_id = b.learning_outcome_id
  AND a.element_id = b.element_id
  AND a.deleted_at IS NULL
  AND b.deleted_at IS NULL;

-- 2. Create partial unique index on (learning_outcome_id, element_id) for active (non-soft-deleted) records
CREATE UNIQUE INDEX IF NOT EXISTS idx_cur_cp_detail_learning_outcome_element 
ON public.cur_cp_detail (learning_outcome_id, element_id) 
WHERE deleted_at IS NULL;
