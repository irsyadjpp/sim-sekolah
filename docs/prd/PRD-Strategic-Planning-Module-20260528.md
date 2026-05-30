# Product Requirements Document (PRD)
## Strategic Planning Module

**Document Version:** 1.0  
**Date:** 2025-05-28  
**Module:** Strategic Planning  
**Status:** Draft  

---

## 1. Executive Summary

The Strategic Planning Module is a comprehensive educational planning and analysis system designed to help schools integrate data-driven decision-making into their curriculum development process. The module provides tools for collecting educational data, conducting strategic analyses (SWOT, Root Cause, Fishbone), profiling student needs, and integrating these insights into the Kurikulum Satuan Pendidikan (KSP) documents.

The module serves as a bridge between raw educational data (Rapor Pendidikan, Surveys, FGD sessions) and actionable curriculum planning, enabling schools to create evidence-based educational strategies.

---

## 2. Product Overview

### 2.1 Problem Statement

Schools in Indonesia face challenges in:
- Integrating data from multiple sources (Rapor Pendidikan API, surveys, FGD sessions) into a unified planning framework
- Conducting systematic strategic analysis to identify strengths, weaknesses, opportunities, and threats
- Performing root cause analysis on educational metrics to understand underlying issues
- Translating analysis results into concrete curriculum adjustments in KSP documents
- Tracking the implementation and effectiveness of improvement initiatives

### 2.2 Solution

The Strategic Planning Module provides:
1. **Data Integration Layer**: Synchronization with Kemdikbud Rapor Pendidikan API
2. **Data Collection Tools**: Dynamic surveys and virtual FGD sessions
3. **Analysis Frameworks**: SWOT, Root Cause (5-Whys), and Fishbone diagram analysis
4. **Student Profiling**: Enhanced student needs assessment with action planning
5. **KSP Integration**: Structured integration of analysis results into curriculum documents
6. **Workflow Management**: Approval workflows, version history, and progress tracking

### 2.3 Target Users

- **School Principals (Kepsek)**: Strategic decision-making and approval
- **Teachers (Guru)**: Data collection, analysis participation, and implementation
- **School Staff**: Survey administration and FGD coordination
- **Parents (Ortu)**: Survey respondents and feedback providers
- **Partners (Mitra)**: External stakeholders in FGD sessions
- **Curriculum Developers**: KSP document creation and integration

---

## 3. Functional Requirements

### 3.1 Rapor Pendidikan Integration

#### 3.1.1 Data Synchronization
- **FR-RP-001**: The system shall synchronize literacy, numeracy, and character scores from the Kemdikbud Rapor Pendidikan API
- **FR-RP-002**: The system shall store raw JSON data from the API for reference
- **FR-RP-003**: The system shall track synchronization status (SUCCESS, FAILED, PENDING, SYNCING)
- **FR-RP-004**: The system shall log synchronization errors with detailed messages
- **FR-RP-005**: The system shall support manual re-synchronization on failure

#### 3.1.2 Data Management
- **FR-RP-006**: The system shall allow CRUD operations on Rapor Pendidikan records
- **FR-RP-007**: The system shall support filtering by school, year, and semester
- **FR-RP-008**: The system shall validate school_id as a valid UUID
- **FR-RP-009**: The system shall validate year and semester fields (max 10 characters)
- **FR-RP-010**: The system shall validate score ranges (0-100 for literacy, numeracy, character)

#### 3.1.3 API Endpoints
```
POST   /api/v1/strategic-planning/rapor
GET    /api/v1/strategic-planning/rapor/:id
GET    /api/v1/strategic-planning/rapor
PUT    /api/v1/strategic-planning/rapor/:id
DELETE /api/v1/strategic-planning/rapor/:id
POST   /api/v1/strategic-planning/rapor/sync
```

### 3.2 Survey Management

#### 3.2.1 Survey Creation
- **FR-SV-001**: The system shall allow creation of dynamic surveys with JSON-based form schemas
- **FR-SV-002**: The system shall support multiple target audiences (MURID, ORTU, MITRA, GURU, STAFF)
- **FR-SV-003**: The system shall allow anonymous or identified survey responses
- **FR-SV-004**: The system shall support survey templates for reuse
- **FR-SV-005**: The system shall allow setting response limits and date ranges

#### 3.2.2 Survey Response Collection
- **FR-SV-006**: The system shall collect survey responses in JSON format
- **FR-SV-007**: The system shall track respondent metadata (IP address, user agent)
- **FR-SV-008**: The system shall support multiple responses per survey (if configured)
- **FR-SV-009**: The system shall validate respondent type against target audience

