# PRD - SIM Sekolah Backend System

## Product Requirements Document

**Document Version:** 1.0  
**Date:** 2025-05-27  
**Project:** SIM Sekolah (Sistem Informasi Manajemen Sekolah) Backend  
**Scope:** Backend API System for Primary School Management  

---

## 1. Product Overview

SIM Sekolah Backend is a comprehensive RESTful API system designed to power the digital transformation of Indonesian primary schools implementing the Kurikulum Merdeka curriculum. The system provides a robust, scalable, and secure backend infrastructure that supports web and mobile frontends, enabling schools to manage all aspects of educational operations digitally.

The product is specifically designed to address the unique challenges of Indonesian education, including schools in remote areas with limited connectivity, the need for local curriculum adaptation, and compliance with national education standards. The system integrates modern AI capabilities to enhance educational outcomes while maintaining simplicity and reliability for users with varying levels of digital literacy.

### 1.1 Target Users

- **Primary**: School administrators, teachers, students, and parents
- **Secondary**: Education authorities, system administrators, technical support staff
- **Tertiary**: Ministry of education officials, researchers, policymakers

### 1.2 Value Proposition

- **Comprehensive Digitalization**: End-to-end digital management of school operations
- **Curriculum Compliance**: Built-in support for Kurikulum Merdeka requirements
- **AI-Enhanced**: Intelligent features for assessment, planning, and decision support
- **Remote-Friendly**: Optimized for schools with limited connectivity
- **Data-Driven**: Analytics and reporting for informed decision-making
- **Secure & Compliant**: Enterprise-grade security and educational compliance

---

## 2. User Personas

### 2.1 School Administrator (Principal/Operator)

**Profile**: 
- Age: 35-55 years old
- Technical proficiency: Basic to intermediate
- Goals: Efficient school management, compliance reporting, data-driven decision making
- Pain points: Manual paperwork, fragmented data, reporting deadlines

**Key Needs**:
- Overview of school operations and performance
- Easy report generation for authorities
- Teacher and student management
- Resource allocation optimization
- Communication with stakeholders

### 2.2 Teacher

**Profile**:
- Age: 25-50 years old
- Technical proficiency: Basic to intermediate
- Goals: Effective teaching, reduced administrative burden, student progress tracking
- Pain points: Time-consuming administrative tasks, manual assessment, lack of resources

**Key Needs**:
- Lesson planning tools
- Student assessment and grading
- Attendance tracking
- Parent communication
- Access to teaching resources

### 2.3 Student

**Profile**:
- Age: 6-12 years old (primary school)
- Technical proficiency: Basic (digital native)
- Goals: Learning progress, access to materials, communication
- Pain points: Limited access to grades, lack of learning resources

**Key Needs**:
- Access to learning materials
- View grades and progress
- Communication with teachers
- Submit assignments
- Track attendance

### 2.4 Parent/Guardian

**Profile**:
- Age: 30-50 years old
- Technical proficiency: Basic to intermediate
- Goals: Monitor child's progress, communicate with school, support learning
- Pain points: Lack of information about child's progress, limited communication channels

**Key Needs**:
- Monitor child's academic progress
- View attendance records
- Communicate with teachers
- Access school announcements
- Pay school fees (future enhancement)

### 2.5 Super Admin

**Profile**:
- Age: 25-45 years old
- Technical proficiency: Advanced
- Goals: System stability, user management, technical support
- Pain points: System issues, user management complexity, security concerns

**Key Needs**:
- User and role management
- System monitoring and health checks
- Technical support capabilities
- Security management
- System configuration

---

## 3. User Stories & Acceptance Criteria

### 3.1 Authentication & Authorization

#### US-AUTH-001: User Registration
**As a** teacher or school staff  
**I want to** register myself in the system  
**So that** I can access the school management system

**Acceptance Criteria**:
- System MUST validate required fields: full_name, username, email, password
- System MUST ensure username uniqueness across the system
- System MUST validate email format and uniqueness
- System MUST enforce minimum 6-character password requirement
- System MUST assign default "GURU" role to new registrants
- System MUST hash passwords using bcrypt before storage
- System MUST send confirmation email upon successful registration
- System MUST log registration event for audit purposes
- System MUST return appropriate error messages for validation failures

**Traceability**: `auth/handler.go:Register()`, `auth/service.go:Register()`

#### US-AUTH-002: User Login with MFA
**As a** registered user  
**I want to** login with email and password  
**So that** I can access my account securely

**Acceptance Criteria**:
- System MUST validate email and password fields
- System MUST authenticate against stored credentials
- System MUST check account status (enabled, non-locked, non-expired)
- System MUST enforce MFA setup on first login
- System MUST require MFA verification if already enabled
- System MUST generate temporary token for MFA verification flow
- System MUST provide QR code and secret for MFA setup
- System MUST return appropriate error messages for failed authentication
- System MUST log successful and failed login attempts
- System MUST issue JWT access token upon successful authentication

**Traceability**: `auth/handler.go:Login()`, `auth/service.go:Login()`

#### US-AUTH-003: Token Refresh
**As a** authenticated user  
**I want to** refresh my access token automatically  
**So that** I can continue using the system without frequent re-login

**Acceptance Criteria**:
- System MUST accept refresh token from HTTP-only cookie
- System MUST validate refresh token against database
- System MUST check refresh token expiration
- System MUST verify user account status before refresh
- System MUST generate new access token with user roles
- System MUST rotate refresh tokens for security
- System MUST set new refresh token in HTTP-only cookie
- System MUST invalidate old refresh token
- System MUST return user data with new token
- System MUST handle invalid or expired tokens gracefully

