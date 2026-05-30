package school

import (
	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

// MasterSchool - normalized basic school info
type MasterSchool struct {
	ID             uuid.UUID `gorm:"type:uuid;default:uuidv7();primaryKey" json:"id"`
	NPSN           string    `gorm:"type:varchar(20);uniqueIndex" json:"npsn"`
	SchoolName     string    `gorm:"type:varchar(255);not null" json:"school_name"`
	Phone          string    `gorm:"type:varchar(30)" json:"phone"`
	Email          string    `gorm:"type:varchar(100)" json:"email"`
	Status         string    `gorm:"type:varchar(20)" json:"status"`
	OperatingHours string    `gorm:"type:varchar(255)" json:"operating_hours"`
	BOSStatus      string    `gorm:"type:varchar(100)" json:"bos_status"`

	common.Auditable
}

func (MasterSchool) TableName() string {
	return "master_school"
}

// SchoolLocation - normalized location data
type SchoolLocation struct {
	ID          uuid.UUID `gorm:"type:uuid;default:uuidv7();primaryKey" json:"id"`
	SchoolID    uuid.UUID `gorm:"type:uuid;not null" json:"school_id"`
	District    string    `gorm:"type:varchar(100)" json:"district"`
	Regency     string    `gorm:"type:varchar(100)" json:"regency"`
	Province    string    `gorm:"type:varchar(100)" json:"province"`
	Country     string    `gorm:"type:varchar(100);default:'Indonesia'" json:"country"`
	Latitude    float64   `gorm:"type:decimal(10,8)" json:"latitude"`
	Longitude   float64   `gorm:"type:decimal(11,8)" json:"longitude"`
	FullAddress string    `gorm:"type:text" json:"full_address"`
	PostalCode  string    `gorm:"type:varchar(10)" json:"postal_code"`

	common.Auditable
}

func (SchoolLocation) TableName() string {
	return "school_location"
}

// SchoolStatistics - normalized enrollment statistics
type SchoolStatistics struct {
	ID              uuid.UUID `gorm:"type:uuid;default:uuidv7();primaryKey" json:"id"`
	SchoolID        uuid.UUID `gorm:"type:uuid;not null" json:"school_id"`
	TotalStudents   int64     `gorm:"type:bigint" json:"total_students"`
	MaleStudents    int64     `gorm:"type:bigint" json:"male_students"`
	FemaleStudents  int64     `gorm:"type:bigint" json:"female_students"`
	TotalTeachers   int64     `gorm:"type:bigint" json:"total_teachers"`
	MaleTeachers    int64     `gorm:"type:bigint" json:"male_teachers"`
	FemaleTeachers  int64     `gorm:"type:bigint" json:"female_teachers"`
	TotalStaff      int64     `gorm:"type:bigint" json:"total_staff"`
	RombelCount     int64     `gorm:"type:bigint" json:"rombel_count"`
	StudentRatio    string    `gorm:"type:varchar(50)" json:"student_ratio"`
	StudentReligion string    `gorm:"type:varchar(100)" json:"student_religion"`
	ReportDate      string    `gorm:"type:date;default:CURRENT_DATE" json:"report_date"`

	common.Auditable
}

func (SchoolStatistics) TableName() string {
	return "school_statistics"
}

// SchoolInfrastructure - normalized infrastructure data
type SchoolInfrastructure struct {
	ID                    uuid.UUID `gorm:"type:uuid;default:uuidv7();primaryKey" json:"id"`
	SchoolID              uuid.UUID `gorm:"type:uuid;not null" json:"school_id"`
	ElectricityCapacity   int64     `gorm:"type:bigint" json:"electricity_capacity"`
	SignalStatus          string    `gorm:"type:varchar(50)" json:"signal_status"`
	WaterSource           string    `gorm:"type:varchar(100)" json:"water_source"`
	InternetAccess        string    `gorm:"type:varchar(50)" json:"internet_access"`
	ClassroomCount        int64     `gorm:"type:bigint" json:"classroom_count"`
	ClassroomGoodCount    int64     `gorm:"type:bigint" json:"classroom_good_count"`
	ClassroomDamagedCount int64     `gorm:"type:bigint" json:"classroom_damaged_count"`
	LibraryCount          int64     `gorm:"type:bigint" json:"library_count"`
	LabCount              int64     `gorm:"type:bigint" json:"lab_count"`
	ToiletStudentCount    int64     `gorm:"type:bigint" json:"toilet_student_count"`
	ToiletTeacherCount    int64     `gorm:"type:bigint" json:"toilet_teacher_count"`
	InfrastructureSummary string    `gorm:"type:text" json:"infrastructure_summary"`
	ReportDate            string    `gorm:"type:date;default:CURRENT_DATE" json:"report_date"`

	common.Auditable
}

func (SchoolInfrastructure) TableName() string {
	return "school_infrastructure"
}

// SchoolAcademic - normalized academic programs
type SchoolAcademic struct {
	ID             uuid.UUID `gorm:"type:uuid;default:uuidv7();primaryKey" json:"id"`
	SchoolID       uuid.UUID `gorm:"type:uuid;not null" json:"school_id"`
	Curriculum     string    `gorm:"type:varchar(100)" json:"curriculum"`
	Accreditation  string    `gorm:"type:varchar(50)" json:"accreditation"`
	EducationForm  string    `gorm:"type:varchar(100)" json:"education_form"`
	GraduationData string    `gorm:"type:varchar(255)" json:"graduation_data"`

	common.Auditable
}

func (SchoolAcademic) TableName() string {
	return "school_academic"
}

// SchoolAdministration - normalized administrative information
type SchoolAdministration struct {
	ID             uuid.UUID `gorm:"type:uuid;default:uuidv7();primaryKey" json:"id"`
	SchoolID       uuid.UUID `gorm:"type:uuid;not null" json:"school_id"`
	PrincipalName  string    `gorm:"type:varchar(255)" json:"principal_name"`
	OperatorName   string    `gorm:"type:varchar(255)" json:"operator_name"`
	Vision         string    `gorm:"type:text" json:"vision"`
	VisionMeaning  string    `gorm:"type:text" json:"vision_meaning"`
	Mission        string    `gorm:"type:text" json:"mission"`
	Goal           string    `gorm:"type:text" json:"goal"`
	SyncSystem     string    `gorm:"type:varchar(100)" json:"sync_system"`
	SyncCompliance string    `gorm:"type:varchar(100)" json:"sync_compliance"`

	common.Auditable
}

func (SchoolAdministration) TableName() string {
	return "school_administration"
}

// SchoolComplete - composite struct for API responses (all normalized tables combined)
type SchoolComplete struct {
	MasterSchool
	SchoolLocation
	SchoolStatistics
	SchoolInfrastructure
	SchoolAcademic
	SchoolAdministration
}
