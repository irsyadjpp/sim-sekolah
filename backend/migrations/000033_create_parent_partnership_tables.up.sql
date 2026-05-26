-- Parent-Teacher Partnership Tracking System
-- This migration creates tables for tracking parent-teacher partnerships and communications

-- Parent Partnership table to track partnership records
CREATE TABLE master_parent_partnership (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    parent_id UUID REFERENCES auth_user(id) ON DELETE CASCADE,
    partnership_type VARCHAR(50) NOT NULL,  -- PRIMARY, SECONDARY, EMERGENCY
    relationship VARCHAR(50) NOT NULL,  -- FATHER, MOTHER, GUARDIAN, GRANDPARENT
    contact_primary VARCHAR(20) NOT NULL,
    contact_secondary VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    communication_preference VARCHAR(50) DEFAULT 'PHONE',  -- PHONE, EMAIL, WHATSAPP, IN_PERSON
    involvement_level VARCHAR(20) DEFAULT 'MODERATE',  -- LOW, MODERATE, HIGH, VERY_HIGH
    notes TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Communication Log table to track all communications
CREATE TABLE trx_parent_communication (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    partnership_id UUID NOT NULL REFERENCES master_parent_partnership(id) ON DELETE CASCADE,
    teacher_id UUID NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    communication_type VARCHAR(50) NOT NULL,  -- PHONE_CALL, EMAIL, MEETING, WHATSAPP, NOTE
    communication_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    subject VARCHAR(200),
    content TEXT NOT NULL,
    direction VARCHAR(20) NOT NULL,  -- INCOMING, OUTGOING
    status VARCHAR(20) DEFAULT 'COMPLETED',  -- SCHEDULED, COMPLETED, CANCELLED, FOLLOW_UP
    follow_up_required BOOLEAN DEFAULT false,
    follow_up_date TIMESTAMPTZ,
    response_received BOOLEAN DEFAULT false,
    response_date TIMESTAMPTZ,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Meeting Schedule table for parent-teacher meetings
CREATE TABLE trx_parent_meeting (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    partnership_id UUID NOT NULL REFERENCES master_parent_partnership(id) ON DELETE CASCADE,
    teacher_id UUID NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    meeting_type VARCHAR(50) NOT NULL,  -- PARENT_TEACHER_CONFERENCE, IEP_MEETING, BEHAVIOR_DISCUSSION, ACADEMIC_REVIEW
    scheduled_date TIMESTAMPTZ NOT NULL,
    duration_minutes INT DEFAULT 30,
    location VARCHAR(100) DEFAULT 'SCHOOL',
    agenda TEXT,
    status VARCHAR(20) DEFAULT 'SCHEDULED',  -- SCHEDULED, CONFIRMED, COMPLETED, CANCELLED, NO_SHOW
    attendance_status VARCHAR(20),  -- ATTENDED, NO_SHOW, RESCHEDULED
    summary TEXT,
    action_items TEXT[],
    next_meeting_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Partnership Activity tracking for parent involvement
CREATE TABLE trx_partnership_activity (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    partnership_id UUID NOT NULL REFERENCES master_parent_partnership(id) ON DELETE CASCADE,
    activity_type VARCHAR(50) NOT NULL,  -- VOLUNTEER, EVENT_ATTENDANCE, HOMEWORK_SUPPORT, SCHOOL_VISIT, WORKSHOP
    activity_date DATE NOT NULL,
    description TEXT,
    hours_contributed DECIMAL(4,2),
    impact_rating VARCHAR(20),  -- LOW, MEDIUM, HIGH
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for better query performance
CREATE INDEX idx_parent_partnership_student ON master_parent_partnership(student_id);
CREATE INDEX idx_parent_partnership_parent ON master_parent_partnership(parent_id);
CREATE INDEX idx_parent_partnership_active ON master_parent_partnership(is_active);
CREATE INDEX idx_parent_partnership_deleted ON master_parent_partnership(deleted_at);
CREATE INDEX idx_communication_partnership ON trx_parent_communication(partnership_id);
CREATE INDEX idx_communication_teacher ON trx_parent_communication(teacher_id);
CREATE INDEX idx_communication_date ON trx_parent_communication(communication_date);
CREATE INDEX idx_communication_deleted ON trx_parent_communication(deleted_at);
CREATE INDEX idx_meeting_partnership ON trx_parent_meeting(partnership_id);
CREATE INDEX idx_meeting_teacher ON trx_parent_meeting(teacher_id);
CREATE INDEX idx_meeting_date ON trx_parent_meeting(scheduled_date);
CREATE INDEX idx_meeting_status ON trx_parent_meeting(status);
CREATE INDEX idx_meeting_deleted ON trx_parent_meeting(deleted_at);
CREATE INDEX idx_activity_partnership ON trx_partnership_activity(partnership_id);
CREATE INDEX idx_activity_date ON trx_partnership_activity(activity_date);
CREATE INDEX idx_activity_deleted ON trx_partnership_activity(deleted_at);

-- Add comments for documentation
COMMENT ON TABLE master_parent_partnership IS 'Master table for parent-teacher partnerships';
COMMENT ON TABLE trx_parent_communication IS 'Transaction table for tracking parent-teacher communications';
COMMENT ON TABLE trx_parent_meeting IS 'Transaction table for scheduled parent-teacher meetings';
COMMENT ON TABLE trx_partnership_activity IS 'Transaction table for tracking parent involvement activities';
