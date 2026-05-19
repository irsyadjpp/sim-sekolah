package ai

import "fmt"

func GetPromptTemplate(generationType, studentName, contextData string) string {
	baseInstruction := "Kamu adalah seorang guru SD yang profesional, empatik, dan memahami prinsip Kurikulum Merdeka serta Deep Learning (Meaningful, Joyful, Mindful learning). "
	baseInstruction += "Tugasmu adalah membuat kalimat narasi rapor berdasarkan data mentah berikut. "
	baseInstruction += "Aturan mutlak:\n"
	baseInstruction += "- Gunakan Bahasa Indonesia baku (EYD) yang mudah dipahami orang tua.\n"
	baseInstruction += "- Gunakan sudut pandang orang ketiga (menyebut nama siswa).\n"
	baseInstruction += "- Hindari kata-kata negatif yang menjatuhkan, gunakan diksi yang memotivasi (Growth Mindset).\n"
	baseInstruction += "- Tulis dalam 1 paragraf singkat (maksimal 2-3 kalimat).\n"
	baseInstruction += "- Jangan berikan pengantar atau penutup (seperti 'Baik, ini narasinya:'), cukup kembalikan teks narasinya saja.\n\n"

	var specificInstruction string

	switch generationType {
	case "competency_achieved":
		specificInstruction = fmt.Sprintf("Buat narasi 'Capaian Kompetensi yang Dikuasai' untuk siswa bernama %s berdasarkan data: '%s'. Fokus pada pujian atas materi yang sudah berhasil dipahami dengan baik.", studentName, contextData)

	case "competency_needs_improvement":
		specificInstruction = fmt.Sprintf("Buat narasi 'Area yang Perlu Ditingkatkan' untuk siswa bernama %s berdasarkan data: '%s'. Fokus pada dorongan positif dan harapan ke depannya tanpa terkesan menyalahkan.", studentName, contextData)

	case "p5_description":
		specificInstruction = fmt.Sprintf("Buat narasi untuk rapor Projek Penguatan Profil Pelajar Pancasila (P5) untuk siswa bernama %s berdasarkan data aktivitas projek: '%s'. Tekankan pada karakter Pancasila yang terbangun (seperti gotong royong, bernalar kritis, kebhinekaan global).", studentName, contextData)

	case "deep_learning_observation":
		specificInstruction = fmt.Sprintf("Buat narasi observasi 'Pembelajaran Mendalam (Deep Learning)' untuk siswa bernama %s berdasarkan catatan mentah: '%s'. Kaitkan dengan kemampuan kolaborasi, pemikiran kritis, dan pembelajaran yang bermakna bagi siswa.", studentName, contextData)

	case "homeroom_notes":
		specificInstruction = fmt.Sprintf("Buat 'Catatan Wali Kelas' di akhir rapor untuk siswa bernama %s berdasarkan ringkasan berikut: '%s'. Berikan apresiasi atas usahanya selama satu semester ini dan pesan motivasi untuk semester/kelas berikutnya.", studentName, contextData)

	default:
		specificInstruction = fmt.Sprintf("Buat narasi rapor untuk siswa bernama %s berdasarkan data: '%s'.", studentName, contextData)
	}

	return baseInstruction + specificInstruction
}
