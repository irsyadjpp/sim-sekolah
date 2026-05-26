package intervention

import (
	"github.com/google/uuid"
)

type InterventionService interface {
	CreateRemedialProgram(request *RemedialProgramRequest) (*RemedialProgramResponse, error)
	GetRemedialProgramByID(id string) (*RemedialProgramResponse, error)
	GetAllRemedialPrograms() ([]RemedialProgramResponse, error)
	UpdateRemedialProgram(id string, request *RemedialProgramRequest) (*RemedialProgramResponse, error)
	DeleteRemedialProgram(id string) error

	CreateEnrichmentProgram(request *EnrichmentProgramRequest) (*EnrichmentProgramResponse, error)
	GetEnrichmentProgramByID(id string) (*EnrichmentProgramResponse, error)
	GetAllEnrichmentPrograms() ([]EnrichmentProgramResponse, error)
	UpdateEnrichmentProgram(id string, request *EnrichmentProgramRequest) (*EnrichmentProgramResponse, error)
	DeleteEnrichmentProgram(id string) error

	CreateStudentAssignment(request *StudentInterventionAssignmentRequest) (*StudentInterventionAssignmentResponse, error)
	GetStudentAssignmentByID(id string) (*StudentInterventionAssignmentResponse, error)
	GetAssignmentsByStudent(studentID string) ([]StudentInterventionAssignmentResponse, error)
	UpdateStudentAssignment(id string, request *StudentInterventionAssignmentRequest) (*StudentInterventionAssignmentResponse, error)
	DeleteStudentAssignment(id string) error

	GetInterventionSummary(schoolID string) (*InterventionSummaryResponse, error)
}

type interventionService struct {
	repo InterventionRepository
}

func NewInterventionService(repo InterventionRepository) InterventionService {
	return &interventionService{repo: repo}
}

func remedialToResponse(program *RemedialProgram) *RemedialProgramResponse {
	var subjectID *string
	if program.SubjectID != nil {
		subjID := program.SubjectID.String()
		subjectID = &subjID
	}

	return &RemedialProgramResponse{
		ID:              program.ID.String(),
		ProgramName:     program.ProgramName,
		SubjectID:       subjectID,
		TargetGrade:     program.TargetGrade,
		Description:     program.Description,
		LearningGaps:    program.LearningGaps,
		Strategies:      program.Strategies,
		Resources:       program.Resources,
		DurationWeeks:   program.DurationWeeks,
		SessionsPerWeek: program.SessionsPerWeek,
		SuccessCriteria: program.SuccessCriteria,
		IsActive:        program.IsActive,
		CreatedAt:       program.CreatedAt,
		UpdatedAt:       program.UpdatedAt,
	}
}

func enrichmentToResponse(program *EnrichmentProgram) *EnrichmentProgramResponse {
	var subjectID *string
	if program.SubjectID != nil {
		subjID := program.SubjectID.String()
		subjectID = &subjID
	}

	return &EnrichmentProgramResponse{
		ID:              program.ID.String(),
		ProgramName:     program.ProgramName,
		SubjectID:       subjectID,
		TargetGrade:     program.TargetGrade,
		Description:     program.Description,
		AdvancedTopics:  program.AdvancedTopics,
		Projects:        program.Projects,
		Resources:       program.Resources,
		DurationWeeks:   program.DurationWeeks,
		SessionsPerWeek: program.SessionsPerWeek,
		SuccessCriteria: program.SuccessCriteria,
		IsActive:        program.IsActive,
		CreatedAt:       program.CreatedAt,
		UpdatedAt:       program.UpdatedAt,
	}
}

func assignmentToResponse(assignment *StudentInterventionAssignment) *StudentInterventionAssignmentResponse {
	return &StudentInterventionAssignmentResponse{
		ID:               assignment.ID.String(),
		StudentID:        assignment.StudentID.String(),
		ProgramID:        assignment.ProgramID.String(),
		InterventionType: assignment.InterventionType,
		TeacherID:        assignment.TeacherID.String(),
		AssignmentDate:   assignment.AssignmentDate,
		StartDate:        assignment.StartDate,
		EndDate:          assignment.EndDate,
		Status:           assignment.Status,
		PriorityLevel:    assignment.PriorityLevel,
		BaselineScore:    assignment.BaselineScore,
		TargetScore:      assignment.TargetScore,
		CurrentScore:     assignment.CurrentScore,
		Progress:         assignment.Progress,
		CustomizedPlan:   assignment.CustomizedPlan,
		Notes:            assignment.Notes,
		CreatedAt:        assignment.CreatedAt,
		UpdatedAt:        assignment.UpdatedAt,
	}
}

