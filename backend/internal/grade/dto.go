package grade

type CreateGradeRequest struct {
	PhaseID    string `json:"phase_id" validate:"required,uuid"`
	GradeLevel int    `json:"grade_level" validate:"required,min=1,max=12"`
	GradeName  string `json:"grade_name" validate:"required,max=20"`
}

type UpdateGradeRequest struct {
	PhaseID    string `json:"phase_id" validate:"omitempty,uuid"`
	GradeLevel int    `json:"grade_level" validate:"omitempty,min=1,max=12"`
	GradeName  string `json:"grade_name" validate:"omitempty,max=20"`
}
