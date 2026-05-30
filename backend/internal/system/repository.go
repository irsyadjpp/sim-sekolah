package system

import (
	"context"
	"time"

	"sim-sekolah/pkg/logger"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type SystemRepository interface {
	InitViewsAndSeed(ctx context.Context) error
	GetPimpinanKSP(ctx context.Context) ([]map[string]interface{}, error)
	GetPimpinanCognitive(ctx context.Context) ([]map[string]interface{}, error)
	GetPimpinanP5(ctx context.Context) ([]map[string]interface{}, error)
	GetGuruCompliance(ctx context.Context) ([]map[string]interface{}, error)
	GetGuruStudentWatch(ctx context.Context) ([]map[string]interface{}, error)
	GetGuruAutomationQueue(ctx context.Context) ([]AutomationQueue, error)
	GetOperatorDataCompleteness(ctx context.Context) ([]map[string]interface{}, error)
	GetOperatorTelemetry(ctx context.Context) ([]ServerTelemetry, error)
}

type systemRepository struct {
	db *gorm.DB
}

func NewSystemRepository(db *gorm.DB) SystemRepository {
	return &systemRepository{db: db}
}

func (r *systemRepository) GetPimpinanKSP(ctx context.Context) ([]map[string]interface{}, error) {
	var results []map[string]interface{}
	err := r.db.WithContext(ctx).Table("vw_dashboard_pimpinan_ksp").Find(&results).Error
	return results, err
}

func (r *systemRepository) GetPimpinanCognitive(ctx context.Context) ([]map[string]interface{}, error) {
	var results []map[string]interface{}
	err := r.db.WithContext(ctx).Table("vw_dashboard_pimpinan_kognitif").Find(&results).Error
	return results, err
}

func (r *systemRepository) GetPimpinanP5(ctx context.Context) ([]map[string]interface{}, error) {
	var results []map[string]interface{}
	err := r.db.WithContext(ctx).Table("vw_dashboard_pimpinan_profil_p5").Find(&results).Error
	return results, err
}

func (r *systemRepository) GetGuruCompliance(ctx context.Context) ([]map[string]interface{}, error) {
	var results []map[string]interface{}
	err := r.db.WithContext(ctx).Table("vw_dashboard_guru_modul_compliance").Find(&results).Error
	return results, err
}

func (r *systemRepository) GetGuruStudentWatch(ctx context.Context) ([]map[string]interface{}, error) {
	var results []map[string]interface{}
	err := r.db.WithContext(ctx).Table("vw_dashboard_guru_pantauan_siswa").Find(&results).Error
	return results, err
}

func (r *systemRepository) GetGuruAutomationQueue(ctx context.Context) ([]AutomationQueue, error) {
	var results []AutomationQueue
	err := r.db.WithContext(ctx).Order("created_at desc").Limit(10).Find(&results).Error
	return results, err
}

func (r *systemRepository) GetOperatorDataCompleteness(ctx context.Context) ([]map[string]interface{}, error) {
	var results []map[string]interface{}
	err := r.db.WithContext(ctx).Table("vw_dashboard_operator_kelengkapan_data").Find(&results).Error
	return results, err
}

func (r *systemRepository) GetOperatorTelemetry(ctx context.Context) ([]ServerTelemetry, error) {
	var results []ServerTelemetry
	err := r.db.WithContext(ctx).Order("logged_at desc").Limit(5).Find(&results).Error
	return results, err
}

func (r *systemRepository) InitViewsAndSeed(ctx context.Context) error {
	logger.Info("Starting initialization of database views and seeding system telemetry/automation queues...")

	// 1. Create Database Views
	views := []struct {
		Name string
		SQL  string
	}{
// 		{
// 			Name: "vw_dashboard_pimpinan_kognitif",
// 			SQL: `
// 				CREATE OR REPLACE VIEW vw_dashboard_pimpinan_kognitif AS
// 				SELECT 
// 					c.id AS classroom_id,
// 					c.classroom_name,
// 					sub.subject_name,
// 					qb.tingkat AS tingkat_kognitif,
// 					ROUND(AVG(ascore.score), 2) AS rata_rata_nilai,
// 					COUNT(ascore.id) AS total_sampel_jawaban
// 				FROM trx_academic_score ascore
// 				JOIN trx_question_bank qb ON ascore.question_id = qb.id
// 				JOIN trx_teaching_module tm ON qb.module_id = tm.id
// 				JOIN trx_atp atp ON tm.atp_id = atp.id
// 				JOIN master_classroom c ON atp.classroom_id = c.id
// 				JOIN master_subject sub ON atp.subject_id = sub.id
// 				WHERE c.academic_year_id = (SELECT id FROM master_academic_year WHERE is_active = true LIMIT 1)
// 				GROUP BY c.id, c.classroom_name, sub.subject_name, qb.tingkat;
// 			`,
// 		},
		{
			Name: "vw_dashboard_pimpinan_profil_p5",
			SQL: `
				CREATE OR REPLACE VIEW vw_dashboard_pimpinan_profil_p5 AS
				SELECT 
					pd.dimension_name,
					ap5.capaian AS predikat_rubrik,
					COUNT(ap5.id) AS jumlah_siswa
				FROM trx_assessment_p5 ap5
				JOIN master_profile_dimension pd ON ap5.dimension_id = pd.id
				GROUP BY pd.dimension_name, ap5.capaian;
			`,
		},
// 		{
// 			Name: "vw_dashboard_guru_modul_compliance",
// 			SQL: `
// 				CREATE OR REPLACE VIEW vw_dashboard_guru_modul_compliance AS
// 				SELECT 
// 					tm.id AS teaching_module_id,
// 					tm.title AS judul_modul,
// 					t.full_name AS nama_guru,
// 					sub.subject_name,
// 					COUNT(DISTINCT tma.stage_id) AS jumlah_tahap_terpenuhi,
// 					CASE 
// 						WHEN COUNT(DISTINCT tma.stage_id) >= 3 THEN 'PATUH'
// 						ELSE 'BELUM LENGKAP (Wajib Refleksi)'
// 					END AS status_kepatuhan
// 				FROM trx_teaching_module tm
// 				JOIN trx_atp atp ON tm.atp_id = atp.id
// 				JOIN master_classroom c ON atp.classroom_id = c.id
// 				JOIN trx_teaching_assignment ta ON c.id = ta.classroom_id AND atp.subject_id = ta.subject_id
// 				JOIN master_teacher t ON ta.teacher_id = t.id
// 				JOIN master_subject sub ON atp.subject_id = sub.id
// 				LEFT JOIN trx_teaching_module_activity tma ON tm.id = tma.module_id
// 				GROUP BY tm.id, tm.title, t.full_name, sub.subject_name;
// 			`,
// 		},
// 		{
// 			Name: "vw_dashboard_guru_pantauan_siswa",
// 			SQL: `
// 				CREATE OR REPLACE VIEW vw_dashboard_guru_pantauan_siswa AS
// 				SELECT 
// 					s.id AS student_id,
// 					s.full_name AS nama_siswa,
// 					c.classroom_name,
// 					COALESCE(att.sick, 0) + COALESCE(att.permission, 0) + COALESCE(att.unexcused, 0) AS total_absen,
// 					ROUND(AVG(ascore.score), 2) AS rata_rata_akademik,
// 					CASE 
// 						WHEN (COALESCE(att.sick, 0) + COALESCE(att.permission, 0) + COALESCE(att.unexcused, 0)) >= 5 OR AVG(ascore.score) < 65 THEN 'PERLU INTERVENSI'
// 						ELSE 'AMAN'
// 					END AS status_peringatan
// 				FROM master_student s
// 				JOIN trx_enrollment e ON s.id = e.student_id
// 				JOIN master_classroom c ON e.classroom_id = c.id
// 				LEFT JOIN trx_attendance att ON s.id = att.student_id AND c.id = att.classroom_id
// 				LEFT JOIN trx_academic_score ascore ON s.id = ascore.student_id
// 				WHERE c.academic_year_id = (SELECT id FROM master_academic_year WHERE is_active = true LIMIT 1)
// 				GROUP BY s.id, s.full_name, c.classroom_name, att.sick, att.permission, att.unexcused;
// 			`,
// 		},
		{
			Name: "vw_dashboard_operator_kelengkapan_data",
			SQL: `
				CREATE OR REPLACE VIEW vw_dashboard_operator_kelengkapan_data AS
				SELECT 
					sch.school_name,
					CASE WHEN sa.vision IS NOT NULL AND sa.mission IS NOT NULL THEN 100 ELSE 0 END AS persentase_profil_dasar,
					CASE WHEN COUNT(DISTINCT t.id) > 0 THEN 100 ELSE 0 END AS persentase_data_guru,
					CASE WHEN COUNT(DISTINCT s.id) > 0 THEN 100 ELSE 0 END AS persentase_data_siswa,
					CASE WHEN COUNT(DISTINCT lc.id) > 0 THEN 100 ELSE 0 END AS persentase_karakteristik_lokal
				FROM master_school sch
				LEFT JOIN master_teacher t ON sch.id = t.school_id
					LEFT JOIN school_administration sa ON sch.id = sa.school_id
				LEFT JOIN master_student s ON sch.id = s.school_id
				LEFT JOIN master_local_context lc ON sch.id::text = lc.school_id
				GROUP BY sch.school_name, sa.vision, sa.mission;
			`,
		},
	}

	for _, v := range views {
		logger.Info("Creating database view: " + v.Name)
		_ = r.db.WithContext(ctx).Exec("DROP VIEW IF EXISTS public." + v.Name + " CASCADE;").Error
		if err := r.db.WithContext(ctx).Exec(v.SQL).Error; err != nil {
			logger.Error("Failed to create database view "+v.Name, err)
			return err
		}
	}

	// 2. Seed Server Telemetry data if empty
	var telemetryCount int64
	r.db.Model(&ServerTelemetry{}).Count(&telemetryCount)
	if telemetryCount == 0 {
		logger.Info("Seeding initial server telemetries...")
		telemetries := []ServerTelemetry{
			{
				CpuUsagePercent:    42.5,
				RamUsagePercent:    48.0,
				StorageFreeGB:      850.5,
				ServerTemperatureC: 46.2,
				EngineStatus:       "RUNNING",
				LoggedAt:           time.Now().Add(-15 * time.Minute),
			},
			{
				CpuUsagePercent:    55.2,
				RamUsagePercent:    52.4,
				StorageFreeGB:      850.5,
				ServerTemperatureC: 49.5,
				EngineStatus:       "RUNNING",
				LoggedAt:           time.Now().Add(-10 * time.Minute),
			},
			{
				CpuUsagePercent:    44.1,
				RamUsagePercent:    48.2,
				StorageFreeGB:      850.2,
				ServerTemperatureC: 46.8,
				EngineStatus:       "RUNNING",
				LoggedAt:           time.Now(),
			},
		}
		for _, t := range telemetries {
			if err := r.db.WithContext(ctx).Create(&t).Error; err != nil {
				logger.Error("Failed to seed server telemetry", err)
				return err
			}
		}
	}

	// 3. Seed Automation Queue data if empty and a user exists
	var queueCount int64
	r.db.Model(&AutomationQueue{}).Count(&queueCount)
	if queueCount == 0 {
		var userIDStr string
		err := r.db.Raw("SELECT id FROM auth_user LIMIT 1").Scan(&userIDStr).Error
		userID, parseErr := uuid.Parse(userIDStr)
		if err == nil && parseErr == nil && userID != uuid.Nil {
			logger.Info("Seeding initial automation queue tasks for user ID: " + userID.String())
			queues := []AutomationQueue{
				{
					TaskType:    "PERUMUSAN_KSP",
					ReferenceID: uuid.New(),
					UserID:      userID,
					Status:      "ANTREAN",
					CreatedAt:   time.Now().Add(-2 * time.Minute),
					UpdatedAt:   time.Now().Add(-2 * time.Minute),
				},
				{
					TaskType:    "PERUMUSAN_MODUL",
					ReferenceID: uuid.New(),
					UserID:      userID,
					Status:      "PROSES",
					CreatedAt:   time.Now().Add(-5 * time.Minute),
					UpdatedAt:   time.Now().Add(-1 * time.Minute),
				},
				{
					TaskType:    "NARASI_RAPOR",
					ReferenceID: uuid.New(),
					UserID:      userID,
					Status:      "SELESAI",
					CreatedAt:   time.Now().Add(-10 * time.Minute),
					UpdatedAt:   time.Now().Add(-3 * time.Minute),
				},
				{
					TaskType:    "NARASI_RAPOR",
					ReferenceID: uuid.New(),
					UserID:      userID,
					Status:      "GAGAL",
					ErrorLog:    "OOM Killer: LLM Lokal Llama-3 melebihi batas memori RAM 16GB pada server intranet sekolah.",
					CreatedAt:   time.Now().Add(-15 * time.Minute),
					UpdatedAt:   time.Now().Add(-14 * time.Minute),
				},
			}
			for _, q := range queues {
				if err := r.db.WithContext(ctx).Create(&q).Error; err != nil {
					logger.Error("Failed to seed automation queue", err)
					return err
				}
			}
		} else {
			logger.Warn("Skipping automation queue seeding because no user exists in auth_user table yet.", nil)
		}
	}

	logger.Info("Tampilan database diinisialisasi dan data awal berhasil diselesaikan!")
	return nil
}
