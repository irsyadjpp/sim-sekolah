package supervision

import (
	"github.com/google/uuid"
)

type SupervisionService interface {
	// SupervisionCycle operations
	CreateCycle(request *SupervisionCycleRequest) (*SupervisionCycleResponse, error)
	GetCycleByID(id string) (*SupervisionCycleResponse, error)
	GetAllCycles() ([]SupervisionCycleResponse, error)
	GetCyclesBySchool(schoolID string) ([]SupervisionCycleResponse, error)
	GetCyclesByAcademicYear(academicYearID string) ([]SupervisionCycleResponse, error)
	GetActiveCycles() ([]SupervisionCycleResponse, error)
	UpdateCycle(id string, request *SupervisionCycleRequest) (*SupervisionCycleResponse, error)
	DeleteCycle(id string) error

	// TeacherObservation operations
	CreateObservation(request *TeacherObservationRequest) (*TeacherObservationResponse, error)
	GetObservationByID(id string) (*TeacherObservationResponse, error)
	GetAllObservations() ([]TeacherObservationResponse, error)
	GetObservationsByTeacher(teacherID string) ([]TeacherObservationResponse, error)
	GetObservationsByObserver(observerID string) ([]TeacherObservationResponse, error)
	GetObservationsByCycle(cycleID string) ([]TeacherObservationResponse, error)
	GetObservationsByStatus(status string) ([]TeacherObservationResponse, error)
	UpdateObservation(id string, request *TeacherObservationRequest) (*TeacherObservationResponse, error)
	DeleteObservation(id string) error

	// SupervisionFeedback operations
	CreateFeedback(request *SupervisionFeedbackRequest) (*SupervisionFeedbackResponse, error)
	GetFeedbackByID(id string) (*SupervisionFeedbackResponse, error)
	GetAllFeedback() ([]SupervisionFeedbackResponse, error)
	GetFeedbackByTeacher(teacherID string) ([]SupervisionFeedbackResponse, error)
	GetFeedbackByObservation(observationID string) ([]SupervisionFeedbackResponse, error)
	UpdateFeedback(id string, request *SupervisionFeedbackRequest) (*SupervisionFeedbackResponse, error)
	DeleteFeedback(id string) error

	// SupervisionAnalytics operations
	GetAnalyticsBySchool(schoolID string) ([]SupervisionAnalyticsResponse, error)
	GetAnalyticsByAcademicYear(academicYearID string) ([]SupervisionAnalyticsResponse, error)
	GetLatestAnalytics(schoolID string) (*SupervisionAnalyticsResponse, error)
	GenerateAnalytics(schoolID, academicYearID string) (*SupervisionAnalyticsResponse, error)

	// Summary operations
	GetSupervisionSummary(schoolID string) (*SupervisionSummaryResponse, error)
}

type supervisionService struct {
	repo SupervisionRepository
}

func NewSupervisionService(repo SupervisionRepository) SupervisionService {
	return &supervisionService{repo: repo}
}

// Helper function to convert cycle model to response
func cycleToResponse(cycle *SupervisionCycle) *SupervisionCycleResponse {
	return &SupervisionCycleResponse{
		ID:               cycle.ID.String(),
		CycleName:        cycle.CycleName,
		AcademicYearID:   cycle.AcademicYearID.String(),
		SchoolID:         cycle.SchoolID.String(),
		StartDate:        cycle.StartDate,
		EndDate:          cycle.EndDate,
		Status:           cycle.Status,
		Description:      cycle.Description,
		SupervisorID:     cycle.SupervisorID.String(),
		Goals:            cycle.Goals,
		ExpectedOutcomes: cycle.ExpectedOutcomes,
		IsActive:         cycle.IsActive,
		CreatedAt:        cycle.CreatedAt,
		UpdatedAt:        cycle.UpdatedAt,
	}
}