#### 3.2.3 Survey Management
- **FR-SV-010**: The system shall support survey lifecycle states (DRAFT, ACTIVE, CLOSED, ARCHIVED)
- **FR-SV-011**: The system shall allow categorization of survey templates
- **FR-SV-012**: The system shall provide response analytics and aggregation

#### 3.2.4 API Endpoints
```
POST   /api/v1/strategic-planning/surveys
GET    /api/v1/strategic-planning/surveys/:id
GET    /api/v1/strategic-planning/surveys
PUT    /api/v1/strategic-planning/surveys/:id
DELETE /api/v1/strategic-planning/surveys/:id
POST   /api/v1/strategic-planning/surveys/:id/responses
GET    /api/v1/strategic-planning/surveys/:id/responses
GET    /api/v1/strategic-planning/surveys/:id/responses/:id
```

### 3.3 FGD (Focus Group Discussion) Sessions

#### 3.3.1 Session Management
- **FR-FGD-001**: The system shall allow creation of virtual FGD sessions
- **FR-FGD-002**: The system shall support multiple session types (VIRTUAL, HYBRID, OFFLINE)
- **FR-FGD-003**: The system shall store conference platform details (Zoom, Google Meet, WebEx)
- **FR-FGD-004**: The system shall track session status (SCHEDULED, IN_PROGRESS, COMPLETED, CANCELLED)
- **FR-FGD-005**: The system shall allow session recording and URL storage

#### 3.3.2 Participant Management
- **FR-FGD-006**: The system shall manage FGD participants with roles (KEPSEK, GURU, STAFF, ORTU, MITRA, MODERATOR)
- **FR-FGD-007**: The system shall track invitation and attendance status
- **FR-FGD-008**: The system shall record join/leave timestamps
- **FR-FGD-009**: The system shall allow contribution rating (1-5) and feedback

#### 3.3.3 Collaboration Features
- **FR-FGD-010**: The system shall support collaborative notes (TEXT, MARKDOWN, RICH_TEXT)
- **FR-FGD-011**: The system shall perform sentiment analysis on session notes
- **FR-FGD-012**: The system shall calculate sentiment scores (0-1)

#### 3.3.4 API Endpoints
```
POST   /api/v1/strategic-planning/fgd/sessions
GET    /api/v1/strategic-planning/fgd/sessions/:id
GET    /api/v1/strategic-planning/fgd/sessions
PUT    /api/v1/strategic-planning/fgd/sessions/:id
DELETE /api/v1/strategic-planning/fgd/sessions/:id
POST   /api/v1/strategic-planning/fgd/sessions/:id/participants
GET    /api/v1/strategic-planning/fgd/sessions/:id/participants
PUT    /api/v1/strategic-planning/fgd/sessions/:id/participants/:id
```

### 3.4 Student Needs Enhanced

#### 3.4.1 Student Profiling
- **FR-SN-001**: The system shall create enhanced student profiles linked to master_student_context_ext
- **FR-SN-002**: The system shall profile students across multiple dimensions (e.g., PENALARAN_KRITIS, KREATIVITAS)
- **FR-SN-003**: The system shall integrate survey data into student needs assessment
- **FR-SN-004**: The system shall perform gap analysis between current status and desired outcomes
- **FR-SN-005**: The system shall assign priority levels (1-5, 1 highest)

#### 3.4.2 Action Planning
- **FR-SN-006**: The system shall create action plans for addressing student needs
- **FR-SN-007**: The system shall assign action plans to responsible users
- **FR-SN-008**: The system shall set due dates for action plans
- **FR-SN-009**: The system shall track action plan status (NOT_STARTED, IN_PROGRESS, COMPLETED, ON_HOLD, CANCELLED)
- **FR-SN-010**: The system shall track progress percentage (0-100)

#### 3.4.3 History Tracking
- **FR-SN-011**: The system shall maintain history of status changes and assessments
- **FR-SN-012**: The system shall record assessment methods (SURVEY, OBSERVATION, INTERVIEW, TEST, REVIEW)
- **FR-SN-013**: The system shall track assessor information and notes
- **FR-SN-014**: The system shall schedule next assessment dates

#### 3.4.4 API Endpoints
```
POST   /api/v1/strategic-planning/student-needs
GET    /api/v1/strategic-planning/student-needs/:id
GET    /api/v1/strategic-planning/student-needs
PUT    /api/v1/strategic-planning/student-needs/:id
DELETE /api/v1/strategic-planning/student-needs/:id
GET    /api/v1/strategic-planning/student-needs/:id/history
```

