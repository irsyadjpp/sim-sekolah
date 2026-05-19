package common

import "github.com/gofiber/fiber/v2"

type Response struct {
	Status  string      `json:"status"`
	Message string      `json:"message"`
	Data    interface{} `json:"data,omitempty"`
	Error   interface{} `json:"error,omitempty"`
}

type PaginationResponse struct {
	Status     string      `json:"status"`
	Message    string      `json:"message"`
	Data       interface{} `json:"data"`
	Page       int         `json:"page"`
	Limit      int         `json:"limit"`
	TotalRows  int64       `json:"total_rows"`
	TotalPages int         `json:"total_pages"`
}

func Success(c *fiber.Ctx, message string, data interface{}) error {
	return c.Status(fiber.StatusOK).JSON(Response{
		Status:  "success",
		Message: message,
		Data:    data,
	})
}

func Created(c *fiber.Ctx, message string, data interface{}) error {
	return c.Status(fiber.StatusCreated).JSON(Response{
		Status:  "success",
		Message: message,
		Data:    data,
	})
}

func Error(c *fiber.Ctx, code int, message string, err interface{}) error {
	return c.Status(code).JSON(Response{
		Status:  "error",
		Message: message,
		Error:   err,
	})
}

func Paginated(
	c *fiber.Ctx,
	message string,
	data interface{},
	page int,
	limit int,
	totalRows int64,
) error {

	totalPages := int((totalRows + int64(limit) - 1) / int64(limit))

	return c.Status(fiber.StatusOK).JSON(PaginationResponse{
		Status:     "success",
		Message:    message,
		Data:       data,
		Page:       page,
		Limit:      limit,
		TotalRows:  totalRows,
		TotalPages: totalPages,
	})
}