// Helper function to convert observation model to response
func observationToResponse(observation *TeacherObservation) *TeacherObservationResponse {
	var supervisionCycleID *string
	if observation.SupervisionCycleID != nil {
		cycleID := observation.SupervisionCycleID.String()
		supervisionCycleID = &cycleID
	}

	var subjectID *string
	if observation.SubjectID != nil {
		subjID := observation.SubjectID.String()
		subjectID = &subjID
	}

	var classroomID *string
	if observation.ClassroomID != nil {
		classID := observation.ClassroomID.String()
		classroomID = &classID
	}

	return &TeacherObservationResponse{
		ID:                  observation.ID.String(),
		SupervisionCycleID:  supervisionCycleID,
		TeacherID:           observation.TeacherID.String(),
		ObserverID:          observation.ObserverID.String(),
		SubjectID:           subjectID,
		ClassroomID:         classroomID,
		ObservationDate:     observation.ObservationDate,
		ObservationType:     observation.ObservationType,
		Status:              observation.Status,
		StartTime:           observation.StartTime,
		EndTime:             observation.EndTime,
		LessonTopic:         observation.LessonTopic,
		ClassGrade:          observation.ClassGrade,
		Strengths:           observation.Strengths,
		AreasForImprovement: observation.AreasForImprovement,
		Notes:               observation.Notes,
		Score:               observation.Score,
		MaxScore:            observation.MaxScore,
		CreatedAt:           observation.CreatedAt,
		UpdatedAt:           observation.UpdatedAt,
	}
}

// Helper function to convert feedback model to response
func feedbackToResponse(feedback *SupervisionFeedback) *SupervisionFeedbackResponse {
	return &SupervisionFeedbackResponse{
		ID:                 feedback.ID.String(),
		ObservationID:      feedback.ObservationID.String(),
		TeacherID:          feedback.TeacherID.String(),
		FeedbackDate:       feedback.FeedbackDate,
		FeedbackProviderID: feedback.FeedbackProviderID.String(),
		Status:             feedback.Status,
		Strengths:          feedback.Strengths,
		ImprovementAreas:   feedback.ImprovementAreas,
		Recommendations:    feedback.Recommendations,
		ActionPlan:         feedback.ActionPlan,
		FollowUpDate:       feedback.FollowUpDate,
		TeacherResponse:    feedback.TeacherResponse,
		ResponseDate:       feedback.ResponseDate,
		IsAcknowledged:     feedback.IsAcknowledged,
		OverallRating:      feedback.OverallRating,
		Comments:           feedback.Comments,
		CreatedAt:          feedback.CreatedAt,
		UpdatedAt:          feedback.UpdatedAt,
	}
}

// Helper function to convert analytics model to response
func analyticsToResponse(analytics *SupervisionAnalytics) *SupervisionAnalyticsResponse {
	var supervisionCycleID *string
	if analytics.SupervisionCycleID != nil {
		cycleID := analytics.SupervisionCycleID.String()
		supervisionCycleID = &cycleID
	}

	return &SupervisionAnalyticsResponse{
		ID:                     analytics.ID.String(),
		SchoolID:               analytics.SchoolID.String(),
		AcademicYearID:         analytics.AcademicYearID.String(),
		SupervisionCycleID:     supervisionCycleID,
		AnalyticsDate:          analytics.AnalyticsDate,
		TotalObservations:      analytics.TotalObservations,
		CompletedObservations:  analytics.CompletedObservations,
		AverageScore:           analytics.AverageScore,
		TeachersSupervised:     analytics.TeachersSupervised,
		ImprovementRate:        analytics.ImprovementRate,
		FeedbackCompletionRate: analytics.FeedbackCompletionRate,
		TopStrengths:           analytics.TopStrengths,
		CommonImprovementAreas: analytics.CommonImprovementAreas,
		CreatedAt:              analytics.CreatedAt,
		UpdatedAt:              analytics.UpdatedAt,
	}
}

// SupervisionCycle operations
func (s *supervisionService) CreateCycle(request *SupervisionCycleRequest) (*SupervisionCycleResponse, error) {
	cycle := &SupervisionCycle{
		CycleName:        request.CycleName,
		AcademicYearID:   uuid.MustParse(request.AcademicYearID),
		SchoolID:         uuid.MustParse(request.SchoolID),
		StartDate:        request.StartDate,
		EndDate:          request.EndDate,
		Status:           request.Status,
		Description:      request.Description,
		SupervisorID:     uuid.MustParse(request.SupervisorID),
		Goals:            request.Goals,
		ExpectedOutcomes: request.ExpectedOutcomes,
		IsActive:         request.IsActive,
	}

	if err := s.repo.CreateCycle(cycle); err != nil {
		return nil, err
	}

	return cycleToResponse(cycle), nil
}

