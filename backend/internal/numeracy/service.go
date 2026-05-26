package numeracy

import (
	"errors"

	"github.com/google/uuid"
)

type Service interface {
	// Indicator operations
	CreateIndicator(request NumeracyIndicatorRequest) (*NumeracyIndicatorResponse, error)
	GetIndicatorByID(id uuid.UUID) (*NumeracyIndicatorResponse, error)
	GetIndicators(filter map[string]interface{}) ([]NumeracyIndicatorResponse, error)
	UpdateIndicator(id uuid.UUID, request NumeracyIndicatorRequest) (*NumeracyIndicatorResponse, error)
	DeleteIndicator(id uuid.UUID) error

	// Assessment operations
	CreateAssessment(request NumeracyAssessmentRequest) (*NumeracyAssessmentResponse, error)
	GetAssessmentByID(id uuid.UUID) (*NumeracyAssessmentResponse, error)
	GetAssessments(filter map[string]interface{}) ([]NumeracyAssessmentResponse, error)
	UpdateAssessment(id uuid.UUID, request NumeracyAssessmentRequest) (*NumeracyAssessmentResponse, error)
	DeleteAssessment(id uuid.UUID) error

	// Growth operations
	CreateGrowth(request NumeracyGrowthRequest) (*NumeracyGrowthResponse, error)
	GetGrowthByID(id uuid.UUID) (*NumeracyGrowthResponse, error)
	GetGrowthByStudentAndPeriod(studentID uuid.UUID, period string) (*NumeracyGrowthResponse, error)
	GetGrowths(filter map[string]interface{}) ([]NumeracyGrowthResponse, error)
	UpdateGrowth(id uuid.UUID, request NumeracyGrowthRequest) (*NumeracyGrowthResponse, error)
	DeleteGrowth(id uuid.UUID) error
	CalculateStudentGrowth(studentID uuid.UUID, period string, academicYearID uuid.UUID) (*NumeracyGrowthResponse, error)

	// Intervention operations
	CreateIntervention(request NumeracyInterventionRequest) (*NumeracyInterventionResponse, error)
	GetInterventionByID(id uuid.UUID) (*NumeracyInterventionResponse, error)
	GetInterventions(filter map[string]interface{}) ([]NumeracyInterventionResponse, error)
	UpdateIntervention(id uuid.UUID, request NumeracyInterventionRequest) (*NumeracyInterventionResponse, error)
	DeleteIntervention(id uuid.UUID) error

	// Analytics operations
	GetNumeracyAnalytics(request NumeracyAnalyticsRequest) (*NumeracyAnalyticsResponse, error)
}

type service struct {
	repo Repository
}

func NewService(repo Repository) Service {
	return &service{repo: repo}
}

// Indicator operations
func (s *service) CreateIndicator(request NumeracyIndicatorRequest) (*NumeracyIndicatorResponse, error) {
	// Validate numeracy type
	if !IsValidNumeracyType(request.NumeracyType) {
		return nil, errors.New("invalid numeracy type")
	}

	indicator := &NumeracyIndicator{
		ID:            uuid.New(),
		PhaseID:       request.PhaseID,
		NumeracyType:  request.NumeracyType,
		IndicatorCode: request.IndicatorCode,
		IndicatorName: request.IndicatorName,
		Description:   request.Description,
		GradeLevel:    request.GradeLevel,
		MinAge:        request.MinAge,
		MaxAge:        request.MaxAge,
		Difficulty:    request.Difficulty,
		Examples:      request.Examples,
	}

	if request.IsActive != nil {
		indicator.IsActive = *request.IsActive
	}

	err := s.repo.CreateIndicator(indicator)
	if err != nil {
		return nil, err
	}

	return s.modelToIndicatorResponse(indicator), nil
}

func (s *service) GetIndicatorByID(id uuid.UUID) (*NumeracyIndicatorResponse, error) {
	indicator, err := s.repo.GetIndicatorByID(id)
	if err != nil {
		return nil, err
	}
	return s.modelToIndicatorResponse(indicator), nil
}

func (s *service) GetIndicators(filter map[string]interface{}) ([]NumeracyIndicatorResponse, error) {
	indicators, err := s.repo.GetIndicators(filter)
	if err != nil {
		return nil, err
	}

	responses := make([]NumeracyIndicatorResponse, len(indicators))
	for i, indicator := range indicators {
		responses[i] = *s.modelToIndicatorResponse(&indicator)
	}
	return responses, nil
}