### 3.5 SWOT Analysis

#### 3.5.1 SWOT Item Management
- **FR-SW-001**: The system shall allow creation of SWOT items across four quadrants (S, W, O, T)
- **FR-SW-002**: The system shall link SWOT items to source data (SURVEY, RAPOR, FGD, LOCAL_CONTEXT, SCHOOL_DATA, MANUAL)
- **FR-SW-003**: The system shall categorize and tag SWOT items
- **FR-SW-004**: The system shall assign priority (1-5), impact score (1-5), and urgency score (1-5)
- **FR-SW-005**: The system shall link SWOT items to action items

#### 3.5.2 SWOT Sessions
- **FR-SW-006**: The system shall create SWOT analysis sessions to group related items
- **FR-SW-007**: The system shall track session status (DRAFT, IN_PROGRESS, COMPLETED, ARCHIVED)
- **FR-SW-008**: The system shall assign facilitators to sessions
- **FR-SW-009**: The system shall generate session summaries and key insights
- **FR-SW-010**: The system shall support session templates for reuse

#### 3.5.3 AI Integration
- **FR-SW-011**: The system shall integrate with AI service for SWOT generation
- **FR-SW-012**: The system shall generate SWOT items from provided context data
- **FR-SW-013**: The system shall support AI-powered SWOT analysis

#### 3.5.4 API Endpoints
```
POST   /api/v1/strategic-planning/swot/items
GET    /api/v1/strategic-planning/swot/items/:id
GET    /api/v1/strategic-planning/swot/items
PUT    /api/v1/strategic-planning/swot/items/:id
DELETE /api/v1/strategic-planning/swot/items/:id
POST   /api/v1/strategic-planning/swot/sessions
GET    /api/v1/strategic-planning/swot/sessions/:id
GET    /api/v1/strategic-planning/swot/sessions
PUT    /api/v1/strategic-planning/swot/sessions/:id
DELETE /api/v1/strategic-planning/swot/sessions/:id
POST   /api/v1/strategic-planning/swot/sessions/:id/items
POST   /api/v1/strategic-planning/swot/generate
```

### 3.6 Root Cause Analysis

#### 3.6.1 5-Whys Analysis
- **FR-RC-001**: The system shall support 5-Whys methodology for root cause analysis
- **FR-RC-002**: The system shall link root cause analysis to Rapor Pendidikan metrics
- **FR-RC-003**: The system shall record each "why" level (why_1 through why_5)
- **FR-RC-004**: The system shall identify the root cause and category
- **FR-RC-005**: The system shall create corrective action plans (kegiatan_benahi)

#### 3.6.2 Assignment and Tracking
- **FR-RC-006**: The system shall assign root cause actions to responsible users
- **FR-RC-007**: The system shall set due dates for corrective actions
- **FR-RC-008**: The system shall track status (IDENTIFIED, IN_PROGRESS, RESOLVED, ON_HOLD, CANCELLED)
- **FR-RC-009**: The system shall track completion percentage (0-100)
- **FR-RC-010**: The system shall record actual completion dates

#### 3.6.3 Validation
- **FR-RC-011**: The system shall support validation of root cause analysis
- **FR-RC-012**: The system shall record validator information and validation notes
- **FR-RC-013**: The system shall track validation results (APPROVED, REJECTED, NEEDS_REVISION)
- **FR-RC-014**: The system shall link root cause to SWOT items

#### 3.6.4 History Tracking
- **FR-RC-015**: The system shall maintain history of status changes and progress updates
- **FR-RC-016**: The system shall record validation history

#### 3.6.5 AI Integration
- **FR-RC-017**: The system shall integrate with AI service for root cause generation
- **FR-RC-018**: The system shall generate 5-Whys analysis from problem descriptions

#### 3.6.6 API Endpoints
```
POST   /api/v1/strategic-planning/root-cause
GET    /api/v1/strategic-planning/root-cause/:id
GET    /api/v1/strategic-planning/root-cause
PUT    /api/v1/strategic-planning/root-cause/:id
DELETE /api/v1/strategic-planning/root-cause/:id
POST   /api/v1/strategic-planning/root-cause/:id/validate
GET    /api/v1/strategic-planning/root-cause/:id/history
POST   /api/v1/strategic-planning/root-cause/generate
```

### 3.7 Fishbone Diagram

