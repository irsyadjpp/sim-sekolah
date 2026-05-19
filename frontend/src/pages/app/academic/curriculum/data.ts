export interface CPData {
  id: string;
  subject: string;
  phase: string;
  rasional: string;
  tujuan: string;
  karakteristik: { elemen: string; deskripsi: string }[];
  capaian: string[];
}

export const dummyData: CPData[] = [
  {
    id: "1",
    subject: "Matematika",
    phase: "Fase A",
    rasional:
      "Matematika merupakan ilmu yang mendasari perkembangan teknologi modern. Pada Fase A, rasional utamanya adalah membangun fondasi penalaran dasar dan kepekaan bilangan (number sense).",
    tujuan:
      "Peserta didik dapat memahami konsep dasar bilangan, operasi hitung sederhana, dan pengenalan bangun datar serta ruang.",
    karakteristik: [
      { elemen: "Bilangan", deskripsi: "Mengenal dan memahami bilangan cacah sampai 100." },
      { elemen: "Aljabar", deskripsi: "Mengenal pola gambar dan pola bilangan sederhana." },
      { elemen: "Geometri", deskripsi: "Mengenal bangun datar dan bangun ruang dasar." },
    ],
    capaian: [
      "Peserta didik dapat membaca, menulis, dan membandingkan bilangan bulat hingga 100.",
      "Peserta didik dapat melakukan operasi penjumlahan dan pengurangan sederhana.",
      "Peserta didik dapat mengidentifikasi bentuk-bentuk geometri di sekitarnya.",
    ],
  },
  {
    id: "2",
    subject: "Bahasa Indonesia",
    phase: "Fase B",
    rasional:
      "Bahasa Indonesia adalah alat komunikasi utama. Pada Fase B, difokuskan pada peningkatan literasi membaca dan menulis teks dengan struktur yang lebih kompleks.",
    tujuan:
      "Peserta didik mampu memahami teks informasional dan fiksi, serta menyajikan gagasan secara lisan dan tulisan yang terstruktur.",
    karakteristik: [
      { elemen: "Menyimak", deskripsi: "Mampu menyimak dan memahami informasi dari teks lisan." },
      { elemen: "Membaca", deskripsi: "Mampu membaca lancar dan memahami ide pokok teks." },
      { elemen: "Menulis", deskripsi: "Mampu menulis narasi dan deskripsi sederhana." },
    ],
    capaian: [
      "Peserta didik dapat menyimpulkan informasi dari teks yang dibaca.",
      "Peserta didik dapat menulis karangan singkat dengan ejaan yang benar.",
      "Peserta didik dapat menyampaikan presentasi singkat di depan kelas.",
    ],
  },
  {
    id: "3",
    subject: "Ilmu Pengetahuan Alam (IPA)",
    phase: "Fase C",
    rasional:
      "IPA memfasilitasi peserta didik untuk mengeksplorasi alam semesta. Fase C mempersiapkan pemikiran analitis terhadap fenomena alam.",
    tujuan:
      "Peserta didik mampu menjelaskan konsep sains dasar dan melakukan eksperimen sederhana dengan metode ilmiah.",
    karakteristik: [
      { elemen: "Pemahaman Sains", deskripsi: "Memahami interaksi antar makhluk hidup dan lingkungannya." },
      { elemen: "Keterampilan Proses", deskripsi: "Mampu mengamati, menanya, dan melakukan percobaan sederhana." },
    ],
    capaian: [
      "Peserta didik mampu menganalisis sistem organ pada manusia dan fungsinya.",
      "Peserta didik mampu melakukan percobaan sederhana tentang perubahan wujud benda.",
      "Peserta didik mampu menjelaskan peran energi listrik dalam kehidupan.",
    ],
  },
];