func (s *supervisionService) GetCycleByID(id string) (*SupervisionCycleResponse, error) {
	cycleID, err := uuid.Parse(id)
	if err != nil {
		return nil, err
	}

	cycle, err := s.repo.GetCycleByID(cycleID)
	if err != nil {
		return nil, err
	}

	return cycleToResponse(cycle), nil
}

func (s *supervisionService) GetAllCycles() ([]SupervisionCycleResponse, error) {
	cycles, err := s.repo.GetAllCycles()
	if err != nil {
		return nil, err
	}

	responses := make([]SupervisionCycleResponse, len(cycles))
	for i, cycle := range cycles {
		responses[i] = *cycleToResponse(&cycle)
	}

	return responses, nil
}

func (s *supervisionService) GetCyclesBySchool(schoolID string) ([]SupervisionCycleResponse, error) {
	schoolUUID, err := uuid.Parse(schoolID)
	if err != nil {
		return nil, err
	}

	cycles, err := s.repo.GetCyclesBySchool(schoolUUID)
	if err != nil {
		return nil, err
	}

	responses := make([]SupervisionCycleResponse, len(cycles))
	for i, cycle := range cycles {
		responses[i] = *cycleToResponse(&cycle)
	}

	return responses, nil
}

func (s *supervisionService) GetCyclesByAcademicYear(academicYearID string) ([]SupervisionCycleResponse, error) {
	academicYearUUID, err := uuid.Parse(academicYearID)
	if err != nil {
		return nil, err
	}

	cycles, err := s.repo.GetCyclesByAcademicYear(academicYearUUID)
	if err != nil {
		return nil, err
	}

	responses := make([]SupervisionCycleResponse, len(cycles))
	for i, cycle := range cycles {
		responses[i] = *cycleToResponse(&cycle)
	}

	return responses, nil
}

func (s *supervisionService) GetActiveCycles() ([]SupervisionCycleResponse, error) {
	cycles, err := s.repo.GetActiveCycles()
	if err != nil {
		return nil, err
	}

	responses := make([]SupervisionCycleResponse, len(cycles))
	for i, cycle := range cycles {
		responses[i] = *cycleToResponse(&cycle)
	}

	return responses, nil
}

func (s *supervisionService) UpdateCycle(id string, request *SupervisionCycleRequest) (*SupervisionCycleResponse, error) {
	cycleID, err := uuid.Parse(id)
	if err != nil {
		return nil, err
	}

	cycle, err := s.repo.GetCycleByID(cycleID)
	if err != nil {
		return nil, err
	}

	cycle.CycleName = request.CycleName
	cycle.AcademicYearID = uuid.MustParse(request.AcademicYearID)
	cycle.SchoolID = uuid.MustParse(request.SchoolID)
	cycle.StartDate = request.StartDate
	cycle.EndDate = request.EndDate
	cycle.Status = request.Status
	cycle.Description = request.Description
	cycle.SupervisorID = uuid.MustParse(request.SupervisorID)
	cycle.Goals = request.Goals
	cycle.ExpectedOutcomes = request.ExpectedOutcomes
	cycle.IsActive = request.IsActive

	if err := s.repo.UpdateCycle(cycle); err != nil {
		return nil, err
	}

	return cycleToResponse(cycle), nil
}

func (s *supervisionService) DeleteCycle(id string) error {
	cycleID, err := uuid.Parse(id)
	if err != nil {
		return err
	}

	return s.repo.DeleteCycle(cycleID)
}

// TeacherObservation operations
func (s *supervisionService) CreateObservation(request *TeacherObservationRequest) (*TeacherObservationResponse, error) {
	var supervisionCycleID *uuid.UUID
	if request.SupervisionCycleID != nil {
		cycleID := uuid.MustParse(*request.SupervisionCycleID)
		supervisionCycleID = &cycleID
	}

	var subjectID *uuid.UUID
	if request.SubjectID != nil {
		subjID := uuid.MustParse(*request.SubjectID)
		subjectID = &subjID
	}

	var classroomID *uuid.UUID
	if request.ClassroomID != nil {
		classID := uuid.MustParse(*request.ClassroomID)
		classroomID = &classID
	}

	observation := &TeacherObservation{
		SupervisionCycleID:  supervisionCycleID,
		TeacherID:           uuid.MustParse(request.TeacherID),
		ObserverID:          uuid.MustParse(request.ObserverID),
		SubjectID:           subjectID,
		ClassroomID:         classroomID,
		ObservationDate:     request.ObservationDate,
		ObservationType:     request.ObservationType,
		Status:              request.Status,
		StartTime:           request.StartTime,
		EndTime:             request.EndTime,
		LessonTopic:         request.LessonTopic,
		ClassGrade:          request.ClassGrade,
		Strengths:           request.Strengths,
		AreasForImprovement: request.AreasForImprovement,
		Notes:               request.Notes,
		Score:               request.Score,
		MaxScore:            request.MaxScore,
	}

	if err := s.repo.CreateObservation(observation); err != nil {
		return nil, err
	}

	return observationToResponse(observation), nil
}

