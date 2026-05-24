package reading_literacy

// CreateReadingLevelRequest represents request for creating a new reading level
type CreateReadingLevelRequest struct {
	LevelCode   string `json:"level_code" binding:"required"`
	LevelName   string `json:"level_name" binding:"required"`
	Description string `json:"description" binding:"required"`
	PhaseID     string `json:"phase_id"`
	Indicators  string `json:"indicators"`
	WPMRange    string `json:"wpm_range"`
	IsActive    *bool  `json:"is_active"`
}

// UpdateReadingLevelRequest represents request for updating a reading level
type UpdateReadingLevelRequest struct {
	LevelCode   string `json:"level_code" binding:"omitempty"`
	LevelName   string `json:"level_name" binding:"omitempty"`
	Description string `json:"description" binding:"omitempty"`
	PhaseID     string `json:"phase_id"`
	Indicators  string `json:"indicators"`
	WPMRange    string `json:"wpm_range"`
	IsActive    *bool  `json:"is_active"`
}

// ReadingLevelResponse represents response for reading level
type ReadingLevelResponse struct {
	ID          string `json:"id"`
	LevelCode   string `json:"level_code"`
	LevelName   string `json:"level_name"`
	Description string `json:"description"`
	PhaseID     string `json:"phase_id"`
	Indicators  string `json:"indicators"`
	WPMRange    string `json:"wpm_range"`
	IsActive    bool   `json:"is_active"`
	CreatedAt   string `json:"created_at"`
	UpdatedAt   string `json:"updated_at"`
}

// CreateAssessmentRequest represents request for creating a new reading literacy assessment
type CreateAssessmentRequest struct {
	StudentID          string  `json:"student_id" binding:"required"`
	ReadingLevelID     string  `json:"reading_level_id" binding:"required"`
	AssessmentDate     string  `json:"assessment_date" binding:"required"`
	WordsPerMinute     int     `json:"words_per_minute"`
	ComprehensionScore float64 `json:"comprehension_score"`
	FluencyRating      string  `json:"fluency_rating"`
	AccuracyScore      float64 `json:"accuracy_score"`
	Notes              string  `json:"notes"`
	TeacherID          string  `json:"teacher_id"`
}

// UpdateAssessmentRequest represents request for updating an assessment
type UpdateAssessmentRequest struct {
	ReadingLevelID     string   `json:"reading_level_id" binding:"omitempty"`
	AssessmentDate     string   `json:"assessment_date" binding:"omitempty"`
	WordsPerMinute     *int     `json:"words_per_minute"`
	ComprehensionScore *float64 `json:"comprehension_score"`
	FluencyRating      string   `json:"fluency_rating" binding:"omitempty"`
	AccuracyScore      *float64 `json:"accuracy_score"`
	Notes              string   `json:"notes"`
}

// AssessmentResponse represents response for assessment
type AssessmentResponse struct {
	ID                 string  `json:"id"`
	StudentID          string  `json:"student_id"`
	ReadingLevelID     string  `json:"reading_level_id"`
	AssessmentDate     string  `json:"assessment_date"`
	WordsPerMinute     int     `json:"words_per_minute"`
	ComprehensionScore float64 `json:"comprehension_score"`
	FluencyRating      string  `json:"fluency_rating"`
	AccuracyScore      float64 `json:"accuracy_score"`
	Notes              string  `json:"notes"`
	TeacherID          string  `json:"teacher_id"`
	CreatedAt          string  `json:"created_at"`
	UpdatedAt          string  `json:"updated_at"`
}

// StudentProgressionResponse represents student's reading literacy progression
type StudentProgressionResponse struct {
	StudentID            string               `json:"student_id"`
	StudentName          string               `json:"student_name"`
	Assessments          []AssessmentResponse `json:"assessments"`
	CurrentLevel         ReadingLevelResponse `json:"current_level"`
	ProgressionHistory   []LevelProgress      `json:"progression_history"`
	AverageWPM           int                  `json:"average_wpm"`
	AverageComprehension float64              `json:"average_comprehension"`
	AverageAccuracy      float64              `json:"average_accuracy"`
	FluencyDistribution  map[string]int       `json:"fluency_distribution"`
}

// LevelProgress represents progress through reading levels
type LevelProgress struct {
	ReadingLevelID string `json:"reading_level_id"`
	LevelName      string `json:"level_name"`
	LevelCode      string `json:"level_code"`
	AchievedDate   string `json:"achieved_date"`
	DurationDays   int    `json:"duration_days"`
}

// ClassroomOverviewResponse represents reading literacy overview for a classroom
type ClassroomOverviewResponse struct {
	ClassroomID            string         `json:"classroom_id"`
	ClassroomName          string         `json:"classroom_name"`
	StudentCount           int            `json:"student_count"`
	LevelDistribution      map[string]int `json:"level_distribution"`
	AverageWPM             int            `json:"average_wpm"`
	AverageComprehension   float64        `json:"average_comprehension"`
	StudentsNeedingSupport []StudentNeeds `json:"students_needing_support"`
}

// StudentNeeds represents students who need additional support
type StudentNeeds struct {
	StudentID          string  `json:"student_id"`
	StudentName        string  `json:"student_name"`
	CurrentLevel       string  `json:"current_level"`
	WordsPerMinute     int     `json:"words_per_minute"`
	ComprehensionScore float64 `json:"comprehension_score"`
	Recommendations    string  `json:"recommendations"`
}

// ReadingLevelsResponse represents response for list of reading levels
type ReadingLevelsResponse struct {
	Levels []ReadingLevelResponse `json:"levels"`
	Total  int                    `json:"total"`
}

// AssessmentsResponse represents response for list of assessments
type AssessmentsResponse struct {
	Assessments []AssessmentResponse `json:"assessments"`
	Total       int                  `json:"total"`
}