// RemedialProgram operations
func (s *interventionService) CreateRemedialProgram(request *RemedialProgramRequest) (*RemedialProgramResponse, error) {
	var subjectID *uuid.UUID
	if request.SubjectID != nil {
		subjID := uuid.MustParse(*request.SubjectID)
		subjectID = &subjID
	}

	program := &RemedialProgram{
		ProgramName:     request.ProgramName,
		SubjectID:       subjectID,
		TargetGrade:     request.TargetGrade,
		Description:     request.Description,
		LearningGaps:    request.LearningGaps,
		Strategies:      request.Strategies,
		Resources:       request.Resources,
		DurationWeeks:   request.DurationWeeks,
		SessionsPerWeek: request.SessionsPerWeek,
		SuccessCriteria: request.SuccessCriteria,
		IsActive:        request.IsActive,
	}

	if err := s.repo.CreateRemedialProgram(program); err != nil {
		return nil, err
	}

	return remedialToResponse(program), nil
}

func (s *interventionService) GetRemedialProgramByID(id string) (*RemedialProgramResponse, error) {
	programID, err := uuid.Parse(id)
	if err != nil {
		return nil, err
	}

	program, err := s.repo.GetRemedialProgramByID(programID)
	if err != nil {
		return nil, err
	}

	return remedialToResponse(program), nil
}

func (s *interventionService) GetAllRemedialPrograms() ([]RemedialProgramResponse, error) {
	programs, err := s.repo.GetAllRemedialPrograms()
	if err != nil {
		return nil, err
	}

	responses := make([]RemedialProgramResponse, len(programs))
	for i, program := range programs {
		responses[i] = *remedialToResponse(&program)
	}

	return responses, nil
}

func (s *interventionService) UpdateRemedialProgram(id string, request *RemedialProgramRequest) (*RemedialProgramResponse, error) {
	programID, err := uuid.Parse(id)
	if err != nil {
		return nil, err
	}

	program, err := s.repo.GetRemedialProgramByID(programID)
	if err != nil {
		return nil, err
	}

	var subjectID *uuid.UUID
	if request.SubjectID != nil {
		subjID := uuid.MustParse(*request.SubjectID)
		subjectID = &subjID
	}

	program.ProgramName = request.ProgramName
	program.SubjectID = subjectID
	program.TargetGrade = request.TargetGrade
	program.Description = request.Description
	program.LearningGaps = request.LearningGaps
	program.Strategies = request.Strategies
	program.Resources = request.Resources
	program.DurationWeeks = request.DurationWeeks
	program.SessionsPerWeek = request.SessionsPerWeek
	program.SuccessCriteria = request.SuccessCriteria
	program.IsActive = request.IsActive

	if err := s.repo.UpdateRemedialProgram(program); err != nil {
		return nil, err
	}

	return remedialToResponse(program), nil
}

func (s *interventionService) DeleteRemedialProgram(id string) error {
	programID, err := uuid.Parse(id)
	if err != nil {
		return err
	}

	return s.repo.DeleteRemedialProgram(programID)
}

// EnrichmentProgram operations
func (s *interventionService) CreateEnrichmentProgram(request *EnrichmentProgramRequest) (*EnrichmentProgramResponse, error) {
	var subjectID *uuid.UUID
	if request.SubjectID != nil {
		subjID := uuid.MustParse(*request.SubjectID)
		subjectID = &subjID
	}

	program := &EnrichmentProgram{
		ProgramName:     request.ProgramName,
		SubjectID:       subjectID,
		TargetGrade:     request.TargetGrade,
		Description:     request.Description,
		AdvancedTopics:  request.AdvancedTopics,
		Projects:        request.Projects,
		Resources:       request.Resources,
		DurationWeeks:   request.DurationWeeks,
		SessionsPerWeek: request.SessionsPerWeek,
		SuccessCriteria: request.SuccessCriteria,
		IsActive:        request.IsActive,
	}

	if err := s.repo.CreateEnrichmentProgram(program); err != nil {
		return nil, err
	}

	return enrichmentToResponse(program), nil
}

func (s *interventionService) GetEnrichmentProgramByID(id string) (*EnrichmentProgramResponse, error) {
	programID, err := uuid.Parse(id)
	if err != nil {
		return nil, err
	}

	program, err := s.repo.GetEnrichmentProgramByID(programID)
	if err != nil {
		return nil, err
	}

	return enrichmentToResponse(program), nil
}

func (s *interventionService) GetAllEnrichmentPrograms() ([]EnrichmentProgramResponse, error) {
	programs, err := s.repo.GetAllEnrichmentPrograms()
	if err != nil {
		return nil, err
	}

	responses := make([]EnrichmentProgramResponse, len(programs))
	for i, program := range programs {
		responses[i] = *enrichmentToResponse(&program)
	}

	return responses, nil
}

