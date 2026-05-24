package elemen_desain

// CreateDesignElementRequest represents the request body for creating a new design element
type CreateDesignElementRequest struct {
	Name                 string `json:"design_element_name" binding:"required,min=3,max=255"`
	Description          string `json:"description" binding:"max=1000"`
	FrameworkElementType string `json:"framework_element_type" binding:"required"`
	IsActive             *bool  `json:"is_active"`
}

// UpdateDesignElementRequest represents the request body for updating a design element
type UpdateDesignElementRequest struct {
	Name                 string `json:"design_element_name" binding:"omitempty,min=3,max=255"`
	Description          string `json:"description" binding:"omitempty,max=1000"`
	FrameworkElementType string `json:"framework_element_type" binding:"omitempty"`
	IsActive             *bool  `json:"is_active"`
}

// DesignElementResponse represents the response structure for a design element
type DesignElementResponse struct {
	ID                   string `json:"id"`
	Name                 string `json:"design_element_name"`
	Description          string `json:"description"`
	FrameworkElementType string `json:"framework_element_type"`
	IsActive             bool   `json:"is_active"`
	CreatedAt            string `json:"created_at"`
	UpdatedAt            string `json:"updated_at"`
}

// DesignElementListResponse represents the response structure for a list of design elements
type DesignElementListResponse struct {
	Elements []DesignElementResponse `json:"elements"`
	Total    int                     `json:"total"`
}

// FrameworkGroupResponse represents a group of design elements organized by framework type
type FrameworkGroupResponse struct {
	FrameworkType string                  `json:"framework_type"`
	FrameworkName string                  `json:"framework_name"`
	Elements      []DesignElementResponse `json:"elements"`
	ElementCount  int                     `json:"element_count"`
}

// FrameworkGroupsResponse represents the response structure for all framework groups
type FrameworkGroupsResponse struct {
	Groups []FrameworkGroupResponse `json:"groups"`
}
