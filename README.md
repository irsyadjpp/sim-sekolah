# SIM Sekolah - UPT SDI Bonerate No. 85

Sistem Informasi Manajemen Sekolah terpadu dengan integrasi AI untuk UPT SDI Bonerate No. 85, Kepulauan Selayar.

## 📋 Ringkasan

SIM Sekolah adalah sistem manajemen sekolah komprehensif yang menggabungkan:
- **Manajemen Akademik**: Kurikulum Merdeka, asesmen, pembelajaran mendalam
- **AI Platform**: Monolith AI untuk analisis kurikulum, pembelajaran, dan asesmen
- **Manajemen Administratif**: PPDB, kehadiran, rapor, dan laporan
- **Observabilitas Enterprise**: Monitoring, logging, dan tracing dengan OpenTelemetry

## 🏗️ Arsitektur Sistem

### Monorepo Structure

```
sim-sekolah/
├── backend/                    # Go backend service (Fiber framework)
│   ├── cmd/                   # Application entry point
│   ├── internal/              # Business logic modules
│   │   ├── academic_year/     # Tahun akademik
│   │   ├── assessment/        # Asesmen & evaluasi
│   │   ├── auth/              # Autentikasi & authorization
│   │   ├── curriculum/        # Manajemen kurikulum
│   │   ├── deep_learning/     # Pembelajaran mendalam
│   │   ├── enrollment/        # PPDB & enrollment
│   │   ├── learning/          # Manajemen pembelajaran
│   │   ├── student/           # Data siswa
│   │   ├── teacher/           # Data guru
│   │   └── ...                # 40+ domain modules
│   ├── pkg/                   # Shared packages
│   └── routes/                # API routes
├── frontend/                   # React/TypeScript frontend
│   ├── src/
│   │   ├── pages/
│   │   │   ├── app/           # Main application pages
│   │   │   │   ├── academic/  # Akademik
│   │   │   │   ├── dashboards/# Dasbor
│   │   │   │   ├── education/ # Pendidikan
│   │   │   │   ├── learning/  # Pembelajaran
│   │   │   │   ├── students/  # Siswa
│   │   │   │   └── teachers/  # Guru
│   │   │   ├── auth/          # Autentikasi
│   │   │   └── landing-page/  # Landing page
│   │   ├── components/        # UI components
│   │   ├── services/          # API services
│   │   └── utils/             # Utilities
├── ai-platform/                # AI Platform monolith (Python/FastAPI)
│   ├── monolith/
│   │   ├── app/
│   │   │   ├── ai_core/       # AI layer (LLM, embeddings)
│   │   │   ├── api/           # FastAPI routes
│   │   │   ├── services/       # Business logic
│   │   │   │   ├── document_ingestion/
│   │   │   │   ├── content_processing/
│   │   │   │   ├── intelligence/
│   │   │   │   └── support/
│   │   │   ├── standards-domain/    # Kurikulum Merdeka
│   │   │   ├── curriculum-domain/  # Manajemen kurikulum
│   │   │   ├── assessment-domain/   # Asesmen
│   │   │   ├── learning-domain/     # Pembelajaran mendalam
│   │   │   ├── character-domain/   # Profil Pelajar Pancasila
│   │   │   ├── teacher-domain/     # Guru
│   │   │   └── student-domain/     # Siswa
│   │   └── main.py        # FastAPI entry point
│   ├── knowledge/              # Knowledge base
│   ├── models/                 # ML models
│   └── storage/                # Storage configurations
├── infrastructure/             # Centralized infrastructure
│   ├── compose/
│   │   ├── sim-sekolah/
│   │   │   └── docker-compose.yml  # SIM Sekolah stack
│   │   └── ai-platform/
│   │       └── docker-compose.yml  # AI Platform monolith
│   ├── kubernetes/             # Kubernetes manifests
│   ├── monitoring/             # Grafana, Prometheus, Loki, Tempo
│   ├── services/               # Service configurations
│   │   ├── postgres/
│   │   ├── redis/
│   │   ├── rabbitmq/
│   │   ├── qdrant/
│   │   └── minio/
│   └── scripts/                # Infrastructure scripts
├── docs/                       # Documentation
├── .env                        # Environment variables
├── .env.example                # Environment variables example
└── README.md                   # This file
```