**Traceability**: `auth/handler.go:Refresh()`, `auth/service.go:Refresh()`

#### US-AUTH-004: User Logout
**As a** authenticated user  
**I want to** logout securely  
**So that** my session is terminated and access is revoked

**Acceptance Criteria**:
- System MUST accept refresh token from cookie
- System MUST delete refresh token from database
- System MUST blacklist current access token in Redis
- System MUST clear refresh token from browser cookie
- System MUST handle logout with missing tokens gracefully
- System MUST log logout event for audit purposes

**Traceability**: `auth/handler.go:Logout()`, `auth/service.go:Logout()`

#### US-AUTH-005: Profile Management
**As a** authenticated user  
**I want to** update my profile information  
**So that** my personal information is current

**Acceptance Criteria**:
- System MUST allow updating full name, username, and contact information
- System MUST validate username uniqueness on update
- System MUST allow theme customization (color, mode, layout)
- System MUST allow notification preferences management
- System MUST update profile in database
- System MUST clear relevant cache entries on update
- System MUST return updated profile data
- System MUST log profile update events

**Traceability**: `auth/handler.go:UpdateMe()`, `auth/service.go:UpdateMe()`

### 3.2 School Management

#### US-SCH-001: Create School Profile
**As a** school administrator  
**I want to** create a comprehensive school profile  
**So that** the school information is properly recorded in the system

**Acceptance Criteria**:
- System MUST validate required school information (school_name, NPSN)
- System MUST accept comprehensive school metadata (address, contact, infrastructure)
- System MUST validate NPSN uniqueness
- System MUST store school geographic coordinates (latitude, longitude)
- System MUST capture school vision, mission, and goals
- System MUST record infrastructure details (classrooms, facilities, utilities)
- System MUST store teacher and student statistics
- System MUST trigger AI context embedding after creation
- System MUST return created school profile
- System MUST log school creation event

**Traceability**: `school/handler.go:Create()`, `school/service.go:Create()`

#### US-SCH-002: Update School Information
**As a** school administrator  
**I want to** update school information  
**So that** school records remain current and accurate

**Acceptance Criteria**:
- System MUST accept partial updates to school information
- System MUST validate NPSN uniqueness if changed
- System MUST update only provided fields
- System MUST maintain audit trail of changes
- System MUST trigger AI context embedding update
- System MUST return updated school information
- System MUST log update event

**Traceability**: `school/handler.go:Update()`, `school/service.go:Update()`

#### US-SCH-003: View School Directory
**As a** system user  
**I want to** search and view school information  
**So that** I can find and access school details

**Acceptance Criteria**:
- System MUST support pagination for large result sets
- System MUST support search by school name or NPSN
- System MUST return school basic information in list view
- System MUST provide detailed view for individual schools
- System MUST implement proper access control based on user roles
- System MUST handle search with no results gracefully

**Traceability**: `school/handler.go:GetAll()`, `school/handler.go:GetByID()`

### 3.3 Student Management

#### US-STU-001: Register New Student
**As a** school administrator  
**I want to** register a new student  
**So that** the student can be enrolled in the school

**Acceptance Criteria**:
- System MUST validate required student information (full_name, NISN, NIK)
- System MUST validate NISN uniqueness across the system
- System MUST validate NIK uniqueness across the system
- System MUST capture comprehensive student data (personal, family, health)
- System MUST accept parent/guardian information
- System MUST store supporting document information
- System MUST set initial student status as "applicant"
- System MUST generate student ID automatically
- System MUST log student registration event

**Traceability**: `student/model.go:Student`, `student/handler.go:Create()`

#### US-STU-002: Update Student Information
**As a** school administrator  
**I want to** update student information  
**So that** student records remain accurate

**Acceptance Criteria**:
- System MUST allow updates to student personal information
- System MUST validate NISN and NIK uniqueness if changed
- System MUST maintain audit trail of changes
- System MUST allow status updates (enrolled, active, graduated, etc.)
- System MUST preserve historical data for critical fields
- System MUST log update events

**Traceability**: `student/handler.go:Update()`, `student/service.go:Update()`

#### US-STU-003: View Student Records
**As a** teacher or administrator  
**I want to** view student information  
**So that** I can track student progress and needs

**Acceptance Criteria**:
- System MUST provide student basic information view
- System MUST show student academic history
- System MUST display parent/guardian information
- System MUST show student enrollment status
- System MUST implement proper access control (own students for teachers)
- System MUST support search and filtering

**Traceability**: `student/handler.go:GetByID()`, `student/handler.go:GetAll()`

### 3.4 Assessment Management

#### US-ASM-001: Create Age-Appropriate Assessment
**As a** teacher  
**I want to** create assessments suitable for my students' phase  
**So that** I can evaluate students appropriately

**Acceptance Criteria**:
- System MUST validate assessment type based on student phase (Fase A, B, C)
- System MUST support age-appropriate assessment types:
  - Fase A: Observation, Portfolio
  - Fase B: Performance tasks, Simple projects
  - Fase C: Complex projects, Collaborative assessment, Peer assessment
- System MUST require assessment name and date
- System MUST link assessment to teaching assignment
- System MUST allow assessment criteria configuration
- System MUST store assessment rubric if applicable
- System MUST log assessment creation event

**Traceability**: `assessment/handler.go:CreateAssessment()`, `assessment/model.go:Assessment`

