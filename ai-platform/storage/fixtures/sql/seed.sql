-- AI Platform Test Fixtures
-- This file contains seed data for testing the AI Platform storage systems

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Insert test users
INSERT INTO users (id, email, username, full_name, role, metadata) VALUES
  ('550e8400-e29b-41d4-a716-446655440001', 'admin@test.com', 'admin', 'Test Admin', 'admin', '{"department": "IT"}'::jsonb),
  ('550e8400-e29b-41d4-a716-446655440002', 'teacher@test.com', 'teacher', 'Test Teacher', 'teacher', '{"subjects": ["math", "science"]}'::jsonb),
  ('550e8400-e29b-41d4-a716-446655440003', 'student@test.com', 'student', 'Test Student', 'student', '{"grade": "10"}'::jsonb)
ON CONFLICT (email) DO NOTHING;

-- Insert test documents
INSERT INTO documents (id, title, content, file_type, status, source, metadata) VALUES
  ('550e8400-e29b-41d4-a716-446655440010', 'Introduction to Photosynthesis', 'Photosynthesis is the process by which plants convert sunlight into energy...', 'pdf', 'processed', 'test_fixture', '{"subject": "biology", "grade_level": "10", "difficulty": "easy"}'::jsonb),
  ('550e8400-e29b-41d4-a716-446655440011', 'Algebra Fundamentals', 'Algebra is a branch of mathematics dealing with symbols and the rules for manipulating those symbols...', 'pdf', 'processed', 'test_fixture', '{"subject": "mathematics", "grade_level": "9", "difficulty": "medium"}'::jsonb),
  ('550e8400-e29b-41d4-a716-446655440012', 'Newton Laws of Motion', 'Newton laws of motion describe the relationship between the motion of an object and the forces acting on it...', 'pdf', 'processed', 'test_fixture', '{"subject": "physics", "grade_level": "11", "difficulty": "hard"}'::jsonb)
ON CONFLICT DO NOTHING;

-- Insert test document chunks
INSERT INTO document_chunks (id, document_id, chunk_index, content, metadata) VALUES
  ('550e8400-e29b-41d4-a716-446655440020', '550e8400-e29b-41d4-a716-446655440010', 0, 'Photosynthesis is the process by which plants convert sunlight into energy. This process occurs in chloroplasts and produces glucose and oxygen as byproducts.', '{"section": "introduction", "word_count": 28}'::jsonb),
  ('550e8400-e29b-41d4-a716-446655440021', '550e8400-e29b-41d4-a716-446655440010', 1, 'The light-dependent reactions occur in the thylakoid membranes and require light energy to produce ATP and NADPH.', '{"section": "light_reactions", "word_count": 23}'::jsonb),
  ('550e8400-e29b-41d4-a716-446655440022', '550e8400-e29b-41d4-a716-446655440011', 0, 'Algebra is a branch of mathematics dealing with symbols and the rules for manipulating those symbols. It is a unifying thread of almost all mathematics.', '{"section": "introduction", "word_count": 26}'::jsonb),
  ('550e8400-e29b-41d4-a716-446655440023', '550e8400-e29b-41d4-a716-446655440012', 0, 'Newton first law states that an object will remain at rest or in uniform motion unless acted upon by an external force.', '{"section": "first_law", "word_count": 21}'::jsonb)
ON CONFLICT DO NOTHING;

-- Insert test embeddings
INSERT INTO embeddings (id, chunk_id, model_name, vector_dimension, vector_id) VALUES
  ('550e8400-e29b-41d4-a716-446655440030', '550e8400-e29b-41d4-a716-446655440020', 'bge-m3', 1024, 'vec-001'),
  ('550e8400-e29b-41d4-a716-446655440031', '550e8400-e29b-41d4-a716-446655440021', 'bge-m3', 1024, 'vec-002'),
  ('550e8400-e29b-41d4-a716-446655440032', '550e8400-e29b-41d4-a716-446655440022', 'bge-m3', 1024, 'vec-003'),
  ('550e8400-e29b-41d4-a716-446655440033', '550e8400-e29b-41d4-a716-446655440023', 'bge-m3', 1024, 'vec-004')
ON CONFLICT DO NOTHING;

