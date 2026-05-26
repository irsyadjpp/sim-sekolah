package teaching_reflection

import (
	"github.com/google/uuid"
)

type TeachingReflectionService interface {
	CreateReflection(request *TeachingReflectionRequest) (*TeachingReflectionResponse, error)
	GetReflectionByID(id string) (*TeachingReflectionResponse, error)
	GetReflectionsByTeacher(teacherID string) ([]TeachingReflectionResponse, error)
	UpdateReflection(id string, request *TeachingReflectionRequest) (*TeachingReflectionResponse, error)
	DeleteReflection(id string) error
	GetReflectionSummary(teacherID string) (*ReflectionSummaryResponse, error)
}

type teachingReflectionService struct {
	repo TeachingReflectionRepository
}

func NewTeachingReflectionService(repo TeachingReflectionRepository) TeachingReflectionService {
	return &teachingReflectionService{repo: repo}
}

func reflectionToResponse(reflection *TeachingReflection) *TeachingReflectionResponse {
	var subjectID *string
	if reflection.SubjectID != nil {
		subjID := reflection.SubjectID.String()
		subjectID = &subjID
	}

	var classroomID *string
	if reflection.ClassroomID != nil {
		classID := reflection.ClassroomID.String()
		classroomID = &classID
	}

	return &TeachingReflectionResponse{
		ID:                 reflection.ID.String(),
		TeacherID:          reflection.TeacherID.String(),
		SubjectID:          subjectID,
		ClassroomID:        classroomID,
		ReflectionDate:     reflection.ReflectionDate,
		ReflectionType:     reflection.ReflectionType,
		Status:             reflection.Status,
		LessonTopic:        reflection.LessonTopic,
		WhatWentWell:       reflection.WhatWentWell,
		WhatCouldImprove:   reflection.WhatCouldImprove,
		StudentEngagement:  reflection.StudentEngagement,
		TeachingStrategies: reflection.TeachingStrategies,
		Challenges:         reflection.Challenges,
		Solutions:          reflection.Solutions,
		NextSteps:          reflection.NextSteps,
		SelfRating:         reflection.SelfRating,
		Notes:              reflection.Notes,
		IsPrivate:          reflection.IsPrivate,
		CreatedAt:          reflection.CreatedAt,
		UpdatedAt:          reflection.UpdatedAt,
	}
}

func (s *teachingReflectionService) CreateReflection(request *TeachingReflectionRequest) (*TeachingReflectionResponse, error) {
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

	reflection := &TeachingReflection{
		TeacherID:          uuid.MustParse(request.TeacherID),
		SubjectID:          subjectID,
		ClassroomID:        classroomID,
		ReflectionDate:     request.ReflectionDate,
		ReflectionType:     request.ReflectionType,
		Status:             request.Status,
		LessonTopic:        request.LessonTopic,
		WhatWentWell:       request.WhatWentWell,
		WhatCouldImprove:   request.WhatCouldImprove,
		StudentEngagement:  request.StudentEngagement,
		TeachingStrategies: request.TeachingStrategies,
		Challenges:         request.Challenges,
		Solutions:          request.Solutions,
		NextSteps:          request.NextSteps,
		SelfRating:         request.SelfRating,
		Notes:              request.Notes,
		IsPrivate:          request.IsPrivate,
	}

	if err := s.repo.CreateReflection(reflection); err != nil {
		return nil, err
	}

	return reflectionToResponse(reflection), nil
}

func (s *teachingReflectionService) GetReflectionByID(id string) (*TeachingReflectionResponse, error) {
	reflectionID, err := uuid.Parse(id)
	if err != nil {
		return nil, err
	}

	reflection, err := s.repo.GetReflectionByID(reflectionID)
	if err != nil {
		return nil, err
	}

	return reflectionToResponse(reflection), nil
}

func (s *teachingReflectionService) GetReflectionsByTeacher(teacherID string) ([]TeachingReflectionResponse, error) {
	teacherUUID, err := uuid.Parse(teacherID)
	if err != nil {
		return nil, err
	}

	reflections, err := s.repo.GetReflectionsByTeacher(teacherUUID)
	if err != nil {
		return nil, err
	}

	responses := make([]TeachingReflectionResponse, len(reflections))
	for i, reflection := range reflections {
		responses[i] = *reflectionToResponse(&reflection)
	}

	return responses, nil
}

func (s *teachingReflectionService) UpdateReflection(id string, request *TeachingReflectionRequest) (*TeachingReflectionResponse, error) {
	reflectionID, err := uuid.Parse(id)
	if err != nil {
		return nil, err
	}

	reflection, err := s.repo.GetReflectionByID(reflectionID)
	if err != nil {
		return nil, err
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

	reflection.TeacherID = uuid.MustParse(request.TeacherID)
	reflection.SubjectID = subjectID
	reflection.ClassroomID = classroomID
	reflection.ReflectionDate = request.ReflectionDate
	reflection.ReflectionType = request.ReflectionType
	reflection.Status = request.Status
	reflection.LessonTopic = request.LessonTopic
	reflection.WhatWentWell = request.WhatWentWell
	reflection.WhatCouldImprove = request.WhatCouldImprove
	reflection.StudentEngagement = request.StudentEngagement
	reflection.TeachingStrategies = request.TeachingStrategies
	reflection.Challenges = request.Challenges
	reflection.Solutions = request.Solutions
	reflection.NextSteps = request.NextSteps
	reflection.SelfRating = request.SelfRating
	reflection.Notes = request.Notes
	reflection.IsPrivate = request.IsPrivate

	if err := s.repo.UpdateReflection(reflection); err != nil {
		return nil, err
	}

	return reflectionToResponse(reflection), nil
}

func (s *teachingReflectionService) DeleteReflection(id string) error {
	reflectionID, err := uuid.Parse(id)
	if err != nil {
		return err
	}

	return s.repo.DeleteReflection(reflectionID)
}

func (s *teachingReflectionService) GetReflectionSummary(teacherID string) (*ReflectionSummaryResponse, error) {
	teacherUUID, err := uuid.Parse(teacherID)
	if err != nil {
		return nil, err
	}

	return s.repo.GetReflectionSummary(teacherUUID)
}
