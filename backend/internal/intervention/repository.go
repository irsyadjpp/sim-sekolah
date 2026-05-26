package intervention

import (
	"database/sql"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type InterventionRepository interface {
	// RemedialProgram operations
	CreateRemedialProgram(program *RemedialProgram) error
	GetRemedialProgramByID(id uuid.UUID) (*RemedialProgram, error)
	GetAllRemedialPrograms() ([]RemedialProgram, error)
	UpdateRemedialProgram(program *RemedialProgram) error
	DeleteRemedialProgram(id uuid.UUID) error

	// EnrichmentProgram operations
	CreateEnrichmentProgram(program *EnrichmentProgram) error
	GetEnrichmentProgramByID(id uuid.UUID) (*EnrichmentProgram, error)
	GetAllEnrichmentPrograms() ([]EnrichmentProgram, error)
	UpdateEnrichmentProgram(program *EnrichmentProgram) error
	DeleteEnrichmentProgram(id uuid.UUID) error

	// StudentInterventionAssignment operations
	CreateStudentAssignment(assignment *StudentInterventionAssignment) error
	GetStudentAssignmentByID(id uuid.UUID) (*StudentInterventionAssignment, error)
	GetAssignmentsByStudent(studentID uuid.UUID) ([]StudentInterventionAssignment, error)
	GetAssignmentsByType(interventionType string) ([]StudentInterventionAssignment, error)
	UpdateStudentAssignment(assignment *StudentInterventionAssignment) error
	DeleteStudentAssignment(id uuid.UUID) error

	// Summary operations
	GetInterventionSummary(schoolID uuid.UUID) (*InterventionSummaryResponse, error)
}

type interventionRepository struct {
	db *gorm.DB
}

func NewInterventionRepository(db *gorm.DB) InterventionRepository {
	return &interventionRepository{db: db}
}

// RemedialProgram operations
func (r *interventionRepository) CreateRemedialProgram(program *RemedialProgram) error {
	return r.db.Create(program).Error
}

func (r *interventionRepository) GetRemedialProgramByID(id uuid.UUID) (*RemedialProgram, error) {
	var program RemedialProgram
	err := r.db.Where("id = ?", id).First(&program).Error
	if err != nil {
		return nil, err
	}
	return &program, nil
}

func (r *interventionRepository) GetAllRemedialPrograms() ([]RemedialProgram, error) {
	var programs []RemedialProgram
	err := r.db.Find(&programs).Error
	return programs, err
}

func (r *interventionRepository) UpdateRemedialProgram(program *RemedialProgram) error {
	return r.db.Save(program).Error
}

func (r *interventionRepository) DeleteRemedialProgram(id uuid.UUID) error {
	return r.db.Delete(&RemedialProgram{}, "id = ?", id).Error
}

// EnrichmentProgram operations
func (r *interventionRepository) CreateEnrichmentProgram(program *EnrichmentProgram) error {
	return r.db.Create(program).Error
}

func (r *interventionRepository) GetEnrichmentProgramByID(id uuid.UUID) (*EnrichmentProgram, error) {
	var program EnrichmentProgram
	err := r.db.Where("id = ?", id).First(&program).Error
	if err != nil {
		return nil, err
	}
	return &program, nil
}

func (r *interventionRepository) GetAllEnrichmentPrograms() ([]EnrichmentProgram, error) {
	var programs []EnrichmentProgram
	err := r.db.Find(&programs).Error
	return programs, err
}

func (r *interventionRepository) UpdateEnrichmentProgram(program *EnrichmentProgram) error {
	return r.db.Save(program).Error
}

func (r *interventionRepository) DeleteEnrichmentProgram(id uuid.UUID) error {
	return r.db.Delete(&EnrichmentProgram{}, "id = ?", id).Error
}

// StudentInterventionAssignment operations
func (r *interventionRepository) CreateStudentAssignment(assignment *StudentInterventionAssignment) error {
	return r.db.Create(assignment).Error
}

func (r *interventionRepository) GetStudentAssignmentByID(id uuid.UUID) (*StudentInterventionAssignment, error) {
	var assignment StudentInterventionAssignment
	err := r.db.Where("id = ?", id).First(&assignment).Error
	if err != nil {
		return nil, err
	}
	return &assignment, nil
}

func (r *interventionRepository) GetAssignmentsByStudent(studentID uuid.UUID) ([]StudentInterventionAssignment, error) {
	var assignments []StudentInterventionAssignment
	err := r.db.Where("student_id = ?", studentID).Order("assignment_date DESC").Find(&assignments).Error
	return assignments, err
}

func (r *interventionRepository) GetAssignmentsByType(interventionType string) ([]StudentInterventionAssignment, error) {
	var assignments []StudentInterventionAssignment
	err := r.db.Where("intervention_type = ?", interventionType).Find(&assignments).Error
	return assignments, err
}

func (r *interventionRepository) UpdateStudentAssignment(assignment *StudentInterventionAssignment) error {
	return r.db.Save(assignment).Error
}

func (r *interventionRepository) DeleteStudentAssignment(id uuid.UUID) error {
	return r.db.Delete(&StudentInterventionAssignment{}, "id = ?", id).Error
}

// Summary operations
func (r *interventionRepository) GetInterventionSummary(schoolID uuid.UUID) (*InterventionSummaryResponse, error) {
	var summary InterventionSummaryResponse

	// Count total assignments
	if err := r.db.Model(&StudentInterventionAssignment{}).Count(&summary.TotalAssignments).Error; err != nil {
		return nil, err
	}

	// Count remedial assignments
	if err := r.db.Model(&StudentInterventionAssignment{}).Where("intervention_type = ?", InterventionTypeRemedial).Count(&summary.RemedialAssignments).Error; err != nil {
		return nil, err
	}

	// Count enrichment assignments
	if err := r.db.Model(&StudentInterventionAssignment{}).Where("intervention_type = ?", InterventionTypeEnrichment).Count(&summary.EnrichmentAssignments).Error; err != nil {
		return nil, err
	}

	// Count active interventions
	if err := r.db.Model(&StudentInterventionAssignment{}).Where("status = ?", InterventionStatusActive).Count(&summary.ActiveInterventions).Error; err != nil {
		return nil, err
	}

	// Count completed interventions
	if err := r.db.Model(&StudentInterventionAssignment{}).Where("status = ?", InterventionStatusCompleted).Count(&summary.CompletedInterventions).Error; err != nil {
		return nil, err
	}

	// Calculate average improvement
	var avgImprovement sql.NullFloat64
	if err := r.db.Model(&StudentInterventionAssignment{}).
		Select("AVG(current_score - baseline_score)").
		Where("current_score IS NOT NULL AND baseline_score IS NOT NULL").
		Scan(&avgImprovement).Error; err != nil {
		return nil, err
	}
	if avgImprovement.Valid {
		summary.AverageImprovement = avgImprovement.Float64
	}

	// Calculate success rate (assignments where current_score >= target_score)
	var successCount int64
	var completedCount int64
	r.db.Model(&StudentInterventionAssignment{}).
		Where("status = ? AND current_score >= target_score", InterventionStatusCompleted).
		Count(&successCount)
	r.db.Model(&StudentInterventionAssignment{}).
		Where("status = ?", InterventionStatusCompleted).
		Count(&completedCount)

	if completedCount > 0 {
		summary.SuccessRate = float64(successCount) / float64(completedCount) * 100
	}

	return &summary, nil
}