func (s *interventionService) UpdateEnrichmentProgram(id string, request *EnrichmentProgramRequest) (*EnrichmentProgramResponse, error) {
	programID, err := uuid.Parse(id)
	if err != nil {
		return nil, err
	}

	program, err := s.repo.GetEnrichmentProgramByID(programID)
	if err != nil {
		return nil, err
	}

	var subjectID *uuid.UUID
	if request.SubjectID != nil {
		subjID := uuid.MustParse(*request.SubjectID)
		subjectID = &subjID
	}

	program.ProgramName = request.ProgramName
	program.SubjectID = subjectID
	program.TargetGrade = request.TargetGrade
	program.Description = request.Description
	program.AdvancedTopics = request.AdvancedTopics
	program.Projects = request.Projects
	program.Resources = request.Resources
	program.DurationWeeks = request.DurationWeeks
	program.SessionsPerWeek = request.SessionsPerWeek
	program.SuccessCriteria = request.SuccessCriteria
	program.IsActive = request.IsActive

	if err := s.repo.UpdateEnrichmentProgram(program); err != nil {
		return nil, err
	}

	return enrichmentToResponse(program), nil
}

func (s *interventionService) DeleteEnrichmentProgram(id string) error {
	programID, err := uuid.Parse(id)
	if err != nil {
		return err
	}

	return s.repo.DeleteEnrichmentProgram(programID)
}

// StudentInterventionAssignment operations
func (s *interventionService) CreateStudentAssignment(request *StudentInterventionAssignmentRequest) (*StudentInterventionAssignmentResponse, error) {
	assignment := &StudentInterventionAssignment{
		StudentID:        uuid.MustParse(request.StudentID),
		ProgramID:        uuid.MustParse(request.ProgramID),
		InterventionType: request.InterventionType,
		TeacherID:        uuid.MustParse(request.TeacherID),
		StartDate:        request.StartDate,
		EndDate:          request.EndDate,
		Status:           request.Status,
		PriorityLevel:    request.PriorityLevel,
		BaselineScore:    request.BaselineScore,
		TargetScore:      request.TargetScore,
		CurrentScore:     request.CurrentScore,
		Progress:         request.Progress,
		CustomizedPlan:   request.CustomizedPlan,
		Notes:            request.Notes,
	}

	if err := s.repo.CreateStudentAssignment(assignment); err != nil {
		return nil, err
	}

	return assignmentToResponse(assignment), nil
}

func (s *interventionService) GetStudentAssignmentByID(id string) (*StudentInterventionAssignmentResponse, error) {
	assignmentID, err := uuid.Parse(id)
	if err != nil {
		return nil, err
	}

	assignment, err := s.repo.GetStudentAssignmentByID(assignmentID)
	if err != nil {
		return nil, err
	}

	return assignmentToResponse(assignment), nil
}

func (s *interventionService) GetAssignmentsByStudent(studentID string) ([]StudentInterventionAssignmentResponse, error) {
	studentUUID, err := uuid.Parse(studentID)
	if err != nil {
		return nil, err
	}

	assignments, err := s.repo.GetAssignmentsByStudent(studentUUID)
	if err != nil {
		return nil, err
	}

	responses := make([]StudentInterventionAssignmentResponse, len(assignments))
	for i, assignment := range assignments {
		responses[i] = *assignmentToResponse(&assignment)
	}

	return responses, nil
}

func (s *interventionService) UpdateStudentAssignment(id string, request *StudentInterventionAssignmentRequest) (*StudentInterventionAssignmentResponse, error) {
	assignmentID, err := uuid.Parse(id)
	if err != nil {
		return nil, err
	}

	assignment, err := s.repo.GetStudentAssignmentByID(assignmentID)
	if err != nil {
		return nil, err
	}

	assignment.StudentID = uuid.MustParse(request.StudentID)
	assignment.ProgramID = uuid.MustParse(request.ProgramID)
	assignment.InterventionType = request.InterventionType
	assignment.TeacherID = uuid.MustParse(request.TeacherID)
	assignment.StartDate = request.StartDate
	assignment.EndDate = request.EndDate
	assignment.Status = request.Status
	assignment.PriorityLevel = request.PriorityLevel
	assignment.BaselineScore = request.BaselineScore
	assignment.TargetScore = request.TargetScore
	assignment.CurrentScore = request.CurrentScore
	assignment.Progress = request.Progress
	assignment.CustomizedPlan = request.CustomizedPlan
	assignment.Notes = request.Notes

	if err := s.repo.UpdateStudentAssignment(assignment); err != nil {
		return nil, err
	}

	return assignmentToResponse(assignment), nil
}

func (s *interventionService) DeleteStudentAssignment(id string) error {
	assignmentID, err := uuid.Parse(id)
	if err != nil {
		return err
	}

	return s.repo.DeleteStudentAssignment(assignmentID)
}

func (s *interventionService) GetInterventionSummary(schoolID string) (*InterventionSummaryResponse, error) {
	schoolUUID, err := uuid.Parse(schoolID)
	if err != nil {
		return nil, err
	}

	return s.repo.GetInterventionSummary(schoolUUID)
}
