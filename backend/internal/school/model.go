package school

import (
	"time"

	"github.com/google/uuid"
)

type School struct {
	ID                    uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	NPSN                  string    `gorm:"type:varchar(20);uniqueIndex" json:"npsn"`
	SchoolName            string    `gorm:"type:varchar(255);not null" json:"school_name"`
	Address               string    `gorm:"type:text" json:"address"`
	District              string    `gorm:"type:varchar(100)" json:"district"`
	Regency               string    `gorm:"type:varchar(100)" json:"regency"`
	Province              string    `gorm:"type:varchar(100)" json:"province"`
	Status                string    `gorm:"type:varchar(20)" json:"status"`
	Accreditation         string    `gorm:"type:varchar(5)" json:"accreditation"`
	Phone                 string    `gorm:"type:varchar(30)" json:"phone"`
	Email                 string    `gorm:"type:varchar(100)" json:"email"`
	PrincipalName         string    `gorm:"type:varchar(255)" json:"principal_name"`
	OperatorName          string    `gorm:"type:varchar(255)" json:"operator_name"`
	OperatingHours        string    `gorm:"type:varchar(255)" json:"operating_hours"`
	Latitude              float64   `gorm:"type:decimal(10,8)" json:"latitude"`
	Longitude             float64   `gorm:"type:decimal(11,8)" json:"longitude"`
	TotalStudents         int       `gorm:"type:int" json:"total_students"`
	MaleStudents          int       `gorm:"type:int" json:"male_students"`
	FemaleStudents        int       `gorm:"type:int" json:"female_students"`
	TotalTeachers         int       `gorm:"type:int" json:"total_teachers"`
	MaleTeachers          int       `gorm:"type:int" json:"male_teachers"`
	FemaleTeachers        int       `gorm:"type:int" json:"female_teachers"`
	Curriculum            string    `gorm:"type:varchar(100)" json:"curriculum"`
	ElectricityCapacity   int       `gorm:"type:int" json:"electricity_capacity"`
	SignalStatus          string    `gorm:"type:varchar(50)" json:"signal_status"`
	WaterSource           string    `gorm:"type:varchar(100)" json:"water_source"`
	InternetAccess        string    `gorm:"type:varchar(100)" json:"internet_access"`
	BOSStatus             string    `gorm:"type:varchar(100)" json:"bos_status"`
	InfrastructureSummary string    `gorm:"type:text" json:"infrastructure_summary"`
	GraduationData        string    `gorm:"type:varchar(255)" json:"graduation_data"`
	TeacherPnsCount       int       `gorm:"type:int" json:"teacher_pns_count"`
	TeacherHonorCount     int       `gorm:"type:int" json:"teacher_honor_count"`
	TeacherCertifiedCount string    `gorm:"type:varchar(50)" json:"teacher_certified_count"`
	TeacherQualifiedCount string    `gorm:"type:varchar(50)" json:"teacher_qualified_count"`
	ClassroomCount        int       `gorm:"type:int" json:"classroom_count"`
	ClassroomGoodCount    int       `gorm:"type:int" json:"classroom_good_count"`
	ClassroomDamagedCount int       `gorm:"type:int" json:"classroom_damaged_count"`
	LibraryCount          int       `gorm:"type:int" json:"library_count"`
	ToiletStudentCount    int       `gorm:"type:int" json:"toilet_student_count"`
	ToiletTeacherCount    int       `gorm:"type:int" json:"toilet_teacher_count"`
	StudentReligion       string    `gorm:"type:varchar(100)" json:"student_religion"`
	StudentRatio          string    `gorm:"type:varchar(100)" json:"student_ratio"`
	Vision                string    `gorm:"type:text" json:"vision"`
	VisionMeaning         string    `gorm:"type:text" json:"vision_meaning"`
	Mission               string    `gorm:"type:text" json:"mission"`
	Goal                  string    `gorm:"type:text" json:"goal"`
	EducationForm         string    `gorm:"type:varchar(100)" json:"education_form"`
	Country               string    `gorm:"type:varchar(100)" json:"country"`
	TotalStaff            int       `gorm:"type:int" json:"total_staff"`
	LabCount              int       `gorm:"type:int" json:"lab_count"`
	RombelCount           int       `gorm:"type:int" json:"rombel_count"`
	SyncSystem            string    `gorm:"type:varchar(255)" json:"sync_system"`
	SyncCompliance        string    `gorm:"type:varchar(255)" json:"sync_compliance"`
	CreatedAt             time.Time `gorm:"type:timestamp;default:CURRENT_TIMESTAMP" json:"created_at"`
}

func (School) TableName() string {
	return "master_school"
}