#### 3.7.1 Diagram Management
- **FR-FB-001**: The system shall create Fishbone (Ishikawa) diagrams for cause-effect analysis
- **FR-FB-002**: The system shall define the head effect (main problem/outcome)
- **FR-FB-003**: The system shall support multiple diagram types (STANDARD, SIMPLIFIED, EXTENDED)
- **FR-FB-004**: The system shall configure bone categories (MANUSIA, METODE, MATERIAL, FASILITAS, LINGKUNGAN, UANG, MANAJEMEN, CUSTOM)
- **FR-FB-005**: The system shall link diagrams to root cause and SWOT items

#### 3.7.2 Node Management
- **FR-FB-006**: The system shall create nodes within bone categories
- **FR-FB-007**: The system shall support hierarchical node structure (levels 1-5)
- **FR-FB-008**: The system shall position nodes on canvas (x, y coordinates)
- **FR-FB-009**: The system shall customize node appearance (color, size)
- **FR-FB-010**: The system shall mark main bone nodes

#### 3.7.3 Connection Management
- **FR-FB-011**: The system shall create connections between nodes
- **FR-FB-012**: The system shall customize connection styles (DIRECT, DASHED, DOTTED)
- **FR-FB-013**: The system shall adjust line weight and style

#### 3.7.4 Diagram Features
- **FR-FB-014**: The system shall support diagram templates
- **FR-FB-015**: The system shall track diagram status (DRAFT, IN_PROGRESS, COMPLETED, ARCHIVED)
- **FR-FB-016**: The system shall attach evidence URLs to nodes

#### 3.7.5 AI Integration
- **FR-FB-017**: The system shall integrate with AI service for fishbone generation
- **FR-FB-018**: The system shall generate fishbone diagrams from problem descriptions

#### 3.7.6 API Endpoints
```
POST   /api/v1/strategic-planning/fishbone/diagrams
GET    /api/v1/strategic-planning/fishbone/diagrams/:id
GET    /api/v1/strategic-planning/fishbone/diagrams
PUT    /api/v1/strategic-planning/fishbone/diagrams/:id
DELETE /api/v1/strategic-planning/fishbone/diagrams/:id
POST   /api/v1/strategic-planning/fishbone/diagrams/:id/nodes
GET    /api/v1/strategic-planning/fishbone/diagrams/:id/nodes
PUT    /api/v1/strategic-planning/fishbone/diagrams/:id/nodes/:id
DELETE /api/v1/strategic-planning/fishbone/diagrams/:id/nodes/:id
POST   /api/v1/strategic-planning/fishbone/diagrams/:id/connections
POST   /api/v1/strategic-planning/fishbone/generate
```

### 3.8 KSP Analysis Integration

#### 3.8.1 Integration Management
- **FR-KSP-001**: The system shall integrate analysis results into KSP curriculum documents
- **FR-KSP-002**: The system shall link integrations to curriculum documents (trx_curriculum_document)
- **FR-KSP-003**: The system shall support multiple integration types (SWOT, ROOT_CAUSE, FISHBONE, STUDENT_NEEDS, RAPOR_PENDIDIKAN, COMBINED)
- **FR-KSP-004**: The system shall specify which KSP section uses the analysis
- **FR-KSP-005**: The system shall assign weight (0-2) to indicate influence level

#### 3.8.2 Approval Workflow
- **FR-KSP-006**: The system shall support approval workflow for integrations
- **FR-KSP-007**: The system shall track integration status (PENDING, APPROVED, REJECTED, MODIFIED)
- **FR-KSP-008**: The system shall record approver information and approval notes
- **FR-KSP-009**: The system shall track which sections use the integration

#### 3.8.3 Recommendations
- **FR-KSP-010**: The system shall generate recommendations based on analysis
- **FR-KSP-011**: The system shall categorize recommendations (CURRICULUM_ADJUSTMENT, RESOURCE_ALLOCATION, TEACHING_METHOD, ASSESSMENT, EXTRACURRICULAR, PARTNERSHIP)
- **FR-KSP-012**: The system shall assign priority (1-5) to recommendations
- **FR-KSP-013**: The system shall track recommendation status (SUGGESTED, ACCEPTED, REJECTED, IMPLEMENTED, DEFERRED)
- **FR-KSP-014**: The system shall record implementation details and effectiveness ratings
- **FR-KSP-015**: The system shall assign confidence scores (0-1) to recommendations