#### US-ASM-002: Enter Student Scores
**As a** teacher  
**I want to** enter scores for assessments  
**So that** student progress can be tracked

**Acceptance Criteria**:
- System MUST accept scores for multiple students at once
- System MUST validate score ranges based on assessment type
- System MUST allow qualitative feedback/notes for each student
- System MUST prevent duplicate score entries for same student-assessment
- System MUST calculate summary statistics automatically
- System MUST store score history for audit trail
- System MUST trigger AI narrative generation if configured
- System MUST log score entry events

**Traceability**: `assessment/handler.go:UpsertScores()`, `assessment/model.go:AssessmentScore`

#### US-ASM-003: Generate AI Narrative Feedback
**As a** teacher  
**I want to** generate AI-powered narrative feedback for assessments  
**So that** I can provide detailed, personalized feedback efficiently

**Acceptance Criteria**:
- System MUST accept assessment context and student data
- System MUST generate narratives using AI service integration
- System MUST incorporate local context in narrative generation
- System MUST allow teacher review and editing of AI-generated content
- System MUST maintain original AI-generated content for audit
- System MUST handle AI service failures gracefully
- System MUST log AI generation events

**Traceability**: `ai/handler.go:GenerateNarrative()`, `ai/service.go:GenerateNarrative()`

#### US-ASM-004: Track Daily Attendance
**As a** teacher  
**I want to** track daily student attendance  
**So that** attendance records are maintained accurately

**Acceptance Criteria**:
- System MUST allow attendance entry by classroom and date
- System MUST support attendance statuses: Hadir, Sakit, Izin, Alpa
- System MUST allow optional notes for each attendance record
- System MUST prevent duplicate attendance entries
- System MUST calculate attendance summary statistics
- System MUST maintain historical attendance records
- System MUST log attendance entry events

**Traceability**: `assessment/handler.go:UpsertAttendances()`, `assessment/model.go:DailyAttendance`

### 3.5 Curriculum Management

#### US-CUR-001: Create Curriculum Document
**As a** school administrator  
**I want to** create curriculum documents  
**So that** the school curriculum is properly documented

**Acceptance Criteria**:
- System MUST validate required fields (academic_year, school, curriculum_type)
- System MUST support curriculum types: Intrakurikuler, Kokurikuler, Ekstrakurikuler
- System MUST support curriculum classification: KUMER, K13, Muatan Lokal
- System MUST implement document status workflow (Draft → Review → Final)
- System MUST allow chapter-based content organization
- System MUST integrate local context into curriculum
- System MUST maintain version history of curriculum changes
- System MUST log curriculum creation events

**Traceability**: `curriculum/model.go:CurriculumDocument`, `curriculum/handler.go:Create()`

#### US-CUR-002: Manage Kokurikuler Activities
**As a** school administrator  
**I want to** manage co-curricular activities  
**So that** students have comprehensive learning opportunities

**Acceptance Criteria**:
- System MUST allow creation of kokurikuler activities
- System MUST link activities to curriculum documents
- System MUST allow subject integration for activities
- System MUST capture activity schedules and descriptions
- System MUST support activity activation/deactivation
- System MUST maintain activity history
- System MUST log activity management events

**Traceability**: `curriculum/model.go:KokurikulerActivity`, `curriculum/handler.go:CreateKokurikuler()`

#### US-CUR-003: Manage Ekstrakurikuler Activities
**As a** school administrator  
**I want to** manage extra-curricular activities  
**So that** students have holistic development opportunities

**Acceptance Criteria**:
- System MUST allow creation of ekstrakurikuler activities
- System MUST support activity categories: Olahraga, Seni, Organisasi, Lainnya
- System MUST allow instructor assignment
- System MUST capture activity schedules and descriptions
- System MUST support activity activation/deactivation
- System MUST maintain activity history
- System MUST log activity management events

**Traceability**: `curriculum/model.go:EkstrakurikulerActivity`, `curriculum/handler.go:CreateEkstrakurikuler()`

### 3.6 Classroom Management

#### US-CLS-001: Create Classroom
**As a** school administrator  
**I want to** create classrooms  
**So that** students can be properly organized for learning

**Acceptance Criteria**:
- System MUST validate required fields (school, academic_year, grade, phase, classroom_name)
- System MUST enforce unique homeroom teacher assignment per academic year
- System MUST set default maximum quota (28 students)
- System MUST allow classroom characteristics description
- System MUST link classroom to appropriate grade and phase
- System MUST log classroom creation events

**Traceability**: `classroom/model.go:Classroom`, `classroom/handler.go:Create()`

#### US-CLS-002: Assign Homeroom Teacher
**As a** school administrator  
**I want to** assign homeroom teachers to classrooms  
**So that** each classroom has proper teacher supervision

**Acceptance Criteria**:
- System MUST validate teacher availability and qualifications
- System MUST prevent duplicate homeroom assignments in same academic year
- System MUST update existing assignment if teacher is reassigned
- System MUST maintain assignment history
- System MUST log assignment changes

**Traceability**: `classroom/handler.go:Update()`, `classroom/service.go:Update()`

#### US-CLS-003: Manage Student Enrollment
**As a** school administrator  
**I want to** enroll students in classrooms  
**So that** students are properly assigned for learning

**Acceptance Criteria**:
- System MUST validate classroom capacity before enrollment
- System MUST prevent duplicate enrollment of same student
- System MUST maintain enrollment history
- System MUST support enrollment status changes
- System MUST balance classroom sizes when possible
- System MUST log enrollment events

