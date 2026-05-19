package learning

import (
	"context"
	"errors"
	"fmt"
	"time"

	"sim-sekolah/internal/ai"
	"sim-sekolah/internal/deep_learning/tahapan_kognitif"
	"sim-sekolah/pkg/cache"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type LearningService interface {
	SaveTeachingModule(ctx context.Context, module *TeachingModule) error
	GenerateTeachingModuleAI(ctx context.Context, atpID uuid.UUID, schoolContext string) (string, error)
	SaveProjectModule(ctx context.Context, project *ProjectModule) error

	// ATP CRUD
	GetAllATP(classroomID string) ([]ATP, error)
	GetATPByID(id string) (*ATP, error)
	SaveATP(ctx context.Context, atp *ATP) error
	DeleteATP(ctx context.Context, id string) error
}

type learningService struct {
	db        *gorm.DB
	aiService ai.AIService
}

func NewLearningService(db *gorm.DB, aiService ai.AIService) LearningService {
	return &learningService{db: db, aiService: aiService}
}

func (s *learningService) SaveTeachingModule(ctx context.Context, module *TeachingModule) error {
	// 1. Validasi "Merefleksi" wajib ada dalam kegiatan
	hasRefleksi := false
	for _, activity := range module.Activities {
		var stage tahapan_kognitif.CognitiveStage
		if err := s.db.First(&stage, "id = ?", activity.StageID).Error; err == nil {
			if stage.Name == "Merefleksi" || stage.Name == "Reflecting" || stage.Name == "Menciptakan" || stage.Name == "Reflect" {
				hasRefleksi = true
				break
			}
		}
	}

	if !hasRefleksi && len(module.Activities) > 0 {
		return errors.New("modul ajar ditolak: tahap 'Merefleksi' wajib disertakan untuk memenuhi standar Deep Learning")
	}

	// 2. Simpan dengan transaksi
	return s.db.Transaction(func(tx *gorm.DB) error {
		if err := tx.Save(module).Error; err != nil {
			return err
		}
		return nil
	})
}

func (s *learningService) GenerateTeachingModuleAI(ctx context.Context, atpID uuid.UUID, schoolContext string) (string, error) {
	// 1. Fetch ATP details
	var atp ATP
	if err := s.db.Preload("Details.Objective").First(&atp, "id = ?", atpID).Error; err != nil {
		return "", err
	}

	// 2. Build prompt
	tpDescriptions := ""
	for i, d := range atp.Details {
		tpDescriptions += fmt.Sprintf("%d. %s\n", i+1, d.Objective.Description)
	}

	prompt := fmt.Sprintf(`
		Buatlah Modul Ajar (RPP) berskema PAIKEM untuk alur tujuan pembelajaran berikut:
		%s
		
		Konteks Spesifik Sekolah: %s
		
		Aturan Mutlak:
		1. Kegiatan HARUS dipetakan ke dalam 3 tahapan kognitif: Memahami, Mengaplikasi, Merefleksi.
		2. Manfaatkan elemen lingkungan sekitar sekolah secara eksplisit dalam kegiatan pembelajaran.
		3. Output harus dalam format narasi yang siap diedit oleh guru.
	`, tpDescriptions, schoolContext)

	// 3. Call AI Service
	return s.aiService.GenerateNarrative(ctx, ai.GenerateNarrativeRequest{
		GenerationType: "MODUL_AJAR",
		ContextData:    prompt,
	})
}

func (s *learningService) SaveProjectModule(ctx context.Context, project *ProjectModule) error {
	// Validasi P5 wajib >= 2 dimensi profil lulusan
	if len(project.Dimensions) < 2 {
		return errors.New("modul projek (P5) harus berelasi dengan minimal 2 Dimensi Profil Lulusan")
	}

	return s.db.Save(project).Error
}

func (s *learningService) GetAllATP(classroomID string) ([]ATP, error) {
	ctx := context.Background()
	cacheKey := fmt.Sprintf("atp:list:classroom:%s", classroomID)

	var cached []ATP
	if cache.GlobalCache != nil {
		if err := cache.GlobalCache.Get(ctx, cacheKey, &cached); err == nil {
			return cached, nil
		}
	}

	var results []ATP
	query := s.db.Preload("Subject")
	if classroomID != "" {
		query = query.Where("classroom_id = ?", classroomID)
	}
	err := query.Find(&results).Error

	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Set(ctx, cacheKey, results, 1*time.Hour)
	}

	return results, err
}

func (s *learningService) GetATPByID(id string) (*ATP, error) {
	var result ATP
	err := s.db.Preload("Subject").Preload("Classroom").Preload("Details.Objective").First(&result, "id = ?", id).Error
	return &result, err
}

func (s *learningService) SaveATP(ctx context.Context, atp *ATP) error {
	err := s.db.Transaction(func(tx *gorm.DB) error {
		// Clear existing details for replacement
		if atp.ID != uuid.Nil {
			tx.Where("atp_id = ?", atp.ID).Delete(&ATPDetail{})
		}
		return tx.Save(atp).Error
	})

	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.DeletePattern(context.Background(), "atp:list:*")
	}
	return err
}

func (s *learningService) DeleteATP(ctx context.Context, id string) error {
	var atp ATP
	if err := s.db.WithContext(ctx).First(&atp, "id = ?", id).Error; err != nil {
		return err
	}

	updates := map[string]interface{}{
		"deleted_at": time.Now(),
	}
	if userID, ok := ctx.Value("user_id").(string); ok && userID != "" {
		updates["deleted_by"] = userID
	}

	err := s.db.WithContext(ctx).Model(&atp).Updates(updates).Error
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.DeletePattern(context.Background(), "atp:list:*")
	}
	return err
}
