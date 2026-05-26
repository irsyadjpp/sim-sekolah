package question_bank

import (
	"time"

	"sim-sekolah/internal/common"

	"github.com/google/uuid"
	"github.com/lib/pq"
)

// Question Types
const (
	QuestionTypeMultipleChoice  = "MULTIPLE_CHOICE"
	QuestionTypeTrueFalse       = "TRUE_FALSE"
	QuestionTypeShortAnswer     = "SHORT_ANSWER"
	QuestionTypeEssay           = "ESSAY"
	QuestionTypeMatching        = "MATCHING"
	QuestionTypeFillInBlank     = "FILL_IN_BLANK"
	QuestionTypeDragAndDrop     = "DRAG_AND_DROP"
	QuestionTypeHotSpot         = "HOT_SPOT"
	QuestionTypeMultipleSelect  = "MULTIPLE_SELECT"
	QuestionTypeNumeric         = "NUMERIC"
	QuestionTypeOrderedResponse = "ORDERED_RESPONSE"
)

// Difficulty Levels
const (
	DifficultyEasy   = "EASY"
	DifficultyMedium = "MEDIUM"
	DifficultyHard   = "HARD"
	DifficultyExpert = "EXPERT"
)

// Question Status
const (
	QuestionStatusDraft     = "DRAFT"
	QuestionStatusPending   = "PENDING"
	QuestionStatusApproved  = "APPROVED"
	QuestionStatusRejected  = "REJECTED"
	QuestionStatusArchived  = "ARCHIVED"
	QuestionStatusPublished = "PUBLISHED"
)

// Bloom's Taxonomy Levels
const (
	BloomRemember   = "REMEMBER"
	BloomUnderstand = "UNDERSTAND"
	BloomApply      = "APPLY"
	BloomAnalyze    = "ANALYZE"
	BloomEvaluate   = "EVALUATE"
	BloomCreate     = "CREATE"
)

