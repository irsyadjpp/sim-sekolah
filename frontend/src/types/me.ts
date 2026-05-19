// Shared types for user profile (used by Settings & Profile pages)

export interface TeacherProfile {
  id: string;
  full_name: string;
  gender: string;
  birth_place: string;
  birth_date: string;
  nik: string;
  nuptk: string;
  niy_nigk: string;
  religion: string;
  nationality: string;
  photo_url: string;
  full_address: string;
  hamlet: string;
  rt_rw: string;
  village: string;
  district: string;
  regency: string;
  province: string;
  postal_code: string;
  phone: string;
  email: string;
  nip: string;
  employment_status: string;
  teaching_subject: string;
  additional_position: string;
  teaching_hours: number;
  is_active: boolean;
  last_education: string;
  major: string;
  university_name: string;
  graduation_year: number;
  is_certified: boolean;
  certificate_number: string;
  teaching_preference: string;
}

export interface StudentProfile {
  id: string;
  full_name: string;
  nis: string;
  nisn: string;
  gender: string;
  birth_place: string;
  birth_date: string;
  religion: string;
  nationality: string;
  photo_url: string;
  full_address: string;
  rt_rw: string;
  village: string;
  district: string;
  regency: string;
  province: string;
  postal_code: string;
  enrollment_year: number;
  curriculum: string;
  student_status: string;
  blood_type: string;
  height: number;
  weight: number;
  medical_history: string;
  disability: string;
}

export interface MeData {
  id: string;
  full_name: string;
  username: string;
  email: string;
  roles: string[];
  theme_color?: string;
  theme_mode?: string;
  content_type?: string;
  left_menu_type?: string;

  // Security & Notifications
  two_factor_enabled?: boolean;
  email_notifications?: boolean;
  push_notifications?: boolean;

  teacher?: TeacherProfile;
  student?: StudentProfile;
}
