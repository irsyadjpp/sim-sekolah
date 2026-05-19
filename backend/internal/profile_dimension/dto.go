package profile_dimension

type CreateProfileDimensionRequest struct {
	DimensionCode string `json:"dimension_code" validate:"required"`
	DimensionName string `json:"dimension_name" validate:"required"`
	Description   string `json:"description"`
	IsActive      *bool  `json:"is_active"`
}

type UpdateProfileDimensionRequest struct {
	DimensionCode string `json:"dimension_code"`
	DimensionName string `json:"dimension_name"`
	Description   string `json:"description"`
	IsActive      *bool  `json:"is_active"`
}