#### 3.8.4 Templates
- **FR-KSP-016**: The system shall create KSP integration templates
- **FR-KSP-017**: The system shall define template structure in JSON format
- **FR-KSP-018**: The system shall support public/private templates
- **FR-KSP-019**: The system shall track template usage statistics

#### 3.8.5 Document Compilation
- **FR-KSP-020**: The system shall compile integrated analysis into KSP documents
- **FR-KSP-021**: The system shall support multiple document formats
- **FR-KSP-022**: The system shall generate document URLs and metadata

#### 3.8.6 API Endpoints
```
POST   /api/v1/strategic-planning/ksp-integrations
GET    /api/v1/strategic-planning/ksp-integrations/:id
GET    /api/v1/strategic-planning/ksp-integrations
PUT    /api/v1/strategic-planning/ksp-integrations/:id
DELETE /api/v1/strategic-planning/ksp-integrations/:id
POST   /api/v1/strategic-planning/ksp-integrations/:id/approve
POST   /api/v1/strategic-planning/ksp-integrations/:id/recommendations
GET    /api/v1/strategic-planning/ksp-integrations/:id/recommendations
POST   /api/v1/strategic-planning/ksp-templates
GET    /api/v1/strategic-planning/ksp-templates
POST   /api/v1/strategic-planning/ksp-integrations/:id/compile
```

---

## 4. User Stories

### 4.1 Rapor Pendidikan

**US-RP-001**: As a School Principal, I want to synchronize Rapor Pendidikan data from Kemdikbud API so that I can view my school's literacy, numeracy, and character scores.

**US-RP-002**: As a School Principal, I want to view synchronization status so that I can troubleshoot any data sync failures.

**US-RP-003**: As a Curriculum Developer, I want to filter Rapor Pendidikan data by year and semester so that I can analyze trends over time.

### 4.2 Surveys

**US-SV-001**: As a School Staff, I want to create dynamic surveys with custom form schemas so that I can collect specific data from different audiences.

**US-SV-002**: As a School Staff, I want to create survey templates so that I can reuse common survey structures.

**US-SV-003**: As a Parent, I want to respond to surveys anonymously so that I can provide honest feedback without fear of identification.

**US-SV-004**: As a School Principal, I want to view survey response analytics so that I can understand stakeholder sentiments.

### 4.3 FGD Sessions

**US-FGD-001**: As a School Principal, I want to schedule virtual FGD sessions so that I can gather input from various stakeholders.

**US-FGD-002**: As a Moderator, I want to manage FGD participants and track attendance so that I can ensure proper participation.

**US-FGD-003**: As a Participant, I want to join FGD sessions via conference links so that I can contribute to discussions.

**US-FGD-004**: As a School Principal, I want to view sentiment analysis of FGD notes so that I can understand overall session tone.

### 4.4 Student Needs

**US-SN-001**: As a Teacher, I want to profile student needs across multiple dimensions so that I can provide targeted support.

**US-SN-002**: As a School Counselor, I want to create action plans for student needs so that I can track intervention progress.

**US-SN-003**: As a School Principal, I want to view student needs history so that I can assess intervention effectiveness over time.

**US-SN-004**: As a Teacher, I want to assign action plans to specific users so that responsibilities are clear.

### 4.5 SWOT Analysis

**US-SW-001**: As a School Principal, I want to create SWOT items so that I can document strengths, weaknesses, opportunities, and threats.

**US-SW-002**: As a Curriculum Developer, I want to link SWOT items to source data so that I can trace the origin of each item.

**US-SW-003**: As a School Principal, I want to create SWOT sessions to group related items so that I can organize analysis by topic.

**US-SW-004**: As a Facilitator, I want to use AI to generate SWOT items from context data so that I can accelerate the analysis process.

### 4.6 Root Cause Analysis

**US-RC-001**: As a School Principal, I want to perform 5-Whys analysis on problematic metrics so that I can identify root causes.

**US-RC-002**: As a Teacher, I want to create corrective action plans so that I can address identified root causes.

**US-RC-003**: As a School Principal, I want to validate root cause analysis so that I can ensure accuracy before implementation.

**US-RC-004**: As a Curriculum Developer, I want to use AI to generate 5-Whys analysis so that I can save time on manual analysis.

### 4.7 Fishbone Diagram

**US-FB-001**: As a School Principal, I want to create Fishbone diagrams so that I can visualize cause-effect relationships.

**US-FB-002**: As a Teacher, I want to add nodes to bone categories so that I can break down causes systematically.

**US-FB-003**: As a Curriculum Developer, I want to connect nodes to show relationships so that I can build complete diagrams.

