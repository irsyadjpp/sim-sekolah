package promotion

import (
	"context"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type PromotionRepository interface {
	PromoteStudents(ctx context.Context, sourceClassroomID, targetClassroomID string, studentIDs []uuid.UUID, operatorID uuid.UUID) error
	GraduateStudents(ctx context.Context, studentIDs []uuid.UUID) error
}

type promotionRepository struct {
	db *gorm.DB
}

func NewPromotionRepository(db *gorm.DB) PromotionRepository {
	return &promotionRepository{db: db}
}

func (r *promotionRepository) PromoteStudents(ctx context.Context, sourceClassroomID, targetClassroomID string, studentIDs []uuid.UUID, operatorID uuid.UUID) error {
	return r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		sourceUUID := uuid.MustParse(sourceClassroomID)
		targetUUID := uuid.MustParse(targetClassroomID)

		type Enrollment struct {
			ID          uuid.UUID `gorm:"column:id;primaryKey"`
			ClassroomID uuid.UUID `gorm:"column:classroom_id"`
			StudentID   uuid.UUID `gorm:"column:student_id"`
		}

		for _, studentID := range studentIDs {
			// 1. Hapus pendaftaran lama di kelas tujuan jika ada (idempotency)
			if err := tx.Exec("DELETE FROM trx_enrollment WHERE classroom_id = ? AND student_id = ?", targetUUID, studentID).Error; err != nil {
				return err
			}

			// 2. Buat pendaftaran kelas baru
			newEnrollment := Enrollment{
				ID:          uuid.New(),
				ClassroomID: targetUUID,
				StudentID:   studentID,
			}
			if err := tx.Table("trx_enrollment").Create(&newEnrollment).Error; err != nil {
				return err
			}

			// 3. Catat log promosi akademik
			newLog := AcademicPromotionLog{
				ID:                uuid.New(),
				StudentID:         studentID,
				SourceClassroomID: sourceUUID,
				TargetClassroomID: targetUUID,
				PromotedBy:        operatorID,
			}
			if err := tx.Create(&newLog).Error; err != nil {
				return err
			}

			// 4. Pastikan status siswa diatur ke active
			if err := tx.Exec("UPDATE master_student SET student_status = 'active' WHERE id = ?", studentID).Error; err != nil {
				return err
			}
		}

		return nil
	})
}

func (r *promotionRepository) GraduateStudents(ctx context.Context, studentIDs []uuid.UUID) error {
	return r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		if len(studentIDs) == 0 {
			return nil
		}

		// Update status siswa ke graduated secara massal
		return tx.Exec("UPDATE master_student SET student_status = 'graduated' WHERE id IN ?", studentIDs).Error
	})
}
