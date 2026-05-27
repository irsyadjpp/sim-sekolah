# AI Platform Knowledge Base

This directory contains the educational knowledge base for the AI Platform, including curriculum documents, textbooks, learning materials, and domain ontologies.

## Directory Structure

```
knowledge/
├── cp/                    # Capaian Pembelajaran (Learning Outcomes)
│   ├── bahasa/           # Bahasa Indonesia learning outcomes
│   ├── ipa/              # Ilmu Pengetahuan Alam (Natural Sciences)
│   ├── ips/              # Ilmu Pengetahuan Sosial (Social Sciences)
│   └── matematika/       # Mathematics learning outcomes
├── atp/                  # Alur Tujuan Pembelajaran (Learning Objectives Flow)
├── buku_guru/            # Teacher's textbooks
├── buku_siswa/           # Student's textbooks
├── modul_ajar/           # Learning modules
├── asesmen/              # Assessment materials
├── media/                # Educational media resources
├── p5/                   # Projek Penguatan Profil Pelajar Pancasila
├── ontology/             # Educational domain ontologies
└── temporary/            # Temporary staging area

```

## Knowledge Categories

### Curriculum Documents

#### Capaian Pembelajaran (CP)
- **Format**: JSON/CSV/Markdown
- **Content**: Learning outcomes by subject and grade level
- **Structure**: Organized by subject (bahasa, ipa, ips, matematika)
- **Updates**: Per curriculum revision cycle

#### Alur Tujuan Pembelajaran (ATP)
- **Format**: JSON/CSV/Markdown
- **Content**: Learning objectives flow and sequencing
- **Structure**: Organized by grade level and subject
- **Updates**: Per academic year

### Learning Materials

#### Buku Guru (Teacher's Books)
- **Format**: PDF, DOCX
- **Content**: Teacher guides and instructional materials
- **Structure**: Organized by subject and grade level
- **Versioning**: Track publisher editions

#### Buku Siswa (Student's Books)
- **Format**: PDF, DOCX
- **Content**: Student textbooks and workbooks
- **Structure**: Organized by subject and grade level
- **Versioning**: Track publisher editions

#### Modul Ajar (Learning Modules)
- **Format**: PDF, DOCX, MD
- **Content**: Self-contained learning modules
- **Structure**: Organized by topic and difficulty level
- **Versioning**: Track content revisions

### Assessment Materials

#### Asesmen (Assessments)
- **Format**: PDF, DOCX, JSON
- **Content**: Test items, rubrics, evaluation criteria
- **Structure**: Organized by subject and assessment type
- **Versioning**: Track assessment revisions

### Additional Resources

#### Media (Media Resources)
- **Format**: Images, videos, audio, interactive content
- **Content**: Educational media and multimedia resources
- **Structure**: Organized by media type and subject
- **Versioning**: Track media updates

#### P5 (Pancasila Student Profile Projects)
- **Format**: PDF, DOCX, Project templates
- **Content**: Project-based learning materials
- **Structure**: Organized by grade level and project theme
- **Versioning**: Track project template revisions

#### Ontology (Domain Ontologies)
- **Format**: RDF/OWL, TTL, JSON-LD
- **Content**: Educational domain knowledge graphs
- **Structure**: Organized by domain (curriculum, concepts, competencies)
- **Versioning**: Track ontology schema evolution

## Versioning Strategy

### File Versioning
- Use semantic versioning for document revisions: `v1.0.0`, `v1.1.0`, `v2.0.0`
- Store version metadata in `VERSION` files
- Maintain change logs in `CHANGELOG.md` files

### Metadata Standards
Each knowledge asset should include:
- **Title**: Document title
- **Subject**: Subject area
- **Grade Level**: Target grade(s)
- **Author**: Content author/creator
- **Publisher**: Content publisher
- **Publication Date**: Original publication date
- **Last Updated**: Last modification date
- **Version**: Current version
- **Language**: Document language
- **Format**: File format (PDF, DOCX, etc.)
- **License**: Usage license
- **Tags**: Subject-specific tags
- **Curriculum Alignment**: CP/ATP references

### Directory Naming Convention
```
knowledge/{category}/{subject}/{grade}/{version}/
```

Example:
```
knowledge/buku_siswa/matematika/kelas-10/v1.0.0/
```

## Ingestion Pipeline

Knowledge assets are ingested into the AI Platform through the ingestion pipeline:

1. **Upload**: Assets uploaded to MinIO object storage
2. **Parse**: Content extracted and structured
3. **Chunk**: Text split into semantic units
4. **Embed**: Vector embeddings generated
5. **Index**: Stored in Qdrant vector database
6. **Enrich**: Educational metadata added
7. **Graph**: Knowledge graph relationships created

See `pipelines/ingestion/` for pipeline implementation.

## Quality Assurance

### Content Validation
- Format validation (file type, size, structure)
- Content quality checks (completeness, accuracy)
- Curriculum alignment verification
- Duplicate detection

### Metadata Validation
- Required fields present
- Valid values for enums and controlled vocabularies
- Date format validation
- Reference integrity (CP/ATP references)

## Access Control

### Storage Access
- **Public**: Curriculum documents (CP, ATP)
- **Internal**: Licensed materials (textbooks)
- **Restricted**: Assessment materials (protected content)

### Usage Rights
- **Creative Commons**: Open educational resources
- **Fair Use**: Educational use exceptions
- **Licensed**: Publisher-specific licenses
- **Proprietary**: Internal use only

## Maintenance

### Regular Updates
- **Curriculum Revisions**: When Ministry updates curriculum
- **Content Refresh**: Annual review and updates
- **New Materials**: Add as published
- **Obsolete Content**: Archive or remove outdated materials

### Archive Policy
- Move obsolete versions to `archive/` subdirectory
- Maintain for at least 3 academic years
- Compress large archived files
- Document removal rationale

## Integration Points

### Services Integration
- **Parser Service**: Document parsing and extraction
- **Metadata Service**: Educational metadata enrichment
- **Embedding Service**: Vector generation
- **Retrieval Service**: Knowledge retrieval
- **Generation Service**: Content generation

### External Systems
- **Ministry of Education**: Curriculum API (if available)
- **Publishers**: Textbook distribution systems
- **LMS Integration**: Learning management systems
- **Assessment Platforms**: Test delivery systems

## Best Practices

1. **Standardize Formats**: Use consistent file formats within categories
2. **Version Control**: Track all document revisions
3. **Metadata Completeness**: Ensure all required metadata fields
4. **Quality Assurance**: Validate content before ingestion
5. **Backup Strategy**: Regular backups of knowledge base
6. **Access Management**: Implement proper access controls
7. **Documentation**: Document content sources and licensing
8. **Regular Audits**: Periodic content quality audits

## Troubleshooting

### Ingestion Failures
- Check file format compatibility
- Verify file size limits
- Validate metadata completeness
- Review service availability

### Quality Issues
- Run content validation scripts
- Check curriculum alignment
- Verify source authenticity
- Review user feedback

## Contact

For questions about the knowledge base:
- Content Issues: curriculum team
- Technical Issues: platform engineering team
- Licensing Questions: legal department