**US-FB-004**: As a School Principal, I want to use AI to generate Fishbone diagrams so that I can quickly create visual analyses.

### 4.8 KSP Integration

**US-KSP-001**: As a Curriculum Developer, I want to integrate analysis results into KSP documents so that curriculum decisions are data-driven.

**US-KSP-002**: As a School Principal, I want to approve integrations so that I can control which analyses influence the curriculum.

**US-KSP-003**: As a Curriculum Developer, I want to view recommendations based on analysis so that I can implement suggested improvements.

**US-KSP-004**: As a School Principal, I want to create KSP integration templates so that I can standardize the integration process.

**US-KSP-005**: As a Curriculum Developer, I want to compile integrated analysis into KSP documents so that I can generate final curriculum documents.

---

## 5. Non-Functional Requirements

### 5.1 Performance

- **NFR-PER-001**: API response time for simple CRUD operations shall be under 200ms (p95)
- **NFR-PER-002**: API response time for complex queries (with joins and aggregations) shall be under 500ms (p95)
- **NFR-PER-003**: Database queries shall use appropriate indexes to ensure efficient data retrieval
- **NFR-PER-004**: Pagination shall be implemented for list endpoints to prevent large result sets
- **NFR-PER-005**: The system shall support concurrent users with appropriate connection pooling

### 5.2 Security

- **NFR-SEC-001**: All API endpoints shall require authentication (except public survey responses if configured)
- **NFR-SEC-002**: Authorization shall be enforced based on user roles and school ownership
- **NFR-SEC-003**: Sensitive data (e.g., conference passwords) shall be encrypted at rest
- **NFR-SEC-004**: API requests shall be rate-limited to prevent abuse
- **NFR-SEC-005**: Input validation shall be performed on all API endpoints
- **NFR-SEC-006**: SQL injection prevention shall be enforced through parameterized queries (GORM)
- **NFR-SEC-007**: Audit trails shall be maintained for all data modifications

### 5.3 Reliability

- **NFR-REL-001**: The system shall maintain 99.5% uptime during business hours
- **NFR-REL-002**: Database transactions shall be used for multi-step operations to ensure data consistency
- **NFR-REL-003**: Soft deletes shall be implemented to allow data recovery
- **NFR-REL-004**: Error handling shall be comprehensive with appropriate HTTP status codes
- **NFR-REL-005**: External API calls (e.g., Kemdikbud, AI service) shall have timeout and retry logic

### 5.4 Scalability

- **NFR-SCL-001**: The system shall support horizontal scaling through stateless API design
- **NFR-SCL-002**: Database indexes shall be optimized for query patterns
- **NFR-SCL-003**: JSONB fields shall be indexed appropriately for JSON queries
- **NFR-SCL-004**: The system shall support multiple schools with proper data isolation

### 5.5 Maintainability

- **NFR-MAI-001**: Code shall follow Go best practices and conventions
- **NFR-MAI-002**: Business logic shall be separated into service layer
- **NFR-MAI-003**: Database operations shall be abstracted through repository layer
- **NFR-MAI-004**: API contracts shall be documented through DTOs with validation tags
- **NFR-MAI-005**: Database schema changes shall be managed through migration scripts

### 5.6 Usability

- **NFR-USA-001**: API error messages shall be clear and actionable
- **NFR-USA-002**: Validation errors shall include field-specific messages
- **NFR-USA-003**: API responses shall follow consistent structure
- **NFR-USA-004**: Pagination metadata shall be included in list responses

---

## 6. Technical Constraints

### 6.1 Technology Stack

- **Backend Framework**: Go with Fiber web framework
- **ORM**: GORM for PostgreSQL database operations
- **Database**: PostgreSQL with UUID extension
- **Authentication**: JWT-based authentication (middleware.Protected)
- **AI Integration**: gRPC client for Strategic Analysis Service (strategic-analysis-service:50063)
- **External API**: Kemdikbud Rapor Pendidikan API

### 6.2 Database Constraints

- **Primary Keys**: All tables use UUID primary keys with uuid_generate_v4()
- **Foreign Keys**: CASCADE or SET NULL deletion behavior based on relationship
- **Audit Fields**: All tables include created_at, updated_at, deleted_at, created_by, updated_by, deleted_by
- **Check Constraints**: Enumerated values enforced through CHECK constraints
- **Indexes**: Strategic indexes on foreign keys, status fields, and frequently queried columns
- **Soft Deletes**: Implemented through deleted_at TIMESTAMPTZ field

### 6.3 API Constraints

