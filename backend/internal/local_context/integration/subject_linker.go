package integration

import (
	"context"
	"errors"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// SubjectContextLinker handles linking local contexts to subjects
type SubjectContextLinker struct {
	db *gorm.DB
}

func NewSubjectContextLinker(db *gorm.DB) *SubjectContextLinker {
	return &SubjectContextLinker{db: db}
}

// LinkContextToSubject links a local context to a subject
// This would typically update the subject's local_context_ids array field
func (s *SubjectContextLinker) LinkContextToSubject(ctx context.Context, subjectID, contextID uuid.UUID) error {
	// In PostgreSQL with UUID array, we need to use raw SQL
	query := `
		UPDATE master_subject
		SET local_context_ids = array_append(
			COALESCE(local_context_ids, ARRAY[]::uuid[]),
			$1
		)
		WHERE id = $2 AND NOT ($1 = ANY(local_context_ids))
	`
	return s.db.WithContext(ctx).Exec(query, contextID, subjectID).Error
}

// UnlinkContextFromSubject unlinks a local context from a subject
func (s *SubjectContextLinker) UnlinkContextFromSubject(ctx context.Context, subjectID, contextID uuid.UUID) error {
	query := `
		UPDATE master_subject
		SET local_context_ids = array_remove(local_context_ids, $1)
		WHERE id = $2
	`
	return s.db.WithContext(ctx).Exec(query, contextID, subjectID).Error
}

// GetContextsBySubject retrieves all local contexts linked to a subject
func (s *SubjectContextLinker) GetContextsBySubject(ctx context.Context, subjectID uuid.UUID) ([]uuid.UUID, error) {
	var contextIDs []uuid.UUID
	query := `
		SELECT local_context_ids
		FROM master_subject
		WHERE id = $1
	`
	err := s.db.WithContext(ctx).Raw(query, subjectID).Scan(&contextIDs).Error
	return contextIDs, err
}

// GetSubjectsByContext retrieves all subjects that use a specific local context
func (s *SubjectContextLinker) GetSubjectsByContext(ctx context.Context, contextID uuid.UUID) ([]uuid.UUID, error) {
	var subjectIDs []uuid.UUID
	query := `
		SELECT id
		FROM master_subject
		WHERE $1 = ANY(local_context_ids)
	`
	err := s.db.WithContext(ctx).Raw(query, contextID).Scan(&subjectIDs).Error
	return subjectIDs, err
}

// CreateSubjectContextUtilization records when a context is used in a subject
func (s *SubjectContextLinker) CreateSubjectContextUtilization(ctx context.Context, contextID, subjectID uuid.UUID, utilizationType, description string) error {
	// Check if utilization record already exists
	var count int64
	checkQuery := `
		SELECT COUNT(*)
		FROM trx_local_context_utilization
		WHERE context_id = $1 AND subject_id = $2 AND utilization_type = $3
	`
	err := s.db.WithContext(ctx).Raw(checkQuery, contextID, subjectID, utilizationType).Scan(&count).Error
	if err != nil {
		return err
	}

	if count > 0 {
		return errors.New("utilization record already exists")
	}

	query := `
		INSERT INTO trx_local_context_utilization (context_id, subject_id, utilization_type, description)
		VALUES ($1, $2, $3, $4)
	`
	return s.db.WithContext(ctx).Exec(query, contextID, subjectID, utilizationType, description).Error
}

// GetSubjectUtilizationSummary provides utilization statistics for a subject
func (s *SubjectContextLinker) GetSubjectUtilizationSummary(ctx context.Context, subjectID uuid.UUID) (map[string]interface{}, error) {
	query := `
		SELECT
			COUNT(*) as total_utilizations,
			COUNT(DISTINCT context_id) as unique_contexts,
			utilization_type
		FROM trx_local_context_utilization
		WHERE subject_id = $1
		GROUP BY utilization_type
	`

	var results []struct {
		TotalUtilizations int64  `json:"total_utilizations"`
		UniqueContexts    int64  `json:"unique_contexts"`
		UtilizationType   string `json:"utilization_type"`
	}

	err := s.db.WithContext(ctx).Raw(query, subjectID).Scan(&results).Error
	if err != nil {
		return nil, err
	}

	summary := make(map[string]interface{})
	summary["by_type"] = results
	summary["total"] = len(results)

	return summary, nil
}

// GetContextUtilizationAcrossSubjects provides statistics about how a context is used across subjects
func (s *SubjectContextLinker) GetContextUtilizationAcrossSubjects(ctx context.Context, contextID uuid.UUID) (map[string]interface{}, error) {
	query := `
		SELECT
			COUNT(*) as total_usages,
			COUNT(DISTINCT subject_id) as unique_subjects,
			utilization_type
		FROM trx_local_context_utilization
		WHERE context_id = $1
		GROUP BY utilization_type
	`

	var results []struct {
		TotalUsages     int64  `json:"total_usages"`
		UniqueSubjects  int64  `json:"unique_subjects"`
		UtilizationType string `json:"utilization_type"`
	}

	err := s.db.WithContext(ctx).Raw(query, contextID).Scan(&results).Error
	if err != nil {
		return nil, err
	}

	summary := make(map[string]interface{})
	summary["by_type"] = results
	summary["total"] = len(results)

	return summary, nil
}