// Question represents a question in the question bank
type Question struct {
	ID                uuid.UUID      `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	QuestionText      string         `gorm:"type:text;not null" json:"question_text"`
	QuestionType      string         `gorm:"type:varchar(50);not null;index" json:"question_type"`
	SubjectID         *uuid.UUID     `gorm:"type:uuid;index" json:"subject_id"`
	TopicID           *uuid.UUID     `gorm:"type:uuid;index" json:"topic_id"`
	GradeLevelID      *uuid.UUID     `gorm:"type:uuid;index" json:"grade_level_id"`
	Difficulty        string         `gorm:"type:varchar(20);not null;index" json:"difficulty"`
	BloomLevel        string         `gorm:"type:varchar(20)" json:"bloom_level"`
	Points            float64        `gorm:"type:numeric(5,2);default:1.0" json:"points"`
	TimeLimit         *int           `gorm:"type:integer" json:"time_limit"` // in seconds
	Status            string         `gorm:"type:varchar(20);not null;default:DRAFT" json:"status"`
	Explanation       string         `gorm:"type:text" json:"explanation"`
	Hints             pq.StringArray `gorm:"type:jsonb" json:"hints"`
	Tags              pq.StringArray `gorm:"type:jsonb" json:"tags"`
	AuthorID          uuid.UUID      `gorm:"type:uuid;not null;index" json:"author_id"`
	SchoolID          uuid.UUID      `gorm:"type:uuid;not null;index" json:"school_id"`
	IsPublic          bool           `gorm:"default:false" json:"is_public"`
	AllowReview       bool           `gorm:"default:true" json:"allow_review"`
	RandomizeOptions  bool           `gorm:"default:false" json:"randomize_options"`
	UsageCount        int            `gorm:"default:0" json:"usage_count"`
	CorrectRate       float64        `gorm:"type:numeric(5,2)" json:"correct_rate"`  // Percentage of correct answers
	AverageTime       float64        `gorm:"type:numeric(10,2)" json:"average_time"` // Average time to answer in seconds
	LastUsedAt        *time.Time     `gorm:"type:timestamp" json:"last_used_at"`
	EffectiveDate     *time.Time     `gorm:"type:timestamp" json:"effective_date"`
	ExpiryDate        *time.Time     `gorm:"type:timestamp" json:"expiry_date"`
	ReferenceMaterial string         `gorm:"type:text" json:"reference_material"`

	common.Auditable
}

func (Question) TableName() string {
	return "questions"
}

// QuestionOption represents options for multiple choice questions
type QuestionOption struct {
	ID         uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	QuestionID uuid.UUID `gorm:"type:uuid;not null;index" json:"question_id"`
	OptionText string    `gorm:"type:text;not null" json:"option_text"`
	IsCorrect  bool      `gorm:"default:false" json:"is_correct"`
	Order      int       `gorm:"default:0" json:"order"`
	Feedback   string    `gorm:"type:text" json:"feedback"`

	common.Auditable
}

func (QuestionOption) TableName() string {
	return "question_options"
}

// QuestionAnswer represents correct answers for non-multiple choice questions
type QuestionAnswer struct {
	ID            uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	QuestionID    uuid.UUID `gorm:"type:uuid;not null;index" json:"question_id"`
	AnswerText    string    `gorm:"type:text;not null" json:"answer_text"`
	IsCorrect     bool      `gorm:"default:true" json:"is_correct"`
	Order         int       `gorm:"default:0" json:"order"`      // For ordered response questions
	MatchWith     string    `gorm:"type:text" json:"match_with"` // For matching questions
	Explanation   string    `gorm:"type:text" json:"explanation"`
	PartialCredit float64   `gorm:"type:numeric(5,2)" json:"partial_credit"`

	common.Auditable
}

func (QuestionAnswer) TableName() string {
	return "question_answers"
}

// QuestionSet represents a collection of questions
type QuestionSet struct {
	ID             uuid.UUID      `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	Name           string         `gorm:"type:varchar(255);not null" json:"name"`
	Description    string         `gorm:"type:text" json:"description"`
	SubjectID      *uuid.UUID     `gorm:"type:uuid;index" json:"subject_id"`
	GradeLevelID   *uuid.UUID     `gorm:"type:uuid;index" json:"grade_level_id"`
	AuthorID       uuid.UUID      `gorm:"type:uuid;not null;index" json:"author_id"`
	SchoolID       uuid.UUID      `gorm:"type:uuid;not null;index" json:"school_id"`
	QuestionIDs    pq.StringArray `gorm:"type:jsonb" json:"question_ids"`
	TotalQuestions int            `gorm:"default:0" json:"total_questions"`
	TotalPoints    float64        `gorm:"type:numeric(10,2);default:0" json:"total_points"`
	EstimatedTime  int            `gorm:"default:0" json:"estimated_time"` // in minutes
	Difficulty     string         `gorm:"type:varchar(20)" json:"difficulty"`
	IsPublic       bool           `gorm:"default:false" json:"is_public"`
	UsageCount     int            `gorm:"default:0" json:"usage_count"`
	LastUsedAt     *time.Time     `gorm:"type:timestamp" json:"last_used_at"`

	common.Auditable
}

func (QuestionSet) TableName() string {
	return "question_sets"
}

// QuestionDifficultyCalibration represents calibrated difficulty for questions
type QuestionDifficultyCalibration struct {
	ID                   uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	QuestionID           uuid.UUID `gorm:"type:uuid;not null;uniqueIndex" json:"question_id"`
	OriginalDifficulty   string    `gorm:"type:varchar(20)" json:"original_difficulty"`
	CalibratedDifficulty string    `gorm:"type:varchar(20)" json:"calibrated_difficulty"`
	CalibrationScore     float64   `gorm:"type:numeric(5,2)" json:"calibration_score"` // 0-100
	TotalAttempts        int       `gorm:"default:0" json:"total_attempts"`
	CorrectAttempts      int       `gorm:"default:0" json:"correct_attempts"`
	AverageTime          float64   `gorm:"type:numeric(10,2)" json:"average_time"`
	DiscriminationIndex  float64   `gorm:"type:numeric(5,2)" json:"discrimination_index"`
	LastCalibratedAt     time.Time `gorm:"type:timestamp" json:"last_calibrated_at"`
	CalibratedBy         uuid.UUID `gorm:"type:uuid" json:"calibrated_by"`

	common.Auditable
}

