-- AI Platform Test Fixture Cleanup
-- This script removes all test fixture data from the database

-- Warning: This will delete all data! Use with caution!

-- Delete audit logs (no foreign key dependencies)
DELETE FROM audit_logs WHERE id LIKE '550e8400-e29b-41d4-a716-44665544008%';

-- Delete messages (depends on conversations)
DELETE FROM messages WHERE id LIKE '550e8400-e29b-41d4-a716-44665544007%';

-- Delete conversations (depends on users)
DELETE FROM conversations WHERE id LIKE '550e8400-e29b-41d4-a716-44665544006%';

-- Delete embeddings (depends on document_chunks)
DELETE FROM embeddings WHERE id LIKE '550e8400-e29b-41d4-a716-44665544003%';

-- Delete document_chunks (depends on documents)
DELETE FROM document_chunks WHERE id LIKE '550e8400-e29b-41d4-a716-44665544002%';

-- Delete documents
DELETE FROM documents WHERE id LIKE '550e8400-e29b-41d4-a716-44665544001%';

-- Delete knowledge entries
DELETE FROM knowledge_entries WHERE id LIKE '550e8400-e29b-41d4-a716-44665544004%';

-- Delete models
DELETE FROM models WHERE id LIKE '550e8400-e29b-41d4-a716-44665544005%';

-- Delete users
DELETE FROM users WHERE id LIKE '550e8400-e29b-41d4-a716-44665544000%';

-- Optional: Reset sequences
-- SELECT setval('documents_id_seq', 1, false);
-- SELECT setval('users_id_seq', 1, false);
-- Add more sequence resets as needed