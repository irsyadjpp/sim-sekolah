package olah_aspect

// CreateOlahAspectRequest is the request body for creating a new olah aspect
type CreateOlahAspectRequest struct {
	AspectCode string `json:"aspect_code" validate:"required,max=20"`
	AspectName string `json:"aspect_name" validate:"required,max=100"`
	Definition string `json:"definition" validate:"required,max=500"`
	Indicators string `json:"indicators" validate:"required"` // JSON array of indicators
}

// UpdateOlahAspectRequest is the request body for updating an olah aspect
// All fields are optional (partial update)
type UpdateOlahAspectRequest struct {
	AspectCode string `json:"aspect_code" validate:"omitempty,max=20"`
	AspectName string `json:"aspect_name" validate:"omitempty,max=100"`
	Definition string `json:"definition" validate:"omitempty,max=500"`
	Indicators string `json:"indicators"`
	IsActive   *bool  `json:"is_active"`
}
