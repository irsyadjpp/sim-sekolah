package learning_principle

// CreateLearningPrincipleRequest is the request body for creating a new learning principle
type CreateLearningPrincipleRequest struct {
	PrincipleCode          string `json:"principle_code" validate:"required,max=30"`
	PrincipleName          string `json:"principle_name" validate:"required,max=100"`
	Description            string `json:"description" validate:"required,max=500"`
	KeyCharacteristics     string `json:"key_characteristics" validate:"required"`     // JSON array
	ImplementationExamples string `json:"implementation_examples" validate:"required"` // JSON array
}

// UpdateLearningPrincipleRequest is the request body for updating a learning principle
// All fields are optional (partial update)
type UpdateLearningPrincipleRequest struct {
	PrincipleCode          string `json:"principle_code" validate:"omitempty,max=30"`
	PrincipleName          string `json:"principle_name" validate:"omitempty,max=100"`
	Description            string `json:"description" validate:"omitempty,max=500"`
	KeyCharacteristics     string `json:"key_characteristics"`
	ImplementationExamples string `json:"implementation_examples"`
	IsActive               *bool  `json:"is_active"`
}