func (s *service) UpdateIndicator(id uuid.UUID, request NumeracyIndicatorRequest) (*NumeracyIndicatorResponse, error) {
	// Validate numeracy type
	if !IsValidNumeracyType(request.NumeracyType) {
		return nil, errors.New("invalid numeracy type")
	}

	indicator, err := s.repo.GetIndicatorByID(id)
	if err != nil {
		return nil, err
	}

	indicator.PhaseID = request.PhaseID
	indicator.NumeracyType = request.NumeracyType
	indicator.IndicatorCode = request.IndicatorCode
	indicator.IndicatorName = request.IndicatorName
	indicator.Description = request.Description
	indicator.GradeLevel = request.GradeLevel
	indicator.MinAge = request.MinAge
	indicator.MaxAge = request.MaxAge
	indicator.Difficulty = request.Difficulty
	indicator.Examples = request.Examples

	if request.IsActive != nil {
		indicator.IsActive = *request.IsActive
	}

	err = s.repo.UpdateIndicator(indicator)
	if err != nil {
		return nil, err
	}

	return s.modelToIndicatorResponse(indicator), nil
}

func (s *service) DeleteIndicator(id uuid.UUID) error {
	return s.repo.DeleteIndicator(id)
}

// Assessment operations
func (s *service) CreateAssessment(request NumeracyAssessmentRequest) (*NumeracyAssessmentResponse, error) {
	// Validate mastery level
	if !IsValidMasteryLevel(request.MasteryLevel) {
		return nil, errors.New("invalid mastery level")
	}

	assessment := &NumeracyAssessment{
		ID:             uuid.New(),
		StudentID:      request.StudentID,
		IndicatorID:    request.IndicatorID,
		AssessmentDate: request.AssessmentDate,
		AssessmentType: request.AssessmentType,
		Score:          request.Score,
		MasteryLevel:   request.MasteryLevel,
		ResponseTime:   request.ResponseTime,
		Attempts:       request.Attempts,
		TeacherID:      request.TeacherID,
		Notes:          request.Notes,
		EvidenceFiles:  request.EvidenceFiles,
	}

	if assessment.Attempts == 0 {
		assessment.Attempts = 1
	}

	err := s.repo.CreateAssessment(assessment)
	if err != nil {
		return nil, err
	}

	return s.modelToAssessmentResponse(assessment), nil
}

func (s *service) GetAssessmentByID(id uuid.UUID) (*NumeracyAssessmentResponse, error) {
	assessment, err := s.repo.GetAssessmentByID(id)
	if err != nil {
		return nil, err
	}
	return s.modelToAssessmentResponse(assessment), nil
}

func (s *service) GetAssessments(filter map[string]interface{}) ([]NumeracyAssessmentResponse, error) {
	assessments, err := s.repo.GetAssessments(filter)
	if err != nil {
		return nil, err
	}

	responses := make([]NumeracyAssessmentResponse, len(assessments))
	for i, assessment := range assessments {
		responses[i] = *s.modelToAssessmentResponse(&assessment)
	}
	return responses, nil
}

func (s *service) UpdateAssessment(id uuid.UUID, request NumeracyAssessmentRequest) (*NumeracyAssessmentResponse, error) {
	// Validate mastery level
	if !IsValidMasteryLevel(request.MasteryLevel) {
		return nil, errors.New("invalid mastery level")
	}

	assessment, err := s.repo.GetAssessmentByID(id)
	if err != nil {
		return nil, err
	}

	assessment.StudentID = request.StudentID
	assessment.IndicatorID = request.IndicatorID
	assessment.AssessmentDate = request.AssessmentDate
	assessment.AssessmentType = request.AssessmentType
	assessment.Score = request.Score
	assessment.MasteryLevel = request.MasteryLevel
	assessment.ResponseTime = request.ResponseTime
	assessment.Attempts = request.Attempts
	assessment.TeacherID = request.TeacherID
	assessment.Notes = request.Notes
	assessment.EvidenceFiles = request.EvidenceFiles

	if assessment.Attempts == 0 {
		assessment.Attempts = 1
	}

	err = s.repo.UpdateAssessment(assessment)
	if err != nil {
		return nil, err
	}

	return s.modelToAssessmentResponse(assessment), nil
}

func (s *service) DeleteAssessment(id uuid.UUID) error {
	return s.repo.DeleteAssessment(id)
}