func (QuestionDifficultyCalibration) TableName() string {
	return "question_difficulty_calibration"
}

// QuestionUsageAnalytics represents usage analytics for questions
type QuestionUsageAnalytics struct {
	ID              uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	QuestionID      uuid.UUID  `gorm:"type:uuid;not null;index" json:"question_id"`
	AssessmentID    *uuid.UUID `gorm:"type:uuid;index" json:"assessment_id"`
	UsageDate       time.Time  `gorm:"type:timestamp;not null;index" json:"usage_date"`
	TotalAttempts   int        `gorm:"default:0" json:"total_attempts"`
	CorrectAttempts int        `gorm:"default:0" json:"correct_attempts"`
	AverageTime     float64    `gorm:"type:numeric(10,2)" json:"average_time"`
	SkipCount       int        `gorm:"default:0" json:"skip_count"`
	ReviewCount     int        `gorm:"default:0" json:"review_count"`
}

func (QuestionUsageAnalytics) TableName() string {
	return "question_usage_analytics"
}

// QuestionTag represents tags for questions
type QuestionTag struct {
	ID         uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	Name       string    `gorm:"type:varchar(50);not null;uniqueIndex" json:"name"`
	Color      string    `gorm:"type:varchar(7)" json:"color"`
	Category   string    `gorm:"type:varchar(50)" json:"category"`
	UsageCount int       `gorm:"default:0" json:"usage_count"`

	common.Auditable
}

func (QuestionTag) TableName() string {
	return "question_tags"
}

// QuestionTagAssociation represents many-to-many relationship between questions and tags
type QuestionTagAssociation struct {
	QuestionID uuid.UUID `gorm:"type:uuid;primaryKey;autoIncrement:false" json:"question_id"`
	TagID      uuid.UUID `gorm:"type:uuid;primaryKey;autoIncrement:false" json:"tag_id"`

	common.Auditable
}

func (QuestionTagAssociation) TableName() string {
	return "question_tag_associations"
}

// QuestionCategory represents categories for organizing questions
type QuestionCategory struct {
	ID          uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	Name        string     `gorm:"type:varchar(100);not null;uniqueIndex" json:"name"`
	Description string     `gorm:"type:text" json:"description"`
	ParentID    *uuid.UUID `gorm:"type:uuid;index" json:"parent_id"`
	SortOrder   int        `gorm:"default:0" json:"sort_order"`
	Icon        string     `gorm:"type:varchar(50)" json:"icon"`
	Color       string     `gorm:"type:varchar(7)" json:"color"`
	IsActive    bool       `gorm:"default:true" json:"is_active"`

	common.Auditable
}

func (QuestionCategory) TableName() string {
	return "question_categories"
}

// QuestionReview represents reviews for questions
type QuestionReview struct {
	ID         uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	QuestionID uuid.UUID `gorm:"type:uuid;not null;index" json:"question_id"`
	ReviewerID uuid.UUID `gorm:"type:uuid;not null;index" json:"reviewer_id"`
	Rating     int       `gorm:"type:integer;not null" json:"rating"` // 1-5
	Comments   string    `gorm:"type:text" json:"comments"`
	ReviewDate time.Time `gorm:"type:timestamp;not null;default:CURRENT_TIMESTAMP" json:"review_date"`
	IsApproved bool      `gorm:"default:false" json:"is_approved"`

	common.Auditable
}

