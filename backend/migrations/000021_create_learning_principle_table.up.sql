-- Migration: Create master_learning_principle table
-- Description: Table for storing the 3 learning principles from Deep Learning framework
-- Created: 2024-05-24

CREATE TABLE IF NOT EXISTS master_learning_principle (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    principle_code VARCHAR(30) UNIQUE NOT NULL,
    principle_name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    key_characteristics TEXT,
    implementation_examples TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for performance
CREATE INDEX idx_learning_principle_code ON master_learning_principle(principle_code);
CREATE INDEX idx_learning_principle_active ON master_learning_principle(is_active) WHERE deleted_at IS NULL;
CREATE INDEX idx_learning_principle_deleted ON master_learning_principle(deleted_at);

-- Add comment
COMMENT ON TABLE master_learning_principle IS 'Master table for 3 learning principles from Deep Learning framework: Berkesadaran, Bermakna, Menggembirakan';
COMMENT ON COLUMN master_learning_principle.principle_code IS 'Unique code for the learning principle (BERKESADARAN, BERMAKNA, MENGENGIRAKAN)';
COMMENT ON COLUMN master_learning_principle.principle_name IS 'Name of the learning principle';
COMMENT ON COLUMN master_learning_principle.description IS 'Detailed definition according to Deep Learning framework';
COMMENT ON COLUMN master_learning_principle.key_characteristics IS 'JSON array of key characteristics for each learning principle';
COMMENT ON COLUMN master_learning_principle.implementation_examples IS 'JSON array of implementation examples for each learning principle';
