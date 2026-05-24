package peer_assessment

import (
	"time"

	"github.com/google/uuid"
)

// PeerAssessmentTemplate DTOs

type CreatePeerAssessmentTemplateRequest struct {
	TemplateName    string  `json:"template_name" binding:"required"`
	AssessmentType  string  `json:"assessment_type" binding:"required,oneof=SELF PEER GROUP"`
	SubjectID       *string `json:"subject_id"`
	Phase           string  `json:"phase" binding:"required,oneof=FASE_A FASE_B FASE_C"`
	AssessmentFocus string  `json:"assessment_focus" binding:"required,oneof=COLLABORATION COMMUNICATION CREATIVITY CRITICAL_THINKING PARTICIPATION"`
	Description     string  `json:"description" binding:"required"`
	Criteria        string  `json:"criteria" binding:"required"`     // JSON string
	RatingScale     string  `json:"rating_scale" binding:"required"` // JSON string
	Instructions    string  `json:"instructions"`
	IsActive        *bool   `json:"is_active"`
}

type UpdatePeerAssessmentTemplateRequest struct {
	TemplateName    string  `json:"template_name" binding:"omitempty"`
	AssessmentType  string  `json:"assessment_type" binding:"omitempty,oneof=SELF PEER GROUP"`
	SubjectID       *string `json:"subject_id"`
	Phase           string  `json:"phase" binding:"omitempty,oneof=FASE_A FASE_B FASE_C"`
	AssessmentFocus string  `json:"assessment_focus" binding:"omitempty,oneof=COLLABORATION COMMUNICATION CREATIVITY CRITICAL_THINKING PARTICIPATION"`
	Description     string  `json:"description" binding:"omitempty"`
	Criteria        string  `json:"criteria" binding:"omitempty"`     // JSON string
	RatingScale     string  `json:"rating_scale" binding:"omitempty"` // JSON string
	Instructions    string  `json:"instructions"`
	IsActive        *bool   `json:"is_active"`
}

type PeerAssessmentTemplateResponse struct {
	ID              string    `json:"id"`
	TemplateName    string    `json:"template_name"`
	AssessmentType  string    `json:"assessment_type"`
	SubjectID       *string   `json:"subject_id"`
	Phase           string    `json:"phase"`
	AssessmentFocus string    `json:"assessment_focus"`
	Description     string    `json:"description"`
	Criteria        string    `json:"criteria"`
	RatingScale     string    `json:"rating_scale"`
	Instructions    string    `json:"instructions"`
	IsActive        bool      `json:"is_active"`
	CreatedAt       time.Time `json:"created_at"`
	UpdatedAt       time.Time `json:"updated_at"`
	CreatedBy       *string   `json:"created_by,omitempty"`
	UpdatedBy       *string   `json:"updated_by,omitempty"`
}

// SelfAssessment DTOs

type CreateSelfAssessmentRequest struct {
	StudentID       string   `json:"student_id" binding:"required"`
	TemplateID      string   `json:"template_id" binding:"required"`
	TeacherID       *string  `json:"teacher_id"`
	AssessmentDate  string   `json:"assessment_date"` // RFC3339 format
	Context         string   `json:"context"`
	Responses       string   `json:"responses" binding:"required"` // JSON string
	SelfReflection  string   `json:"self_reflection"`
	GoalsSet        []string `json:"goals_set"`
	ConfidenceLevel string   `json:"confidence_level" binding:"omitempty,oneof=LOW MEDIUM HIGH"`
	TeacherFeedback string   `json:"teacher_feedback"`
}

type UpdateSelfAssessmentRequest struct {
	TeacherID       *string  `json:"teacher_id"`
	AssessmentDate  string   `json:"assessment_date"` // RFC3339 format
	Context         string   `json:"context"`
	Responses       string   `json:"responses" binding:"omitempty"` // JSON string
	SelfReflection  string   `json:"self_reflection"`
	GoalsSet        []string `json:"goals_set"`
	ConfidenceLevel string   `json:"confidence_level" binding:"omitempty,oneof=LOW MEDIUM HIGH"`
	TeacherFeedback string   `json:"teacher_feedback"`
}

type SelfAssessmentResponse struct {
	ID              string    `json:"id"`
	StudentID       string    `json:"student_id"`
	TemplateID      string    `json:"template_id"`
	TeacherID       *string   `json:"teacher_id"`
	AssessmentDate  time.Time `json:"assessment_date"`
	Context         string    `json:"context"`
	Responses       string    `json:"responses"`
	SelfReflection  string    `json:"self_reflection"`
	GoalsSet        []string  `json:"goals_set"`
	ConfidenceLevel string    `json:"confidence_level"`
	TeacherFeedback string    `json:"teacher_feedback"`
	CreatedAt       time.Time `json:"created_at"`
	UpdatedAt       time.Time `json:"updated_at"`
}

// PeerAssessment DTOs