func (s *supervisionService) GetObservationByID(id string) (*TeacherObservationResponse, error) {
	observationID, err := uuid.Parse(id)
	if err != nil {
		return nil, err
	}

	observation, err := s.repo.GetObservationByID(observationID)
	if err != nil {
		return nil, err
	}

	return observationToResponse(observation), nil
}

func (s *supervisionService) GetAllObservations() ([]TeacherObservationResponse, error) {
	observations, err := s.repo.GetAllObservations()
	if err != nil {
		return nil, err
	}

	responses := make([]TeacherObservationResponse, len(observations))
	for i, observation := range observations {
		responses[i] = *observationToResponse(&observation)
	}

	return responses, nil
}

func (s *supervisionService) GetObservationsByTeacher(teacherID string) ([]TeacherObservationResponse, error) {
	teacherUUID, err := uuid.Parse(teacherID)
	if err != nil {
		return nil, err
	}

	observations, err := s.repo.GetObservationsByTeacher(teacherUUID)
	if err != nil {
		return nil, err
	}

	responses := make([]TeacherObservationResponse, len(observations))
	for i, observation := range observations {
		responses[i] = *observationToResponse(&observation)
	}

	return responses, nil
}

func (s *supervisionService) GetObservationsByObserver(observerID string) ([]TeacherObservationResponse, error) {
	observerUUID, err := uuid.Parse(observerID)
	if err != nil {
		return nil, err
	}

	observations, err := s.repo.GetObservationsByObserver(observerUUID)
	if err != nil {
		return nil, err
	}

	responses := make([]TeacherObservationResponse, len(observations))
	for i, observation := range observations {
		responses[i] = *observationToResponse(&observation)
	}

	return responses, nil
}

func (s *supervisionService) GetObservationsByCycle(cycleID string) ([]TeacherObservationResponse, error) {
	cycleUUID, err := uuid.Parse(cycleID)
	if err != nil {
		return nil, err
	}

	observations, err := s.repo.GetObservationsByCycle(cycleUUID)
	if err != nil {
		return nil, err
	}

	responses := make([]TeacherObservationResponse, len(observations))
	for i, observation := range observations {
		responses[i] = *observationToResponse(&observation)
	}

	return responses, nil
}

func (s *supervisionService) GetObservationsByStatus(status string) ([]TeacherObservationResponse, error) {
	observations, err := s.repo.GetObservationsByStatus(status)
	if err != nil {
		return nil, err
	}

	responses := make([]TeacherObservationResponse, len(observations))
	for i, observation := range observations {
		responses[i] = *observationToResponse(&observation)
	}

	return responses, nil
}

