package teaching_assignment

type CreateTeachingAssignmentRequest struct {
	ClassroomID string `json:"classroom_id" validate:"required,uuid"`
	TeacherID   string `json:"teacher_id" validate:"required,uuid"`
	SubjectID   string `json:"subject_id" validate:"required,uuid"`
}

type UpdateTeachingAssignmentRequest struct {
	TeacherID string `json:"teacher_id" validate:"omitempty,uuid"`
	SubjectID string `json:"subject_id" validate:"omitempty,uuid"`
}
