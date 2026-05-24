package integration

import (
	"context"
	"errors"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// ActivityContextLinker handles linking local contexts to teaching module activities
type ActivityContextLinker struct {
	db *gorm.DB
}

func NewActivityContextLinker(db *gorm.DB) *ActivityContextLinker {
	return &ActivityContextLinker{db: db}
}

// LinkContextToModule links a local context to a teaching module
func (a *ActivityContextLinker) LinkContextToModule(ctx context.Context, moduleID, contextID uuid.UUID) error {
	query := `
		UPDATE trx_teaching_module
		SET local_context_ids = array_append(
			COALESCE(local_context_ids, ARRAY[]::uuid[]),
			$1
		)
		WHERE id = $2 AND NOT ($1 = ANY(local_context_ids))
	`
	return a.db.WithContext(ctx).Exec(query, contextID, moduleID).Error
}

// UnlinkContextFromModule unlinks a local context from a teaching module
func (a *ActivityContextLinker) UnlinkContextFromModule(ctx context.Context, moduleID, contextID uuid.UUID) error {
	query := `
		UPDATE trx_teaching_module
		SET local_context_ids = array_remove(local_context_ids, $1)
		WHERE id = $2
	`
	return a.db.WithContext(ctx).Exec(query, contextID, moduleID).Error
}

// GetContextsByModule retrieves all local contexts linked to a teaching module
func (a *ActivityContextLinker) GetContextsByModule(ctx context.Context, moduleID uuid.UUID) ([]uuid.UUID, error) {
	var contextIDs []uuid.UUID
	query := `
		SELECT local_context_ids
		FROM trx_teaching_module
		WHERE id = $1
	`
	err := a.db.WithContext(ctx).Raw(query, moduleID).Scan(&contextIDs).Error
	return contextIDs, err
}

// GetModulesByContext retrieves all teaching modules that use a specific local context
func (a *ActivityContextLinker) GetModulesByContext(ctx context.Context, contextID uuid.UUID) ([]uuid.UUID, error) {
	var moduleIDs []uuid.UUID
	query := `
		SELECT id
		FROM trx_teaching_module
		WHERE $1 = ANY(local_context_ids)
	`
	err := a.db.WithContext(ctx).Raw(query, contextID).Scan(&moduleIDs).Error
	return moduleIDs, err
}

// CreateModuleContextUtilization records when a context is used in a module
func (a *ActivityContextLinker) CreateModuleContextUtilization(ctx context.Context, contextID, moduleID uuid.UUID, utilizationType, description string) error {
	// Check if utilization record already exists
	var count int64
	checkQuery := `
		SELECT COUNT(*)
		FROM trx_local_context_utilization
		WHERE context_id = $1 AND module_id = $2 AND utilization_type = $3
	`
	err := a.db.WithContext(ctx).Raw(checkQuery, contextID, moduleID, utilizationType).Scan(&count).Error
	if err != nil {
		return err
	}

	if count > 0 {
		return errors.New("utilization record already exists")
	}

	query := `
		INSERT INTO trx_local_context_utilization (context_id, module_id, utilization_type, description)
		VALUES ($1, $2, $3, $4)
	`
	return a.db.WithContext(ctx).Exec(query, contextID, moduleID, utilizationType, description).Error
}

// GetModuleUtilizationSummary provides utilization statistics for a module
func (a *ActivityContextLinker) GetModuleUtilizationSummary(ctx context.Context, moduleID uuid.UUID) (map[string]interface{}, error) {
	query := `
		SELECT
			COUNT(*) as total_utilizations,
			COUNT(DISTINCT context_id) as unique_contexts,
			utilization_type
		FROM trx_local_context_utilization
		WHERE module_id = $1
		GROUP BY utilization_type
	`

	var results []struct {
		TotalUtilizations int64  `json:"total_utilizations"`
		UniqueContexts    int64  `json:"unique_contexts"`
		UtilizationType   string `json:"utilization_type"`
	}

	err := a.db.WithContext(ctx).Raw(query, moduleID).Scan(&results).Error
	if err != nil {
		return nil, err
	}

	summary := make(map[string]interface{})
	summary["by_type"] = results
	summary["total"] = len(results)

	return summary, nil
}

// GetContextUtilizationAcrossModules provides statistics about how a context is used across modules
func (a *ActivityContextLinker) GetContextUtilizationAcrossModules(ctx context.Context, contextID uuid.UUID) (map[string]interface{}, error) {
	query := `
		SELECT
			COUNT(*) as total_usages,
			COUNT(DISTINCT module_id) as unique_modules,
			utilization_type
		FROM trx_local_context_utilization
		WHERE context_id = $1
		GROUP BY utilization_type
	`

	var results []struct {
		TotalUsages     int64  `json:"total_usages"`
		UniqueModules   int64  `json:"unique_modules"`
		UtilizationType string `json:"utilization_type"`
	}

	err := a.db.WithContext(ctx).Raw(query, contextID).Scan(&results).Error
	if err != nil {
		return nil, err
	}

	summary := make(map[string]interface{})
	summary["by_type"] = results
	summary["total"] = len(results)

	return summary, nil
}

// GetOverallContextUtilization provides overall statistics about context usage
func (a *ActivityContextLinker) GetOverallContextUtilization(ctx context.Context) (map[string]interface{}, error) {
	query := `
		SELECT
			COUNT(*) as total_utilizations,
			COUNT(DISTINCT context_id) as unique_contexts,
			COUNT(DISTINCT subject_id) as subjects_using,
			COUNT(DISTINCT module_id) as modules_using
		FROM trx_local_context_utilization
	`

	var result struct {
		TotalUtilizations int64 `json:"total_utilizations"`
		UniqueContexts    int64 `json:"unique_contexts"`
		SubjectsUsing     int64 `json:"subjects_using"`
		ModulesUsing      int64 `json:"modules_using"`
	}

	err := a.db.WithContext(ctx).Raw(query).Scan(&result).Error
	if err != nil {
		return nil, err
	}

	summary := make(map[string]interface{})
	summary["total_utilizations"] = result.TotalUtilizations
	summary["unique_contexts"] = result.UniqueContexts
	summary["subjects_using"] = result.SubjectsUsing
	summary["modules_using"] = result.ModulesUsing

	return summary, nil
}

// GetMostUsedContexts retrieves the most frequently used local contexts
func (a *ActivityContextLinker) GetMostUsedContexts(ctx context.Context, limit int) ([]map[string]interface{}, error) {
	query := `
		SELECT
			lc.id,
			lc.title,
			COUNT(DISTINCT lcu.subject_id) + COUNT(DISTINCT lcu.module_id) as usage_count
		FROM master_local_context lc
		LEFT JOIN trx_local_context_utilization lcu ON lc.id = lcu.context_id
		GROUP BY lc.id, lc.title
		ORDER BY usage_count DESC
		LIMIT $1
	`

	var results []struct {
		ID         uuid.UUID `json:"id"`
		Title      string    `json:"title"`
		UsageCount int64     `json:"usage_count"`
	}

	err := a.db.WithContext(ctx).Raw(query, limit).Scan(&results).Error
	if err != nil {
		return nil, err
	}

	summary := make([]map[string]interface{}, len(results))
	for i, r := range results {
		summary[i] = map[string]interface{}{
			"id":          r.ID,
			"title":       r.Title,
			"usage_count": r.UsageCount,
		}
	}

	return summary, nil
}