- **Content-Type**: application/json
- **Authentication**: Bearer token in Authorization header
- **Validation**: Request validation using struct tags (validate:"required,uuid", etc.)
- **Error Handling**: Standardized error response format
- **Pagination**: Page and per_page parameters for list endpoints

### 6.4 Integration Constraints

- **gRPC Service**: Strategic Analysis Service must be available at strategic-analysis-service:50063
- **Kemdikbud API**: Rapor Pendidikan API must be accessible with proper credentials
- **Curriculum Document**: Integration requires existing trx_curriculum_document records
- **Master Data**: Dependencies on master_school, auth_user, master_student_context_ext tables

### 6.5 Data Constraints

- **JSONB Storage**: Flexible schema data stored in JSONB fields (form_schema, raw_data, participants, etc.)
- **Array Fields**: Tags and categories stored as VARCHAR(100)[] arrays
- **Decimal Precision**: Scores stored as DECIMAL(5,2) for precision
- **Timestamps**: All timestamps use TIMESTAMPTZ for timezone awareness
- **Text Limits**: VARCHAR fields have appropriate length limits based on use case

### 6.6 Workflow Constraints

- **In-Memory Storage**: Version history and approval workflows currently use in-memory stores (noted for production replacement with database tables)
- **Status Transitions**: Status fields have defined valid values enforced by CHECK constraints
- **Priority Levels**: Priority fields use 1-5 scale (1 highest)
- **Percentage Fields**: Progress and completion percentages use 0-100 range

---

## 7. Data Model

### 7.1 Core Entities

#### Rapor Pendidikan
- Stores literacy, numeracy, character scores from Kemdikbud API
- Links to master_school
- Tracks sync status and errors

#### Surveys & Survey Responses
- Dynamic surveys with JSON form schemas
- Support for multiple target audiences
- Anonymous or identified responses
- Template support for reuse

#### FGD Sessions & Participants
- Virtual meeting management
- Conference platform integration
- Participant attendance tracking
- Sentiment analysis on notes

#### Student Needs Enhanced & History
- Enhanced student profiling
- Action plan management
- Progress tracking
- Assessment history

#### SWOT Items, Sessions, Session Items
- Four-quadrant SWOT analysis
- Session-based organization
- Source data linking
- AI generation support

#### Root Causes & History
- 5-Whys methodology
- Corrective action planning
- Validation workflow
- Progress tracking

#### Fishbone Diagrams, Nodes, Connections
- Cause-effect visualization
- Hierarchical node structure
- Canvas positioning
- Template support

#### KSP Integration, Recommendations, Templates
- Integration with curriculum documents
- Approval workflow
- Recommendation management
- Template system

### 7.2 Relationships

- **School**: All entities belong to a school (master_school)
- **User**: Audit fields link to auth_user
- **Analysis Integration**: SWOT, Root Cause, Fishbone can link to each other
- **KSP Integration**: Links all analysis types to curriculum documents
- **Survey Integration**: Student needs can link to survey responses
- **Rapor Integration**: Root cause can link to Rapor Pendidikan metrics

---

## 8. Acceptance Criteria

### 8.1 Rapor Pendidikan

- **AC-RP-001**: Given a valid school_id, year, and semester, when I sync Rapor Pendidikan data, then the system should retrieve and store literacy, numeracy, and character scores with sync_status = 'SUCCESS'
- **AC-RP-002**: Given a sync failure, when I check the record, then sync_status should be 'FAILED' with error message populated
- **AC-RP-003**: Given invalid school_id format, when I create a Rapor record, then the system should return validation error

### 8.2 Surveys

- **AC-SV-001**: Given a valid survey configuration, when I create a survey, then the system should store it with status = 'DRAFT'
- **AC-SV-002**: Given an active survey, when a respondent submits answers, then the system should store the response with submitted_at timestamp
- **AC-SV-003**: Given an anonymous survey, when a respondent submits, then respondent_id should be NULL

### 8.3 FGD Sessions

- **AC-FGD-001**: Given valid session details, when I create an FGD session, then the system should store it with status = 'SCHEDULED'
- **AC-FGD-002**: Given a participant joins a session, when I update attendance, then joined_at should be populated
- **AC-FGD-003**: Given session notes are saved, when I retrieve the session, then sentiment_score should be calculated

### 8.4 Student Needs

- **AC-SN-001**: Given a student context, when I create a student needs profile, then the system should link it to master_student_context_ext
- **AC-SN-002**: Given an action plan is created, when I assign it to a user, then action_plan_assigned_to should be populated
- **AC-SN-003**: Given progress is updated, when I check the record, then progress_percentage should reflect the update

