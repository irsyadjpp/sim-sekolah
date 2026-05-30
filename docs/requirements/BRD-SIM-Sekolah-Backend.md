# BRD - SIM Sekolah Backend System

## Business Requirements Document

**Document Version:** 1.0  
**Date:** 2025-05-27  
**Project:** SIM Sekolah (Sistem Informasi Manajemen Sekolah) Backend  
**Scope:** Backend API System for Primary School Management  

---

## 1. Executive Summary

SIM Sekolah Backend is a comprehensive school management system designed specifically for Indonesian primary schools (SD) implementing the Kurikulum Merdeka curriculum. The system provides a centralized platform for managing academic operations, student and teacher data, assessment processes, curriculum implementation, and integrates AI-powered capabilities for enhanced educational outcomes. The backend serves as the core data processing and business logic layer, supporting web and mobile frontends through RESTful APIs.

The system addresses the unique challenges of Indonesian education, including remote island schools, limited infrastructure, and the need for localized curriculum adaptation while maintaining national education standards.

---

## 2. Business Objectives

### 2.1 Primary Objectives

1. **Digital Transformation**: Enable comprehensive digitalization of school management processes to replace manual paper-based systems
2. **Curriculum Compliance**: Ensure full implementation of Kurikulum Merdeka requirements including phase-based learning (Fase A, B, C)
3. **Data Centralization**: Create a unified repository for all school-related data including students, teachers, assessments, and academic records
4. **Accessibility**: Provide reliable system access for schools in remote areas with limited internet connectivity
5. **Decision Support**: Enable data-driven decision-making through comprehensive reporting and analytics

### 2.2 Secondary Objectives

1. **Parent Engagement**: Facilitate communication between schools and parents/guardians
2. **Teacher Efficiency**: Reduce administrative burden on teachers through automation
3. **Student Monitoring**: Enable continuous monitoring of student progress and early intervention
4. **Resource Optimization**: Optimize allocation of school resources including classrooms, teachers, and materials
5. **Compliance Reporting**: Simplify generation of reports required by educational authorities

---

## 3. Stakeholder Analysis

### 3.1 Primary Stakeholders

| Stakeholder | Role | Interests | System Access Level |
|-------------|------|-----------|-------------------|
| **School Administrators** | Principals, School Operators | Overall school management, reporting, compliance | Full administrative access |
| **Teachers** | Classroom teachers, Subject teachers | Student assessment, lesson planning, attendance tracking | Teaching-related modules |
| **Students** | Primary school students | Access to learning materials, grades, schedules | Limited read access |
| **Parents/Guardians** | Student parents | Monitor child's progress, communication with school | Read access to child data |
| **Super Admin** | System administrators | System configuration, user management, technical oversight | Full system access |

### 3.2 Secondary Stakeholders

| Stakeholder | Role | Interests |
|-------------|------|-----------|
| **Local Education Authorities** | District/City education offices | Compliance monitoring, aggregated reporting |
| **Ministry of Education** | National education body | Policy implementation, data collection |
| **Technical Support Team** | IT support staff | System maintenance, troubleshooting |

---

## 4. Business Process

### 4.1 Authentication & Authorization Flow

1. **User Registration**: Teachers/staff self-register with email verification
2. **Login Process**: Email/password authentication with mandatory MFA setup
3. **Role Assignment**: Default role assignment (GURU) with ability to upgrade
4. **Access Control**: Role-based access control (RBAC) for module access
5. **Session Management**: JWT-based authentication with refresh tokens
6. **Audit Logging**: All critical actions logged for security and compliance

### 4.2 Student Enrollment Process

1. **New Student Registration**: Capture comprehensive student data including personal, family, and health information
2. **Document Verification**: Validate NISN, NIK, and other official documents
3. **Classroom Assignment**: Automatic assignment based on grade, capacity, and balance
4. **Parent Account Creation**: Automatic parent account generation for each enrolled student
5. **Enrollment Confirmation**: System-generated confirmation and documentation

### 4.3 Academic Assessment Process

1. **Assessment Creation**: Teachers create age-appropriate assessments based on student phase
2. **Assessment Types**: Support for observation, portfolio, performance tasks, projects, and peer assessment
3. **Score Entry**: Teachers enter scores with qualitative feedback
4. **Progress Tracking**: Continuous monitoring of student academic progress
5. **Report Generation**: Automated generation of student progress reports

### 4.4 Curriculum Implementation Process

1. **Curriculum Document Creation**: Schools create curriculum documents aligned with Kurikulum Merdeka
2. **Phase-Based Content**: Organize content by learning phases (A, B, C)
3. **Local Context Integration**: Incorporate local cultural and geographical context
4. **Activity Planning**: Plan intrakurikuler, kokurikuler, and ekstrakurikuler activities
5. **Implementation Tracking**: Monitor curriculum implementation progress

### 4.5 AI-Enhanced Workflow

