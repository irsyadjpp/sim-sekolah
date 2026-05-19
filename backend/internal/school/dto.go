package school

type CreateSchoolRequest struct {
	NPSN                  string  `json:"npsn" validate:"omitempty,max=20"`
	SchoolName            string  `json:"school_name" validate:"required,max=255"`
	Address               string  `json:"address"`
	District              string  `json:"district"`
	Regency               string  `json:"regency"`
	Province              string  `json:"province"`
	Status                string  `json:"status"`
	Accreditation         string  `json:"accreditation"`
	Phone                 string  `json:"phone" validate:"omitempty,max=30"`
	Email                 string  `json:"email" validate:"omitempty,email,max=100"`
	PrincipalName         string  `json:"principal_name"`
	OperatorName          string  `json:"operator_name"`
	OperatingHours        string  `json:"operating_hours"`
	Latitude              float64 `json:"latitude"`
	Longitude             float64 `json:"longitude"`
	TotalStudents         int     `json:"total_students"`
	MaleStudents          int     `json:"male_students"`
	FemaleStudents        int     `json:"female_students"`
	TotalTeachers         int     `json:"total_teachers"`
	MaleTeachers          int     `json:"male_teachers"`
	FemaleTeachers        int     `json:"female_teachers"`
	Curriculum            string  `json:"curriculum"`
	ElectricityCapacity   int     `json:"electricity_capacity"`
	SignalStatus          string  `json:"signal_status"`
	WaterSource           string  `json:"water_source"`
	InternetAccess        string  `json:"internet_access"`
	BOSStatus             string  `json:"bos_status"`
	InfrastructureSummary string  `json:"infrastructure_summary"`
	GraduationData        string  `json:"graduation_data"`
	TeacherPnsCount       int     `json:"teacher_pns_count"`
	TeacherHonorCount     int     `json:"teacher_honor_count"`
	TeacherCertifiedCount string  `json:"teacher_certified_count"`
	TeacherQualifiedCount string  `json:"teacher_qualified_count"`
	ClassroomCount        int     `json:"classroom_count"`
	ClassroomGoodCount    int     `json:"classroom_good_count"`
	ClassroomDamagedCount int     `json:"classroom_damaged_count"`
	LibraryCount          int     `json:"library_count"`
	ToiletStudentCount    int     `json:"toilet_student_count"`
	ToiletTeacherCount    int     `json:"toilet_teacher_count"`
	StudentReligion       string  `json:"student_religion"`
	StudentRatio          string  `json:"student_ratio"`
	Vision                string  `json:"vision"`
	VisionMeaning         string  `json:"vision_meaning"`
	Mission               string  `json:"mission"`
	Goal                  string  `json:"goal"`
	EducationForm         string  `json:"education_form"`
	Country               string  `json:"country"`
	TotalStaff            int     `json:"total_staff"`
	LabCount              int     `json:"lab_count"`
	RombelCount           int     `json:"rombel_count"`
	SyncSystem            string  `json:"sync_system"`
	SyncCompliance        string  `json:"sync_compliance"`
}

type UpdateSchoolRequest struct {
	NPSN                  string  `json:"npsn" validate:"omitempty,max=20"`
	SchoolName            string  `json:"school_name" validate:"omitempty,max=255"`
	Address               string  `json:"address"`
	District              string  `json:"district"`
	Regency               string  `json:"regency"`
	Province              string  `json:"province"`
	Status                string  `json:"status"`
	Accreditation         string  `json:"accreditation"`
	Phone                 string  `json:"phone" validate:"omitempty,max=30"`
	Email                 string  `json:"email" validate:"omitempty,email,max=100"`
	PrincipalName         string  `json:"principal_name"`
	OperatorName          string  `json:"operator_name"`
	OperatingHours        string  `json:"operating_hours"`
	Latitude              float64 `json:"latitude"`
	Longitude             float64 `json:"longitude"`
	TotalStudents         int     `json:"total_students"`
	MaleStudents          int     `json:"male_students"`
	FemaleStudents        int     `json:"female_students"`
	TotalTeachers         int     `json:"total_teachers"`
	MaleTeachers          int     `json:"male_teachers"`
	FemaleTeachers        int     `json:"female_teachers"`
	Curriculum            string  `json:"curriculum"`
	ElectricityCapacity   int     `json:"electricity_capacity"`
	SignalStatus          string  `json:"signal_status"`
	WaterSource           string  `json:"water_source"`
	InternetAccess        string  `json:"internet_access"`
	BOSStatus             string  `json:"bos_status"`
	InfrastructureSummary string  `json:"infrastructure_summary"`
	GraduationData        string  `json:"graduation_data"`
	TeacherPnsCount       int     `json:"teacher_pns_count"`
	TeacherHonorCount     int     `json:"teacher_honor_count"`
	TeacherCertifiedCount string  `json:"teacher_certified_count"`
	TeacherQualifiedCount string  `json:"teacher_qualified_count"`
	ClassroomCount        int     `json:"classroom_count"`
	ClassroomGoodCount    int     `json:"classroom_good_count"`
	ClassroomDamagedCount int     `json:"classroom_damaged_count"`
	LibraryCount          int     `json:"library_count"`
	ToiletStudentCount    int     `json:"toilet_student_count"`
	ToiletTeacherCount    int     `json:"toilet_teacher_count"`
	StudentReligion       string  `json:"student_religion"`
	StudentRatio          string  `json:"student_ratio"`
	Vision                string  `json:"vision"`
	VisionMeaning         string  `json:"vision_meaning"`
	Mission               string  `json:"mission"`
	Goal                  string  `json:"goal"`
	EducationForm         string  `json:"education_form"`
	Country               string  `json:"country"`
	TotalStaff            int     `json:"total_staff"`
	LabCount              int     `json:"lab_count"`
	RombelCount           int     `json:"rombel_count"`
	SyncSystem            string  `json:"sync_system"`
	SyncCompliance        string  `json:"sync_compliance"`
}