### 8.5 SWOT Analysis

- **AC-SW-001**: Given a valid SWOT item, when I create it, then the system should store it with the correct quadrant (S, W, O, T)
- **AC-SW-002**: Given a SWOT session, when I add items to it, then the junction table should link session and items
- **AC-SW-003**: Given AI generation request, when I call the generate endpoint, then the system should return AI-generated SWOT items

### 8.6 Root Cause Analysis

- **AC-RC-001**: Given a problem description, when I perform 5-Whys analysis, then the system should store all 5 why levels
- **AC-RC-002**: Given a root cause is identified, when I create a corrective action, then kegiatan_benahi should be populated
- **AC-RC-003**: Given validation is performed, when I validate the analysis, then validation_result should be recorded

### 8.7 Fishbone Diagram

- **AC-FB-001**: Given a head effect, when I create a Fishbone diagram, then the system should store it with status = 'DRAFT'
- **AC-FB-002**: Given a bone category, when I add a node, then the system should store it with the correct category
- **AC-FB-003**: Given two nodes, when I create a connection, then the system should link them in the connections table

### 8.8 KSP Integration

- **AC-KSP-001**: Given analysis results, when I create an integration, then the system should link it to a curriculum document
- **AC-KSP-002**: Given an integration is pending, when I approve it, then integration_status should change to 'APPROVED'
- **AC-KSP-003**: Given recommendations are generated, when I view the integration, then recommendations should be listed with priority

---

## 9. Open Issues / Future Enhancements

### 9.1 Known Limitations

1. **In-Memory Storage**: Version history and approval workflows use in-memory stores in service_ksp_phase6.go. These should be replaced with database tables for production use.

2. **AI Service Dependency**: The module depends on the Strategic Analysis Service being available at strategic-analysis-service:50063. Service unavailability will affect AI-powered features.

3. **External API Reliability**: Rapor Pendidikan API synchronization depends on Kemdikbud API availability and stability.

### 9.2 Future Enhancements

1. **Real-time Collaboration**: Add WebSocket support for real-time collaboration on FGD sessions and Fishbone diagrams.

2. **Advanced Analytics**: Implement more sophisticated analytics and reporting dashboards.

3. **Export/Import**: Add functionality to export and import analysis data for backup and sharing.

4. **Mobile Support**: Develop mobile-friendly interfaces for survey responses and FGD participation.

5. **Notification System**: Implement notifications for action plan due dates, approval requests, and session reminders.

6. **Multi-language Support**: Add support for multiple languages in surveys and analysis templates.

---

## 10. Glossary

- **KSP**: Kurikulum Satuan Pendidikan (School Curriculum Document)
- **FGD**: Focus Group Discussion
- **SWOT**: Strengths, Weaknesses, Opportunities, Threats
- **5-Whys**: Root cause analysis methodology asking "why" five times
- **Fishbone**: Ishikawa diagram for cause-effect analysis
- **Rapor Pendidikan**: Indonesian Ministry of Education's education report API
- **DTO**: Data Transfer Object
- **GORM**: Go ORM library for database operations
- **Fiber**: Go web framework
- **gRPC**: Remote Procedure Call framework
- **UUID**: Universally Unique Identifier
- **JSONB**: Binary JSON format for PostgreSQL

---

## 11. Appendix

### 11.1 Database Migration Files

- 000050_create_rapor_pendidikan_tables.up.sql
- 000051_create_survey_tables.up.sql
- 000052_create_fgd_sessions_tables.up.sql
- 000053_create_student_needs_enhanced_tables.up.sql
- 000054_create_swot_analysis_tables.up.sql
- 000055_create_root_cause_tables.up.sql
- 000056_create_fishbone_diagram_tables.up.sql
- 000057_create_ksp_analysis_integration_tables.up.sql

### 11.2 Go Source Files

- backend/internal/strategic_planning/handler.go
- backend/internal/strategic_planning/routes.go
- backend/internal/strategic_planning/dto.go
- backend/internal/strategic_planning/model.go
- backend/internal/strategic_planning/service.go
- backend/internal/strategic_planning/service_ksp_phase6.go
- backend/internal/strategic_planning/repository.go

### 11.3 External Dependencies

- github.com/gofiber/fiber/v2
- gorm.io/gorm
- github.com/google/uuid
- grpc_clients (Strategic Analysis Service)

---

**Document End**
