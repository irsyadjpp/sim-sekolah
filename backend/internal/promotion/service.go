package promotion

import (
	"context"
	"errors"

	"github.com/google/uuid"
)

type PromotionService interface {
	PromoteStudents(ctx context.Context, req PromoteRequest, operatorID string) error
	GraduateStudents(ctx context.Context, req GraduateRequest) error
}

type promotionService struct {
	repo PromotionRepository
}

func NewPromotionService(repo PromotionRepository) PromotionService {
	return &promotionService{repo: repo}
}

func (s *promotionService) PromoteStudents(ctx context.Context, req PromoteRequest, operatorID string) error {
	opUUID, err := uuid.Parse(operatorID)
	if err != nil {
		return errors.New("invalid operator ID")
	}

	var studentUUIDs []uuid.UUID
	for _, idStr := range req.StudentIDs {
		u, err := uuid.Parse(idStr)
		if err != nil {
			return errors.New("invalid student ID: " + idStr)
		}
		studentUUIDs = append(studentUUIDs, u)
	}

	return s.repo.PromoteStudents(ctx, req.SourceClassroomID, req.TargetClassroomID, studentUUIDs, opUUID)
}

func (s *promotionService) GraduateStudents(ctx context.Context, req GraduateRequest) error {
	var studentUUIDs []uuid.UUID
	for _, idStr := range req.StudentIDs {
		u, err := uuid.Parse(idStr)
		if err != nil {
			return errors.New("invalid student ID: " + idStr)
		}
		studentUUIDs = append(studentUUIDs, u)
	}

	return s.repo.GraduateStudents(ctx, studentUUIDs)
}
