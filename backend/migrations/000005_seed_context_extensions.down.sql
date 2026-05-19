DELETE FROM master_school_context_ext 
WHERE school_id IN (SELECT id FROM master_school WHERE npsn = '40304877');

DELETE FROM master_school_local_context 
WHERE school_id IN (SELECT id FROM master_school WHERE npsn = '40304877');

DELETE FROM master_local_context 
WHERE id IN (
    'd78b1cf6-5384-48f8-b3d4-4f4094ab4711',
    'd78b1cf6-5384-48f8-b3d4-4f4094ab4712',
    'd78b1cf6-5384-48f8-b3d4-4f4094ab4713'
);
