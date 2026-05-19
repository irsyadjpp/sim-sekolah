package system

import (
	"time"

	"github.com/google/uuid"
)

type AuditLog struct {
	ID             uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id" example:"a425fa98-4362-4f74-9a33-8dcfbaeecc45"` // UUID identifikasi unik entri audit log
	UserID         *uuid.UUID `gorm:"type:uuid" json:"user_id" example:"c5d2f366-3ff2-422c-807a-44c618bef84f"`                                  // ID pengguna (aktor) yang melakukan operasi
	Action         string     `gorm:"type:varchar(100);not null" json:"action" example:"UPDATE"`                                                // Jenis aksi keamanan: 'LOGIN', 'CREATE', 'UPDATE', 'DELETE', 'MFA_ENABLE'
	Entity         string     `gorm:"type:varchar(100);not null" json:"entity" example:"students"`                                              // Nama tabel database atau objek yang dimodifikasi
	EntityID       string     `gorm:"type:varchar(100)" json:"entity_id" example:"7e83162c-cbeb-4cd6-b027-2239a1ca481c"`                        // ID kunci utama dari entitas target yang dimodifikasi
	IPAddress      string     `gorm:"type:varchar(45)" json:"ip_address" example:"192.168.1.10"`                                                // Alamat IP klien pengirim permintaan
	ImpersonatorID *uuid.UUID `gorm:"type:uuid" json:"impersonator_id,omitempty" example:"d81fa945-9e89-4c71-8ddc-84f1bcf8f4cc"`                // ID pengguna asli (impersonator) yang melakukan tindakan (opsional)
	CreatedAt      time.Time  `gorm:"type:timestamp;default:CURRENT_TIMESTAMP" json:"created_at" example:"2026-05-18T13:45:46Z"`                // Waktu presisi saat kejadian berlangsung

	// Joined fields
	UserFullName         string `gorm:"->" json:"user_full_name,omitempty" example:"Budi Santoso"`         // Nama lengkap dari aktor pengguna (opsional)
	UserEmail            string `gorm:"->" json:"user_email,omitempty" example:"budi@sd.sch.id"`           // Alamat email aktif dari aktor pengguna (opsional)
	ImpersonatorFullName string `gorm:"->" json:"impersonator_full_name,omitempty" example:"Guru A"`       // Nama lengkap eksekutor asli (opsional)
	ImpersonatorEmail    string `gorm:"->" json:"impersonator_email,omitempty" example:"guru_a@sd.sch.id"` // Email eksekutor asli (opsional)
}

func (AuditLog) TableName() string {
	return "audit_logs"
}
