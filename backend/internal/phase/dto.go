package phase

// CreatePhaseRequest adalah request body untuk membuat fase baru.
type CreatePhaseRequest struct {
	Code        string `json:"code"        validate:"required,max=5"`
	Name        string `json:"name"        validate:"required,max=50"`
	Description string `json:"description"`
}

// UpdatePhaseRequest adalah request body untuk memperbarui fase.
// Semua field bersifat opsional (partial update).
type UpdatePhaseRequest struct {
	Code        string `json:"code"        validate:"omitempty,max=5"`
	Name        string `json:"name"        validate:"omitempty,max=50"`
	Description string `json:"description"`
}
