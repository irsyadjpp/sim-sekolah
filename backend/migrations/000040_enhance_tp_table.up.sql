-- Migration: Enhance TP (Learning Objective) Table
-- Created: 2026-05-25
-- Description: This migration enhances the cur_learning_objective table with sequencing, difficulty tagging, cognitive domain, and time estimation

-- Add new columns to cur_learning_objective table
ALTER TABLE cur_learning_objective 
ADD COLUMN IF NOT EXISTS sequence INTEGER DEFAULT 1,
ADD COLUMN IF NOT EXISTS difficulty_level VARCHAR(20) DEFAULT 'MEDIUM',
ADD COLUMN IF NOT EXISTS cognitive_domain VARCHAR(50),
ADD COLUMN IF NOT EXISTS estimated_hours DECIMAL(5,2) DEFAULT 1.0;

-- Add indexes for new columns
CREATE INDEX IF NOT EXISTS idx_learning_objective_sequence ON cur_learning_objective(sequence);
CREATE INDEX IF NOT EXISTS idx_learning_objective_difficulty ON cur_learning_objective(difficulty_level);

-- Add comments for documentation
COMMENT ON COLUMN cur_learning_objective.sequence IS 'Urutan TP dalam alur pembelajaran (TP sequencing)';
COMMENT ON COLUMN cur_learning_objective.difficulty_level IS 'Tingkat kesulitan TP: EASY, MEDIUM, HARD';
COMMENT ON COLUMN cur_learning_objective.cognitive_domain IS 'Domain kognitif Bloom: C1 (Remembering), C2 (Understanding), C3 (Applying), C4 (Analyzing), C5 (Evaluating), C6 (Creating)';
COMMENT ON COLUMN cur_learning_objective.estimated_hours IS 'Estimasi waktu pembelajaran dalam jam';

-- Add check constraint for difficulty_level
ALTER TABLE cur_learning_objective 
ADD CONSTRAINT chk_difficulty_level 
CHECK (difficulty_level IN ('EASY', 'MEDIUM', 'HARD'));

-- Add check constraint for cognitive_domain
ALTER TABLE cur_learning_objective 
ADD CONSTRAINT chk_cognitive_domain 
CHECK (cognitive_domain IS NULL OR cognitive_domain IN ('C1', 'C2', 'C3', 'C4', 'C5', 'C6'));
