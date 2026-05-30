# MinIO AIStor Knowledge Integration for SIM Sekolah

## Comprehensive Integration Guide untuk Backend & AI Platform

---

## Overview

Mengintegrasikan knowledge folder ke SeaweedFS akan memberikan benefits untuk:
- **Backend Services**: School, Teacher, Classroom, Student, Portfolio, Assessment, etc.
- **AI Platform Services**: Parser, Semantic Chunk, Embedding, Retrieval, Generation, etc.

---

## Architecture Diagram

### Current Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    SIM Sekolah Backend                      │
├─────────────────────────────────────────────────────────────┤
│  School  │ Teacher │ Classroom │ Student │ Portfolio │ ...  │
│  Service │ Service │ Service  │ Service │ Service  │      │
│    ↓     │    ↓    │    ↓      │    ↓    │    ↓      │      │
│  Local Filesystem (knowledge/)                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    AI Platform                              │
├─────────────────────────────────────────────────────────────┤
│  Parser │ Semantic │ Embedding │ Retrieval │ Generation    │
│  Service│ Chunk     │ Service   │ Service   │ Service       │
│    ↓    │    ↓     │    ↓      │    ↓      │    ↓          │
│  Local Filesystem (ai-platform/knowledge/)                 │
└─────────────────────────────────────────────────────────────┘
```

### Target Architecture
```
┌─────────────────────────────────────────────────────────────┐
│              SeaweedFS S3 Storage                          │
│  Bucket: knowledge-assets                                  │
├─────────────────────────────────────────────────────────────┤
│  knowledge/cp/                                             │
│  knowledge/atp/                                            │
│  knowledge/buku_guru/                                       │
│  knowledge/buku_siswa/                                      │
│  knowledge/modul_ajar/                                     │
│  knowledge/asesmen/                                        │
│  knowledge/media/                                          │
│  knowledge/p5/                                             │
│  knowledge/ontology/                                       │
└─────────────────────────────────────────────────────────────┘
           ↓ S3 API (http://seaweedfs-s3:8333)
┌─────────────────────────────────────────────────────────────┐
│                    SIM Sekolah Backend                      │
├─────────────────────────────────────────────────────────────┤
│  School  │ Teacher │ Classroom │ Student │ Portfolio │ ...  │
│  Service │ Service │ Service  │ Service │ Service  │      │
│    ↓     │    ↓    │    ↓      │    ↓    │    ↓      │      │
│  SeaweedFS S3 Client                                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    AI Platform                              │
├─────────────────────────────────────────────────────────────┤
│  Parser │ Semantic │ Embedding │ Retrieval │ Generation    │
│  Service│ Chunk     │ Service   │ Service   │ Service       │
│    ↓    │    ↓     │    ↓      │    ↓      │    ↓          │
│  SeaweedFS S3 Client                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Backend Integration Examples

### 1. School Service Integration

#### Current Implementation (Local Filesystem)
```go
// backend/internal/school/service.go (current)
func (s *schoolService) GetSchoolCurriculum(ctx context.Context, schoolID string) (*SchoolCurriculum, error) {
    // Read curriculum dari local filesystem
    curriculumPath := fmt.Sprintf("knowledge/cp/school/%s/curriculum.json", schoolID)
    data, err := os.ReadFile(curriculumPath)
    if err != nil {
        return nil, err
    }
    
    var curriculum SchoolCurriculum
    json.Unmarshal(data, &curriculum)
    return &curriculum, nil
}
```

#### SeaweedFS Implementation
```go
// backend/internal/school/service.go (with SeaweedFS)
import (
    "github.com/minio/minio-go/v7"
    "context"
)

type SeaweedFSConfig struct {
    Endpoint        string
    AccessKey       string
    SecretKey       string
    BucketName      string
    KnowledgePrefix string
}

type schoolService struct {
    repo         SchoolRepository
    seaweedfs    *minio.Client
    seaweedConfig SeaweedFSConfig
}

func NewSchoolService(repo SchoolRepository, seaweedConfig SeaweedFSConfig) SchoolService {
    // Initialize SeaweedFS client
    seaweedfs, err := minio.New(seaweedConfig.Endpoint, &minio.Options{
        Creds:  credentials.NewStaticV4(seaweedConfig.AccessKey, seaweedConfig.SecretKey, ""),
        Secure: false,
    })
    if err != nil {
        log.Printf("Warning: Failed to initialize SeaweedFS client: %v", err)
    }
    
    return &schoolService{
        repo:         repo,
        seaweedfs:    seaweedfs,
        seaweedConfig: seaweedConfig,
    }
}

func (s *schoolService) GetSchoolCurriculum(ctx context.Context, schoolID string) (*SchoolCurriculum, error) {
    // Coba ambil dari SeaweedFS dulu
    if s.seaweedfs != nil {
        objectKey := fmt.Sprintf("%scp/school/%s/curriculum.json", s.seaweedConfig.KnowledgePrefix, schoolID)
        
        obj, err := s.seaweedfs.GetObject(ctx, s.seaweedConfig.BucketName, objectKey, minio.GetObjectOptions{})
        if err == nil {
            defer obj.Close()
            
            var buf bytes.Buffer
            _, err = buf.ReadFrom(obj)
            if err == nil {
                var curriculum SchoolCurriculum
                json.Unmarshal(buf.Bytes(), &curriculum)
                return &curriculum, nil
            }
        }
    }
    
    // Fallback ke local filesystem jika SeaweedFS gagal
    curriculumPath := fmt.Sprintf("knowledge/cp/school/%s/curriculum.json", schoolID)
    data, err := os.ReadFile(curriculumPath)
    if err != nil {
        return nil, err
    }
    
    var curriculum SchoolCurriculum
    json.Unmarshal(data, &curriculum)
    return &curriculum, nil
}

func (s *schoolService) UploadSchoolDocument(ctx context.Context, schoolID string, document []byte, metadata map[string]string) error {
    if s.seaweedfs == nil {
        return errors.New("SeaweedFS client not initialized")
    }
    
    objectKey := fmt.Sprintf("%sdocuments/school/%s/%s", s.seaweedConfig.KnowledgePrefix, schoolID, metadata["filename"])
    
    _, err := s.seaweedfs.PutObject(ctx, s.seaweedConfig.BucketName, objectKey, bytes.NewReader(document), int64(len(document)), minio.PutObjectOptions{
        ContentType: metadata["content_type"],
        UserMetadata: metadata,
    })
    
    return err
}
```

### 2. Teacher Service Integration

#### Current Implementation
```go
// backend/internal/teacher/service.go (current)
func (s *teacherService) GetTeacherModules(ctx context.Context, teacherID string) ([]TeacherModule, error) {
    // Read teaching modules dari local filesystem
    modulePath := fmt.Sprintf("knowledge/modul_ajar/teacher/%s/modules.json", teacherID)
    data, err := os.ReadFile(modulePath)
    // ...
}
```

#### SeaweedFS Implementation
```go
// backend/internal/teacher/service.go (with SeaweedFS)
func (s *teacherService) GetTeacherModules(ctx context.Context, teacherID string) ([]TeacherModule, error) {
    if s.seaweedfs != nil {
        objectKey := fmt.Sprintf("%smodul_ajar/teacher/%s/modules.json", s.seaweedConfig.KnowledgePrefix, teacherID)
        
        obj, err := s.seaweedfs.GetObject(ctx, s.seaweedConfig.BucketName, objectKey, minio.GetObjectOptions{})
        if err == nil {
            defer obj.Close()
            
            var buf bytes.Buffer
            buf.ReadFrom(obj)
            
            var modules []TeacherModule
            json.Unmarshal(buf.Bytes(), &modules)
            return modules, nil
        }
    }
    
    // Fallback ke local filesystem
    modulePath := fmt.Sprintf("knowledge/modul_ajar/teacher/%s/modules.json", teacherID)
    data, err := os.ReadFile(modulePath)
    if err != nil {
        return nil, err
    }
    
    var modules []TeacherModule
    json.Unmarshal(data, &modules)
    return modules, nil
}

func (s *teacherService) GetATPForSubject(ctx context.Context, teacherID, subject string) (*ATPDocument, error) {
    // Ambil ATP dari SeaweedFS berdasarkan subject yang diajar oleh teacher
    if s.seaweedfs != nil {
        objectKey := fmt.Sprintf("%satp/%s/kelas-*/latest.json", s.seaweedConfig.KnowledgePrefix, subject)
        
        // List objects untuk mencari latest ATP
        objects, err := s.seaweedfs.ListObjects(ctx, s.seaweedConfig.BucketName, minio.ListObjectsOptions{
            Prefix: fmt.Sprintf("%satp/%s/", s.seaweedConfig.KnowledgePrefix, subject),
        })
        if err == nil && len(objects) > 0 {
            // Get latest object
            latestObj := objects[len(objects)-1]
            obj, err := s.seaweedfs.GetObject(ctx, s.seaweedConfig.BucketName, latestObj.Key, minio.GetObjectOptions{})
            if err == nil {
                defer obj.Close()
                
                var buf bytes.Buffer
                buf.ReadFrom(obj)
                
                var atp ATPDocument
                json.Unmarshal(buf.Bytes(), &atp)
                return &atp, nil
            }
        }
    }
    
    // Fallback logic
    return nil, errors.New("ATP not found")
}
```

### 3. Student Service Integration

#### Enhanced Features with SeaweedFS
```go
// backend/internal/student/service.go (enhanced with SeaweedFS)
func (s *studentService) GetPersonalizedLearningPath(ctx context.Context, studentID string) (*LearningPath, error) {
    // Get student profile
    student, err := s.repo.GetByID(ctx, studentID)
    if err != nil {
        return nil, err
    }
    
    // Get personalized content dari SeaweedFS
    if s.seaweedfs != nil {
        // Get CP yang sesuai dengan grade dan phase student
        objectKey := fmt.Sprintf("%scp/%s/kelas-%s/latest.json", 
            s.seaweedConfig.KnowledgePrefix, 
            student.PreferredSubject,
            student.GradeLevel)
        
        obj, err := s.seaweedfs.GetObject(ctx, s.seaweedConfig.BucketName, objectKey, minio.GetObjectOptions{})
        if err == nil {
            defer obj.Close()
            
            var buf bytes.Buffer
            buf.ReadFrom(obj)
            
            var cp CurriculumProgram
            json.Unmarshal(buf.Bytes(), &cp)
            
            // Generate personalized learning path berdasarkan CP dan student profile
            learningPath := s.generateLearningPathFromCP(cp, student)
            return learningPath, nil
        }
    }
    
    return nil, errors.New("Personalized learning path generation failed")
}

func (s *studentService) GetRecommendedResources(ctx context.Context, studentID string, topic string) ([]LearningResource, error) {
    if s.seaweedfs != nil {
        // Search resources berdasarkan topic di SeaweedFS
        prefix := fmt.Sprintf("%sresources/%s/", s.seaweedConfig.KnowledgePrefix, topic)
        
        objects, err := s.seaweedfs.ListObjects(ctx, s.seaweedConfig.BucketName, minio.ListObjectsOptions{
            Prefix: prefix,
        })
        if err == nil {
            var resources []LearningResource
            for _, obj := range objects {
                objInfo, err := s.seaweedfs.StatObject(ctx, s.seaweedConfig.BucketName, obj.Key, minio.StatObjectOptions{})
                if err == nil {
                    metadata := objInfo.UserMetadata
                    resources = append(resources, LearningResource{
                        Title: metadata["title"],
                        Subject: metadata["subject"],
                        Difficulty: metadata["difficulty"],
                        URL: fmt.Sprintf("s3://%s/%s", s.seaweedConfig.BucketName, obj.Key),
                    })
                }
            }
            return resources, nil
        }
    }
    
    return nil, errors.New("No resources found")
}
```

### 4. Portfolio Service Integration

```go
// backend/internal/portfolio/service.go (with SeaweedFS)
func (s *portfolioService) GetStudentPortfolioTemplate(ctx context.Context, studentID string) (*PortfolioTemplate, error) {
    if s.seaweedfs != nil {
        // Get portfolio template dari knowledge base
        objectKey := fmt.Sprintf("%sportfolio/templates/student_template.json", s.seaweedConfig.KnowledgePrefix)
        
        obj, err := s.seaweedfs.GetObject(ctx, s.seaweedConfig.BucketName, objectKey, minio.GetObjectOptions{})
        if err == nil {
            defer obj.Close()
            
            var buf bytes.Buffer
            buf.ReadFrom(obj)
            
            var template PortfolioTemplate
            json.Unmarshal(buf.Bytes(), &template)
            return &template, nil
        }
    }
    
    return nil, errors.New("Portfolio template not found")
}

func (s *portfolioService) UploadPortfolioArtifact(ctx context.Context, studentID, artifactType string, file []byte, metadata map[string]string) error {
    if s.seaweedfs == nil {
        return errors.New("SeaweedFS client not initialized")
    }
    
    // Upload artifact ke SeaweedFS dengan structured path
    objectKey := fmt.Sprintf("%sportfolio/student/%s/%s/%s", 
        s.seaweedConfig.KnowledgePrefix, 
        studentID, 
        artifactType,
        metadata["filename"])
    
    _, err := s.seaweedfs.PutObject(ctx, s.seaweedConfig.BucketName, objectKey, bytes.NewReader(file), int64(len(file)), minio.PutObjectOptions{
        ContentType: metadata["content_type"],
        UserMetadata: metadata,
    })
    
    return err
}
```

### 5. Assessment Service Integration

```go
// backend/internal/assessment/service.go (with SeaweedFS)
func (s *assessmentService) GenerateAssessmentFromTemplate(ctx context.Context, subject, grade string) (*Assessment, error) {
    if s.seaweedfs != nil {
        // Get assessment template dari knowledge base
        objectKey := fmt.Sprintf("%sasesmen/%s/kelas-%s/template.json", 
            s.seaweedConfig.KnowledgePrefix, 
            subject,
            grade)
        
        obj, err := s.seaweedfs.GetObject(ctx, s.seaweedConfig.BucketName, objectKey, minio.GetObjectOptions{})
        if err == nil {
            defer obj.Close()
            
            var buf bytes.Buffer
            buf.ReadFrom(obj)
            
            var template AssessmentTemplate
            json.Unmarshal(buf.Bytes(), &template)
            
            // Generate assessment dari template
            assessment := s.generateAssessment(template)
            return assessment, nil
        }
    }
    
    return nil, errors.New("Assessment template not found")
}

func (s *assessmentService) GetRubricCriteria(ctx context.Context, subject, assessmentType string) ([]RubricCriteria, error) {
    if s.seaweedfs != nil {
        // Get rubric criteria dari knowledge base
        objectKey := fmt.Sprintf("%srubrics/%s/%s/criteria.json", 
            s.seaweedConfig.KnowledgePrefix, 
            subject,
            assessmentType)
        
        obj, err := s.seaweedfs.GetObject(ctx, s.seaweedConfig.BucketName, objectKey, minio.GetObjectOptions{})
        if err == nil {
            defer obj.Close()
            
            var buf bytes.Buffer
            buf.ReadFrom(obj)
            
            var criteria []RubricCriteria
            json.Unmarshal(buf.Bytes(), &criteria)
            return criteria, nil
        }
    }
    
    return nil, errors.New("Rubric criteria not found")
}
```

---

## Configuration Updates

### Backend Configuration

```go
// backend/config/config.go
type SeaweedFSConfig struct {
    Enabled        bool   `env:"SEAWEEDFS_ENABLED" envDefault:"true"`
    Endpoint       string `env:"SEAWEEDFS_ENDPOINT" envDefault:"http://seaweedfs-s3:8333"`
    AccessKey      string `env:"SEAWEEDFS_ACCESS_KEY" envDefault:"admin"`
    SecretKey      string `env:"SEAWEEDFS_SECRET_KEY" envDefault:"admin"`
    BucketName     string `env:"SEAWEEDFS_BUCKET" envDefault:"knowledge-assets"`
    KnowledgePrefix string `env:"SEAWEEDFS_PREFIX" envDefault:"knowledge/"`
    
    // Performance tuning
    MaxConcurrent int `env:"SEAWEEDFS_MAX_CONCURRENT" envDefault:"10"`
    ConnectTimeout int `env:"SEAWEEDFS_CONNECT_TIMEOUT" envDefault:"30"`
    ReadTimeout   int `env:"SEAWEEDFS_READ_TIMEOUT" envDefault:"90"`
    
    // Caching
    EnableCache    bool   `env:"SEAWEEDFS_CACHE_ENABLED" envDefault:"true"`
    CacheTTL       int    `env:"SEAWEEDFS_CACHE_TTL" envDefault:"3600"`
    CacheDir       string `env:"SEAWEEDFS_CACHE_DIR" envDefault:"/tmp/seaweedfs_cache"`
    
    // Fallback
    FallbackToLocal bool   `env:"SEAWEEDFS_FALLBACK_LOCAL" envDefault:"true"`
    LocalPath       string `env:"SEAWEEDFS_LOCAL_PATH" envDefault:"./knowledge"`
}

type Config struct {
    Database DatabaseConfig
    Redis   RedisConfig
    RabbitMQ RabbitMQConfig
    SeaweedFS SeaweedFSConfig
    // ... other configs
}
```

### Docker Compose Updates

```yaml
# docker-compose.yml (backend section)
backend:
  environment:
    # Existing configurations
    - DATABASE_URL=${DATABASE_URL}
    - REDIS_HOST=${REDIS_HOST}
    - RABBITMQ_URL=${RABBITMQ_URL}
    
    # SeaweedFS Configuration
    - SEAWEEDFS_ENABLED=true
    - SEAWEEDFS_ENDPOINT=http://seaweedfs-s3:8333
    - SEAWEEDFS_ACCESS_KEY=${SEAWEEDFS_ACCESS_KEY:-admin}
    - SEAWEEDFS_SECRET_KEY=${SEAWEEDFS_SECRET_KEY:-admin}
    - SEAWEEDFS_BUCKET=knowledge-assets
    - SEAWEEDFS_PREFIX=knowledge/
    - SEAWEEDFS_MAX_CONCURRENT=10
    - SEAWEEDFS_CONNECT_TIMEOUT=30
    - SEAWEEDFS_READ_TIMEOUT=90
    - SEAWEEDFS_CACHE_ENABLED=true
    - SEAWEEDFS_CACHE_TTL=3600
    - SEAWEEDFS_CACHE_DIR=/tmp/seaweedfs_cache
    - SEAWEEDFS_FALLBACK_LOCAL=true
    - SEAWEEDFS_LOCAL_PATH=/app/knowledge
```

---

## Benefits Summary

### Backend Services
- **School Service**: Centralized curriculum management, easier updates
- **Teacher Service**: Teaching materials distribution, ATP access
- **Student Service**: Personalized learning paths, resource recommendations
- **Portfolio Service**: Artifact storage, template management
- **Assessment Service**: Assessment templates, rubric criteria

### AI Platform Services
- **Parser Service**: Document ingestion dari centralized storage
- **Semantic Chunk Service**: Educational chunking dengan metadata enrichment
- **Embedding Service**: Vector generation dengan consistent source
- **Retrieval Service**: Knowledge retrieval dengan S3 API
- **Generation Service**: Content generation menggunakan reliable knowledge source

### System-Wide Benefits
- **Scalability**: Horizontal scaling untuk both backend dan AI services
- **Consistency**: Single source of truth untuk semua knowledge assets
- **Maintenance**: Centralized updates dan version control
- **Reliability**: Built-in replication dan failover
- **Performance**: Distributed access, caching, parallel processing

---

## Migration Timeline

### Phase 1: Foundation (1-2 weeks)
- [ ] Setup SeaweedFS bucket structure
- [ ] Create migration scripts
- [ ] Test connectivity dengan existing services

### Phase 2: Backend Integration (2-3 weeks)
- [ ] Update School Service with SeaweedFS
- [ ] Update Teacher Service with SeaweedFS
- [ ] Update Student Service with SeaweedFS
- [ ] Update other backend services

### Phase 3: AI Platform Integration (2-3 weeks)
- [ ] Update Parser Service
- [ ] Update Semantic Chunk Service
- [ ] Update Embedding Service
- [ ] Update other AI services

### Phase 4: Testing & Validation (1-2 weeks)
- [ ] Integration testing
- [ ] Performance testing
- [ ] Fallback mechanism validation

### Phase 5: Deployment (1 week)
- [ ] Staged rollout
- [ ] Monitoring
- [ ] Documentation

---

## Monitoring & Maintenance

### Metrics to Monitor
```go
// backend/internal/monitoring/seaweedfs_metrics.go
type SeaweedFSMetrics struct {
    TotalRequests      int64
    SuccessfulRequests int64
    FailedRequests     int64
    CacheHits          int64
    CacheMisses        int64
    AverageLatency     float64
    CurrentConnections int64
}

func (m *SeaweedFSMetrics) RecordRequest(success bool, latency float64) {
    m.TotalRequests++
    if success {
        m.SuccessfulRequests++
    } else {
        m.FailedRequests++
    }
    m.AverageLatency = (m.AverageLatency*float64(m.TotalRequests-1) + latency) / float64(m.TotalRequests)
}
```

### Health Checks
```go
// backend/internal/health/seaweedfs_health.go
func CheckSeaweedFSHealth(config SeaweedFSConfig) error {
    seaweedfs, err := minio.New(config.Endpoint, &minio.Options{
        Creds:  credentials.NewStaticV4(config.AccessKey, config.SecretKey, ""),
        Secure: false,
    })
    if err != nil {
        return err
    }
    
    // Test bucket access
    _, err = seaweedfs.BucketExists(context.Background(), config.BucketName)
    return err
}
```

---

## Conclusion

Migrating knowledge folder ke SeaweedFS provides significant benefits untuk seluruh SIM Sekolah ecosystem, baik backend maupun AI Platform services. Implementation ini:

1. **Scales horizontally** untuk handle growth
2. **Provides reliability** dengan built-in replication
3. **Simplifies maintenance** dengan centralized storage
4. **Enables new features** seperti personalized learning paths
5. **Maintains compatibility** dengan fallback mechanisms

Timeline total: **8-11 weeks** untuk complete migration.
