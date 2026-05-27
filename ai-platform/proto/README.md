# Protocol Buffers - AI Platform

This directory contains the canonical Protocol Buffer definitions for the AI Platform. This is the single source of truth for all service contracts.

## Directory Structure

```
proto/
├── buf.yaml              # Buf configuration for linting and validation
├── buf.gen.yaml          # Buf generation configuration
├── common/               # Shared types, enums, and errors
│   ├── common.proto      # Common message definitions
│   ├── errors.proto      # Standard error codes and messages
│   └── enums.proto       # Common enumerations
├── audit_service.proto   # Audit service definitions
├── embedding_service.proto
├── generation_service.proto
├── metadata_service.proto
├── moderation_service.proto
├── parser_service.proto
├── reranking_service.proto
├── retrieval_service.proto
├── semantic_chunk_service.proto
└── vision_service.proto
```

## Service Protocols

The following services have gRPC protocol definitions:

1. **Audit Service** (`audit_service.proto`) - Audit logging and compliance tracking
2. **Embedding Service** (`embedding_service.proto`) - Text and image embeddings
3. **Generation Service** (`generation_service.proto`) - LLM text generation
4. **Metadata Service** (`metadata_service.proto`) - Document metadata extraction
5. **Moderation Service** (`moderation_service.proto`) - Content moderation
6. **Parser Service** (`parser_service.proto`) - Document parsing and extraction
7. **Reranking Service** (`reranking_service.proto`) - Result reranking
8. **Retrieval Service** (`retrieval_service.proto`) - Vector search and retrieval
9. **Semantic Chunk Service** (`semantic_chunk_service.proto`) - Intelligent document chunking
10. **Vision Service** (`vision_service.proto`) - Image processing and OCR

## Common Types

The `common/` directory contains shared types used across multiple services:

- **common.proto**: Standard response wrappers, pagination, document references, health checks
- **errors.proto**: Standard error codes and error message format
- **enums.proto**: Common enumerations (document formats, status codes, model types, etc.)

## Usage

### Prerequisites

Install the Buf CLI:
```bash
# macOS
brew install bufbuild/buf/buf

# Linux
curl -sSL https://github.com/bufbuild/buf/releases/latest/download/buf-Linux-x86_64 -o /usr/local/bin/buf
chmod +x /usr/local/bin/buf

# Windows (PowerShell)
iwr -useb https://github.com/bufbuild/buf/releases/latest/download/buf-Windows-x86_64.exe -OutFile buf.exe
```

### Linting

Check proto files for lint errors:
```bash
cd proto
buf lint
```

### Breaking Change Detection

Check for breaking changes:
```bash
cd proto
buf breaking --against '.git#branch=main'
```

### Code Generation

Generate Python and Go stubs:
```bash
cd proto
buf generate
```

This will generate:
- Python stubs in `../shared/grpc/python/`
- Go stubs in `../sdk/go/`

### Format

Format proto files:
```bash
cd proto
buf format -w
```

## Development Workflow

1. **Modify proto files**: Edit `.proto` files in this directory
2. **Lint**: Run `buf lint` to check for errors
3. **Format**: Run `buf format -w` to format files
4. **Generate**: Run `buf generate` to generate stubs
5. **Test**: Test generated code in your services
6. **Commit**: Commit both proto files and generated code

## Package Naming

All proto files use the package naming convention:
```
package ai.platform.<service_name>.v1;
```

Common types use:
```
package ai.platform.common.v1;
```

## Versioning

- Proto files follow semantic versioning
- Breaking changes require a new major version
- Additions are backward compatible
- Deprecate old fields/messages before removing

## Dependencies

This workspace depends on:
- `buf.build/googleapis/googleapis` - Google API common types

## Generated Code Locations

- **Python**: `../shared/grpc/python/`
- **Go**: `../sdk/go/`

## Backend Integration

The Go backend in `../backend/internal/ai/proto/` contains Go-specific customizations (e.g., `go_package` options). Those files should be kept in sync with the canonical definitions in this directory.

## Best Practices

1. **Use common types**: Import from `common/` when possible
2. **Document fields**: Add comments for all messages and fields
3. **Use enums**: Define enums instead of magic strings/numbers
4. **Handle errors**: Use standard error codes from `errors.proto`
5. **Version packages**: Use `v1` suffix for package names
6. **Future-proof**: Add `reserved` ranges for future fields

## Troubleshooting

### Import Errors

If you get import errors, ensure:
- All proto files have proper syntax
- Package names are consistent
- Dependencies are declared in `buf.yaml`

### Generation Failures

If generation fails:
1. Check Buf CLI version: `buf --version`
2. Update dependencies: `buf mod update`
3. Check for syntax errors: `buf lint`

### Breaking Changes

To check for breaking changes against main:
```bash
buf breaking --against '.git#branch=main'
```

## Additional Resources

- [Buf Documentation](https://buf.build/docs)
- [Protocol Buffers Guide](https://protobuf.dev/)
- [gRPC Python Documentation](https://grpc.io/docs/languages/python/)
- [gRPC Go Documentation](https://grpc.io/docs/languages/go/)