1. **Context Embedding**: Automatic embedding of school context for AI retrieval
2. **Narrative Generation**: AI-powered generation of assessment narratives and feedback
3. **Strategic Analysis**: AI analysis of school characteristics and recommendations
4. **Content Processing**: Automated processing of educational content through AI services

---

## 5. Functional Scope

### 5.1 Core Business Capabilities

#### 5.1.1 Identity & Access Management
- User registration and authentication
- Multi-factor authentication (MFA) enforcement
- Role-based access control (RBAC)
- Password management and recovery
- User profile management
- Session management and security
- Audit logging and compliance tracking

#### 5.1.2 School Management
- School profile management with comprehensive metadata
- Infrastructure and resource tracking
- Vision, mission, and goal management
- Local context integration (geographic, cultural, economic)
- External partnership management
- School context embedding for AI capabilities

#### 5.1.3 Academic Year Management
- Academic year configuration and management
- Semester and period management
- Academic calendar maintenance
- Enrollment period management

#### 5.1.4 Student Management
- Comprehensive student records (personal, family, academic, health)
- Student status tracking (applicant, enrolled, active, graduated)
- Parent/guardian information management
- Document management (NISN, NIK, certificates)
- Photo and biometric data management

#### 5.1.5 Teacher Management
- Teacher profile management
- Certification and qualification tracking
- Teaching assignment management
- Professional development records
- Performance evaluation tracking

#### 5.1.6 Classroom Management
- Classroom creation and configuration
- Homeroom teacher assignment
- Student enrollment and capacity management
- Classroom characteristics and needs assessment
- Schedule and resource allocation

#### 5.1.7 Curriculum Management
- Curriculum document creation and management
- Phase-based content organization (Fase A, B, C)
- Chapter and lesson content management
- Kokurikuler and ekstrakurikuler activity planning
- Local context integration
- Curriculum status workflow (Draft → Review → Final)

#### 5.1.8 Assessment & Evaluation
- Age-appropriate assessment types by phase
- Assessment creation and scheduling
- Score entry and management
- Qualitative feedback and narrative generation
- Attendance tracking (daily and summary)
- SD-specific assessment criteria management
- P5 (Projek Penguatan Profil Pelajar Pancasila) assessment

#### 5.1.9 Subject & Grade Management
- Subject catalog management
- Grade level configuration
- Subject-grade mapping
- Learning material organization

#### 5.1.10 Learning Management
- Lesson planning and management
- Learning experience tracking
- Teaching assignment management
- Schedule management
- Learning resource management

#### 5.1.11 AI Integration
- AI-powered narrative generation for assessments
- School context embedding for retrieval-augmented generation
- Strategic analysis and recommendations
- Content processing and analysis
- Multi-modal AI service integration (text, vision, parsing)

#### 5.1.12 Communication System
- Internal messaging system
- Parent-teacher communication
- Announcement broadcasting
- Notification management

#### 5.1.13 Character Development
- Character intervention programs
- Behavioral tracking
- P5 project management
- Profile dimension assessment
- Character rubric management

#### 5.1.14 Specialized Learning Modules
- Reading literacy assessment and tracking
- Numeracy skills assessment and tracking
- Foundational skills monitoring
- Differentiated instruction planning
- Individual learning plan management

#### 5.1.15 Reporting & Analytics
- Student progress reports
- Teacher performance reports
- School operational reports
- Compliance reporting
- Dashboard and analytics
- Data export capabilities

### 5.2 Supporting Capabilities

#### 5.2.1 System Administration
- User management and administration
- Permission and role management
- System configuration
- Health monitoring
- Database optimization and monitoring

#### 5.2.2 Data Management
- Data validation and integrity
- Audit trail maintenance
- Data backup and recovery
- Migration management
- Cache management for performance

#### 5.2.3 Integration Capabilities
- External system integration (Dapodikdasmen)
- API gateway and rate limiting
- Message queue integration (RabbitMQ)
- Caching layer integration (Redis)
- OpenTelemetry monitoring integration

---

## 6. Compliance & Governance

### 6.1 Data Privacy & Security

- **Personal Data Protection**: Comprehensive protection of student and teacher personal data
- **Access Control**: Strict role-based access control with audit trails
- **Data Encryption**: Encryption of sensitive data at rest and in transit
- **Authentication Security**: MFA enforcement, secure password policies
- **Session Management**: Secure session handling with token blacklisting
- **Audit Logging**: Complete audit trail of all system access and modifications

### 6.2 Educational Compliance

- **Kurikulum Merdeka Compliance**: Full alignment with national curriculum requirements
- **Assessment Standards**: Age-appropriate assessment methods per educational phase
- **Reporting Standards**: Compliance with Ministry of Education reporting requirements
- **Data Standards**: Alignment with Dapodikdasmen data standards
- **Accessibility**: Support for schools with limited infrastructure and connectivity

### 6.3 Operational Governance

