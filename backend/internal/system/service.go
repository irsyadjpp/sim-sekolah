package system

import (
	"context"
	"time"

	"sim-sekolah/internal/common"

	"github.com/redis/go-redis/v9"
)

type SystemService interface {
	GetPimpinanDashboard(ctx context.Context) (map[string]interface{}, error)
	GetGuruDashboard(ctx context.Context) (map[string]interface{}, error)
	GetOperatorDashboard(ctx context.Context) (map[string]interface{}, error)
}

type systemService struct {
	repo SystemRepository
	rdb  *redis.Client
}

func NewSystemService(repo SystemRepository, rdb *redis.Client) SystemService {
	return &systemService{repo: repo, rdb: rdb}
}

func (s *systemService) GetPimpinanDashboard(ctx context.Context) (map[string]interface{}, error) {
	cacheKey := "dashboard:pimpinan"
	return common.GetOrSetCache(ctx, s.rdb, cacheKey, 10*time.Minute, func() (map[string]interface{}, error) {
		// GetPimpinanKSP is commented out due to missing trx_ksp_document table in normalized schema
		// kspProgress, err := s.repo.GetPimpinanKSP(ctx)
		// if err != nil {
		// 	return nil, err
		// }
		kspProgress := []map[string]interface{}{} // Empty placeholder

		// Commented out due to missing tables in normalized schema
		// cognitiveStats, err := s.repo.GetPimpinanCognitive(ctx)
		// if err != nil {
		// 	return nil, err
		// }
		cognitiveStats := []map[string]interface{}{} // Empty placeholder

		p5Stats, err := s.repo.GetPimpinanP5(ctx)
		if err != nil {
			return nil, err
		}

		designElements := []map[string]interface{}{
			{"label": "Praktik Pedagogis", "value": 42, "color": "var(--mui-palette-primary-main)"},
			{"label": "Lingkungan Belajar (Pesisir Pantai)", "value": 35, "color": "var(--mui-palette-success-main)", "highlight": true},
			{"label": "Kemitraan Belajar (Wali & Komite)", "value": 28, "color": "var(--mui-palette-secondary-main)"},
			{"label": "Pemanfaatan Digital (Lokal Intranet)", "value": 12, "color": "orange"},
		}

		return map[string]interface{}{
			"ksp_progress":            kspProgress,
			"cognitive_stats":         cognitiveStats,
			"p5_character_stats":      p5Stats,
			"design_elements_mapping": designElements,
		}, nil
	})
}

func (s *systemService) GetGuruDashboard(ctx context.Context) (map[string]interface{}, error) {
	cacheKey := "dashboard:guru"
	return common.GetOrSetCache(ctx, s.rdb, cacheKey, 10*time.Minute, func() (map[string]interface{}, error) {
		// Commented out due to missing tables in normalized schema
		// moduleCompliance, err := s.repo.GetGuruCompliance(ctx)
		// if err != nil {
		// 	return nil, err
		// }
		moduleCompliance := []map[string]interface{}{} // Empty placeholder

		// Commented out due to missing tables in normalized schema
		// studentWatch, err := s.repo.GetGuruStudentWatch(ctx)
		// if err != nil {
		// 	return nil, err
		// }
		studentWatch := []map[string]interface{}{} // Empty placeholder

		automationQueue, err := s.repo.GetGuruAutomationQueue(ctx)
		if err != nil {
			return nil, err
		}

		mindfulObservations := []map[string]interface{}{
			{
				"aspect":     "Berkesadaran (Mindful)",
				"percentage": 90,
				"ref":        "Anak-anak hening sejenak mendengarkan deru ombak pantai Bonerate sebelum mulai menggambar pola laut.",
			},
			{
				"aspect":     "Bermakna (Meaningful)",
				"percentage": 85,
				"ref":        "Belajar operasi matematika langsung menggunakan media kerang dan pasir pantai.",
			},
			{
				"aspect":     "Menggembirakan (Joyful)",
				"percentage": 95,
				"ref":        "Eksplorasi langsung biotopo pantai pesisir sangat memicu rasa ingin tahu siswa kelas IV!",
			},
		}

		return map[string]interface{}{
			"module_compliance":    moduleCompliance,
			"student_watch":        studentWatch,
			"automation_queue":     automationQueue,
			"mindful_observations": mindfulObservations,
		}, nil
	})
}

func (s *systemService) GetOperatorDashboard(ctx context.Context) (map[string]interface{}, error) {
	cacheKey := "dashboard:operator"
	return common.GetOrSetCache(ctx, s.rdb, cacheKey, 10*time.Minute, func() (map[string]interface{}, error) {
		dataCompleteness, err := s.repo.GetOperatorDataCompleteness(ctx)
		if err != nil {
			return nil, err
		}

		telemetries, err := s.repo.GetOperatorTelemetry(ctx)
		if err != nil {
			return nil, err
		}

		servicesHealth := []map[string]interface{}{
			{
				"service": "Database Utama (PostgreSQL)",
				"desc":    "Menampung seluruh tabel data induk sekolah",
				"status":  "Berjalan",
			},
			{
				"service": "Mesin Otomasi Sistem (Lokal)",
				"desc":    "Penyusun dokumen KSP & modul ajar mandiri secara asinkron",
				"status":  "Berjalan",
			},
			{
				"service": "Antrean Pesan Lokal (Redis)",
				"desc":    "Manajer antrean tugas operasional intranet",
				"status":  "Berjalan",
			},
		}

		return map[string]interface{}{
			"data_completeness": dataCompleteness,
			"server_telemetry":  telemetries,
			"services_health":   servicesHealth,
		}, nil
	})
}
