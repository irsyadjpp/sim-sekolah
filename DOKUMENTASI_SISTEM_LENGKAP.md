# Dokumentasi Lengkap Sistem SIM Sekolah Terpadu

## Table of Contents
1. [Overview Sistem](#overview-sistem)
2. [Arsitektur Sistem](#arsitektur-sistem)
3. [Backend API](#backend-api)
4. [Frontend Application](#frontend-application)
5. [AI Platform](#ai-platform)
6. [Integrasi Antar Komponen](#integrasi-antar-komponen)
7. [Technology Stack](#technology-stack)
8. [Fitur Utama](#fitur-utama)
9. [Database Schema](#database-schema)
10. [Security & Authentication](#security--authentication)

---

## Overview Sistem

SIM Sekolah Terpadu adalah sistem informasi manajemen sekolah enterprise-grade yang dirancang khusus untuk SD Negeri dengan dukungan Kurikulum Merdeka. Sistem ini terdiri dari tiga komponen utama:

1. **Backend API** - Go-based REST API dengan Fiber framework
2. **Frontend Application** - React-based SPA dengan modern UI
3. **AI Platform** - Python-based educational intelligence platform

### Tujuan Utama
- Manajemen operasional sekolah SD Negeri (tanpa modul pembayaran)
- Kompatibilitas dengan sinkronisasi Dapodik
- Dukungan standar rapor Kurikulum Merdeka 2026 (KSP)
- Integrasi AI berbasis Google Gemini untuk administrasi guru
- Kemampuan Deep Learning untuk pembelajaran personal

---

## Arsitektur Sistem

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (ReactJS)                        │
│                    UI & User Interaction                      │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP/REST
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                  Backend API (Go + Fiber)                   │
│            Business Logic & Data Management                  │
└─────────────────────────┬───────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ↓               ↓               ↓
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │PostgreSQL│   │  Redis   │   │RabbitMQ  │
    └──────────┘   └──────────┘   └──────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                  AI Platform (Python)                       │
│         Educational Intelligence & AI Services               │
└─────────────────────────────────────────────────────────────┘
```

### Microservices Architecture
Sistem menggunakan arsitektur modular dengan pemisahan yang jelas antara komponen:

- **Backend**: Menangani business logic, authentication, school management
- **Frontend**: Menangani UI, dashboard, user interaction  
- **AI Platform**: Menangani AI processing, document intelligence, educational analytics

---

## Backend API

### Struktur Folder
```
backend/
├── cmd/                    # Application entry point
│   └── main.go            # Main application file
├── config/                # Configuration files
│   ├── database.go        # Database configuration
│   ├── env.go            # Environment variables
│   ├── migrate.go        # Database migration
│   ├── rabbitmq.go       # Message broker config
│   ├── redis.go          # Cache configuration
│   ├── shutdown.go       # Graceful shutdown
│   └── viper.go          # Configuration management
├── internal/              # Private application code
│   ├── academic_year/    # Manajemen tahun ajaran
│   ├── ai/              # AI integration endpoints
│   ├── assessment/      # Manajemen asesmen & penilaian
│   ├── auth/            # Authentication & authorization
│   ├── character_intervention/ # Intervensi karakter
│   ├── classroom/       # Manajemen rombel
│   ├── communication/   # Komunikasi (pesan, pengumuman)
│   ├── cp/              # Capaian Pembelajaran
│   ├── curriculum/      # Manajemen kurikulum
│   ├── database_monitoring/ # Monitoring database
│   ├── deep_learning/   # Deep learning features
│   ├── differentiated_instruction/ # Pembelajaran berdiferensiasi
│   ├── document_repository/ # Repositori dokumen
│   ├── enrollment/      # Pendaftaran siswa
│   ├── foundational_skills/ # Literasi & numerasi dasar
│   ├── grade/           # Manajemen tingkat kelas
│   ├── individual_learning_plan/ # ILP
│   ├── intelligence/    # Intelligence testing
│   ├── intervention/    # Intervensi akademik
│   ├── learning/        # Pembelajaran
│   ├── learning_experience/ # Pengalaman belajar
│   ├── learning_principle/ # Prinsip pembelajaran
│   ├── lesson_planning/ # Perencanaan pembelajaran
│   ├── local_context/   # Konteks lokal
│   ├── numeracy/        # Numerasi
│   ├── offline/         # Offline sync
│   ├── olah_aspect/     # Aspek OLah (P5)
│   ├── p5/              # Projek P5
│   ├── parent_partnership/ # Kemitraan orang tua
│   ├── peer_assessment/ # Asesmen sejawat
│   ├── permission/      # Manajemen hak akses
│   ├── phase/           # Manajemen fase
│   ├── play_based_learning/ # Pembelajaran berbasis main
│   ├── portfolio/       # Portfolio siswa
│   ├── profile_dimension/ # Dimensi profil pelajar
│   ├── promotion/       # Kenaikan kelas
│   ├── reading_literacy/ # Literasi membaca
│   ├── report/          # Rapor
│   ├── rubric/          # Rubrik penilaian
│   ├── schedule/        # Jadwal pelajaran
│   ├── school/          # Manajemen sekolah
│   ├── spmb/            # PPDB/SPMB
│   ├── student/         # Manajemen siswa
│   ├── subject/         # Manajemen mata pelajaran
│   ├── supervision/     # Supervisi akademik
│   ├── system/          # System monitoring & audit
│   ├── teacher/         # Manajemen guru
│   ├── teaching_assignment/ # Penugasan mengajar
│   └── teaching_reflection/ # Refleksi mengajar
├── routes/              # API route definitions
│   ├── health.routes.go
│   └── routes.go       # Main route setup
├── pkg/                 # Public library code
├── migrations/          # Database migration files
├── scripts/            # Utility scripts
└── tools/              # Build & development tools
```

### Modul Backend Utama

#### 1. Modul Institusi & Aktor
- **academic_year**: Manajemen tahun ajaran aktif
- **school**: Manajemen profil sekolah
- **grade**: Manajemen tingkat kelas (1-6)
- **teacher**: Manajemen data guru dengan auto-create user
- **student**: Manajemen data siswa lengkap
- **user**: Manajemen user sistem
- **permission**: RBAC (Role-Based Access Control)

#### 2. Modul Kurikulum Merdeka
- **cp**: Capaian Pembelajaran
- **phase**: Manajemen fase (A, B, C)
- **subject**: Mata pelajaran per fase
- **curriculum**: Kurikulum Satuan Pendidikan (KSP)
- **profile_dimension**: Dimensi Profil Pelajar Pancasila
- **learning_principle**: Prinsip pembelajaran
- **learning_experience**: Pengalaman belajar
- **olah_aspect**: Aspek OLah (Olah Lima)

#### 3. Modul Konteks Lokal
- **local_context**: 
  - Konteks lingkungan sekolah
  - Realitas sosial & budaya
  - Potensi daerah
  - Pengalaman nyata siswa
  - Integrasi dengan modul ajar & P5

#### 4. Modul Manajemen Kelas & KBM
- **classroom**: Rombongan belajar
- **enrollment**: Pendaftaran siswa ke rombel (bulk)
- **teaching_assignment**: Penugasan guru per mata pelajaran
- **schedule**: Jadwal pelajaran

#### 5. Modul Asesmen & Penilaian
- **assessment**: 
  - Asesmen formatif & sumatif
  - Bulk upsert nilai
  - Management asesmen
- **rubric**: Rubrik penilaian
- **question_bank**: Bank soal
- **portfolio**: Portfolio siswa
- **peer_assessment**: Asesmen sejawat

#### 6. Modul Pembelajaran
- **learning**: Manajemen pembelajaran
- **lesson_planning**: Perencanaan pembelajaran
- **p5**: Projek Penguatan Profil Pelajar Pancasila
- **intervention**: Intervensi akademik
- **character_intervention**: Intervensi karakter

#### 7. Modul SD Spesifik (Kurikulum Merdeka)
- **foundational_skills**: Literasi & numerasi dasar
- **reading_literacy**: Literasi membaca
- **numeracy**: Numerasi
- **deep_learning**: Pembelajaran mendalam
- **differentiated_instruction**: Pembelajaran berdiferensiasi
- **play_based_learning**: Pembelajaran berbasis main
- **individual_learning_plan**: ILP

#### 8. Modul Rapor & Laporan
- **report**: Rapor Kurikulum Merdeka
  - Nilai intrakurikuler
  - Nilai P5
  - Observasi deep learning
- **supervision**: Supervisi akademik
- **teaching_reflection**: Refleksi mengajar

#### 9. Modul Komunikasi
- **communication**:
  - Pengumuman sekolah
  - Pesan internal
  - Notifikasi

#### 10. Modul SPMB/PPDB
- **spmb**: Sistem Penerimaan Murid Baru
  - Alur pendaftaran lengkap
  - Auto-generate data siswa aktif
  - Generate NIS lokal

#### 11. Modul Security & Audit
- **auth**: 
  - JWT authentication
  - HttpOnly cookie
  - MFA (TOTP)
  - Token expiration policy
- **system**:
  - Audit logging (GORM hooks)
  - System telemetry
  - Database monitoring

#### 12. Modul AI Integration
- **ai**: 
  - Google Gemini integration
  - Auto-generated narratives
  - AI-powered features

#### 13. Modul Infrastructure
- **offline**: Offline synchronization
- **document_repository**: Document management system
- **database_monitoring**: Database health monitoring

### Pattern Backend
Setiap modul mengikuti struktur standar:
```
modul/
├── dto.go          # Data Transfer Objects
├── model.go        # Database models
├── repository.go   # Database operations
├── service.go      # Business logic
├── handler.go      # HTTP handlers
└── routes.go       # Route definitions
```

---

## Frontend Application

### Struktur Folder
```
frontend/src/
├── components/          # Reusable components
│   ├── charts/         # Chart components
│   ├── data-grid/      # Data grid components
│   ├── guards/         # Route guards (auth, guest)
│   ├── icons/          # Icon components
│   ├── layout/         # Layout components
│   │   ├── containers/ # Main layout containers
│   │   ├── menu/       # Navigation menu
│   │   └── shortcuts/  # Keyboard shortcuts
│   └── plugins/        # Special components
├── pages/              # Page components
│   ├── app/           # Main application pages
│   │   ├── academic/  # Academic pages
│   │   │   ├── curriculum/
│   │   │   ├── evaluation/
│   │   │   ├── subjects/
│   │   │   ├── foundational-skills/
│   │   │   ├── reading-literacy/
│   │   │   ├── numeracy/
│   │   │   ├── supervision/
│   │   │   └── question-bank/
│   │   ├── learning/  # Learning pages
│   │   │   ├── modules/
│   │   │   ├── projects/
│   │   │   ├── lesson-plans/
│   │   │   ├── intervention/
│   │   │   └── character/
│   │   ├── students/  # Student pages
│   │   │   ├── evidence/
│   │   │   ├── growth/
│   │   │   ├── character-growth/
│   │   │   ├── presence/
│   │   │   ├── guidance/
│   │   │   └── ilp/
│   │   ├── teachers/  # Teacher pages
│   │   ├── communication/
│   │   ├── reports/
│   │   ├── analytics/
│   │   ├── system/
│   │   ├── spmb/
│   │   ├── profile/
│   │   ├── local-context/
│   │   └── dashboards/
│   ├── auth/          # Authentication pages
│   └── landing-page/  # Landing page
├── hooks/             # Custom React hooks
├── i18n/              # Internationalization
├── icons/             # Icon definitions
├── lib/               # Utility libraries
├── style/             # Global styles
├── theme/             # Theme configuration
├── types/             # TypeScript type definitions
├── App.tsx            # Main app component
├── config.ts          # App configuration
├── constants.ts       # App constants
├── main.tsx           # Application entry point
├── menu-items.tsx     # Navigation menu structure
└── routes.tsx         # Route definitions
```

### Modul Frontend Utama

#### 1. Menu Structure
Frontend menggunakan menu berbasis yang mencerminkan struktur sistem:

**Data Induk (Institution)**
- School Profile
- Staff Data (Character Building)
- Student Data
- Evidence Data
- Growth Data
- Character Growth Data
- SPMB Online
- Class Data
- Teacher Workload
- Teacher Reflection

**Kurikulum (Curriculum)**
- Standar Belajar:
  - Phases
  - Subjects
  - Standards
  - Objectives
  - Flow
  - Dimensions
- Data Lokal (Local Context)
- KSP Builder
- Kokurikuler
- Ekstrakurikuler

**Pembelajaran (Learning)**
- Class Schedule
- Daily Presence
- Teaching Modules:
  - Drafts
  - Library
- P5 Projects
- Lesson Planning
- Intervention

**SD Spesifik**
- Foundational Skills:
  - Assessment
  - Progress
- Reading Literacy:
  - Assessment
  - Progression
- Numeracy

**Asesmen (Assessment)**
- Question Bank
- Formative Value
- Summative Value
- SD Assessment Criteria
- Portfolio
- Rubric
- Supervision

**Laporan (Reports)**
- P5 Achievement
- Gradebook Recap
- Print Rapport

**Analytics**
- Learning Analytics

**Komunikasi (Communication)**
- Announcements
- Messages

**Sistem (System)**
- Access Rights
- Academic Year Cycle
- Grade Level Master
- Data Index
- Database Monitoring
- Document Repository
- Offline Sync

#### 2. Component Architecture
Frontend menggunakan component-based architecture dengan:
- **Layout Components**: Header, Footer, Sidebar, Main Container
- **Data Components**: DataGrid, Charts, Forms
- **Guard Components**: AuthGuard, GuestGuard
- **UI Components**: Buttons, Inputs, Modals, Notifications

#### 3. State Management
Menggunakan React Context API dan custom hooks untuk state management lokal.

#### 4. Routing
Client-side routing dengan React Router untuk navigasi antar halaman.

---

## AI Platform

### Struktur Folder
```
ai-platform/
├── ai-agents/                  # AI Agent implementations
├── deployment/                 # Deployment configurations
│   ├── dev/
│   ├── staging/
│   └── production/
├── docs/                       # Documentation
├── educational-intelligence/   # Educational AI engines
│   ├── adaptive-learning-engine/
│   ├── assessment-engine/
│   ├── curriculum-engine/
│   ├── learning-graph-engine/
│   ├── learning-progression-engine/
│   ├── pedagogy-engine/
│   └── recommendation-engine/
├── educational-observability/  # AI monitoring & observability
├── educational-ontology/       # Educational knowledge structures
├── hallucination-guard/         # AI hallucination prevention
│   ├── retrieval-grounding-validator/
│   ├── pedagogy-validator/
│   ├── competency-validator/
│   ├── phase-validator/
│   ├── assessment-validator/
│   └── curriculum-validator/
├── infra/                      # Infrastructure configurations
│   ├── prometheus/
│   ├── postgres/
│   ├── rabbitmq/
│   ├── kubernetes/
│   ├── loki/
│   ├── grafana/
│   ├── kafka/
│   ├── qdrant/
│   ├── nginx/
│   ├── minio/
│   ├── tempo/
│   └── docker/
├── knowledge/                  # Knowledge base management
├── models/                     # AI model management
├── notebooks/                  # Jupyter notebooks
├── pipelines/                  # AI processing pipelines
├── retrieval-enhancement/      # RAG & retrieval systems
├── scripts/                    # Utility scripts
├── semantic-enrichment/        # Semantic processing
├── services/                   # Microservices
│   ├── audit-service/
│   ├── embedding-service/
│   ├── gateway-service/
│   ├── generation-service/
│   ├── metadata-service/
│   ├── moderation-service/
│   ├── monitoring-service/
│   ├── notification-service/
│   ├── orchestration-service/
│   ├── parser-service/
│   ├── reranking-service/
│   ├── retrieval-service/
│   ├── semantic-chunk-service/
│   └── vision-service/
├── shared/                     # Shared utilities
├── storage/                    # Storage management
├── tests/                      # Test suites
└── workers/                    # Background workers
```

### Modul AI Platform Utama

#### 1. Educational Intelligence Layer
- **curriculum-engine**: Validasi CP, ATP, fase, grade alignment
- **pedagogy-engine**: Analisis pedagogi (inquiry, differentiated, deep learning)
- **assessment-engine**: Pembuatan asesmen formatif, HOTS, rubric generation
- **learning-progression-engine**: Deteksi mastery progression, prerequisite gaps
- **learning-graph-engine**: Knowledge graph pendidikan (competency graph)
- **adaptive-learning-engine**: Sistem pembelajaran adaptif
- **recommendation-engine**: Rekomendasi pembelajaran personal

#### 2. Document Intelligence Pipeline
- **parser-service**: PDF processing, text extraction
- **vision-service**: Image processing, OCR
- **semantic-chunk-service**: Semantic chunking berbasis kurikulum
- **metadata-service**: Metadata extraction
- **embedding-service**: Text & formula embeddings

#### 3. Retrieval Enhancement
- **retrieval-service**: Hybrid retrieval (semantic + metadata + pedagogy)
- **reranking-service**: Re-ranking hasil retrieval
- **retrieval-grounding-validator**: Validasi grounding

#### 4. AI Generation & Orchestration
- **generation-service**: AI content generation
- **orchestration-service**: AI workflow orchestration
- **moderation-service**: Content moderation

#### 5. Hallucination Guard
- **curriculum-validator**: Validasi alignment kurikulum
- **pedagogy-validator**: Validasi pedagogis
- **competency-validator**: Validasi kompetensi
- **phase-validator**: Validasi fase
- **assessment-validator**: Validasi asesmen

#### 6. Observability & Governance
- **audit-service**: Audit logging
- **monitoring-service**: AI performance monitoring
- **educational-observability**: Educational metrics tracking

### Knowledge Structure
```
knowledge/
├── cp/              # Capaian Pembelajaran
├── atp/             # Alur Tujuan Pembelajaran
├── buku_guru/       # Buku Guru
├── buku_siswa/      # Buku Siswa
├── modul_ajar/      # Modul Ajar
├── asesmen/         # Bank Asesmen
└── p5/              # Projek P5
```

---

## Integrasi Antar Komponen

### Backend ↔ Frontend Integration
- **Protocol**: HTTP/REST API
- **Authentication**: JWT tokens with HttpOnly cookies
- **Data Format**: JSON
- **CORS**: Configured for allowed origins

### Backend ↔ AI Platform Integration
- **Protocol**: HTTP/REST API
- **Message Queue**: RabbitMQ for async processing
- **Vector Database**: Qdrant for semantic search
- **File Storage**: MinIO/RustFS for document storage

### Data Flow Architecture
```
Frontend → Backend API → PostgreSQL
                 ↓
            Redis (Cache)
                 ↓
            RabbitMQ (Queue)
                 ↓
         AI Platform Services
                 ↓
            Qdrant (Vector DB)
                 ↓
            MinIO (Storage)
```

---

## Technology Stack

### Backend Stack
- **Language**: Go 1.26
- **Framework**: Fiber v2 (web framework)
- **Database**: PostgreSQL 16.5
- **Cache**: Redis v9
- **Message Broker**: RabbitMQ
- **Vector Database**: Qdrant
- **Object Storage**: RustFS
- **ORM**: GORM
- **Migration**: golang-migrate/migrate
- **Observability**: OpenTelemetry + Loki + Tempo + Grafana
- **Documentation**: Swagger
- **AI Integration**: Google Gemini API

### Frontend Stack
- **Framework**: React (TypeScript)
- **Build Tool**: Vite
- **UI Components**: Material-UI (MUI)
- **Routing**: React Router
- **State Management**: React Context API
- **Charts**: Custom chart components
- **Forms**: React Hook Form
- **HTTP Client**: Axios
- **Internationalization**: i18next

### AI Platform Stack
- **Language**: Python
- **Framework**: FastAPI
- **PDF Processing**: PyMuPDF
- **Layout Intelligence**: Unstructured
- **Table Extraction**: Camelot
- **OCR**: Tesseract OCR
- **Formula OCR**: Nougat
- **Embeddings**: BAAI/bge-m3, multilingual-e5-large
- **Vector Database**: Qdrant
- **Queue**: Kafka/RabbitMQ
- **Storage**: MinIO
- **Monitoring**: Prometheus + Grafana

---

## Fitur Utama

### 1. Manajemen Institusi
- Multi-school support
- Tahun ajaran management
- Grade/phase management
- User management dengan RBAC
- Audit logging lengkap

### 2. Manajemen Kurikulum Merdeka
- Kurikulum Satuan Pendidikan (KSP)
- Capaian Pembelajaran (CP)
- Alur Tujuan Pembelajaran (ATP)
- Dimensi Profil Pelajar Pancasila
- Prinsip & Pengalaman Belajar

### 3. Konteks Lokal
- Konteks lingkungan sekolah
- Realitas sosial & budaya
- Potensi daerah
- Rekomendasi kontekstual

### 4. Manajemen Kelas & KBM
- Rombongan belajar
- Bulk enrollment
- Teaching assignments
- Jadwal pelajaran
- Kehadiran harian

### 5. Asesmen & Penilaian
- Asesmen formatif & sumatif
- Bank soal
- Rubrik penilaian
- Portfolio siswa
- Asesmen sejawat
- Bulk upsert nilai

### 6. Pembelajaran
- Modul ajar
- Projek P5
- Perencanaan pembelajaran
- Intervensi akademik
- Intervensi karakter

### 7. SD Spesifik
- Literasi dasar
- Numerasi
- Literasi membaca
- Pembelajaran mendalam
- Pembelajaran berdiferensiasi
- Pembelajaran berbasis main
- ILP

### 8. Rapor & Laporan
- Rapor Kurikulum Merdeka
- Nilai intrakurikuler
- Nilai P5
- Observasi deep learning
- Supervisi akademik
- Refleksi mengajar

### 9. Komunikasi
- Pengumuman sekolah
- Pesan internal
- Notifikasi

### 10. SPMB/PPDB
- Pendaftaran online
- Auto-generate siswa aktif
- Generate NIS lokal
- Alur pendaftaran lengkap

### 11. Security & Governance
- JWT authentication
- MFA (TOTP)
- RBAC
- Audit logging
- Token expiration policy
- Database monitoring

### 12. AI Integration
- Google Gemini integration
- Auto-generated narratives
- Educational intelligence
- Curriculum-aware AI
- Pedagogy-aware retrieval
- Competency-aware learning

### 13. Offline Support
- Offline synchronization
- Background workers
- Conflict resolution

### 14. Document Management
- Document repository
- Version control
- Access control
- Approval workflow

---

## Database Schema

### Main Entities

#### Institution & Actors
- schools (sekolah)
- academic_years (tahun ajaran)
- grades (tingkat kelas)
- phases (fase)
- teachers (guru)
- students (siswa)
- users (user sistem)
- permissions (hak akses)

#### Curriculum
- curricula (kurikulum)
- learning_objectives (capaian pembelajaran)
- teaching_objectives (tujuan pembelajaran)
- subjects (mata pelajaran)
- profile_dimensions (dimensi profil pelajar)
- learning_principles (prinsip pembelajaran)
- learning_experiences (pengalaman belajar)

#### Local Context
- local_contexts (konteks lokal)
- environmental_contexts (konteks lingkungan)
- social_contexts (konteks sosial)
- cultural_contexts (konteks budaya)

#### Class & Learning
- classrooms (rombel)
- enrollments (pendaftaran)
- teaching_assignments (penugasan mengajar)
- schedules (jadwal)
- attendances (kehadiran)

#### Assessment
- assessments (asesmen)
- assessment_items (item asesmen)
- rubrics (rubrik)
- rubric_levels (level rubrik)
- portfolios (portfolio)
- peer_assessments (asesmen sejawat)

#### Learning
- learning_modules (modul ajar)
- lesson_plans (rencana pembelajaran)
- p5_projects (projek P5)
- interventions (intervensi)

#### SD Specific
- foundational_skills (literasi dasar)
- reading_literacy (literasi membaca)
- numeracy_assessments (asesmen numerasi)
- deep_learning_observations (observasi deep learning)
- individual_learning_plans (ILP)

#### Reports
- reports (rapor)
- report_grades (nilai rapor)
- supervisions (supervisi)
- teaching_reflections (refleksi mengajar)

#### Communication
- announcements (pengumuman)
- messages (pesan)
- notifications (notifikasi)

#### SPMB
- spmb_registrations (pendaftaran SPMB)
- spmb_applicants (pelamar)

#### System
- audit_logs (log audit)
- system_metrics (metrik sistem)
- document_repositories (repositori dokumen)

---

## Security & Authentication

### Authentication Flow
1. User submits credentials
2. Backend validates credentials
3. Backend generates JWT token
4. Token stored in HttpOnly cookie
5. MFA verification (if enabled)
6. Token used for subsequent requests

### Security Features
- **JWT Authentication**: Secure token-based authentication
- **HttpOnly Cookies**: Prevent XSS attacks
- **MFA Support**: TOTP-based multi-factor authentication
- **Token Expiration**: Automatic token expiry on weekends/holidays
- **RBAC**: Role-based access control
- **Audit Logging**: Complete audit trail
- **CORS Protection**: Configured CORS policies
- **Rate Limiting**: Redis-based rate limiting
- **SQL Injection Protection**: GORM parameterized queries
- **XSS Protection**: Input sanitization

### Roles & Permissions
- **Super Admin**: Full system access
- **School Admin**: School-level administration
- **Teacher**: Classroom and teaching access
- **Student**: Limited access to own data
- **Parent**: Access to child's data

---

## Deployment Architecture

### Development Environment
```yaml
Services:
  - Backend API (Go)
  - Frontend (React)
  - PostgreSQL
  - Redis
  - RabbitMQ
  - Qdrant
  - RustFS
```

### Production Environment
```yaml
Infrastructure:
  - Kubernetes Cluster
  - PostgreSQL HA
  - Redis Cluster
  - RabbitMQ Cluster
  - Qdrant Cluster
  - MinIO Object Storage
  - Prometheus Monitoring
  - Grafana Dashboard
  - Loki Log Aggregation
  - Tempo Tracing
```

---

## Monitoring & Observability

### OpenTelemetry Integration
- **Tracing**: Distributed tracing with Tempo
- **Logging**: Structured JSON logging with Loki
- **Metrics**: Prometheus metrics collection
- **Dashboard**: Grafana dashboards

### Database Monitoring
- Query performance tracking
- Slow query detection
- Connection pool monitoring
- Database health checks

### AI Observability
- AI response logging
- Retrieval quality metrics
- Hallucination detection
- Performance tracking

---

## API Documentation

### Swagger Integration
Backend dilengkapi dengan dokumentasi Swagger interaktif:
- URL: `http://localhost:8080/swagger/index.html`
- Auto-generated from code annotations
- Interactive API testing
- Complete endpoint documentation

---

## Development Workflow

### Backend Development
```bash
# Install dependencies
go mod tidy

# Run migration (automatic on startup)
# Migration files in /migrations

# Run server
go run cmd/main.go

# Generate Swagger
swag init -g cmd/main.go --parseDependency --parseInternal

# Run tests
go test ./...
```

### Frontend Development
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Run tests
npm test
```

### AI Platform Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run services
python -m services.gateway_service.main

# Run tests
pytest tests/
```

---

## Future Enhancements

### Planned Features
1. **Advanced Analytics**: Learning analytics dashboard
2. **Mobile App**: Native mobile applications
3. **Parent Portal**: Enhanced parent engagement
4. **AI Tutoring**: Personal AI tutoring system
5. **Predictive Analytics**: Early warning systems
6. **Enhanced Rapor**: More comprehensive reporting
7. **Integration Hub**: Third-party system integrations
8. **Advanced AI**: More sophisticated AI capabilities

---

## Support & Maintenance

### Documentation
- Backend README: `backend/README.md`
- AI Platform README: `ai-platform/README.md`
- API Documentation: Swagger UI
- Code Comments: Inline documentation

### Support Channels
- GitHub Issues: Bug tracking and feature requests
- Documentation: Comprehensive system documentation
- Code Review: Regular code review process

---

## Conclusion

SIM Sekolah Terpadu adalah sistem informasi manajemen sekolah modern yang mengintegrasikan:

1. **Enterprise Backend**: Scalable Go-based API dengan modern architecture
2. **Modern Frontend**: React-based SPA dengan intuitive UI
3. **Educational AI**: Python-based AI platform untuk educational intelligence

Sistem ini dirancang khusus untuk mendukung Kurikulum Merdeka dengan fitur-fitur komprehensif untuk manajemen sekolah SD Negeri, mulai dari manajemen institusi, kurikulum, pembelajaran, asesmen, hingga integrasi AI untuk meningkatkan kualitas pendidikan.

Dengan arsitektur modular, teknologi modern, dan fitur-fitur enterprise-grade, sistem ini siap untuk skala produksi dan dapat dikembangkan lebih lanjut sesuai kebutuhan.