**Traceability**: `classroom/model.go:Classroom.Students`, `enrollment/handler.go:Create()`

### 3.7 AI Integration

#### US-AI-001: Generate School Context Embedding
**As a** system  
**I want to** automatically generate embeddings for school context  
**So that** AI services can provide contextualized responses

**Acceptance Criteria**:
- System MUST automatically trigger embedding on school creation/update
- System MUST extract relevant school context information
- System MUST call embedding service with processed context
- System MUST store embedding vectors for retrieval
- System MUST handle embedding service failures gracefully
- System MUST log embedding generation events

**Traceability**: `school/service.go:TriggerContextEmbedding()`, `school/embedding_worker.go`

#### US-AI-002: Process Content Through AI Services
**As a** teacher or administrator  
**I want to** process educational content through AI services  
**So that** I can leverage AI for content enhancement

**Acceptance Criteria**:
- System MUST accept content for AI processing
- System MUST route to appropriate AI service (generation, parsing, analysis)
- System MUST handle different content types (text, documents, images)
- System MUST return processed results with metadata
- System MUST implement proper error handling and retries
- System MUST log AI processing events

**Traceability**: `ai/handler.go:GenerateNarrative()`, `ai/grpc/*_service.go`

### 3.8 Communication System

#### US-COM-001: Send Internal Messages
**As a** system user  
**I want to** send messages to other users  
**So that** I can communicate internally

**Acceptance Criteria**:
- System MUST validate message recipients
- System MUST support individual and group messaging
- System MUST maintain message history
- System MUST show message read status
- System MUST send notifications for new messages
- System MUST log message events

**Traceability**: `communication/handler.go:SendMessage()`, `communication/model.go:Message`

#### US-COM-002: Manage Announcements
**As a** school administrator  
**I want to** create and broadcast announcements  
**So that** important information reaches all stakeholders

**Acceptance Criteria**:
- System MUST allow announcement creation with rich text
- System MUST support targeted recipient groups
- System MUST schedule announcement publication
- System MUST maintain announcement history
- System MUST track announcement read status
- System MUST log announcement events

**Traceability**: `communication/handler.go:CreateAnnouncement()`, `communication/model.go:Announcement`

### 3.9 Character Development

#### US-CHR-001: Manage Character Interventions
**As a** teacher or counselor  
**I want to** record character development interventions  
**So that** student character development can be tracked

**Acceptance Criteria**:
- System MUST allow intervention recording for students
- System MUST link interventions to character dimensions
- System MUST capture intervention details and outcomes
- System MUST maintain intervention history
- System MUST support intervention status tracking
- System MUST log intervention events

**Traceability**: `character_intervention/handler.go:Create()`, `character_intervention/model.go:Intervention`

#### US-CHR-002: Assess P5 Projects
**As a** teacher  
**I want to** assess student performance in P5 projects  
**So that** character development can be evaluated

**Acceptance Criteria**:
- System MUST support P5 project assessment with rubric scales
- System MUST accept character dimension scores (MB, SB, BSH, SAB)
- System MUST link assessments to specific projects
- System MUST maintain assessment history
- System MUST generate P5 assessment reports
- System MUST log assessment events

**Traceability**: `assessment/model.go:AssessmentP5`, `p5/handler.go:CreateAssessment()`

### 3.10 Specialized Learning Modules

#### US-SPL-001: Track Reading Literacy
**As a** teacher  
**I want to** track student reading literacy progress  
**So that** literacy development can be monitored

**Acceptance Criteria**:
- System MUST accept reading literacy assessment data
- System MUST track literacy levels and progress
- System MUST maintain literacy assessment history
- System MUST generate literacy progress reports
- System MUST support intervention recommendations
- System MUST log literacy assessment events

**Traceability**: `reading_literacy/handler.go:CreateAssessment()`, `reading_literacy/model.go:LiteracyAssessment`

#### US-SPL-002: Track Numeracy Skills
**As a** teacher  
**I want to** track student numeracy skills development  
**So that** numeracy progress can be monitored

**Acceptance Criteria**:
- System MUST accept numeracy assessment data
- System MUST track numeracy levels and progress
- System MUST maintain numeracy assessment history
- System MUST generate numeracy progress reports
- System MUST support intervention recommendations
- System MUST log numeracy assessment events

**Traceability**: `numeracy/handler.go:CreateAssessment()`, `numeracy/model.go:NumeracyAssessment`

### 3.11 Reporting & Analytics

#### US-RPT-001: Generate Student Progress Reports
**As a** teacher or parent  
**I want to** generate student progress reports  
**So that** academic development can be reviewed

**Acceptance Criteria**:
- System MUST aggregate assessment data for reporting period
- System MUST include qualitative and quantitative assessments
- System MUST incorporate attendance data
- System MUST generate narrative feedback
- System MUST support multiple report formats
- System MUST implement proper access control
- System MUST log report generation events

**Traceability**: `report/handler.go:GenerateStudentReport()`, `report/service.go:GenerateStudentReport()`

#### US-RPT-002: Generate School Dashboard
**As a** school administrator  
**I want to** view school performance dashboard  
**So that** I can make informed decisions

**Acceptance Criteria**:
- System MUST aggregate key performance indicators
- System MUST display student enrollment statistics
- System MUST show teacher performance metrics
- System MUST present assessment summary data
- System MUST provide trend analysis
- System MUST support filtering and drilling down
- System MUST implement proper access control

