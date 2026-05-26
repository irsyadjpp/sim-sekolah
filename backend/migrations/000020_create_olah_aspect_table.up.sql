-- Migration: Create master_olah_aspect table
-- Description: Table for storing the 4 olah aspects from Deep Learning framework
-- Created: 2024-05-24

CREATE TABLE IF NOT EXISTS master_olah_aspect (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    aspect_code VARCHAR(20) UNIQUE NOT NULL,
    aspect_name VARCHAR(100) NOT NULL,
    definition TEXT NOT NULL,
    indicators TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for performance
CREATE INDEX idx_olah_aspect_code ON master_olah_aspect(aspect_code);
CREATE INDEX idx_olah_aspect_active ON master_olah_aspect(is_active) WHERE deleted_at IS NULL;
CREATE INDEX idx_olah_aspect_deleted ON master_olah_aspect(deleted_at);

-- Add comment
COMMENT ON TABLE master_olah_aspect IS 'Master table for 4 olah aspects from Deep Learning framework: Olah Pikir, Olah Hati, Olah Rasa, Olah Raga';
COMMENT ON COLUMN master_olah_aspect.aspect_code IS 'Unique code for the olah aspect (OLAH_PIKIR, OLAH_HATI, OLAH_RASA, OLAH_RAGA)';
COMMENT ON COLUMN master_olah_aspect.aspect_name IS 'Name of the olah aspect';
COMMENT ON COLUMN master_olah_aspect.definition IS 'Detailed definition according to Deep Learning framework';
COMMENT ON COLUMN master_olah_aspect.indicators IS 'JSON array of key indicators for each olah aspect';