func (s *supervisionService) UpdateObservation(id string, request *TeacherObservationRequest) (*TeacherObservationResponse, error) {
	observationID, err := uuid.Parse(id)
	if err != nil {
		return nil, err
	}

	observation, err := s.repo.GetObservationByID(observationID)
	if err != nil {
		return nil, err
	}

	var supervisionCycleID *uuid.UUID
	if request.SupervisionCycleID != nil {
		cycleID := uuid.MustParse(*request.SupervisionCycleID)
		supervisionCycleID = &cycleID
	}

	var subjectID *uuid.UUID
	if request.SubjectID != nil {
		subjID := uuid.MustParse(*request.SubjectID)
		subjectID = &subjID
	}

	var classroomID *uuid.UUID
	if request.ClassroomID != nil {
		classID := uuid.MustParse(*request.ClassroomID)
		classroomID = &classID
	}

	observation.SupervisionCycleID = supervisionCycleID
	observation.TeacherID = uuid.MustParse(request.TeacherID)
	observation.ObserverID = uuid.MustParse(request.ObserverID)
	observation.SubjectID = subjectID
	observation.ClassroomID = classroomID
	observation.ObservationDate = request.ObservationDate
	observation.ObservationType = request.ObservationType
	observation.Status = request.Status
	observation.StartTime = request.StartTime
	observation.EndTime = request.EndTime
	observation.LessonTopic = request.LessonTopic
	observation.ClassGrade = request.ClassGrade
	observation.Strengths = request.Strengths
	observation.AreasForImprovement = request.AreasForImprovement
	observation.Notes = request.Notes
	observation.Score = request.Score
	observation.MaxScore = request.MaxScore

	if err := s.repo.UpdateObservation(observation); err != nil {
		return nil, err
	}

	return observationToResponse(observation), nil
}

func (s *supervisionService) DeleteObservation(id string) error {
	observationID, err := uuid.Parse(id)
	if err != nil {
		return err
	}

	return s.repo.DeleteObservation(observationID)
}

// SupervisionFeedback operations
func (s *supervisionService) CreateFeedback(request *SupervisionFeedbackRequest) (*SupervisionFeedbackResponse, error) {
	feedback := &SupervisionFeedback{
		ObservationID:      uuid.MustParse(request.ObservationID),
		TeacherID:          uuid.MustParse(request.TeacherID),
		FeedbackDate:       request.FeedbackDate,
		FeedbackProviderID: uuid.MustParse(request.FeedbackProviderID),
		Status:             request.Status,
		Strengths:          request.Strengths,
		ImprovementAreas:   request.ImprovementAreas,
		Recommendations:    request.Recommendations,
		ActionPlan:         request.ActionPlan,
		FollowUpDate:       request.FollowUpDate,
		TeacherResponse:    request.TeacherResponse,
		ResponseDate:       request.ResponseDate,
		IsAcknowledged:     request.IsAcknowledged,
		OverallRating:      request.OverallRating,
		Comments:           request.Comments,
	}

	if err := s.repo.CreateFeedback(feedback); err != nil {
		return nil, err
	}

	return feedbackToResponse(feedback), nil
}

func (s *supervisionService) GetFeedbackByID(id string) (*SupervisionFeedbackResponse, error) {
	feedbackID, err := uuid.Parse(id)
	if err != nil {
		return nil, err
	}

	feedback, err := s.repo.GetFeedbackByID(feedbackID)
	if err != nil {
		return nil, err
	}

	return feedbackToResponse(feedback), nil
}

func (s *supervisionService) GetAllFeedback() ([]SupervisionFeedbackResponse, error) {
	feedbacks, err := s.repo.GetAllFeedback()
	if err != nil {
		return nil, err
	}

	responses := make([]SupervisionFeedbackResponse, len(feedbacks))
	for i, feedback := range feedbacks {
		responses[i] = *feedbackToResponse(&feedback)
	}

	return responses, nil
}

func (s *supervisionService) GetFeedbackByTeacher(teacherID string) ([]SupervisionFeedbackResponse, error) {
	teacherUUID, err := uuid.Parse(teacherID)
	if err != nil {
		return nil, err
	}

	feedbacks, err := s.repo.GetFeedbackByTeacher(teacherUUID)
	if err != nil {
		return nil, err
	}

	responses := make([]SupervisionFeedbackResponse, len(feedbacks))
	for i, feedback := range feedbacks {
		responses[i] = *feedbackToResponse(&feedback)
	}

	return responses, nil
}

func (s *supervisionService) GetFeedbackByObservation(observationID string) ([]SupervisionFeedbackResponse, error) {
	observationUUID, err := uuid.Parse(observationID)
	if err != nil {
		return nil, err
	}

	feedbacks, err := s.repo.GetFeedbackByObservation(observationUUID)
	if err != nil {
		return nil, err
	}

	responses := make([]SupervisionFeedbackResponse, len(feedbacks))
	for i, feedback := range feedbacks {
		responses[i] = *feedbackToResponse(&feedback)
	}

	return responses, nil
}

