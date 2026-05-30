import { DEFAULTS } from "@/config";

interface SurveyQuestion {
  question_type: string;
  question_text: string;
  description?: string;
  required: boolean;
  options?: string[];
}

interface SurveyTemplate {
  name: string;
  description: string;
  category: string;
  questions: SurveyQuestion[];
}

const TEMPLATES: Record<string, SurveyTemplate> = {
  sarpras: {
    name: "Survey Sarana Prasarana Sekolah",
    description: "Template survey untuk mengevaluasi kondisi sarana dan prasarana sekolah",
    category: "assessment",
    questions: [
      {
        question_type: "single_choice",
        question_text: "Bagaimana kondisi ruang kelas yang tersedia?",
        description: "Evaluasi kelayakan ruang kelas",
        required: true,
        options: ["Sangat Baik", "Baik", "Cukup", "Kurang", "Sangat Kurang"],
      },
      {
        question_type: "single_choice",
        question_text: "Apakah fasilitas laboratorium tersedia dan layak digunakan?",
        description: "Ketersediaan dan kondisi laboratorium",
        required: true,
        options: ["Tersedia dan layak", "Tersedia tapi perlu perbaikan", "Tidak tersedia"],
      },
      {
        question_type: "single_choice",
        question_text: "Bagaimana kondisi perpustakaan sekolah?",
        description: "Evaluasi perpustakaan",
        required: true,
        options: ["Sangat Baik", "Baik", "Cukup", "Kurang", "Sangat Kurang"],
      },
      {
        question_type: "single_choice",
        question_text: "Apakah fasilitas sanitasi (toilet) mencukupi dan bersih?",
        description: "Evaluasi fasilitas sanitasi",
        required: true,
        options: ["Sangat Baik", "Baik", "Cukup", "Kurang", "Sangat Kurang"],
      },
      {
        question_type: "text",
        question_text: "Saran perbaikan untuk sarana prasarana sekolah",
        description: "Tuliskan saran dan masukan",
        required: false,
      },
    ],
  },
  minat_bakat: {
    name: "Survey Minat dan Bakat Siswa",
    description: "Template survey untuk mengidentifikasi minat dan bakat siswa",
    category: "research",
    questions: [
      {
        question_type: "multiple_choice",
        question_text: "Apa bidang yang paling Anda minati?",
        description: "Pilih semua yang sesuai",
        required: true,
        options: [
          "Sains dan Teknologi",
          "Seni dan Musik",
          "Olahraga",
          "Bahasa dan Sastra",
          "Matematika",
          "Sosial dan Kemanusiaan",
          "Komputer dan IT",
          "Lainnya",
        ],
      },
      {
        question_type: "single_choice",
        question_text: "Aktivitas ekstrakurikuler apa yang ingin Anda ikuti?",
        description: "Pilih satu pilihan",
        required: true,
        options: [
          "Olahraga",
          "Seni Tari/Musik",
          "KIR/Ilmu Pengetahuan",
          "Pramuka",
          "Paskibra",
          "PMR",
          "Rohis/Rohis",
          "English Club",
          "Komputer",
          "Tidak tertarik ekstrakurikuler",
        ],
      },
      {
        question_type: "rating",
        question_text: "Seberapa besar minat Anda dalam bidang akademik?",
        description: "Rating 1-5",
        required: true,
      },
      {
        question_type: "rating",
        question_text: "Seberapa besar minat Anda dalam bidang non-akademik?",
        description: "Rating 1-5",
        required: true,
      },
      {
        question_type: "textarea",
        question_text: "Ceritakan bakat khusus yang Anda miliki",
        description: "Jelaskan bakat atau keahlian khusus",
        required: false,
      },
    ],
  },
  masukan_orang_tua: {
    name: "Survey Masukan Orang Tua",
    description: "Template survey untuk mengumpulkan masukan dari orang tua/wali murid",
    category: "feedback",
    questions: [
      {
        question_type: "rating",
        question_text: "Bagaimana penilaian Anda terhadap kualitas pengajaran di sekolah?",
        description: "Rating 1-5",
        required: true,
      },
      {
        question_type: "rating",
        question_text: "Bagaimana komunikasi antara sekolah dan orang tua?",
        description: "Rating 1-5",
        required: true,
      },
      {
        question_type: "single_choice",
        question_text: "Apakah Anda puas dengan fasilitas sekolah?",
        description: "Evaluasi fasilitas",
        required: true,
        options: ["Sangat Puas", "Puas", "Cukup Puas", "Kurang Puas", "Tidak Puas"],
      },
      {
        question_type: "multiple_choice",
        question_text: "Apa aspek yang perlu ditingkatkan?",
        description: "Pilih semua yang sesuai",
        required: true,
        options: [
          "Kualitas pengajaran",
          "Fasilitas sekolah",
          "Komunikasi",
          "Disiplin",
          "Ekstrakurikuler",
          "Kebersihan",
          "Keamanan",
          "Lainnya",
        ],
      },
      {
        question_type: "textarea",
        question_text: "Masukan dan saran untuk perbaikan sekolah",
        description: "Tuliskan masukan konstruktif",
        required: false,
      },
      {
        question_type: "text",
        question_text: "Nama lengkap orang tua/wali",
        description: "Opsional untuk identifikasi",
        required: false,
      },
    ],
  },
};

export async function seedSurveyTemplates() {
  const token = localStorage.getItem("accessToken");
  if (!token) {
    throw new Error("Authentication token not found");
  }

  const results = {
    success: [] as string[],
    failed: [] as string[],
  };

  for (const [key, template] of Object.entries(TEMPLATES)) {
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/strategic-planning/survey-templates`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          ...template,
          is_system_template: true,
        }),
      });

      if (res.ok) {
        results.success.push(template.name);
      } else {
        results.failed.push(template.name);
      }
    } catch (error) {
      console.error(`Failed to create template ${template.name}:`, error);
      results.failed.push(template.name);
    }
  }

  return results;
}

export function getTemplateNames() {
  return Object.keys(TEMPLATES);
}

export function getTemplate(key: string): SurveyTemplate | undefined {
  return TEMPLATES[key];
}

export const TEMPLATES_LIST = Object.entries(TEMPLATES).map(([key, template]) => ({
  key,
  ...template,
}));