**Traceability**: `system/handler.go:GetDashboard()`, `system/service.go:GetDashboard()`

---

## 4. API Requirements

### 4.1 API Architecture

- **Protocol**: RESTful API over HTTP/HTTPS
- **Data Format**: JSON for request and response bodies
- **Authentication**: JWT Bearer tokens with refresh token mechanism
- **Documentation**: OpenAPI/Swagger 3.0 specification
- **Versioning**: URL-based versioning (/api/v1/)

### 4.2 API Endpoint Categories

#### 4.2.1 Authentication Endpoints
```
POST   /api/v1/otentikasi/daftar              - User registration
POST   /api/v1/otentikasi/masuk              - User login
POST   /api/v1/otentikasi/segarkan           - Token refresh
POST   /api/v1/otentikasi/keluar             - User logout
POST   /api/v1/otentikasi/lupa-kata-sandi    - Forgot password
POST   /api/v1/otentikasi/atur-ulang-kata-sandi - Reset password
POST   /api/v1/otentikasi/verifikasi-2fa     - MFA verification
GET    /api/v1/otentikasi/saya               - Get current user profile
PUT    /api/v1/otentikasi/saya               - Update current user profile
POST   /api/v1/otentikasi/saya/foto          - Upload profile photo
POST   /api/v1/otentikasi/ubah-kata-sandi    - Change password
POST   /api/v1/otentikasi/2fa/atur           - Setup MFA
POST   /api/v1/otentikasi/2fa/aktifkan       - Enable MFA
POST   /api/v1/otentikasi/2fa/nonaktifkan    - Disable MFA
POST   /api/v1/otentikasi/penyamaran         - Impersonate user
POST   /api/v1/otentikasi/berhenti-penyamaran - Stop impersonation
```

#### 4.2.2 School Management Endpoints
```
GET    /api/v1/sekolah                       - Get all schools (paginated)
GET    /api/v1/sekolah/:id                   - Get school by ID
POST   /api/v1/sekolah                       - Create school (admin only)
PUT    /api/v1/sekolah/:id                   - Update school (admin only)
DELETE /api/v1/sekolah/:id                   - Delete school (super admin only)
```

#### 4.2.3 Student Management Endpoints
```
GET    /api/v1/siswa                         - Get all students (paginated)
GET    /api/v1/siswa/:id                     - Get student by ID
POST   /api/v1/siswa                         - Register new student
PUT    /api/v1/siswa/:id                     - Update student information
DELETE /api/v1/siswa/:id                     - Delete student record
```

#### 4.2.4 Assessment Endpoints
```
GET    /api/v1/tugas-mengajar/:assignmentId/penilaian - Get assessments
POST   /api/v1/tugas-mengajar/:assignmentId/penilaian - Create assessment
GET    /api/v1/penilaian/:id                  - Get assessment by ID
PUT    /api/v1/penilaian/:id                  - Update assessment
DELETE /api/v1/penilaian/:id                  - Delete assessment
GET    /api/v1/penilaian/:id/nilai            - Get assessment scores
POST   /api/v1/penilaian/:id/nilai            - Upsert assessment scores
GET    /api/v1/kelas/:classroomId/kehadiran   - Get attendance records
POST   /api/v1/kelas/:classroomId/kehadiran   - Upsert attendance records
```

#### 4.2.5 Curriculum Endpoints
```
POST   /api/v1/kurikulum                     - Create curriculum document
GET    /api/v1/kurikulum/:id                 - Get curriculum document
PUT    /api/v1/kurikulum/:id                 - Update curriculum document
POST   /api/v1/kurikulum/:id/kokurikuler     - Add kokurikuler activity
POST   /api/v1/kurikulum/:id/ekstrakurikuler - Add ekstrakurikuler activity
```

#### 4.2.6 AI Integration Endpoints
```
POST   /api/v1/ai/generate-narrative         - Generate AI narrative
POST   /api/v1/ai/analyze-context            - Analyze school context
POST   /api/v1/ai/process-content            - Process content through AI
```

### 4.3 API Response Format

#### Success Response
```json
{
  "success": true,
  "message": "Operation successful",
  "data": { /* response data */ }
}
```

#### Error Response
```json
{
  "success": false,
  "message": "Error message",
  "error": "Detailed error information"
}
```

#### Paginated Response
```json
{
  "success": true,
  "message": "Data retrieved successfully",
  "data": [ /* array of items */ ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "total_pages": 10
  }
}
```

### 4.4 HTTP Status Codes

- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required or failed
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

### 4.5 Security Requirements

- **Authentication**: JWT tokens with 1-hour expiration
- **Rate Limiting**: 100 requests per minute per IP
- **CORS**: Configurable allowed origins
- **Input Validation**: Comprehensive validation on all inputs
- **SQL Injection Prevention**: Parameterized queries via GORM
- **XSS Prevention**: Input sanitization and output encoding
- **CSRF Protection**: Token-based CSRF protection

---

## 5. Data Requirements

### 5.1 Core Data Entities

#### 5.1.1 User & Authentication
- **User**: ID, full_name, username, email, password_hash, roles, settings, security flags
- **Role**: ID, role_name, permissions
- **RefreshToken**: ID, user_id, token, expired_at
- **PasswordResetToken**: ID, user_id, token, expired_at

