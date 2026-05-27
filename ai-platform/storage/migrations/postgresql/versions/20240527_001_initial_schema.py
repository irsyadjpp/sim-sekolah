"""Initial schema for AI Platform core tables

Revision ID: 001_initial
Revises: 
Create Date: 2024-05-27

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Documents table
    op.create_table(
        "documents",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("file_path", sa.String(1000), nullable=True),
        sa.Column("file_type", sa.String(50), nullable=True),
        sa.Column("file_size", sa.BigInteger(), nullable=True),
        sa.Column("mime_type", sa.String(100), nullable=True),
        sa.Column("status", sa.String(50), nullable=False, default="pending"),
        sa.Column("source", sa.String(100), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("indexed_at", sa.TIMESTAMP(), nullable=True),
    )
    op.create_index("idx_documents_status", "documents", ["status"])
    op.create_index("idx_documents_source", "documents", ["source"])
    op.create_index("idx_documents_created_at", "documents", ["created_at"])

    # Document chunks table
    op.create_table(
        "document_chunks",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("document_id", sa.UUID(), sa.ForeignKey("documents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("start_pos", sa.Integer(), nullable=True),
        sa.Column("end_pos", sa.Integer(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("NOW()"), nullable=False),
    )
    op.create_index("idx_document_chunks_document_id", "document_chunks", ["document_id"])
    op.create_index("idx_document_chunks_chunk_index", "document_chunks", ["chunk_index"])

    # Embeddings table
    op.create_table(
        "embeddings",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("chunk_id", sa.UUID(), sa.ForeignKey("document_chunks.id", ondelete="CASCADE"), nullable=False),
        sa.Column("model_name", sa.String(100), nullable=False),
        sa.Column("vector_dimension", sa.Integer(), nullable=False),
        sa.Column("vector_id", sa.String(100), nullable=True),  # Reference to Qdrant vector ID
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("NOW()"), nullable=False),
    )
    op.create_index("idx_embeddings_chunk_id", "embeddings", ["chunk_id"])
    op.create_index("idx_embeddings_model_name", "embeddings", ["model_name"])

    # Knowledge base entries table
    op.create_table(
        "knowledge_entries",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("category", sa.String(100), nullable=True),
        sa.Column("difficulty", sa.String(50), nullable=True),
        sa.Column("competency", sa.String(100), nullable=True),
        sa.Column("taxonomy_path", sa.String(500), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("version", sa.String(20), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(), server_default=sa.text("NOW()"), nullable=False),
    )
    op.create_index("idx_knowledge_entries_category", "knowledge_entries", ["category"])
    op.create_index("idx_knowledge_entries_difficulty", "knowledge_entries", ["difficulty"])
    op.create_index("idx_knowledge_entries_competency", "knowledge_entries", ["competency"])

    # Models table
    op.create_table(
        "models",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False, unique=True),
        sa.Column("type", sa.String(50), nullable=False),  # embedding, llm, etc.
        sa.Column("version", sa.String(20), nullable=False),
        sa.Column("framework", sa.String(50), nullable=True),  # pytorch, tensorflow, etc.
        sa.Column("path", sa.String(1000), nullable=True),
        sa.Column("config", sa.JSON(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("status", sa.String(50), nullable=False, default="active"),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(), server_default=sa.text("NOW()"), nullable=False),
    )
    op.create_index("idx_models_name", "models", ["name"])
    op.create_index("idx_models_type", "models", ["type"])
    op.create_index("idx_models_status", "models", ["status"])

    # Users table
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("username", sa.String(100), nullable=False, unique=True),
        sa.Column("full_name", sa.String(255), nullable=True),
        sa.Column("role", sa.String(50), nullable=False, default="user"),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(), server_default=sa.text("NOW()"), nullable=False),
    )
    op.create_index("idx_users_email", "users", ["email"])
    op.create_index("idx_users_username", "users", ["username"])
    op.create_index("idx_users_role", "users", ["role"])

    # Audit log table
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("user_id", sa.UUID(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("resource_type", sa.String(100), nullable=False),
        sa.Column("resource_id", sa.String(100), nullable=True),
        sa.Column("changes", sa.JSON(), nullable=True),
        sa.Column("ip_address", sa.String(50), nullable=True),
        sa.Column("user_agent", sa.String(500), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("NOW()"), nullable=False),
    )
    op.create_index("idx_audit_logs_user_id", "audit_logs", ["user_id"])
    op.create_index("idx_audit_logs_action", "audit_logs", ["action"])
    op.create_index("idx_audit_logs_resource_type", "audit_logs", ["resource_type"])
    op.create_index("idx_audit_logs_created_at", "audit_logs", ["created_at"])

    # Conversations table
    op.create_table(
        "conversations",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("user_id", sa.UUID(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(500), nullable=True),
        sa.Column("context", sa.JSON(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("NOW()"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(), server_default=sa.text("NOW()"), nullable=False),
    )
    op.create_index("idx_conversations_user_id", "conversations", ["user_id"])
    op.create_index("idx_conversations_created_at", "conversations", ["created_at"])

    # Messages table
    op.create_table(
        "messages",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("conversation_id", sa.UUID(), sa.ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("role", sa.String(20), nullable=False),  # user, assistant, system
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("NOW()"), nullable=False),
    )
    op.create_index("idx_messages_conversation_id", "messages", ["conversation_id"])
    op.create_index("idx_messages_role", "messages", ["role"])
    op.create_index("idx_messages_created_at", "messages", ["created_at"])


def downgrade() -> None:
    op.drop_table("messages")
    op.drop_table("conversations")
    op.drop_table("audit_logs")
    op.drop_table("users")
    op.drop_table("models")
    op.drop_table("knowledge_entries")
    op.drop_table("embeddings")
    op.drop_table("document_chunks")
    op.drop_table("documents")