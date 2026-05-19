import uuid
from langchain_text_splitters import RecursiveCharacterTextSplitter
from services.postgres_svc import fetch_data_by_category, save_chunk
from services.qdrant_svc import upsert_vector, init_qdrant

# Pastikan koleksi Qdrant sudah ada saat worker mulai
init_qdrant()

def process_comprehensive_ingestion(task_data):
    """
    Dispatcher utama untuk memproses ingestion berdasarkan kategori A-E.
    task_data contoh: {"category": "A", "sekolah_id": "...", "target_id": "...", "source_name": "CP Matematika"}
    """
    cat = task_data.get('category')
    sekolah_id = task_data.get('sekolah_id')
    target_id = task_data.get('target_id')
    source_name = task_data.get('source_name', 'unknown_source')

    print(f"\n⚙️  Processing Ingestion - Category: {cat} | Source: {source_name}")

    # 1. Ambil Konten dan Metadata Awal dari Database
    content, base_metadata = fetch_data_by_category(cat, target_id)
    
    if not content:
        print(f"⚠️  Data tidak ditemukan atau kosong untuk ID: {target_id}")
        return False

    # 2. Tentukan Strategi Chunking (Besar potongan teks)
    # A & E (Regulasi & Lingkungan) butuh konteks luas. 
    # C & D (Guru & Siswa) biasanya teks pendek/profil, butuh chunk padat.
    if cat in ['A', 'E']:
        chunk_size = 1200
        chunk_overlap = 200
        separators = ["\n# ", "\n## ", "\n\n", ". ", " "]
    else:
        chunk_size = 600
        chunk_overlap = 100
        separators = ["\n\n", "\n", " "]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators
    )
    
    chunks = splitter.split_text(content)
    print(f"✂️  Teks dipecah menjadi {len(chunks)} chunks.")

    # 3. Simpan per Chunk ke Postgres dan Qdrant
    for i, text in enumerate(chunks):
        chunk_id = str(uuid.uuid4())
        
        # Gabungkan metadata agar pencarian RAG nantinya sangat akurat
        full_metadata = {
            **base_metadata,
            "sekolah_id": sekolah_id,
            "category_code": cat,
            "chunk_index": i,
            "source": source_name
        }

        # A. Simpan teks asli ke Postgres (untuk referensi tampilan UI)
        save_chunk(chunk_id, sekolah_id, text, cat, source_name, full_metadata)
        
        # B. Simpan vektor ke Qdrant (untuk 'otak' pencarian AI)
        try:
            upsert_vector(chunk_id, text, full_metadata)
        except Exception as e:
            print(f"❌ Qdrant Error pada chunk {i}: {e}")
            continue

        if (i + 1) % 10 == 0:
            print(f"⏳ Telah memproses {i+1}/{len(chunks)} chunks...")

    print(f"✅ Berhasil Ingest Kategori {cat}: {source_name}")
    return True