# Storage Migrations

This directory contains migration scripts for managing database schemas and collection configurations.

## Structure

```
storage/migrations/
├── postgresql/          # PostgreSQL database migrations
│   ├── versions/       # Migration version files
│   ├── env.py         # Alembic environment configuration
│   ├── script.py.mako # Migration script template
│   └── alembic.ini    # Alembic configuration
├── qdrant/            # Qdrant collection schemas
│   ├── collections/   # Collection definitions
│   └── apply.py       # Collection creation script
└── README.md          # This file
```

## PostgreSQL Migrations

Uses Alembic for database version control.

### Running Migrations

```bash
# Apply all migrations
cd storage/migrations/postgresql
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Create new migration
alembic revision --autogenerate -m "description"

# Check current version
alembic current

# View migration history
alembic history
```

### Migration Files

Naming convention: `{revision}_{description}.py`

Example: `001_initial_schema.py`

## Qdrant Collections

Collection schemas are defined in Python files and applied via the apply script.

### Running Collection Setup

```bash
# Apply all collection schemas
cd storage/migrations/qdrant
python apply.py --all

# Apply specific collection
python apply.py --collection document_embeddings

# List collections
python apply.py --list
```

### Collection Files

Each collection is defined in a separate Python file with:
- Collection name
- Vector size and distance metric
- Payload schema
- Indexing configuration

Example: `document_embeddings.py`

## Best Practices

1. **Always review migrations** before applying to production
2. **Test migrations** on staging environment first
3. **Backup database** before major schema changes
4. **Use descriptive migration names** for easy history tracking
5. **Keep migrations reversible** when possible
6. **Document breaking changes** in migration descriptions

## Environment Variables

Required environment variables:

```bash
# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USERNAME=postgres
POSTGRES_PASSWORD=password
POSTGRES_DATABASE=ai_platform

# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

## Troubleshooting

### PostgreSQL Migration Issues

```bash
# Check if migration was applied
alembic current

# View detailed error
alembic upgrade head --sql

# Force specific version (use with caution)
alembic stamp <revision_id>
```

### Qdrant Collection Issues

```bash
# Check if collection exists
python apply.py --check document_embeddings

# Delete and recreate collection
python apply.py --recreate document_embeddings
```