type CreatePeerAssessmentRequest struct {
	AssessorStudentID    string   `json:"assessor_student_id" binding:"required"`
	AssessedStudentID    string   `json:"assessed_student_id" binding:"required"`
	TemplateID           string   `json:"template_id" binding:"required"`
	TeacherID            *string  `json:"teacher_id"`
	AssessmentDate       string   `json:"assessment_date"` // RFC3339 format
	Context              string   `json:"context"`
	Responses            string   `json:"responses" binding:"required"` // JSON string
	PositiveFeedback     string   `json:"positive_feedback"`
	ConstructiveFeedback string   `json:"constructive_feedback"`
	Suggestions          []string `json:"suggestions"`
	RelationshipContext  string   `json:"relationship_context" binding:"omitempty,oneof=GROUP_MEMBER CLASSMATE PROJECT_PARTNER"`
	TeacherNotes         string   `json:"teacher_notes"`
}

type UpdatePeerAssessmentRequest struct {
	TeacherID            *string  `json:"teacher_id"`
	AssessmentDate       string   `json:"assessment_date"` // RFC3339 format
	Context              string   `json:"context"`
	Responses            string   `json:"responses" binding:"omitempty"` // JSON string
	PositiveFeedback     string   `json:"positive_feedback"`
	ConstructiveFeedback string   `json:"constructive_feedback"`
	Suggestions          []string `json:"suggestions"`
	RelationshipContext  string   `json:"relationship_context" binding:"omitempty,oneof=GROUP_MEMBER CLASSMATE PROJECT_PARTNER"`
	TeacherReviewStatus  string   `json:"teacher_review_status" binding:"omitempty,oneof=PENDING APPROVED REJECTED"`
	TeacherNotes         string   `json:"teacher_notes"`
}

type PeerAssessmentResponse struct {
	ID                   string    `json:"id"`
	AssessorStudentID    string    `json:"assessor_student_id"`
	AssessedStudentID    string    `json:"assessed_student_id"`
	TemplateID           string    `json:"template_id"`
	TeacherID            *string   `json:"teacher_id"`
	AssessmentDate       time.Time `json:"assessment_date"`
	Context              string    `json:"context"`
	Responses            string    `json:"responses"`
	PositiveFeedback     string    `json:"positive_feedback"`
	ConstructiveFeedback string    `json:"constructive_feedback"`
	Suggestions          []string  `json:"suggestions"`
	RelationshipContext  string    `json:"relationship_context"`
	TeacherReviewStatus  string    `json:"teacher_review_status"`
	TeacherNotes         string    `json:"teacher_notes"`
	CreatedAt            time.Time `json:"created_at"`
	UpdatedAt            time.Time `json:"updated_at"`
}

// GroupAssessment DTOs

type CreateGroupAssessmentRequest struct {
	GroupID                 uuid.UUID `json:"group_id" binding:"required"`
	GroupName               string    `json:"group_name" binding:"required"`
	TemplateID              string    `json:"template_id" binding:"required"`
	TeacherID               *string   `json:"teacher_id"`
	AssessmentDate          string    `json:"assessment_date"` // RFC3339 format
	Context                 string    `json:"context"`
	ProjectDescription      string    `json:"project_description"`
	GroupResponses          string    `json:"group_responses" binding:"required"` // JSON string
	IndividualContributions string    `json:"individual_contributions"`           // JSON string
	CollaborationRating     string    `json:"collaboration_rating" binding:"omitempty,oneof=POOR FAIR GOOD EXCELLENT"`
	GroupGoals              []string  `json:"group_goals"`
	GroupReflection         string    `json:"group_reflection"`
	TeacherFeedback         string    `json:"teacher_feedback"`
}

type UpdateGroupAssessmentRequest struct {
	GroupName               string   `json:"group_name" binding:"omitempty"`
	TeacherID               *string  `json:"teacher_id"`
	AssessmentDate          string   `json:"assessment_date"` // RFC3339 format
	Context                 string   `json:"context"`
	ProjectDescription      string   `json:"project_description"`
	GroupResponses          string   `json:"group_responses" binding:"omitempty"` // JSON string
	IndividualContributions string   `json:"individual_contributions"`            // JSON string
	CollaborationRating     string   `json:"collaboration_rating" binding:"omitempty,oneof=POOR FAIR GOOD EXCELLENT"`
	GroupGoals              []string `json:"group_goals"`
	GroupReflection         string   `json:"group_reflection"`
	TeacherFeedback         string   `json:"teacher_feedback"`
}

type GroupAssessmentResponse struct {
	ID                      string    `json:"id"`
	GroupID                 string    `json:"group_id"`
	GroupName               string    `json:"group_name"`
	TemplateID              string    `json:"template_id"`
	TeacherID               *string   `json:"teacher_id"`
	AssessmentDate          time.Time `json:"assessment_date"`
	Context                 string    `json:"context"`
	ProjectDescription      string    `json:"project_description"`
	GroupResponses          string    `json:"group_responses"`
	IndividualContributions string    `json:"individual_contributions"`
	CollaborationRating     string    `json:"collaboration_rating"`
	GroupGoals              []string  `json:"group_goals"`
	GroupReflection         string    `json:"group_reflection"`
	TeacherFeedback         string    `json:"teacher_feedback"`
	CreatedAt               time.Time `json:"created_at"`
	UpdatedAt               time.Time `json:"updated_at"`
}