#### 5.1.2 School & Organization
- **School**: ID, NPSN, school_name, address, contact_info, infrastructure, vision_mission, statistics
- **SchoolLocalContext**: ID, school_id, local_occupations, geography, culture, resources
- **AcademicYear**: ID, year, semester, start_date, end_date, status
- **Grade**: ID, grade_level, name, description
- **Phase**: ID, phase_code (A/B/C), phase_name, description

#### 5.1.3 People Management
- **Student**: ID, school_id, personal_info, family_info, academic_info, health_info, status
- **StudentParent**: ID, student_id, parent_type, personal_info, contact_info
- **Teacher**: ID, school_id, personal_info, employment_info, qualifications
- **Staff**: ID, school_id, personal_info, position, employment_info

#### 5.1.4 Academic Structure
- **Classroom**: ID, school_id, academic_year_id, grade_id, phase_id, name, homeroom_teacher_id, capacity
- **Subject**: ID, subject_code, subject_name, description, credits
- **TeachingAssignment**: ID, classroom_id, teacher_id, subject_id, academic_year_id
- **Enrollment**: ID, student_id, classroom_id, academic_year_id, enrollment_date, status

#### 5.1.5 Curriculum & Learning
- **CurriculumDocument**: ID, academic_year_id, school_id, type, classification, status, chapters
- **CurriculumChapter**: ID, curriculum_document_id, chapter_number, title, content
- **KokurikulerActivity**: ID, curriculum_document_id, activity_name, subject_id, schedule
- **EkstrakurikulerActivity**: ID, curriculum_document_id, activity_name, category, instructor_id

#### 5.1.6 Assessment & Evaluation
- **Assessment**: ID, teaching_assignment_id, name, type, age_appropriate_type, date
- **AssessmentScore**: ID, assessment_id, student_id, score, notes
- **Attendance**: ID, student_id, classroom_id, semester, sick, permission, unexcused
- **DailyAttendance**: ID, classroom_id, student_id, date, status, notes
- **SDAssessmentCriteria**: ID, assessment_type, phase_id, criteria_name, description, rubric_elements

#### 5.1.7 Character Development
- **CharacterIntervention**: ID, student_id, dimension_id, intervention_type, description, outcome
- **AssessmentP5**: ID, student_id, project_id, dimension_id, capaian (MB/SB/BSH/SAB)
- **ProfileDimension**: ID, dimension_code, dimension_name, description, indicators

#### 5.1.8 Communication
- **Message**: ID, sender_id, recipient_id, subject, content, read_status, sent_at
- **Announcement**: ID, sender_id, title, content, target_audience, published_at, expiry_at
- **Notification**: ID, user_id, type, title, content, read_status, created_at

#### 5.1.9 AI & Analytics
- **AIEmbedding**: ID, entity_type, entity_id, embedding_vector, context_data
- **AIGenerationLog**: ID, user_id, generation_type, input_data, output_data, model_used
- **SystemAnalytics**: ID, metric_name, metric_value, timestamp, dimensions

### 5.2 Data Relationships

- **School** 1:N → **Students, Teachers, Classrooms, CurriculumDocuments**
- **AcademicYear** 1:N → **Classrooms, Enrollments, CurriculumDocuments**
- **Classroom** N:M → **Students** (through Enrollment)
- **Teacher** N:M → **Classrooms** (through TeachingAssignment)
- **Student** 1:N → **StudentParents, AssessmentScores, Attendances**
- **Assessment** 1:N → **AssessmentScores**
- **CurriculumDocument** 1:N → **CurriculumChapters, KokurikulerActivities, EkstrakurikulerActivities**

### 5.3 Data Validation Rules

- **Email**: Must be valid email format, unique across users
- **NISN**: Must be 10-digit numeric, unique across students
- **NIK**: Must be 16-digit numeric, unique across students
- **NPSN**: Must be 8-digit numeric, unique across schools
- **Username**: Alphanumeric with underscores, 3-50 characters, unique
- **Password**: Minimum 8 characters, must include letter and number
- **Phone**: Must match Indonesian phone number format
- **Dates**: Must be valid dates, logical sequence (birth_date < enrollment_date)

### 5.4 Data Retention & Archival

- **Active Data**: 7 years online for current students and recent graduates
- **Archived Data**: 10 years offline storage for historical records
- **Audit Logs**: 5 years retention for security and compliance
- **System Logs**: 1 year retention for operational troubleshooting
- **Backup Data**: 90 days retention, with monthly long-term archives

---

## 6. Non-Functional Requirements

### 6.1 Performance Requirements

- **API Response Time**: 95th percentile < 500ms for standard operations
- **Database Query Time**: 95th percentile < 200ms for indexed queries
- **Concurrent Users**: Support 100+ concurrent users per school instance
- **Throughput**: 1000+ requests per minute per school instance
- **Page Load Time**: < 2 seconds for standard dashboard pages
- **File Upload**: Support uploads up to 10MB with progress indication

### 6.2 Scalability Requirements

- **Horizontal Scaling**: Stateless design enables horizontal scaling
- **Database Scaling**: Support read replicas for query scaling
- **Cache Layer**: Redis caching for frequently accessed data
- **Load Balancing**: Support for load balancer integration
- **Microservices Ready**: Modular architecture for future microservices decomposition

### 6.3 Availability & Reliability

- **System Uptime**: 99.5% availability during school hours (7AM-4PM local time)
- **Recovery Time Objective (RTO)**: 4 hours for critical systems
- **Recovery Point Objective (RPO)**: 15 minutes for data loss
- **Graceful Degradation**: System remains partially functional during component failures
- **Error Handling**: Comprehensive error handling with user-friendly messages