- **Change Management**: Controlled deployment and migration processes
- **Performance Monitoring**: Continuous system performance and health monitoring
- **Incident Response**: Structured incident handling and recovery procedures
- **Data Retention**: Appropriate data retention policies and archival
- **Backup & Recovery**: Regular backup and tested recovery procedures

### 6.4 Audit & Accountability

- **User Activity Logging**: Comprehensive logging of user actions
- **Data Modification Tracking**: Complete audit trail for data changes
- **System Event Logging**: Technical events and errors logged for troubleshooting
- **Compliance Reporting**: Generation of compliance reports as required
- **Security Incident Tracking**: Documentation and tracking of security incidents

---

## 7. Technical Architecture Overview

### 7.1 System Architecture

- **Backend Framework**: Go (Golang) with Fiber web framework
- **Database**: PostgreSQL with GORM ORM
- **Caching**: Redis for session management and performance optimization
- **Message Queue**: RabbitMQ for asynchronous processing
- **Monitoring**: OpenTelemetry for distributed tracing
- **API Documentation**: Swagger/OpenAPI with multiple UI views (Swagger, ReDoc, Scalar)

### 7.2 Integration Points

- **AI Services**: gRPC integration with multiple AI services (embedding, generation, retrieval, etc.)
- **External Systems**: Integration capabilities with Dapodikdasmen and other educational systems
- **Monitoring Systems**: OpenTelemetry integration for enterprise monitoring
- **Notification Systems**: Email and push notification capabilities

### 7.3 Scalability & Performance

- **Horizontal Scaling**: Stateless design for horizontal scaling
- **Caching Strategy**: Multi-level caching for performance optimization
- **Database Optimization**: Indexed queries, connection pooling, view optimization
- **Rate Limiting**: Redis-backed rate limiting for API protection
- **Compression**: Response compression for bandwidth optimization

---

## 8. Risk Assessment

### 8.1 Technical Risks

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|-------------------|
| Database performance degradation | High | Medium | Regular optimization, indexing, query monitoring |
| AI service integration failures | Medium | Medium | Fallback mechanisms, error handling, retry logic |
| Connectivity issues in remote areas | High | High | Offline capabilities, data synchronization, caching |
| Security breaches | Critical | Low | MFA, encryption, audit logging, regular security reviews |

### 8.2 Operational Risks

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|-------------------|
| Data loss | Critical | Low | Regular backups, tested recovery procedures |
| User adoption resistance | High | Medium | Training, user-friendly design, support |
| Compliance changes | Medium | Medium | Flexible architecture, regular compliance reviews |
| Scalability limitations | High | Low | Horizontal scaling design, performance monitoring |

---

## 9. Success Criteria

### 9.1 Technical Success Criteria

- **System Availability**: 99.5% uptime during school hours
- **Response Time**: API response time < 500ms for 95% of requests
- **Data Accuracy**: 99.9% data accuracy with proper validation
- **Security**: Zero critical security vulnerabilities
- **Scalability**: Support for 100+ concurrent users per school

### 9.2 Business Success Criteria

- **User Adoption**: 90% teacher adoption within 6 months
- **Process Efficiency**: 50% reduction in administrative time for teachers
- **Data Completeness**: 95% student data completeness within 1 year
- **Compliance**: 100% compliance with Ministry of Education reporting requirements
- **User Satisfaction**: 4.5/5 user satisfaction score

---

## 10. Assumptions & Constraints

### 10.1 Assumptions

- Schools have basic internet connectivity (minimum 4G spotty coverage)
- Teachers have basic digital literacy skills
- Parents have access to mobile devices for communication
- Ministry of Education data standards remain stable
- AI services remain available and cost-effective

### 10.2 Constraints

- **Infrastructure**: Must operate effectively with limited bandwidth and unreliable connectivity
- **Budget**: Cost-effective solution suitable for public school funding
- **Timeline**: Phased implementation aligned with academic calendar
- **Regulatory**: Must comply with Indonesian education regulations and data protection laws
- **Technical**: Must support legacy systems and data migration requirements

---

## 11. Future Considerations

### 11.1 Potential Enhancements

1. **Mobile Application**: Native mobile apps for teachers and parents
2. **Offline Capabilities**: Enhanced offline functionality for remote areas
3. **Advanced Analytics**: Predictive analytics for student performance
4. **Integration Expansion**: Integration with more external systems and services
5. **AI Capabilities**: Expansion of AI-powered features and personalization

### 11.2 Scalability Considerations

1. **Multi-School Support**: Expansion to support school district management
2. **Geographic Expansion**: Support for schools across different regions
3. **Vertical Expansion**: Adaptation for different school levels (SMP, SMA)
4. **Integration Marketplace**: Platform for third-party integrations

---

**Document End**

*This BRD has been generated through reverse engineering analysis of the SIM Sekolah Backend codebase, reflecting the actual implemented functionality and business logic.*