func (QuestionReview) TableName() string {
	return "question_reviews"
}

// QuestionImport represents import job for bulk question import
type QuestionImport struct {
	ID             uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ImportFileName string     `gorm:"type:varchar(255);not null" json:"import_file_name"`
	FileURL        string     `gorm:"type:varchar(500);not null" json:"file_url"`
	ImportType     string     `gorm:"type:varchar(20);not null" json:"import_type"`            // CSV, JSON, EXCEL
	Status         string     `gorm:"type:varchar(20);not null;default:PENDING" json:"status"` // PENDING, PROCESSING, COMPLETED, FAILED
	TotalQuestions int        `gorm:"default:0" json:"total_questions"`
	SuccessCount   int        `gorm:"default:0" json:"success_count"`
	FailureCount   int        `gorm:"default:0" json:"failure_count"`
	ErrorLog       string     `gorm:"type:text" json:"error_log"`
	ImportedBy     uuid.UUID  `gorm:"type:uuid;not null" json:"imported_by"`
	ProcessedAt    *time.Time `gorm:"type:timestamp" json:"processed_at"`

	common.Auditable
}

func (QuestionImport) TableName() string {
	return "question_imports"
}

// QuestionExport represents export job for questions
type QuestionExport struct {
	ID             uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ExportName     string     `gorm:"type:varchar(255);not null" json:"export_name"`
	ExportFormat   string     `gorm:"type:varchar(20);not null" json:"export_format"` // CSV, JSON, EXCEL, PDF
	FilterCriteria string     `gorm:"type:jsonb" json:"filter_criteria"`
	Status         string     `gorm:"type:varchar(20);not null;default:PENDING" json:"status"` // PENDING, PROCESSING, COMPLETED, FAILED
	FileURL        string     `gorm:"type:varchar(500)" json:"file_url"`
	TotalQuestions int        `gorm:"default:0" json:"total_questions"`
	ExportedBy     uuid.UUID  `gorm:"type:uuid;not null" json:"exported_by"`
	ProcessedAt    *time.Time `gorm:"type:timestamp" json:"processed_at"`

	common.Auditable
}

func (QuestionExport) TableName() string {
	return "question_exports"
}

// Helper functions

func IsValidQuestionType(questionType string) bool {
	validTypes := map[string]bool{
		QuestionTypeMultipleChoice:  true,
		QuestionTypeTrueFalse:       true,
		QuestionTypeShortAnswer:     true,
		QuestionTypeEssay:           true,
		QuestionTypeMatching:        true,
		QuestionTypeFillInBlank:     true,
		QuestionTypeDragAndDrop:     true,
		QuestionTypeHotSpot:         true,
		QuestionTypeMultipleSelect:  true,
		QuestionTypeNumeric:         true,
		QuestionTypeOrderedResponse: true,
	}
	return validTypes[questionType]
}

func IsValidDifficulty(difficulty string) bool {
	validDifficulties := map[string]bool{
		DifficultyEasy:   true,
		DifficultyMedium: true,
		DifficultyHard:   true,
		DifficultyExpert: true,
	}
	return validDifficulties[difficulty]
}

func IsValidQuestionStatus(status string) bool {
	validStatuses := map[string]bool{
		QuestionStatusDraft:     true,
		QuestionStatusPending:   true,
		QuestionStatusApproved:  true,
		QuestionStatusRejected:  true,
		QuestionStatusArchived:  true,
		QuestionStatusPublished: true,
	}
	return validStatuses[status]
}

func IsValidBloomLevel(bloomLevel string) bool {
	validLevels := map[string]bool{
		BloomRemember:   true,
		BloomUnderstand: true,
		BloomApply:      true,
		BloomAnalyze:    true,
		BloomEvaluate:   true,
		BloomCreate:     true,
	}
	return validLevels[bloomLevel]
}
