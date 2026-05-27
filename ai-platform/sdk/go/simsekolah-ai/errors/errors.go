package errors

import (
	"fmt"
	"net/http"
)

// ErrorCode represents different types of SDK errors
type ErrorCode string

const (
	// Connection errors
	ErrCodeConnectionFailed ErrorCode = "CONNECTION_FAILED"
	ErrCodeTimeout           ErrorCode = "TIMEOUT"
	ErrCodeServiceUnavailable ErrorCode = "SERVICE_UNAVAILABLE"
	
	// Authentication errors
	ErrCodeUnauthorized     ErrorCode = "UNAUTHORIZED"
	ErrCodeInvalidToken     ErrorCode = "INVALID_TOKEN"
	ErrCodeExpiredToken     ErrorCode = "EXPIRED_TOKEN"
	
	// Validation errors
	ErrCodeInvalidRequest   ErrorCode = "INVALID_REQUEST"
	ErrCodeMissingParameter ErrorCode = "MISSING_PARAMETER"
	ErrCodeInvalidParameter ErrorCode = "INVALID_PARAMETER"
	
	// Business logic errors
	ErrCodeNotFound         ErrorCode = "NOT_FOUND"
	ErrCodeAlreadyExists    ErrorCode = "ALREADY_EXISTS"
	ErrCodeConflict         ErrorCode = "CONFLICT"
	
	// Rate limiting
	ErrCodeRateLimited      ErrorCode = "RATE_LIMITED"
	
	// Internal errors
	ErrCodeInternalError    ErrorCode = "INTERNAL_ERROR"
	ErrCodeUnknownError     ErrorCode = "UNKNOWN_ERROR"
)

// SDKError represents an error returned by the SDK
type SDKError struct {
	Code       ErrorCode
	Message    string
	StatusCode int
	Details    map[string]interface{}
	Cause      error
}

// Error implements the error interface
func (e *SDKError) Error() string {
	if e.Cause != nil {
		return fmt.Sprintf("[%s] %s: %v", e.Code, e.Message, e.Cause)
	}
	return fmt.Sprintf("[%s] %s", e.Code, e.Message)
}

// Unwrap returns the underlying cause
func (e *SDKError) Unwrap() error {
	return e.Cause
}

// NewError creates a new SDKError
func NewError(code ErrorCode, message string) *SDKError {
	return &SDKError{
		Code:    code,
		Message: message,
	}
}

// NewErrorWithCause creates a new SDKError with a cause
func NewErrorWithCause(code ErrorCode, message string, cause error) *SDKError {
	return &SDKError{
		Code:    code,
		Message: message,
		Cause:   cause,
	}
}

// NewErrorWithStatus creates a new SDKError with HTTP status code
func NewErrorWithStatus(code ErrorCode, message string, statusCode int) *SDKError {
	return &SDKError{
		Code:       code,
		Message:    message,
		StatusCode: statusCode,
	}
}

// WithDetails adds details to the error
func (e *SDKError) WithDetails(details map[string]interface{}) *SDKError {
	e.Details = details
	return e
}

// Predefined error constructors
func NewConnectionError(message string, cause error) *SDKError {
	return NewErrorWithCause(ErrCodeConnectionFailed, message, cause).WithStatus(http.StatusServiceUnavailable)
}

func NewTimeoutError(message string) *SDKError {
	return NewError(ErrCodeTimeout, message).WithStatus(http.StatusRequestTimeout)
}

func NewUnauthorizedError(message string) *SDKError {
	return NewError(ErrCodeUnauthorized, message).WithStatus(http.StatusUnauthorized)
}

func NewInvalidTokenError(message string) *SDKError {
	return NewError(ErrCodeInvalidToken, message).WithStatus(http.StatusUnauthorized)
}

func NewInvalidRequestError(message string, details map[string]interface{}) *SDKError {
	return NewError(ErrCodeInvalidRequest, message).WithDetails(details).WithStatus(http.StatusBadRequest)
}

func NewNotFoundError(message string) *SDKError {
	return NewError(ErrCodeNotFound, message).WithStatus(http.StatusNotFound)
}

func NewAlreadyExistsError(message string) *SDKError {
	return NewError(ErrCodeAlreadyExists, message).WithStatus(http.StatusConflict)
}

func NewConflictError(message string) *SDKError {
	return NewError(ErrCodeConflict, message).WithStatus(http.StatusConflict)
}

func NewRateLimitedError(message string) *SDKError {
	return NewError(ErrCodeRateLimited, message).WithStatus(http.StatusTooManyRequests)
}

func NewInternalError(message string, cause error) *SDKError {
	return NewErrorWithCause(ErrCodeInternalError, message, cause).WithStatus(http.StatusInternalServerError)
}

// WithStatus sets the HTTP status code
func (e *SDKError) WithStatus(statusCode int) *SDKError {
	e.StatusCode = statusCode
	return e
}

// IsConnectionError checks if error is a connection error
func IsConnectionError(err error) bool {
	if sdkErr, ok := err.(*SDKError); ok {
		return sdkErr.Code == ErrCodeConnectionFailed || 
		       sdkErr.Code == ErrCodeServiceUnavailable
	}
	return false
}

// IsTimeoutError checks if error is a timeout error
func IsTimeoutError(err error) bool {
	if sdkErr, ok := err.(*SDKError); ok {
		return sdkErr.Code == ErrCodeTimeout
	}
	return false
}

// IsAuthError checks if error is an authentication error
func IsAuthError(err error) bool {
	if sdkErr, ok := err.(*SDKError); ok {
		return sdkErr.Code == ErrCodeUnauthorized || 
		       sdkErr.Code == ErrCodeInvalidToken || 
		       sdkErr.Code == ErrCodeExpiredToken
	}
	return false
}

// IsRetryable checks if error is retryable
func IsRetryable(err error) bool {
	if sdkErr, ok := err.(*SDKError); ok {
		return sdkErr.Code == ErrCodeConnectionFailed || 
		       sdkErr.Code == ErrCodeTimeout || 
		       sdkErr.Code == ErrCodeServiceUnavailable
	}
	return false
}