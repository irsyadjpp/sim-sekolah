from app.worker import process_context_ingestion
import uuid

# Contoh ID Sekolah (Pastikan ID ini ada di tabel konteks_sekolah kamu)
ID_SEKOLAH_TEST = "3a4cbeac-3023-4699-8d52-6dc87183df49"

NARASI_TEST = """
Desa Majapahit terletak di perbukitan karst Pasimarannu. Di sini terdapat Gua Majapahit yang eksotis. 
Masyarakatnya didominasi etnis Buton dan mahir berbahasa Bonerate. 
Hasil tani utamanya adalah Kacang Hijau dengan panen 1,2 ton per hektar. 
Jarak ke ibu kota kabupaten adalah 119 mil laut dengan waktu tempuh 11 jam.
"""

if __name__ == "__main__":
    process_context_ingestion(NARASI_TEST, ID_SEKOLAH_TEST)