// Growth operations
func (s *service) CreateGrowth(request NumeracyGrowthRequest) (*NumeracyGrowthResponse, error) {
	growth := &NumeracyGrowth{
		ID:                uuid.New(),
		StudentID:         request.StudentID,
		Period:            request.Period,
		AcademicYearID:    request.AcademicYearID,
		OverallScore:      request.OverallScore,
		NumbersScore:      request.NumbersScore,
		OperationsScore:   request.OperationsScore,
		GeometryScore:     request.GeometryScore,
		MeasurementScore:  request.MeasurementScore,
		DataAnalysisScore: request.DataAnalysisScore,
		MasteryRate:       request.MasteryRate,
		GrowthRate:        request.GrowthRate,
		Percentile:        request.Percentile,
		TeacherID:         request.TeacherID,
		Notes:             request.Notes,
	}

	err := s.repo.CreateGrowth(growth)
	if err != nil {
		return nil, err
	}

	return s.modelToGrowthResponse(growth), nil
}

func (s *service) GetGrowthByID(id uuid.UUID) (*NumeracyGrowthResponse, error) {
	growth, err := s.repo.GetGrowthByID(id)
	if err != nil {
		return nil, err
	}
	return s.modelToGrowthResponse(growth), nil
}

func (s *service) GetGrowthByStudentAndPeriod(studentID uuid.UUID, period string) (*NumeracyGrowthResponse, error) {
	growth, err := s.repo.GetGrowthByStudentAndPeriod(studentID, period)
	if err != nil {
		return nil, err
	}
	return s.modelToGrowthResponse(growth), nil
}

func (s *service) GetGrowths(filter map[string]interface{}) ([]NumeracyGrowthResponse, error) {
	growths, err := s.repo.GetGrowths(filter)
	if err != nil {
		return nil, err
	}

	responses := make([]NumeracyGrowthResponse, len(growths))
	for i, growth := range growths {
		responses[i] = *s.modelToGrowthResponse(&growth)
	}
	return responses, nil
}

func (s *service) UpdateGrowth(id uuid.UUID, request NumeracyGrowthRequest) (*NumeracyGrowthResponse, error) {
	growth, err := s.repo.GetGrowthByID(id)
	if err != nil {
		return nil, err
	}

	growth.StudentID = request.StudentID
	growth.Period = request.Period
	growth.AcademicYearID = request.AcademicYearID
	growth.OverallScore = request.OverallScore
	growth.NumbersScore = request.NumbersScore
	growth.OperationsScore = request.OperationsScore
	growth.GeometryScore = request.GeometryScore
	growth.MeasurementScore = request.MeasurementScore
	growth.DataAnalysisScore = request.DataAnalysisScore
	growth.MasteryRate = request.MasteryRate
	growth.GrowthRate = request.GrowthRate
	growth.Percentile = request.Percentile
	growth.TeacherID = request.TeacherID
	growth.Notes = request.Notes

	err = s.repo.UpdateGrowth(growth)
	if err != nil {
		return nil, err
	}

	return s.modelToGrowthResponse(growth), nil
}

func (s *service) DeleteGrowth(id uuid.UUID) error {
	return s.repo.DeleteGrowth(id)
}

func (s *service) CalculateStudentGrowth(studentID uuid.UUID, period string, academicYearID uuid.UUID) (*NumeracyGrowthResponse, error) {
	// Get all assessments for the student in the period
	filter := map[string]interface{}{
		"student_id": studentID,
	}

	assessments, err := s.repo.GetAssessments(filter)
	if err != nil {
		return nil, err
	}

	if len(assessments) == 0 {
		return nil, errors.New("no assessments found for student")
	}

	// Calculate scores by numeracy type
	var totalScore, count float64
	numeracyScores := make(map[string]float64)
	numeracyCounts := make(map[string]float64)

	for _, assessment := range assessments {
		if assessment.Indicator != nil {
			totalScore += assessment.Score
			count++
			numeracyScores[assessment.Indicator.NumeracyType] += assessment.Score
			numeracyCounts[assessment.Indicator.NumeracyType]++
		}
	}

	averageScore := float64(0)
	if count > 0 {
		averageScore = totalScore / count
	}

	// Calculate mastery rate
	var masteryCount int64
	for _, assessment := range assessments {
		if assessment.MasteryLevel == "MENGUASAI" {
			masteryCount++
		}
	}
	masteryRate := float64(0)
	if len(assessments) > 0 {
		masteryRate = float64(masteryCount) / float64(len(assessments)) * 100
	}

	// Calculate scores by numeracy type
	numbersScore := s.calculateTypeScore(numeracyScores, numeracyCounts, NumeracyTypeNumbers)
	operationsScore := s.calculateTypeScore(numeracyScores, numeracyCounts, NumeracyTypeOperations)
	geometryScore := s.calculateTypeScore(numeracyScores, numeracyCounts, NumeracyTypeGeometry)
	measurementScore := s.calculateTypeScore(numeracyScores, numeracyCounts, NumeracyTypeMeasurement)
	dataAnalysisScore := s.calculateTypeScore(numeracyScores, numeracyCounts, NumeracyTypeDataAnalysis)

	// Create growth record
	growth := &NumeracyGrowth{
		ID:                uuid.New(),
		StudentID:         studentID,
		Period:            period,
		AcademicYearID:    academicYearID,
		OverallScore:      averageScore,
		NumbersScore:      numbersScore,
		OperationsScore:   operationsScore,
		GeometryScore:     geometryScore,
		MeasurementScore:  measurementScore,
		DataAnalysisScore: dataAnalysisScore,
		MasteryRate:       masteryRate,
	}

	err = s.repo.CreateGrowth(growth)
	if err != nil {
		return nil, err
	}

	return s.modelToGrowthResponse(growth), nil
}