## 🚀 Tech Stack

### Backend (Go)
- **Framework**: Fiber v2.52
- **Database**: PostgreSQL with GORM
- **Cache**: Redis
- **Message Queue**: RabbitMQ
- **Object Storage**: MinIO (S3-compatible)
- **Vector Database**: Qdrant
- **Observability**: OpenTelemetry, Prometheus
- **Authentication**: JWT, Multi-Factor Authentication (MFA)
- **API Documentation**: Swagger/OpenAPI

### Frontend (React/TypeScript)
- **Framework**: React 19.2, TypeScript 5.8
- **Build Tool**: Vite 7.2
- **UI Library**: Material-UI (MUI) v7.3
- **Styling**: TailwindCSS v4.1
- **State Management**: React Context, Hooks
- **Routing**: React Router v7.6
- **Forms**: Formik, Yup validation
- **Charts**: MUI X Charts
- **Rich Text**: Toast UI Editor, React Quill
- **Internationalization**: i18next

### AI Platform (Python)
- **Framework**: FastAPI 0.136
- **AI/ML**: LangChain, Transformers, PyTorch
- **Vector Database**: Qdrant
- **Document Processing**: PyMuPDF, pdfplumber, unstructured
- **OCR**: Tesseract
- **NLP**: spaCy, NLTK, sentence-transformers
- **Database**: PostgreSQL (SQLAlchemy), Neo4j (Graph DB)
- **Message Queue**: RabbitMQ (pika, aio-pika)
- **Observability**: OpenTelemetry, Prometheus
- **AI Providers**: OpenAI, Anthropic

### Infrastructure
- **Containerization**: Docker, Docker Compose
- **Orchestration**: Kubernetes (optional)
- **Monitoring**: Prometheus, Grafana, Loki, Tempo
- **Tracing**: OpenTelemetry
- **Reverse Proxy**: Nginx

## 🎯 Fitur Utama

### 1. Manajemen Akademik
- **Kurikulum Merdeka**: CP, ATP, TP, KSP
- **Asesmen**: Formatif, sumatif, autentik
- **Pembelajaran Mendalam**: Inquiry, project-based, differentiated
- **Jadwal & Presensi**: Manajemen jadwal pelajaran dan kehadiran
- **E-Rapor**: Laporan akademik otomatis dengan narasi AI

### 2. AI Platform
- **Document Intelligence**: OCR, table extraction, layout detection
- **Semantic Chunking**: Chunking berbasis konteks kurikulum
- **Embedding & Retrieval**: RAG dengan kurikulum-aware
- **Pedagogy Classification**: Klasifikasi pedagogi pembelajaran
- **Learning Progression**: Tracking perkembangan belajar
- **Adaptive Learning**: Rekomendasi pembelajaran personal

### 3. Manajemen Siswa & Guru
- **PPDB Online**: Penerimaan peserta didik baru
- **Data Siswa**: Profil, akademik, karakter, intervensi
- **Data Guru**: Profil, penugasan, refleksi
- **Karakter**: Profil Pelajar Pancasila
- **Intervensi**: Early warning system

### 4. Laporan & Analitik
- **Dasbor**: Visualisasi data akademik
- **Laporan**: Rapor, statistik, analisis
- **Strategic Planning**: Perencanaan strategis sekolah
- **School Quality**: Indikator mutu sekolah

## 🛠️ Instalasi & Setup

### Prerequisites
- Docker & Docker Compose
- Go 1.26 (untuk development backend)
- Node.js 20+ (untuk development frontend)
- Python 3.14 (untuk development AI Platform)
- PostgreSQL 15+
- Redis 7+
- RabbitMQ 3.12+
- Qdrant 1.7+

### Quick Start dengan Docker Compose

