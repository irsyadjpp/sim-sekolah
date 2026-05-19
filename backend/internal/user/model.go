package user

// Request DTOs
type UpdateUserStatusRequest struct {
	IsEnabled             *bool `json:"is_enabled"`
	AccountNonLocked      *bool `json:"account_non_locked"`
	AccountNonExpired     *bool `json:"account_non_expired"`
	CredentialsNonExpired *bool `json:"credentials_non_expired"`
}

type AssignRoleRequest struct {
	RoleNames []string `json:"role_names" validate:"required,min=1"`
}

type ResetPasswordRequest struct {
	NewPassword string `json:"new_password" validate:"required,min=6"`
}
