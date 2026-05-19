package local_context

// CreateCategoryRequest adalah request body untuk membuat kategori konteks lokal.
type CreateCategoryRequest struct {
	CategoryCode string `json:"category_code" validate:"required,max=50"`
	CategoryName string `json:"category_name" validate:"required,max=100"`
	Description  string `json:"description"`
}

// CreateContextRequest adalah request body untuk membuat data konteks lokal.
type CreateContextRequest struct {
	CategoryID  string `json:"category_id" validate:"required,uuid"`
	Title       string `json:"title"       validate:"required,max=200"`
	Description string `json:"description"`
	Location    string `json:"location"    validate:"max=255"`
	ScopeType   string `json:"scope_type"  validate:"required,oneof=SCHOOL VILLAGE CLASS STUDENT"`
	IsActive    *bool  `json:"is_active"   validate:"omitempty"`
}

// UpdateContextRequest adalah request body untuk memperbarui data konteks lokal.
type UpdateContextRequest struct {
	CategoryID  string `json:"category_id" validate:"omitempty,uuid"`
	Title       string `json:"title"       validate:"omitempty,max=200"`
	Description string `json:"description"`
	Location    string `json:"location"    validate:"omitempty,max=255"`
	ScopeType   string `json:"scope_type"  validate:"omitempty,oneof=SCHOOL VILLAGE CLASS STUDENT"`
	IsActive    *bool  `json:"is_active"   validate:"omitempty"`
}