func (s *service) calculateTypeScore(scores, counts map[string]float64, numeracyType string) float64 {
	if counts[numeracyType] > 0 {
		return scores[numeracyType] / counts[numeracyType]
	}
	return 0
}

// Intervention operations
func (s *service) CreateIntervention(request NumeracyInterventionRequest) (*NumeracyInterventionResponse, error) {
	intervention := &NumeracyIntervention{
		ID:               uuid.New(),
		StudentID:        request.StudentID,
		IndicatorID:      request.IndicatorID,
		InterventionType: request.InterventionType,
		StartDate:        request.StartDate,
		EndDate:          request.EndDate,
		Status:           request.Status,
		Activities:       request.Activities,
		TeacherID:        request.TeacherID,
		Outcome:          request.Outcome,
		Effectiveness:    request.Effectiveness,
	}

	err := s.repo.CreateIntervention(intervention)
	if err != nil {
		return nil, err
	}

	return s.modelToInterventionResponse(intervention), nil
}

func (s *service) GetInterventionByID(id uuid.UUID) (*NumeracyInterventionResponse, error) {
	intervention, err := s.repo.GetInterventionByID(id)
	if err != nil {
		return nil, err
	}
	return s.modelToInterventionResponse(intervention), nil
}

func (s *service) GetInterventions(filter map[string]interface{}) ([]NumeracyInterventionResponse, error) {
	interventions, err := s.repo.GetInterventions(filter)
	if err != nil {
		return nil, err
	}

	responses := make([]NumeracyInterventionResponse, len(interventions))
	for i, intervention := range interventions {
		responses[i] = *s.modelToInterventionResponse(&intervention)
	}
	return responses, nil
}

func (s *service) UpdateIntervention(id uuid.UUID, request NumeracyInterventionRequest) (*NumeracyInterventionResponse, error) {
	intervention, err := s.repo.GetInterventionByID(id)
	if err != nil {
		return nil, err
	}

	intervention.StudentID = request.StudentID
	intervention.IndicatorID = request.IndicatorID
	intervention.InterventionType = request.InterventionType
	intervention.StartDate = request.StartDate
	intervention.EndDate = request.EndDate
	intervention.Status = request.Status
	intervention.Activities = request.Activities
	intervention.TeacherID = request.TeacherID
	intervention.Outcome = request.Outcome
	intervention.Effectiveness = request.Effectiveness

	err = s.repo.UpdateIntervention(intervention)
	if err != nil {
		return nil, err
	}

	return s.modelToInterventionResponse(intervention), nil
}

func (s *service) DeleteIntervention(id uuid.UUID) error {
	return s.repo.DeleteIntervention(id)
}

// Analytics operations
func (s *service) GetNumeracyAnalytics(request NumeracyAnalyticsRequest) (*NumeracyAnalyticsResponse, error) {
	return s.repo.GetNumeracyAnalytics(request)
}

