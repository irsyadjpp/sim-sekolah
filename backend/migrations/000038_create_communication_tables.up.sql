-- Migration: Create communication tables (announcements, messages, notifications)
-- Description: Create tables for school announcements, direct messaging, and system notifications
-- Created: 2025-05-25

-- Create announcements table
CREATE TABLE IF NOT EXISTS announcements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    announcement_type VARCHAR(20) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    target_audience VARCHAR(50),
    target_ids TEXT,
    publish_date DATE NOT NULL,
    expiry_date DATE,
    created_by UUID NOT NULL,
    is_published BOOLEAN DEFAULT false,
    is_featured BOOLEAN DEFAULT false,
    attachment_url VARCHAR(500),
    attachment_name VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for announcements
CREATE INDEX IF NOT EXISTS idx_announcements_type ON announcements(announcement_type) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_announcements_priority ON announcements(priority) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_announcements_audience ON announcements(target_audience) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_announcements_publish_date ON announcements(publish_date) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_announcements_published ON announcements(is_published) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_announcements_featured ON announcements(is_featured) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_announcements_created_by ON announcements(created_by) WHERE deleted_at IS NULL;

-- Add foreign key constraint
ALTER TABLE announcements
ADD CONSTRAINT fk_announcements_created_by
FOREIGN KEY (created_by) REFERENCES auth_user(id) ON DELETE CASCADE;

-- Add comments
COMMENT ON TABLE announcements IS 'School announcements for parents, teachers, and students';
COMMENT ON COLUMN announcements.announcement_type IS 'Type: GENERAL, ACADEMIC, EVENT, EMERGENCY, HOLIDAY';
COMMENT ON COLUMN announcements.priority IS 'Priority: LOW, MEDIUM, HIGH, URGENT';
COMMENT ON COLUMN announcements.target_audience IS 'Target: ALL, TEACHERS, STUDENTS, PARENTS, SPECIFIC_CLASS';
COMMENT ON COLUMN announcements.target_ids IS 'JSON array of target user/class IDs';

-- Create messages table
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sender_id UUID NOT NULL,
    receiver_id UUID NOT NULL,
    subject VARCHAR(200) NOT NULL,
    body TEXT NOT NULL,
    message_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'DRAFT',
    sent_at TIMESTAMPTZ,
    read_at TIMESTAMPTZ,
    parent_id UUID,
    attachment_url VARCHAR(500),
    attachment_name VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for messages
CREATE INDEX IF NOT EXISTS idx_messages_sender ON messages(sender_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_messages_receiver ON messages(receiver_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_messages_type ON messages(message_type) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_messages_status ON messages(status) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_messages_parent ON messages(parent_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_messages_sent_at ON messages(sent_at) WHERE deleted_at IS NULL;

-- Add foreign key constraints
ALTER TABLE messages
ADD CONSTRAINT fk_messages_sender
FOREIGN KEY (sender_id) REFERENCES auth_user(id) ON DELETE CASCADE;

ALTER TABLE messages
ADD CONSTRAINT fk_messages_receiver
FOREIGN KEY (receiver_id) REFERENCES auth_user(id) ON DELETE CASCADE;

ALTER TABLE messages
ADD CONSTRAINT fk_messages_parent
FOREIGN KEY (parent_id) REFERENCES messages(id) ON DELETE SET NULL;

-- Add comments
COMMENT ON TABLE messages IS 'Direct messages between users (teacher-parent, teacher-student, etc.)';
COMMENT ON COLUMN messages.message_type IS 'Type: DIRECT, GROUP, BROADCAST';
COMMENT ON COLUMN messages.status IS 'Status: DRAFT, SENT, DELIVERED, READ, ARCHIVED';
COMMENT ON COLUMN messages.parent_id IS 'For message threads/replies';

-- Create notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    type VARCHAR(20) NOT NULL,
    title VARCHAR(200) NOT NULL,
    body TEXT NOT NULL,
    data JSONB,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    priority VARCHAR(20) DEFAULT 'MEDIUM',
    action_url VARCHAR(500),
    action_text VARCHAR(50),
    sent_at TIMESTAMPTZ,
    read_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    source_id UUID,
    source_type VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for notifications
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_notifications_type ON notifications(type) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_notifications_status ON notifications(status) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_notifications_priority ON notifications(priority) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_notifications_sent_at ON notifications(sent_at) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_notifications_source ON notifications(source_type, source_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_notifications_expires_at ON notifications(expires_at) WHERE deleted_at IS NULL;

-- Add foreign key constraint
ALTER TABLE notifications
ADD CONSTRAINT fk_notifications_user
FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE;

-- Add comments
COMMENT ON TABLE notifications IS 'System notifications for users (messages, reminders, alerts, system notices)';
COMMENT ON COLUMN notifications.type IS 'Type: ANNOUNCEMENT, MESSAGE, REMINDER, ALERT, SYSTEM';
COMMENT ON COLUMN notifications.status IS 'Status: PENDING, SENT, DELIVERED, READ, DISMISSED';
COMMENT ON COLUMN notifications.source_type IS 'Source entity type: ANNOUNCEMENT, MESSAGE, etc.';

-- Create message_read_receipts table
CREATE TABLE IF NOT EXISTS message_read_receipts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    message_id UUID NOT NULL,
    user_id UUID NOT NULL,
    read_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    UNIQUE(message_id, user_id)
);

-- Create indexes for message_read_receipts
CREATE INDEX IF NOT EXISTS idx_read_receipts_message ON message_read_receipts(message_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_read_receipts_user ON message_read_receipts(user_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_read_receipts_read_at ON message_read_receipts(read_at) WHERE deleted_at IS NULL;

-- Add foreign key constraints
ALTER TABLE message_read_receipts
ADD CONSTRAINT fk_read_receipts_message
FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE;

ALTER TABLE message_read_receipts
ADD CONSTRAINT fk_read_receipts_user
FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE;

-- Add comments
COMMENT ON TABLE message_read_receipts IS 'Read receipts for messages tracking which users have read which messages';
COMMENT ON COLUMN message_read_receipts.read_at IS 'Timestamp when message was marked as read';

-- Seed initial announcement priorities for reference
-- This can be expanded based on specific school requirements