### 6.4 Security Requirements

- **Authentication**: Multi-factor authentication (MFA) required for all users
- **Authorization**: Role-based access control (RBAC) with principle of least privilege
- **Data Encryption**: AES-256 encryption for sensitive data at rest
- **Transmission Security**: TLS 1.3 for all data in transit
- **Session Management**: Secure session handling with automatic timeout
- **Input Validation**: Comprehensive validation and sanitization of all inputs
- **SQL Injection Prevention**: Parameterized queries via ORM
- **XSS Prevention**: Output encoding and Content Security Policy
- **CSRF Protection**: Token-based CSRF protection for state-changing operations
- **Security Headers**: Implementation of security headers (CSP, X-Frame-Options, etc.)

### 6.5 Usability Requirements

- **API Consistency**: Consistent API design patterns across all endpoints
- **Error Messages**: Clear, actionable error messages with Indonesian translation
- **Documentation**: Comprehensive API documentation with examples
- **Response Format**: Consistent response structure across all endpoints
- **Pagination**: Consistent pagination implementation for list endpoints
- **Filtering & Sorting**: Standardized filtering and sorting parameters

### 6.6 Compatibility Requirements

- **Browser Support**: Modern browsers (Chrome, Firefox, Safari, Edge) last 2 versions
- **Mobile Support**: Responsive design for tablet and mobile devices
- **API Versioning**: Backward compatibility for at least 2 previous API versions
- **Database Support**: PostgreSQL 12+ (current implementation)
- **Cache Support**: Redis 6+ (current implementation)

### 6.7 Internationalization Requirements

- **Primary Language**: Indonesian (Bahasa Indonesia)
- **Secondary Language**: English (for system administration)
- **Date/Time Format**: Indonesian locale format (DD/MM/YYYY)
- **Number Format**: Indonesian locale format (using dots for thousands, commas for decimals)
- **Currency Format**: Indonesian Rupiah (Rp) formatting

### 6.8 Monitoring & Logging Requirements

- **Application Logging**: Structured JSON logging with correlation IDs
- **Performance Monitoring**: OpenTelemetry integration for distributed tracing
- **Health Checks**: Endpoint health monitoring with automated alerts
- **Error Tracking**: Centralized error tracking and alerting
- **Audit Logging**: Comprehensive audit trail for sensitive operations
- **Metrics Collection**: Collection of key performance and business metrics

### 6.9 Backup & Recovery Requirements

- **Database Backups**: Daily automated backups with 30-day retention
- **Incremental Backups**: Hourly incremental backups for critical data
- **Backup Verification**: Regular backup restoration testing
- **Disaster Recovery**: Documented disaster recovery procedures
- **Geographic Redundancy**: Off-site backup storage for critical data

### 6.10 Compliance Requirements

- **Data Privacy**: Compliance with Indonesian Personal Data Protection Law
- **Educational Compliance**: Alignment with Ministry of Education standards
- **Accessibility**: Compliance with WCAG 2.1 AA accessibility standards
- **Reporting**: Support for required governmental reporting formats
- **Audit Readiness**: Maintain audit trails for compliance verification

---

## 7. Integration Requirements

### 7.1 External System Integrations

#### 7.1.1 Dapodikdasmen Integration
- **Purpose**: Synchronize school and student data with national system
- **Protocol**: REST API or file-based synchronization
- **Data Elements**: School information, student data, teacher data, enrollment data
- **Frequency**: Daily synchronization
- **Error Handling**: Retry mechanism with conflict resolution

#### 7.1.2 AI Services Integration
- **Purpose**: Leverage AI for content generation, analysis, and personalization
- **Protocol**: gRPC for AI service communication
- **Services**: Embedding, generation, retrieval, parsing, vision, strategic analysis
- **Fallback**: Graceful degradation when AI services are unavailable
- **Caching**: Cache AI responses to reduce latency and cost

#### 7.1.3 Notification Services
- **Purpose**: Send email and push notifications to users
- **Protocol**: SMTP for email, FCM/Web Push for push notifications
- **Templates**: Configurable notification templates
- **Scheduling**: Support for scheduled notifications
- **Tracking**: Delivery status tracking and retry logic

### 7.2 Third-Party Service Dependencies

- **PostgreSQL**: Primary database
- **Redis**: Caching and session management
- **RabbitMQ**: Message queue for asynchronous processing
- **OpenTelemetry**: Distributed tracing and monitoring
- **AI Services**: External AI platform for content processing

### 7.3 API Integration Points

- **Webhook Support**: Webhook endpoints for external system notifications
- **API Gateway**: Support for API gateway integration
- **Rate Limiting**: Configurable rate limiting per API key
- **API Documentation**: Interactive API documentation (Swagger, ReDoc, Scalar)

---

## 8. Testing Requirements

### 8.1 Unit Testing
- **Coverage Target**: Minimum 80% code coverage
- **Framework**: Standard Go testing framework
- **Mocking**: Mock external dependencies (database, external APIs)
- **Automation**: Automated execution in CI/CD pipeline

### 8.2 Integration Testing
- **Database Integration**: Test with test database
- **API Integration**: Test API endpoints with various scenarios
- **External Service Integration**: Mock external services for testing
- **Environment**: Dedicated testing environment

### 8.3 Performance Testing
- **Load Testing**: Simulate expected user load
- **Stress Testing**: Test system beyond expected capacity
- **Endurance Testing**: Prolonged performance testing
- **Tools**: Use industry-standard performance testing tools

