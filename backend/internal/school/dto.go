package school

// CreateSchoolRequest - single endpoint for creating complete school data across all normalized tables
type CreateSchoolRequest struct {
	// MasterSchool fields
	NPSN           string `json:"npsn" validate:"omitempty,max=20"`
	SchoolName     string `json:"school_name" validate:"required,max=255"`
	Phone          string `json:"phone" validate:"omitempty,max=30"`
	Email          string `json:"email" validate:"omitempty,email,max=100"`
	Status         string `json:"status"`
	OperatingHours string `json:"operating_hours"`
	BOSStatus      string `json:"bos_status"`

	// SchoolLocation fields
	Address   string  `json:"address"`
	District  string  `json:"district"`
	Regency   string  `json:"regency"`
	Province  string  `json:"province"`
	Country   string  `json:"country"`
	Latitude  float64 `json:"latitude"`
	Longitude float64 `json:"longitude"`

	// SchoolStatistics fields
	TotalStudents   int    `json:"total_students"`
	MaleStudents    int    `json:"male_students"`
	FemaleStudents  int    `json:"female_students"`
	TotalTeachers   int    `json:"total_teachers"`
	MaleTeachers    int    `json:"male_teachers"`
	FemaleTeachers  int    `json:"female_teachers"`
	TotalStaff      int    `json:"total_staff"`
	RombelCount     int    `json:"rombel_count"`
	StudentRatio    string `json:"student_ratio"`
	StudentReligion string `json:"student_religion"`

	// SchoolInfrastructure fields
	ElectricityCapacity   int    `json:"electricity_capacity"`
	SignalStatus          string `json:"signal_status"`
	WaterSource           string `json:"water_source"`
	InternetAccess        string `json:"internet_access"`
	ClassroomCount        int    `json:"classroom_count"`
	ClassroomGoodCount    int    `json:"classroom_good_count"`
	ClassroomDamagedCount int    `json:"classroom_damaged_count"`
	LibraryCount          int    `json:"library_count"`
	LabCount              int    `json:"lab_count"`
	ToiletStudentCount    int    `json:"toilet_student_count"`
	ToiletTeacherCount    int    `json:"toilet_teacher_count"`
	InfrastructureSummary string `json:"infrastructure_summary"`

	// SchoolAcademic fields
	Curriculum     string `json:"curriculum"`
	Accreditation  string `json:"accreditation"`
	EducationForm  string `json:"education_form"`
	GraduationData string `json:"graduation_data"`

	// SchoolAdministration fields
	PrincipalName  string `json:"principal_name"`
	OperatorName   string `json:"operator_name"`
	Vision         string `json:"vision"`
	VisionMeaning  string `json:"vision_meaning"`
	Mission        string `json:"mission"`
	Goal           string `json:"goal"`
	SyncSystem     string `json:"sync_system"`
	SyncCompliance string `json:"sync_compliance"`
}

// UpdateSchoolRequest - single endpoint for updating complete school data across all normalized tables
type UpdateSchoolRequest struct {
	// MasterSchool fields
	NPSN           string `json:"npsn" validate:"omitempty,max=20"`
	SchoolName     string `json:"school_name" validate:"omitempty,max=255"`
	Phone          string `json:"phone" validate:"omitempty,max=30"`
	Email          string `json:"email" validate:"omitempty,email,max=100"`
	Status         string `json:"status"`
	OperatingHours string `json:"operating_hours"`
	BOSStatus      string `json:"bos_status"`

	// SchoolLocation fields
	Address   string  `json:"address"`
	District  string  `json:"district"`
	Regency   string  `json:"regency"`
	Province  string  `json:"province"`
	Country   string  `json:"country"`
	Latitude  float64 `json:"latitude"`
	Longitude float64 `json:"longitude"`

	// SchoolStatistics fields
	TotalStudents   int    `json:"total_students"`
	MaleStudents    int    `json:"male_students"`
	FemaleStudents  int    `json:"female_students"`
	TotalTeachers   int    `json:"total_teachers"`
	MaleTeachers    int    `json:"male_teachers"`
	FemaleTeachers  int    `json:"female_teachers"`
	TotalStaff      int    `json:"total_staff"`
	RombelCount     int    `json:"rombel_count"`
	StudentRatio    string `json:"student_ratio"`
	StudentReligion string `json:"student_religion"`

	// SchoolInfrastructure fields
	ElectricityCapacity   int    `json:"electricity_capacity"`
	SignalStatus          string `json:"signal_status"`
	WaterSource           string `json:"water_source"`
	InternetAccess        string `json:"internet_access"`
	ClassroomCount        int    `json:"classroom_count"`
	ClassroomGoodCount    int    `json:"classroom_good_count"`
	ClassroomDamagedCount int    `json:"classroom_damaged_count"`
	LibraryCount          int    `json:"library_count"`
	LabCount              int    `json:"lab_count"`
	ToiletStudentCount    int    `json:"toilet_student_count"`
	ToiletTeacherCount    int    `json:"toilet_teacher_count"`
	InfrastructureSummary string `json:"infrastructure_summary"`

	// SchoolAcademic fields
	Curriculum     string `json:"curriculum"`
	Accreditation  string `json:"accreditation"`
	EducationForm  string `json:"education_form"`
	GraduationData string `json:"graduation_data"`

	// SchoolAdministration fields
	PrincipalName  string `json:"principal_name"`
	OperatorName   string `json:"operator_name"`
	Vision         string `json:"vision"`
	VisionMeaning  string `json:"vision_meaning"`
	Mission        string `json:"mission"`
	Goal           string `json:"goal"`
	SyncSystem     string `json:"sync_system"`
	SyncCompliance string `json:"sync_compliance"`
}