-- Insert test knowledge entries
INSERT INTO knowledge_entries (id, title, content, category, difficulty, competency, taxonomy_path, version, metadata) VALUES
  ('550e8400-e29b-41d4-a716-446655440040', 'Photosynthesis Process', 'The biological process by which plants convert light energy into chemical energy', 'biology', 'easy', 'scientific_process', 'science.biology.botany', '1.0', '{"grade_level": "10", "duration_minutes": 45}'::jsonb),
  ('550e8400-e29b-41d4-a716-446655440041', 'Linear Equations', 'Mathematical equations where variables appear only in the first degree', 'mathematics', 'medium', 'problem_solving', 'math.algebra.equations', '1.0', '{"grade_level": "9", "prerequisites": ["basic_arithmetic"]}'::jsonb),
  ('550e8400-e29b-41d4-a716-446655440042', 'Force and Motion', 'Study of how forces affect the motion of objects', 'physics', 'hard', 'scientific_reasoning', 'science.physics.mechanics', '1.0', '{"grade_level": "11", "lab_required": true}'::jsonb)
ON CONFLICT DO NOTHING;

-- Insert test models
INSERT INTO models (id, name, type, version, framework, path, config, metadata, status) VALUES
  ('550e8400-e29b-41d4-a716-446655440050', 'bge-m3', 'embedding', '1.0', 'pytorch', '/models/bge-m3', '{"max_seq_length": 512, "dimension": 1024}'::jsonb, '{"language": "multilingual", "license": "MIT"}'::jsonb, 'active'),
  ('550e8400-e29b-41d4-a716-446655440051', 'llama-3-8b', 'llm', '1.0', 'pytorch', '/models/llama-3-8b', '{"context_length": 8192, "dtype": "float16"}'::jsonb, '{"fine_tuned": false, "instruction_tuned": true}'::jsonb, 'active')
ON CONFLICT (name) DO NOTHING;

-- Insert test conversations
INSERT INTO conversations (id, user_id, title, context, metadata) VALUES
  ('550e8400-e29b-41d4-a716-446655440060', '550e8400-e29b-41d4-a716-446655440003', 'Photosynthesis Questions', '{"subject": "biology", "topic": "photosynthesis"}'::jsonb, '{"session_type": "homework_help"}'::jsonb),
  ('550e8400-e29b-41d4-a716-446655440061', '550e8400-e29b-41d4-a716-446655440003', 'Math Problem Solving', '{"subject": "mathematics", "topic": "algebra"}'::jsonb, '{"session_type": "practice"}'::jsonb)
ON CONFLICT DO NOTHING;

-- Insert test messages
INSERT INTO messages (id, conversation_id, role, content, metadata) VALUES
  ('550e8400-e29b-41d4-a716-446655440070', '550e8400-e29b-41d4-a716-446655440060', 'user', 'What is photosynthesis?', '{"turn": 1}'::jsonb),
  ('550e8400-e29b-41d4-a716-446655440071', '550e8400-e29b-41d4-a716-446655440060', 'assistant', 'Photosynthesis is the process by which plants convert sunlight into energy...', '{"turn": 2, "sources": ["doc-001"]}'::jsonb),
  ('550e8400-e29b-41d4-a716-446655440072', '550e8400-e29b-41d4-a716-446655440061', 'user', 'How do I solve 2x + 5 = 15?', '{"turn": 1}'::jsonb),
  ('550e8400-e29b-41d4-a716-446655440073', '550e8400-e29b-41d4-a716-446655440061', 'assistant', 'To solve 2x + 5 = 15, first subtract 5 from both sides...', '{"turn": 2, "steps": 3}'::jsonb)
ON CONFLICT DO NOTHING;

-- Insert test audit logs
INSERT INTO audit_logs (id, user_id, action, resource_type, resource_id, changes, ip_address, user_agent) VALUES
  ('550e8400-e29b-41d4-a716-446655440080', '550e8400-e29b-41d4-a716-446655440001', 'create', 'document', 'doc-001', '{"title": "New Document"}'::jsonb, '127.0.0.1', 'Mozilla/5.0'),
  ('550e8400-e29b-41d4-a716-446655440081', '550e8400-e29b-41d4-a716-446655440001', 'update', 'user', 'user-002', '{"role": "teacher"}'::jsonb, '127.0.0.1', 'Mozilla/5.0')
ON CONFLICT DO NOTHING;