### 8.4 Security Testing
- **Penetration Testing**: Regular security assessments
- **Vulnerability Scanning**: Automated vulnerability scanning
- **Dependency Scanning**: Regular dependency vulnerability checks
- **Code Review**: Security-focused code review process

---

## 9. Deployment Requirements

### 9.1 Infrastructure Requirements

- **Operating System**: Linux (Ubuntu 20.04+ or CentOS 8+)
- **CPU**: Minimum 4 cores, recommended 8+ cores
- **Memory**: Minimum 8GB RAM, recommended 16GB+ RAM
- **Storage**: Minimum 100GB SSD, recommended 500GB+ SSD
- **Network**: 1Gbps network connection

### 9.2 Deployment Architecture

- **Application Server**: Containerized deployment using Docker
- **Load Balancer**: Nginx or similar for load balancing
- **Database**: PostgreSQL with read replica support
- **Cache Layer**: Redis cluster for high availability
- **Monitoring**: Prometheus + Grafana for system monitoring
- **Logging**: ELK stack or similar for log aggregation

### 9.3 Deployment Process

- **CI/CD Pipeline**: Automated build, test, and deployment
- **Blue-Green Deployment**: Zero-downtime deployment strategy
- **Rollback Capability**: Automated rollback capability
- **Database Migrations**: Version-controlled database migrations
- **Configuration Management**: Environment-based configuration

### 9.4 Environment Configuration

- **Development**: Local development environment with hot reload
- **Staging**: Pre-production environment for final testing
- **Production**: Production environment with high availability
- **Configuration Management**: Centralized configuration management

---

## 10. Gap Analysis & Modernization Recommendations

### 10.1 Identified Gaps

#### 10.1.1 Missing Validations
- **File Upload Validation**: Limited validation on uploaded file types and sizes
- **Business Logic Validation**: Some complex business rules lack server-side validation
- **Data Consistency**: Limited cross-entity consistency validation

#### 10.1.2 Error Handling
- **Generic Error Messages**: Some error messages are too generic for user action
- **Error Recovery**: Limited automatic error recovery mechanisms
- **Exception Handling**: Inconsistent exception handling across modules

#### 10.1.3 Performance Optimization
- **Database Query Optimization**: Some complex queries lack proper optimization
- **Caching Strategy**: Inconsistent caching implementation across modules
- **Batch Processing**: Limited batch processing capabilities for bulk operations

#### 10.1.4 Security Enhancements
- **Input Sanitization**: Additional sanitization needed for user-generated content
- **Session Management**: Enhanced session management for security
- **API Security**: Additional API security headers and policies

### 10.2 Modernization Recommendations

#### 10.2.1 Architecture Improvements
1. **Microservices Decomposition**: Consider decomposing into microservices for better scalability
2. **Event-Driven Architecture**: Implement event-driven patterns for better decoupling
3. **API Gateway**: Implement centralized API gateway for cross-cutting concerns
4. **Service Mesh**: Consider service mesh for microservice communication

#### 10.2.2 Technology Enhancements
1. **GraphQL Layer**: Consider GraphQL for flexible data querying
2. **Real-time Communication**: Implement WebSocket for real-time features
3. **Advanced Caching**: Implement multi-layer caching strategy
4. **Database Optimization**: Implement read replicas and query optimization

#### 10.2.3 Operational Improvements
1. **Observability**: Enhanced observability with comprehensive monitoring
2. **Automation**: Increased automation for operational tasks
3. **Disaster Recovery**: Enhanced disaster recovery capabilities
4. **Performance Monitoring**: Real-time performance monitoring and alerting

#### 10.2.4 Feature Enhancements
1. **Offline Capabilities**: Enhanced offline functionality for remote areas
2. **Mobile Optimization**: Dedicated mobile API optimization
3. **Advanced Analytics**: Predictive analytics for student performance
4. **AI Integration**: Expanded AI capabilities for personalization

---

## 11. Assumptions & Dependencies

### 11.1 Assumptions

- Schools have minimum 4G spotty internet connectivity
- Teachers have basic digital literacy skills
- Parents have access to smartphones for communication
- Ministry of Education data standards remain stable
- AI services remain available and cost-effective
- PostgreSQL and Redis services remain available
- Security certificates are properly managed

### 11.2 Dependencies

- **Go 1.21+**: Programming language runtime
- **PostgreSQL 12+**: Primary database
- **Redis 6+**: Caching and session management
- **RabbitMQ**: Message queue for async processing
- **External AI Services**: Third-party AI platform access
- **Dapodikdasmen**: National education system access

---

## 12. Success Metrics

### 12.1 Technical Metrics

- **System Availability**: 99.5% uptime during school hours
- **API Performance**: 95th percentile response time < 500ms
- **Error Rate**: < 0.1% error rate for API calls
- **Test Coverage**: > 80% code coverage
- **Security Vulnerabilities**: Zero critical vulnerabilities

### 12.2 Business Metrics

- **User Adoption**: 90% teacher adoption within 6 months
- **Process Efficiency**: 50% reduction in administrative time
- **Data Quality**: 95% data completeness
- **User Satisfaction**: 4.5/5 user satisfaction score
- **Support Tickets**: < 5% of users submitting support tickets monthly

---

**Document End**

*This PRD has been generated through reverse engineering analysis of the SIM Sekolah Backend codebase, reflecting the actual implemented functionality, API contracts, and technical requirements.*