```bash
# Clone repository
git clone <repository-url>
cd sim-sekolah

# Setup environment variables
cp .env.example .env
# Edit .env dengan konfigurasi yang sesuai

# Start SIM Sekolah stack
docker compose -f infrastructure/compose/sim-sekolah/docker-compose.yml up -d

# Start AI Platform monolith
docker compose -f infrastructure/compose/ai-platform/docker-compose.yml up -d

# Access applications
# Backend: http://localhost:8080
# Frontend: http://localhost:3000
# AI Platform: http://localhost:8000
# Grafana: http://localhost:3030
```

### Development Setup

#### Backend
```bash
cd backend
cp .env.example .env
go mod download
go run cmd/main.go
# API docs: http://localhost:8080/swagger/index.html
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
# http://localhost:3000
```

#### AI Platform
```bash
cd ai-platform/monolith
pip install -r requirements.txt
python -m app.main
# http://localhost:8000
# API docs: http://localhost:8000/docs
```

## 📊 Database Schema

Backend menggunakan PostgreSQL dengan schema yang mencakup:
- **Academic Year**: Tahun akademik, semester
- **Curriculum**: CP, ATP, TP, KSP
- **Assessment**: Asesmen formatif, sumatif
- **Enrollment**: PPDB, pendaftaran, enrollment
- **Learning**: Pembelajaran, jurnal, refleksi
- **Student**: Data siswa, karakter, intervensi
- **Teacher**: Data guru, penugasan
- **User**: Autentikasi, authorization

Migration menggunakan golang-migrate:
```bash
cd backend
migrate -path migrations -database "postgres://user:pass@localhost:5432/dbname?sslmode=disable" up
```

## 🔐 Security

- **Authentication**: JWT dengan MFA
- **Authorization**: Role-Based Access Control (RBAC)
- **Encryption**: TLS untuk komunikasi, enkripsi data sensitif
- **Input Validation**: Validasi input di backend dan frontend
- **SQL Injection**: Menggunakan parameterized queries (GORM)
- **XSS Protection**: Sanitasi input di frontend
- **CORS**: Konfigurasi CORS yang ketat
- **Rate Limiting**: Rate limiting di backend

## 📈 Monitoring & Observability

### Prometheus & Grafana
- Metrics collection dari semua services
- Dashboards untuk monitoring kesehatan sistem
- Alerting untuk anomali

### Loki
- Log aggregation dari semua services
- Structured logging dengan JSON format
- Log querying dengan LogQL

### Tempo
- Distributed tracing dengan OpenTelemetry
- Trace analysis untuk performance debugging
- Service dependency mapping

### OpenTelemetry
- Automatic instrumentation untuk Go, Python, React
- Custom spans untuk business logic
- Export ke Grafana Cloud atau self-hosted

## 🧪 Testing

### Backend
```bash
cd backend
go test ./...
```

### Frontend
```bash
cd frontend
npm test
```

### AI Platform
```bash
cd ai-platform/monolith
pytest
```

## 📚 Dokumentasi

- **Backend**: `/backend/README.md`
- **Frontend**: `/frontend/README.md`
- **AI Platform**: `/ai-platform/README.md`
- **Infrastructure**: `/infrastructure/README.md`
- **API Documentation**: Swagger UI di http://localhost:8080/swagger/index.html

## 🤝 Kontribusi

1. Fork repository
2. Buat branch untuk fitur (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push ke branch (`git push origin feature/amazing-feature`)
5. Buat Pull Request

### Code Style
- **Backend**: Go fmt, golangci-lint
- **Frontend**: ESLint, Prettier
- **AI Platform**: Black, flake8, mypy

### Pre-commit Hooks
- Backend: gofmt, golangci-lint, govulncheck
- Frontend: lint-staged dengan ESLint dan Prettier
- AI Platform: black, flake8, mypy, isort

## 📄 License

MIT License

## 📞 Kontak

- **Developer Team**: admin@simsekolah.com
- **Repository**: [GitHub URL]

---

> *Dokumen ini memberikan panduan komprehensif untuk SIM Sekolah. Untuk dokumentasi spesifik setiap layanan, silakan merujuk pada README.md di direktori masing-masing.*