// Helper functions to convert models to DTOs
func (s *service) modelToIndicatorResponse(indicator *NumeracyIndicator) *NumeracyIndicatorResponse {
	response := &NumeracyIndicatorResponse{
		ID:            indicator.ID,
		PhaseID:       indicator.PhaseID,
		NumeracyType:  indicator.NumeracyType,
		TypeName:      GetNumeracyTypeDescription(indicator.NumeracyType),
		IndicatorCode: indicator.IndicatorCode,
		IndicatorName: indicator.IndicatorName,
		Description:   indicator.Description,
		GradeLevel:    indicator.GradeLevel,
		MinAge:        indicator.MinAge,
		MaxAge:        indicator.MaxAge,
		Difficulty:    indicator.Difficulty,
		Examples:      indicator.Examples,
		IsActive:      indicator.IsActive,
		CreatedAt:     indicator.CreatedAt,
		UpdatedAt:     indicator.UpdatedAt,
	}

	if indicator.Phase != nil {
		response.PhaseName = indicator.Phase.Name
	}

	return response
}

func (s *service) modelToAssessmentResponse(assessment *NumeracyAssessment) *NumeracyAssessmentResponse {
	response := &NumeracyAssessmentResponse{
		ID:             assessment.ID,
		StudentID:      assessment.StudentID,
		IndicatorID:    assessment.IndicatorID,
		AssessmentDate: assessment.AssessmentDate,
		AssessmentType: assessment.AssessmentType,
		Score:          assessment.Score,
		MasteryLevel:   assessment.MasteryLevel,
		LevelName:      GetMasteryLevelDescription(assessment.MasteryLevel),
		ResponseTime:   assessment.ResponseTime,
		Attempts:       assessment.Attempts,
		TeacherID:      assessment.TeacherID,
		Notes:          assessment.Notes,
		EvidenceFiles:  assessment.EvidenceFiles,
		CreatedAt:      assessment.CreatedAt,
		UpdatedAt:      assessment.UpdatedAt,
	}

	if assessment.Student != nil {
		response.StudentName = assessment.Student.FullName
	}

	if assessment.Indicator != nil {
		response.IndicatorName = assessment.Indicator.IndicatorName
		response.IndicatorCode = assessment.Indicator.IndicatorCode
	}

	return response
}

func (s *service) modelToGrowthResponse(growth *NumeracyGrowth) *NumeracyGrowthResponse {
	response := &NumeracyGrowthResponse{
		ID:                growth.ID,
		StudentID:         growth.StudentID,
		Period:            growth.Period,
		AcademicYearID:    growth.AcademicYearID,
		OverallScore:      growth.OverallScore,
		NumbersScore:      growth.NumbersScore,
		OperationsScore:   growth.OperationsScore,
		GeometryScore:     growth.GeometryScore,
		MeasurementScore:  growth.MeasurementScore,
		DataAnalysisScore: growth.DataAnalysisScore,
		MasteryRate:       growth.MasteryRate,
		GrowthRate:        growth.GrowthRate,
		Percentile:        growth.Percentile,
		TeacherID:         growth.TeacherID,
		Notes:             growth.Notes,
		CreatedAt:         growth.CreatedAt,
		UpdatedAt:         growth.UpdatedAt,
	}

	if growth.Student != nil {
		response.StudentName = growth.Student.FullName
	}

	periodNames := map[string]string{
		"SEMESTER_1": "Semester 1",
		"SEMESTER_2": "Semester 2",
	}
	response.PeriodName = periodNames[growth.Period]

	return response
}

func (s *service) modelToInterventionResponse(intervention *NumeracyIntervention) *NumeracyInterventionResponse {
	response := &NumeracyInterventionResponse{
		ID:               intervention.ID,
		StudentID:        intervention.StudentID,
		IndicatorID:      intervention.IndicatorID,
		InterventionType: intervention.InterventionType,
		StartDate:        intervention.StartDate,
		EndDate:          intervention.EndDate,
		Status:           intervention.Status,
		Activities:       intervention.Activities,
		TeacherID:        intervention.TeacherID,
		Outcome:          intervention.Outcome,
		Effectiveness:    intervention.Effectiveness,
		CreatedAt:        intervention.CreatedAt,
		UpdatedAt:        intervention.UpdatedAt,
	}

	if intervention.Student != nil {
		response.StudentName = intervention.Student.FullName
	}

	if intervention.Indicator != nil {
		response.IndicatorName = intervention.Indicator.IndicatorName
		response.IndicatorCode = intervention.Indicator.IndicatorCode
	}

	typeNames := map[string]string{
		"REMEDIAL":   "Remedial",
		"ENRICHMENT": "Pengayaan",
	}
	response.TypeName = typeNames[intervention.InterventionType]

	statusNames := map[string]string{
		"PLANNED":   "Rencana",
		"ONGOING":   "Sedang Berjalan",
		"COMPLETED": "Selesai",
	}
	response.StatusName = statusNames[intervention.Status]

	return response
}
