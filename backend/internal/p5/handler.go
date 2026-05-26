package p5

import (
	"strconv"

	"github.com/gofiber/fiber/v2"
	"github.com/google/uuid"
)

type Handler interface {
	// Project routes
	CreateProject(c *fiber.Ctx) error
	GetProjectByID(c *fiber.Ctx) error
	GetProjects(c *fiber.Ctx) error
	UpdateProject(c *fiber.Ctx) error
	DeleteProject(c *fiber.Ctx) error
	UpdateProjectProgress(c *fiber.Ctx) error

	// Team routes
	CreateTeam(c *fiber.Ctx) error
	GetTeamByID(c *fiber.Ctx) error
	GetTeamsByProject(c *fiber.Ctx) error
	UpdateTeam(c *fiber.Ctx) error
	DeleteTeam(c *fiber.Ctx) error
	AutoGenerateTeams(c *fiber.Ctx) error

	// Team Member routes
	AddTeamMember(c *fiber.Ctx) error
	GetTeamMembers(c *fiber.Ctx) error
	UpdateTeamMember(c *fiber.Ctx) error
	RemoveTeamMember(c *fiber.Ctx) error

	// Milestone routes
	CreateMilestone(c *fiber.Ctx) error
	GetMilestoneByID(c *fiber.Ctx) error
	GetMilestonesByProject(c *fiber.Ctx) error
	UpdateMilestone(c *fiber.Ctx) error
	DeleteMilestone(c *fiber.Ctx) error
	UpdateMilestoneProgress(c *fiber.Ctx) error

	// Participation routes
	CreateParticipation(c *fiber.Ctx) error
	GetParticipationByID(c *fiber.Ctx) error
	GetParticipationsByProject(c *fiber.Ctx) error
	UpdateParticipation(c *fiber.Ctx) error
	DeleteParticipation(c *fiber.Ctx) error
	RecordFinalAssessment(c *fiber.Ctx) error

	// Route registration
	RegisterRoutes(group fiber.Router)
}

type handler struct {
	service Service
}

func NewHandler(service Service) Handler {
	return &handler{service: service}
}

// Project handlers
func (h *handler) CreateProject(c *fiber.Ctx) error {
	var req CreateProjectRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	project, err := h.service.CreateProject(c.Context(), req)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusCreated).JSON(project)
}

func (h *handler) GetProjectByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid project ID"})
	}

	project, err := h.service.GetProjectByID(id)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "Project not found"})
	}

	return c.JSON(project)
}

func (h *handler) GetProjects(c *fiber.Ctx) error {
	filter := make(map[string]interface{})

	if subjectID := c.Query("subject_id"); subjectID != "" {
		filter["subject_id"] = subjectID
	}
	if classroomID := c.Query("classroom_id"); classroomID != "" {
		filter["classroom_id"] = classroomID
	}
	if status := c.Query("status"); status != "" {
		filter["status"] = status
	}
	if academicYearID := c.Query("academic_year_id"); academicYearID != "" {
		filter["academic_year_id"] = academicYearID
	}
	if semester := c.Query("semester"); semester != "" {
		if sem, err := strconv.Atoi(semester); err == nil {
			filter["semester"] = sem
		}
	}

	projects, err := h.service.GetProjects(filter)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(projects)
}

func (h *handler) UpdateProject(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid project ID"})
	}

	var req UpdateProjectRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	project, err := h.service.UpdateProject(c.Context(), id, req)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(project)
}

func (h *handler) DeleteProject(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid project ID"})
	}

	if err := h.service.DeleteProject(c.Context(), id); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusNoContent).Send(nil)
}

func (h *handler) UpdateProjectProgress(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid project ID"})
	}

	if err := h.service.UpdateProjectProgress(c.Context(), id); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(fiber.Map{"message": "Progress updated successfully"})
}

// Team handlers
func (h *handler) CreateTeam(c *fiber.Ctx) error {
	var req CreateTeamRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	team, err := h.service.CreateTeam(c.Context(), req)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusCreated).JSON(team)
}

func (h *handler) GetTeamByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid team ID"})
	}

	team, err := h.service.GetTeamByID(id)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "Team not found"})
	}

	return c.JSON(team)
}

func (h *handler) GetTeamsByProject(c *fiber.Ctx) error {
	projectID, err := uuid.Parse(c.Params("project_id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid project ID"})
	}

	teams, err := h.service.GetTeamsByProject(projectID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(teams)
}

func (h *handler) UpdateTeam(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid team ID"})
	}

	var req UpdateTeamRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	team, err := h.service.UpdateTeam(c.Context(), id, req)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(team)
}

func (h *handler) DeleteTeam(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid team ID"})
	}

	if err := h.service.DeleteTeam(c.Context(), id); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusNoContent).Send(nil)
}

func (h *handler) AutoGenerateTeams(c *fiber.Ctx) error {
	var req AutoGenerateTeamsRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	teams, err := h.service.AutoGenerateTeams(c.Context(), req)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusCreated).JSON(teams)
}

// Team Member handlers
func (h *handler) AddTeamMember(c *fiber.Ctx) error {
	teamID, err := uuid.Parse(c.Params("team_id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid team ID"})
	}

	var req CreateTeamMemberRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	member, err := h.service.AddTeamMember(c.Context(), teamID, req)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusCreated).JSON(member)
}

func (h *handler) GetTeamMembers(c *fiber.Ctx) error {
	teamID, err := uuid.Parse(c.Params("team_id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid team ID"})
	}

	members, err := h.service.GetTeamMembers(teamID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(members)
}

