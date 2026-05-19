package classroom

type CreateClassroomRequest struct {
	SchoolID             string `json:"school_id" validate:"required,uuid"`
	AcademicYearID       string `json:"academic_year_id" validate:"required,uuid"`
	GradeID              string `json:"grade_id" validate:"required,uuid"`
	PhaseID              string `json:"phase_id" validate:"required,uuid"`
	ClassroomName        string `json:"classroom_name" validate:"required,max=50"`
	HomeroomTeacherID    string `json:"homeroom_teacher_id" validate:"omitempty,uuid"`
	MaxQuota             int    `json:"max_quota"`
	ClassCharacteristics string `json:"class_characteristics"`
}

type UpdateClassroomRequest struct {
	GradeID              string `json:"grade_id" validate:"omitempty,uuid"`
	PhaseID              string `json:"phase_id" validate:"omitempty,uuid"`
	ClassroomName        string `json:"classroom_name" validate:"omitempty,max=50"`
	HomeroomTeacherID    string `json:"homeroom_teacher_id" validate:"omitempty,uuid"`
	MaxQuota             int    `json:"max_quota"`
	ClassCharacteristics string `json:"class_characteristics"`
}
