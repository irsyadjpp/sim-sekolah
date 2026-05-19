package report

type GenerateReportRequest struct {
	Semester string `json:"semester" validate:"required,oneof=Ganjil Genap"`
}

type UpsertReportNotesRequest struct {
	HomeroomNotes     string `json:"homeroom_notes"`
	StudentReflection string `json:"student_reflection"`
}

type UpsertReportScoreRequest struct {
	SubjectID                  string  `json:"subject_id" validate:"required,uuid"`
	FinalScore                 float64 `json:"final_score" validate:"min=0,max=100"`
	CompetencyAchieved         string  `json:"competency_achieved"`
	CompetencyNeedsImprovement string  `json:"competency_needs_improvement"`
}

type UpsertReportP5Request struct {
	Theme       string `json:"theme" validate:"required"`
	Description string `json:"description"`
	Predicate   string `json:"predicate"`
}

type UpsertReportDeepLearningRequest struct {
	Aspect           string `json:"aspect" validate:"required"`
	ObservationNotes string `json:"observation_notes"`
}

type UpsertReportExtracurricularRequest struct {
	ActivityName string `json:"activity_name" validate:"required"`
	Predicate    string `json:"predicate"`
	Description  string `json:"description"`
}

type UpsertReportAttendanceRequest struct {
	Sick       int `json:"sick" validate:"min=0"`
	Permission int `json:"permission" validate:"min=0"`
	Unexcused  int `json:"unexcused" validate:"min=0"`
}
