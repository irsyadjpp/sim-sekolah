import json
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

# Hubungkan ke Llama 3 yang berjalan di Ollama
llm = Ollama(model="llama3.2:1b", temperature=0) # Temperature 0 agar jawabannya stabil/kaku

def extract_structural_data(narasi_text):
    """Menyuruh Llama 3 mengubah narasi jadi JSON sesuai DDL"""
    
    template = """
    Kamu adalah asisten data sekolah. Tugasmu mengekstrak informasi dari teks narasi menjadi format JSON.
    
    TEKS NARASI:
    {narasi}
    
    INSTRUKSI:
    Ekstrak data ke dalam format JSON dengan kunci berikut:
    - profil_geografis (isi: bentang_alam, zona_ekologi, titik_wisata)
    - profil_sosial_budaya (isi: etnis_dominan, bahasa_daerah, tradisi_tahunan)
    - kekayaan_alam (isi: flora, fauna, hasil_tani_unggulan)
    - jarak_ke_kabupaten_mil_laut (angka saja)
    - waktu_tempuh_jam (angka saja)

    HANYA keluarkan JSON saja, jangan ada penjelasan lain.
    """
    
    prompt = PromptTemplate(input_variables=["narasi"], template=template)
    
    # Jalankan LLM
    response = llm.invoke(prompt.format(narasi=narasi_text))
    
    try:
        # Membersihkan respons jika LLM nakal dan memberi teks tambahan
        start_index = response.find('{')
        end_index = response.rfind('}') + 1
        json_str = response[start_index:end_index]
        return json.loads(json_str)
    except Exception as e:
        print(f"❌ Gagal memparsing JSON: {e}")
        return None