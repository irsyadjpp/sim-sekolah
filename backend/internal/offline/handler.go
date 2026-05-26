package offline

import (
	"strconv"

	"github.com/gofiber/fiber/v2"
	"github.com/google/uuid"
)

type Handler interface {
	// SyncState routes
	CreateSyncState(c *fiber.Ctx) error
	GetSyncStateByID(c *fiber.Ctx) error
	GetSyncStatesByEntity(c *fiber.Ctx) error
	GetSyncStatesByDevice(c *fiber.Ctx) error
	GetSyncStatesByUser(c *fiber.Ctx) error
	GetPendingSyncStates(c *fiber.Ctx) error
	UpdateSyncState(c *fiber.Ctx) error
	DeleteSyncState(c *fiber.Ctx) error

	// ConflictResolution routes
	CreateConflictResolution(c *fiber.Ctx) error
	GetConflictResolutionByID(c *fiber.Ctx) error
	GetConflictsByEntity(c *fiber.Ctx) error
	GetPendingConflicts(c *fiber.Ctx) error
	UpdateConflictResolution(c *fiber.Ctx) error
	DeleteConflictResolution(c *fiber.Ctx) error

	// Sync operations
	SyncPending(c *fiber.Ctx) error
	GetSyncStatistics(c *fiber.Ctx) error
	GetConflictStatistics(c *fiber.Ctx) error

	// Route registration
	RegisterRoutes(group fiber.Router)
}

type handler struct {
	service Service
}

func NewHandler(service Service) Handler {
	return &handler{service: service}
}

// SyncState handlers
func (h *handler) CreateSyncState(c *fiber.Ctx) error {
	var request SyncStateRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.CreateSyncState(request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusCreated).JSON(response)
}

func (h *handler) GetSyncStateByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid sync state ID"})
	}

	response, err := h.service.GetSyncStateByID(id)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "Sync state not found"})
	}

	return c.JSON(response)
}

func (h *handler) GetSyncStatesByEntity(c *fiber.Ctx) error {
	entityType := c.Query("entity_type")
	entityID := c.Query("entity_id")

	if entityType == "" || entityID == "" {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "entity_type and entity_id are required"})
	}

	response, err := h.service.GetSyncStatesByEntity(entityType, entityID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) GetSyncStatesByDevice(c *fiber.Ctx) error {
	deviceID := c.Query("device_id")
	if deviceID == "" {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "device_id is required"})
	}

	response, err := h.service.GetSyncStatesByDevice(deviceID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) GetSyncStatesByUser(c *fiber.Ctx) error {
	userID := c.Query("user_id")
	if userID == "" {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "user_id is required"})
	}

	response, err := h.service.GetSyncStatesByUser(userID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) GetPendingSyncStates(c *fiber.Ctx) error {
	limit := 0
	if limitStr := c.Query("limit"); limitStr != "" {
		if l, err := strconv.Atoi(limitStr); err == nil {
			limit = l
		}
	}

	response, err := h.service.GetPendingSyncStates(limit)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) UpdateSyncState(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid sync state ID"})
	}

	var request SyncStateRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.UpdateSyncState(id, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) DeleteSyncState(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid sync state ID"})
	}

	err = h.service.DeleteSyncState(id)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(fiber.Map{"message": "Sync state deleted successfully"})
}

// ConflictResolution handlers
func (h *handler) CreateConflictResolution(c *fiber.Ctx) error {
	var request ConflictResolutionRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.CreateConflictResolution(request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusCreated).JSON(response)
}

func (h *handler) GetConflictResolutionByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid conflict resolution ID"})
	}

	response, err := h.service.GetConflictResolutionByID(id)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "Conflict resolution not found"})
	}

	return c.JSON(response)
}

func (h *handler) GetConflictsByEntity(c *fiber.Ctx) error {
	entityType := c.Query("entity_type")
	entityID := c.Query("entity_id")

	if entityType == "" || entityID == "" {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "entity_type and entity_id are required"})
	}

	response, err := h.service.GetConflictsByEntity(entityType, entityID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) GetPendingConflicts(c *fiber.Ctx) error {
	limit := 0
	if limitStr := c.Query("limit"); limitStr != "" {
		if l, err := strconv.Atoi(limitStr); err == nil {
			limit = l
		}
	}

	response, err := h.service.GetPendingConflicts(limit)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) UpdateConflictResolution(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid conflict resolution ID"})
	}

	var request ConflictResolutionRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.UpdateConflictResolution(id, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) DeleteConflictResolution(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid conflict resolution ID"})
	}

	err = h.service.DeleteConflictResolution(id)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(fiber.Map{"message": "Conflict resolution deleted successfully"})
}

// Sync operations handlers
func (h *handler) SyncPending(c *fiber.Ctx) error {
	var request SyncRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.SyncPending(request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) GetSyncStatistics(c *fiber.Ctx) error {
	response, err := h.service.GetSyncStatistics()
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) GetConflictStatistics(c *fiber.Ctx) error {
	response, err := h.service.GetConflictStatistics()
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) RegisterRoutes(group fiber.Router) {
	// SyncState routes
	syncStates := group.Group("/offline/sync-states")
	syncStates.Post("/", h.CreateSyncState)
	syncStates.Get("/:id", h.GetSyncStateByID)
	syncStates.Get("/", h.GetSyncStatesByEntity)
	syncStates.Get("/device/:device_id", h.GetSyncStatesByDevice)
	syncStates.Get("/user/:user_id", h.GetSyncStatesByUser)
	syncStates.Get("/pending", h.GetPendingSyncStates)
	syncStates.Put("/:id", h.UpdateSyncState)
	syncStates.Delete("/:id", h.DeleteSyncState)

	// ConflictResolution routes
	conflicts := group.Group("/offline/conflicts")
	conflicts.Post("/", h.CreateConflictResolution)
	conflicts.Get("/:id", h.GetConflictResolutionByID)
	conflicts.Get("/", h.GetConflictsByEntity)
	conflicts.Get("/pending", h.GetPendingConflicts)
	conflicts.Put("/:id", h.UpdateConflictResolution)
	conflicts.Delete("/:id", h.DeleteConflictResolution)

	// Sync operations
	sync := group.Group("/offline/sync")
	sync.Post("/pending", h.SyncPending)
	sync.Get("/statistics", h.GetSyncStatistics)
	sync.Get("/conflicts/statistics", h.GetConflictStatistics)
}