// GroupAssessmentMember DTOs

type CreateGroupAssessmentMemberRequest struct {
	GroupAssessmentID      string   `json:"group_assessment_id" binding:"required"`
	StudentID              string   `json:"student_id" binding:"required"`
	Role                   string   `json:"role" binding:"omitempty,oneof=LEADER CONTRIBUTOR SUPPORTER OBSERVER"`
	ParticipationRating    string   `json:"participation_rating" binding:"omitempty,oneof=LOW MEDIUM HIGH"`
	PeerFeedbackReceived   []string `json:"peer_feedback_received"`
	SelfContributionRating string   `json:"self_contribution_rating" binding:"omitempty,oneof=LOW MEDIUM HIGH"`
	ContributionNotes      string   `json:"contribution_notes"`
}

type UpdateGroupAssessmentMemberRequest struct {
	Role                   string   `json:"role" binding:"omitempty,oneof=LEADER CONTRIBUTOR SUPPORTER OBSERVER"`
	ParticipationRating    string   `json:"participation_rating" binding:"omitempty,oneof=LOW MEDIUM HIGH"`
	PeerFeedbackReceived   []string `json:"peer_feedback_received"`
	SelfContributionRating string   `json:"self_contribution_rating" binding:"omitempty,oneof=LOW MEDIUM HIGH"`
	ContributionNotes      string   `json:"contribution_notes"`
}

type GroupAssessmentMemberResponse struct {
	ID                     string    `json:"id"`
	GroupAssessmentID      string    `json:"group_assessment_id"`
	StudentID              string    `json:"student_id"`
	Role                   string    `json:"role"`
	ParticipationRating    string    `json:"participation_rating"`
	PeerFeedbackReceived   []string  `json:"peer_feedback_received"`
	SelfContributionRating string    `json:"self_contribution_rating"`
	ContributionNotes      string    `json:"contribution_notes"`
	CreatedAt              time.Time `json:"created_at"`
	UpdatedAt              time.Time `json:"updated_at"`
}

// PeerAssessmentGuideline DTOs

type CreatePeerAssessmentGuidelineRequest struct {
	Phase             string   `json:"phase" binding:"required,oneof=FASE_A FASE_B FASE_C"`
	GuidelineCategory string   `json:"guideline_category" binding:"required,oneof=GIVING_FEEDBACK RECEIVING_FEEDBACK SELF_REFLECTION"`
	Title             string   `json:"title" binding:"required"`
	Content           string   `json:"content" binding:"required"`
	Examples          []string `json:"examples"`
	Dos               []string `json:"dos"`
	Donts             []string `json:"donts"`
	DisplayOrder      int      `json:"display_order"`
	IsActive          *bool    `json:"is_active"`
}

type UpdatePeerAssessmentGuidelineRequest struct {
	Phase             string   `json:"phase" binding:"omitempty,oneof=FASE_A FASE_B FASE_C"`
	GuidelineCategory string   `json:"guideline_category" binding:"omitempty,oneof=GIVING_FEEDBACK RECEIVING_FEEDBACK SELF_REFLECTION"`
	Title             string   `json:"title" binding:"omitempty"`
	Content           string   `json:"content" binding:"omitempty"`
	Examples          []string `json:"examples"`
	Dos               []string `json:"dos"`
	Donts             []string `json:"donts"`
	DisplayOrder      int      `json:"display_order"`
	IsActive          *bool    `json:"is_active"`
}

type PeerAssessmentGuidelineResponse struct {
	ID                string    `json:"id"`
	Phase             string    `json:"phase"`
	GuidelineCategory string    `json:"guideline_category"`
	Title             string    `json:"title"`
	Content           string    `json:"content"`
	Examples          []string  `json:"examples"`
	Dos               []string  `json:"dos"`
	Donts             []string  `json:"donts"`
	DisplayOrder      int       `json:"display_order"`
	IsActive          bool      `json:"is_active"`
	CreatedAt         time.Time `json:"created_at"`
	UpdatedAt         time.Time `json:"updated_at"`
	CreatedBy         *string   `json:"created_by,omitempty"`
	UpdatedBy         *string   `json:"updated_by,omitempty"`
}

// Summary Response

type PeerAssessmentSummaryResponse struct {
	TotalTemplates        int `json:"total_templates"`
	ActiveTemplates       int `json:"active_templates"`
	TotalSelfAssessments  int `json:"total_self_assessments"`
	TotalPeerAssessments  int `json:"total_peer_assessments"`
	TotalGroupAssessments int `json:"total_group_assessments"`
	PendingPeerReviews    int `json:"pending_peer_reviews"`
	TotalGuidelines       int `json:"total_guidelines"`
}
