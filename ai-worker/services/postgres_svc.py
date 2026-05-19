import psycopg2
import os
import json
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Membuka koneksi ke PostgreSQL menggunakan env variables."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "sim_sekolah_terpadu"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASS", "password")
    )

def fetch_data_by_category(cat, target_id):
    """
    Mengambil teks mentah dan metadata dasar dari DB berdasarkan kategori RAG.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # KATEGORI A: Dokumen Nasional (Capaian Pembelajaran)
        if cat == 'A':
            cur.execute("""
                SELECT lo.outcome_text, s.subject_name, p.code 
                FROM learning_outcome lo
                JOIN subject s ON lo.subject_id = s.id
                JOIN phase p ON lo.phase_id = p.id
                WHERE lo.id = %s""", (target_id,))
            res = cur.fetchone()
            if res: return res, {"subject": res, "phase": res}

        # KATEGORI B: Data Sekolah (Visi, Misi, Budaya)
        elif cat == 'B':
            cur.execute("SELECT school_name, address FROM school WHERE id = %s", (target_id,))
            res = cur.fetchone()
            # Bisa ditambah query ke konteks_sekolah jika perlu join
            if res: return f"Visi Misi Sekolah {res} di {res}", {"school_name": res}

        # KATEGORI C: Data Guru (Preferensi Mengajar)
        elif cat == 'C':
            cur.execute("SELECT teaching_preference, full_name FROM teacher WHERE id = %s", (target_id,))
            res = cur.fetchone()
            if res: return res, {"teacher_name": res}

        # KATEGORI D: Data Peserta Didik (Karakteristik Kelas)
        elif cat == 'D':
            cur.execute("SELECT class_characteristics, classroom_name FROM classroom WHERE id = %s", (target_id,))
            res = cur.fetchone()
            if res: return res, {"class_name": res}

        # KATEGORI E: Konteks Lokal (Data Desa/Lingkungan)
        elif cat == 'E':
            # Mengambil dari tabel konteks_sekolah yang menyimpan JSONB profil
            cur.execute("SELECT profil_sosial_budaya, kekayaan_alam FROM konteks_sekolah WHERE id = %s", (target_id,))
            res = cur.fetchone()
            if res:
                text = f"Budaya: {json.dumps(res)}. Alam: {json.dumps(res)}"
                return text, {"context": "local_environment"}

        return None, None
    except Exception as e:
        print(f"❌ DB Fetch Error: {e}")
        return None, None
    finally:
        cur.close()
        conn.close()

def save_chunk(chunk_id, sekolah_id, chunk_text, category, source_name, metadata):
    """Menyimpan potongan teks dan metadatanya ke tabel konteks_chunks."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO konteks_chunks (id, sekolah_id, chunk_text, category, source_name, metadata)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (chunk_id, sekolah_id, chunk_text, category, source_name, json.dumps(metadata))
        )
        conn.commit()
    except Exception as e:
        print(f"❌ Error Saving Chunk: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()