package common

import (
	"strconv"

	"github.com/gofiber/fiber/v2"
)

type Pagination struct {
	Page   int
	Limit  int
	Offset int
}

func GetPagination(c *fiber.Ctx) Pagination {

	page, _ := strconv.Atoi(c.Query("page", "1"))
	limit, _ := strconv.Atoi(c.Query("limit", "10"))

	if page < 1 {
		page = 1
	}

	if limit < 1 {
		limit = 10
	}

	offset := (page - 1) * limit

	return Pagination{
		Page:   page,
		Limit:  limit,
		Offset: offset,
	}
}
