package foundational_skills

// CreateSkillStandardRequest represents request for creating a new skill standard
type CreateSkillStandardRequest struct {
	SkillType   string `json:"skill_type" binding:"required"`
	SkillCode   string `json:"skill_code" binding:"required"`
	SkillName   string `json:"skill_name" binding:"required"`
	Description string `json:"description" binding:"required"`
	PhaseID     string `json:"phase_id"`
	Indicators  string `json:"indicators"`
	IsActive    *bool  `json:"is_active"`
}

// UpdateSkillStandardRequest represents request for updating a skill standard
type UpdateSkillStandardRequest struct {
	SkillType   string `json:"skill_type" binding:"omitempty"`
	SkillCode   string `json:"skill_code" binding:"omitempty"`
	SkillName   string `json:"skill_name" binding:"omitempty"`
	Description string `json:"description" binding:"omitempty"`
	PhaseID     string `json:"phase_id"`
	Indicators  string `json:"indicators"`
	IsActive    *bool  `json:"is_active"`
}

// SkillStandardResponse represents response for skill standard
type SkillStandardResponse struct {
	ID          string `json:"id"`
	SkillType   string `json:"skill_type"`
	SkillCode   string `json:"skill_code"`
	SkillName   string `json:"skill_name"`
	Description string `json:"description"`
	PhaseID     string `json:"phase_id"`
	Indicators  string `json:"indicators"`
	IsActive    bool   `json:"is_active"`
	CreatedAt   string `json:"created_at"`
	UpdatedAt   string `json:"updated_at"`
}

// CreateAssessmentRequest represents request for creating a new assessment
type CreateAssessmentRequest struct {
	StudentID       string   `json:"student_id" binding:"required"`
	SkillStandardID string   `json:"skill_standard_id" binding:"required"`
	AssessmentDate  string   `json:"assessment_date" binding:"required"`
	MasteryLevel    string   `json:"mastery_level" binding:"required"`
	Score           *float64 `json:"score"`
	Notes           string   `json:"notes"`
	TeacherID       string   `json:"teacher_id"`
}

// UpdateAssessmentRequest represents request for updating an assessment
type UpdateAssessmentRequest struct {
	SkillStandardID string   `json:"skill_standard_id" binding:"omitempty"`
	AssessmentDate  string   `json:"assessment_date" binding:"omitempty"`
	MasteryLevel    string   `json:"mastery_level" binding:"omitempty"`
	Score           *float64 `json:"score"`
	Notes           string   `json:"notes"`
}

// AssessmentResponse represents response for assessment
type AssessmentResponse struct {
	ID              string   `json:"id"`
	StudentID       string   `json:"student_id"`
	SkillStandardID string   `json:"skill_standard_id"`
	AssessmentDate  string   `json:"assessment_date"`
	MasteryLevel    string   `json:"mastery_level"`
	Score           *float64 `json:"score"`
	Notes           string   `json:"notes"`
	TeacherID       string   `json:"teacher_id"`
	CreatedAt       string   `json:"created_at"`
	UpdatedAt       string   `json:"updated_at"`
}

// StudentProgressResponse represents student's foundational skills progress
type StudentProgressResponse struct {
	StudentID        string                        `json:"student_id"`
	StudentName      string                        `json:"student_name"`
	Assessments      []AssessmentResponse          `json:"assessments"`
	SkillBreakdown   map[string]SkillProgress      `json:"skill_breakdown"`
	OverallMastery   map[string]int                `json:"overall_mastery"`
	LatestAssessment map[string]AssessmentResponse `json:"latest_assessment"`
}

// SkillProgress represents progress per skill type
type SkillProgress struct {
	SkillType        string         `json:"skill_type"`
	TotalAssessments int            `json:"total_assessments"`
	MasteryCount     map[string]int `json:"mastery_count"`
	AverageScore     float64        `json:"average_score"`
}

// SkillStandardsResponse represents response for list of skill standards
type SkillStandardsResponse struct {
	Standards []SkillStandardResponse `json:"standards"`
	Total     int                     `json:"total"`
}

// AssessmentsResponse represents response for list of assessments
type AssessmentsResponse struct {
	Assessments []AssessmentResponse `json:"assessments"`
	Total       int                  `json:"total"`
}