func (h *handler) UpdateTeamMember(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid member ID"})
	}

	var req UpdateTeamMemberRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	member, err := h.service.UpdateTeamMember(c.Context(), id, req)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(member)
}

func (h *handler) RemoveTeamMember(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid member ID"})
	}

	if err := h.service.RemoveTeamMember(c.Context(), id); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusNoContent).Send(nil)
}

// Milestone handlers
func (h *handler) CreateMilestone(c *fiber.Ctx) error {
	projectID, err := uuid.Parse(c.Params("project_id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid project ID"})
	}

	var req CreateMilestoneRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	milestone, err := h.service.CreateMilestone(c.Context(), projectID, req)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusCreated).JSON(milestone)
}

func (h *handler) GetMilestoneByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid milestone ID"})
	}

	milestone, err := h.service.GetMilestoneByID(id)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "Milestone not found"})
	}

	return c.JSON(milestone)
}

func (h *handler) GetMilestonesByProject(c *fiber.Ctx) error {
	projectID, err := uuid.Parse(c.Params("project_id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid project ID"})
	}

	milestones, err := h.service.GetMilestonesByProject(projectID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(milestones)
}

func (h *handler) UpdateMilestone(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid milestone ID"})
	}

	var req UpdateMilestoneRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	milestone, err := h.service.UpdateMilestone(c.Context(), id, req)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(milestone)
}

func (h *handler) DeleteMilestone(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid milestone ID"})
	}

	if err := h.service.DeleteMilestone(c.Context(), id); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusNoContent).Send(nil)
}

func (h *handler) UpdateMilestoneProgress(c *fiber.Ctx) error {
	projectID, err := uuid.Parse(c.Params("project_id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid project ID"})
	}

	if err := h.service.UpdateMilestoneProgress(c.Context(), projectID); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(fiber.Map{"message": "Milestone progress updated successfully"})
}

// Participation handlers
func (h *handler) CreateParticipation(c *fiber.Ctx) error {
	var req CreateParticipationRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	participation, err := h.service.CreateParticipation(c.Context(), req)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusCreated).JSON(participation)
}

func (h *handler) GetParticipationByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid participation ID"})
	}

	participation, err := h.service.GetParticipationByID(id)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "Participation not found"})
	}

	return c.JSON(participation)
}

func (h *handler) GetParticipationsByProject(c *fiber.Ctx) error {
	projectID, err := uuid.Parse(c.Params("project_id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid project ID"})
	}

	participations, err := h.service.GetParticipationsByProject(projectID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(participations)
}

func (h *handler) UpdateParticipation(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid participation ID"})
	}

	var req UpdateParticipationRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	participation, err := h.service.UpdateParticipation(c.Context(), id, req)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(participation)
}

func (h *handler) DeleteParticipation(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid participation ID"})
	}

	if err := h.service.DeleteParticipation(c.Context(), id); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusNoContent).Send(nil)
}

func (h *handler) RecordFinalAssessment(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid participation ID"})
	}

	var req struct {
		FinalScore      float64 `json:"final_score" validate:"required,min=0,max=100"`
		Grade           string  `json:"grade" validate:"required"`
		TeacherFeedback string  `json:"teacher_feedback" validate:"required"`
	}
	if err := c.BodyParser(&req); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	if err := h.service.RecordFinalAssessment(c.Context(), id, req.FinalScore, req.Grade, req.TeacherFeedback); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(fiber.Map{"message": "Final assessment recorded successfully"})
}

func (h *handler) RegisterRoutes(group fiber.Router) {
	projects := group.Group("/projects")
	{
		projects.Post("", h.CreateProject)
		projects.Get("", h.GetProjects)
		projects.Get("/:id", h.GetProjectByID)
		projects.Put("/:id", h.UpdateProject)
		projects.Delete("/:id", h.DeleteProject)
		projects.Put("/:id/progress", h.UpdateProjectProgress)

		// Team routes nested under project
		projects.Get("/:project_id/teams", h.GetTeamsByProject)
		projects.Post("/:project_id/teams", h.CreateTeam)
		projects.Post("/:project_id/teams/auto-generate", h.AutoGenerateTeams)

		// Milestone routes nested under project
		projects.Get("/:project_id/milestones", h.GetMilestonesByProject)
		projects.Post("/:project_id/milestones", h.CreateMilestone)
		projects.Put("/:project_id/milestones/progress", h.UpdateMilestoneProgress)

		// Participation routes nested under project
		projects.Get("/:project_id/participations", h.GetParticipationsByProject)
	}

	teams := group.Group("/teams")
	{
		teams.Get("/:id", h.GetTeamByID)
		teams.Put("/:id", h.UpdateTeam)
		teams.Delete("/:id", h.DeleteTeam)

		// Team member routes nested under team
		teams.Get("/:team_id/members", h.GetTeamMembers)
		teams.Post("/:team_id/members", h.AddTeamMember)
	}

	members := group.Group("/team-members")
	{
		members.Put("/:id", h.UpdateTeamMember)
		members.Delete("/:id", h.RemoveTeamMember)
	}

	milestones := group.Group("/milestones")
	{
		milestones.Get("/:id", h.GetMilestoneByID)
		milestones.Put("/:id", h.UpdateMilestone)
		milestones.Delete("/:id", h.DeleteMilestone)
	}

	participations := group.Group("/participations")
	{
		participations.Post("", h.CreateParticipation)
		participations.Get("/:id", h.GetParticipationByID)
		participations.Put("/:id", h.UpdateParticipation)
		participations.Delete("/:id", h.DeleteParticipation)
		participations.Post("/:id/final-assessment", h.RecordFinalAssessment)
	}
}
