package system

import (
	"time"

	"github.com/google/uuid"
)

type AutomationQueue struct {
	ID          uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	TaskType    string    `gorm:"type:varchar(50);not null" json:"task_type"` // 'PERUMUSAN_KSP', 'PERUMUSAN_MODUL', 'NARASI_RAPOR'
	ReferenceID uuid.UUID `gorm:"type:uuid;not null" json:"reference_id"`
	UserID      uuid.UUID `gorm:"type:uuid;not null" json:"user_id"`
	Status      string    `gorm:"type:varchar(20);default:'ANTREAN';not null;index:idx_sys_queue_status" json:"status"` // 'ANTREAN', 'PROSES', 'SELESAI', 'GAGAL'
	ErrorLog    string    `gorm:"type:text" json:"error_log,omitempty"`
	CreatedAt   time.Time `gorm:"type:timestamp;default:CURRENT_TIMESTAMP" json:"created_at"`
	UpdatedAt   time.Time `gorm:"type:timestamp;default:CURRENT_TIMESTAMP" json:"updated_at"`
}

func (AutomationQueue) TableName() string {
	return "sys_automation_queue"
}

type ServerTelemetry struct {
	ID                 uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	CpuUsagePercent    float64   `gorm:"type:numeric(5,2);not null" json:"cpu_usage_percent"`
	RamUsagePercent    float64   `gorm:"type:numeric(5,2);not null" json:"ram_usage_percent"`
	StorageFreeGB      float64   `gorm:"type:numeric(10,2);not null" json:"storage_free_gb"`
	ServerTemperatureC float64   `gorm:"type:numeric(4,1)" json:"server_temperature_c"`
	EngineStatus       string    `gorm:"type:varchar(20);default:'RUNNING';not null" json:"engine_status"` // 'RUNNING', 'STOPPED'
	LoggedAt           time.Time `gorm:"type:timestamp;default:CURRENT_TIMESTAMP;index:idx_sys_telemetry_logged_at,sort:desc" json:"logged_at"`
}

func (ServerTelemetry) TableName() string {
	return "sys_server_telemetry"
}