func (s *supervisionService) UpdateFeedback(id string, request *SupervisionFeedbackRequest) (*SupervisionFeedbackResponse, error) {
	feedbackID, err := uuid.Parse(id)
	if err != nil {
		return nil, err
	}

	feedback, err := s.repo.GetFeedbackByID(feedbackID)
	if err != nil {
		return nil, err
	}

	feedback.ObservationID = uuid.MustParse(request.ObservationID)
	feedback.TeacherID = uuid.MustParse(request.TeacherID)
	feedback.FeedbackDate = request.FeedbackDate
	feedback.FeedbackProviderID = uuid.MustParse(request.FeedbackProviderID)
	feedback.Status = request.Status
	feedback.Strengths = request.Strengths
	feedback.ImprovementAreas = request.ImprovementAreas
	feedback.Recommendations = request.Recommendations
	feedback.ActionPlan = request.ActionPlan
	feedback.FollowUpDate = request.FollowUpDate
	feedback.TeacherResponse = request.TeacherResponse
	feedback.ResponseDate = request.ResponseDate
	feedback.IsAcknowledged = request.IsAcknowledged
	feedback.OverallRating = request.OverallRating
	feedback.Comments = request.Comments

	if err := s.repo.UpdateFeedback(feedback); err != nil {
		return nil, err
	}

	return feedbackToResponse(feedback), nil
}

func (s *supervisionService) DeleteFeedback(id string) error {
	feedbackID, err := uuid.Parse(id)
	if err != nil {
		return err
	}

	return s.repo.DeleteFeedback(feedbackID)
}

// SupervisionAnalytics operations
func (s *supervisionService) GetAnalyticsBySchool(schoolID string) ([]SupervisionAnalyticsResponse, error) {
	schoolUUID, err := uuid.Parse(schoolID)
	if err != nil {
		return nil, err
	}

	analytics, err := s.repo.GetAnalyticsBySchool(schoolUUID)
	if err != nil {
		return nil, err
	}

	responses := make([]SupervisionAnalyticsResponse, len(analytics))
	for i, analytic := range analytics {
		responses[i] = *analyticsToResponse(&analytic)
	}

	return responses, nil
}

func (s *supervisionService) GetAnalyticsByAcademicYear(academicYearID string) ([]SupervisionAnalyticsResponse, error) {
	academicYearUUID, err := uuid.Parse(academicYearID)
	if err != nil {
		return nil, err
	}

	analytics, err := s.repo.GetAnalyticsByAcademicYear(academicYearUUID)
	if err != nil {
		return nil, err
	}

	responses := make([]SupervisionAnalyticsResponse, len(analytics))
	for i, analytic := range analytics {
		responses[i] = *analyticsToResponse(&analytic)
	}

	return responses, nil
}

func (s *supervisionService) GetLatestAnalytics(schoolID string) (*SupervisionAnalyticsResponse, error) {
	schoolUUID, err := uuid.Parse(schoolID)
	if err != nil {
		return nil, err
	}

	analytics, err := s.repo.GetLatestAnalytics(schoolUUID)
	if err != nil {
		return nil, err
	}

	return analyticsToResponse(analytics), nil
}

func (s *supervisionService) GenerateAnalytics(schoolID, academicYearID string) (*SupervisionAnalyticsResponse, error) {
	schoolUUID, err := uuid.Parse(schoolID)
	if err != nil {
		return nil, err
	}

	academicYearUUID, err := uuid.Parse(academicYearID)
	if err != nil {
		return nil, err
	}

	summary, err := s.repo.GetSupervisionSummary(schoolUUID)
	if err != nil {
		return nil, err
	}

	analytics := &SupervisionAnalytics{
		SchoolID:              schoolUUID,
		AcademicYearID:        academicYearUUID,
		TotalObservations:     summary.TotalObservations,
		CompletedObservations: summary.CompletedObservations,
		AverageScore:          &summary.AverageScore,
		TeachersSupervised:    summary.TeachersSupervised,
	}

	if err := s.repo.CreateAnalytics(analytics); err != nil {
		return nil, err
	}

	return analyticsToResponse(analytics), nil
}

// Summary operations
func (s *supervisionService) GetSupervisionSummary(schoolID string) (*SupervisionSummaryResponse, error) {
	schoolUUID, err := uuid.Parse(schoolID)
	if err != nil {
		return nil, err
	}

	return s.repo.GetSupervisionSummary(schoolUUID)
}
