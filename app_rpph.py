import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

app = FastAPI(title="API Generator RPPH Harian PAUD")

# Mengizinkan halaman Blogger/WordPress Anda untuk mengakses API ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mengambil API Key dari Hugging Face Secrets
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# Struktur data input yang dikirim oleh Guru dari form Blogger
class RPPHHarianRequest(BaseModel):
    hari_tanggal: str
    topik: str
    sub_topik: str
    usia: str
    model_belajar: str
    waktu: str
    catatan_khusus: str

@app.post("/generate-rpph")
async def buat_rpph_harian(data: RPPHHarianRequest):
    # Prompt super detail standar Pengawas/Asesor PAUD Kurikulum Merdeka
    prompt_sistem = f"""
    Anda adalah seorang pengembang kurikulum PAUD, Asesor Akreditasi, dan Kepala Sekolah yang sangat ahli dalam menyusun perangkat ajar Kurikulum Merdeka.
    Buatkan Rencana Pelaksanaan Pembelajaran Harian (RPPH) Harian yang sangat detail, aplikatif, dan kreatif berdasarkan data berikut:
    
    - Hari / Tanggal: {data.hari_tanggal}
    - Topik Utama: {data.topik}
    - Sub-Topik / Fokus Hari Ini: {data.sub_topik}
    - Kelompok Usia: {data.usia}
    - Model Pembelajaran: {data.model_belajar}
    - Alokasi Waktu: {data.waktu}
    - Catatan Khusus/Kebutuhan Kelas: {data.catatan_khusus if data.catatan_khusus else 'Fokus pada stimulasi holistik integratif.'}
    
    Format jawaban harus rapi, menggunakan penomoran yang jelas, dan siap disalin ke Microsoft Word dengan struktur berikut:
    
    ============================================================
    RENCANA PELAKSANAAN PEMBELAJARAN HARIAN (RPPH) PAUD
    ============================================================
    * Hari/Tanggal : {data.hari_tanggal}
    * Kelompok Usia: {data.usia}
    * Alokasi Waktu: {data.waktu}
    * Model Pembelajaran: {data.model_belajar}
    * Topik / Sub-Topik: {data.topik} / {data.sub_topik}
    
    A. TUJUAN KEGIATAN & STIMULASI (CAPAIAN PEMBELAJARAN)
       (Tuliskan 3 poin tujuan operasional yang spesifik mencakup: 1. Nilai Agama & Budi Pekerti, 2. Jati Diri, 3. Dasar Literasi & STEAM yang berkaitan dengan sub-topik)
    
    B. ALAT DAN BAHAN BERMAIN (Utamakan Loose Parts)
       (Sebutkan daftar alat tulis dan ragam bahan alam/kardus/barang bekas yang kontekstual dan aman untuk anak usia {data.usia})
    
    C. KEGIATAN PEMBUKAAN (Estimasi 30 Menit)
       1. SOP Pembukaan (Penyambutan, jurnal pagi, berbaris, salam, doa, fisik motorik kasar pagi).
       2. Pijakan Sebelum Bermain (Membaca buku cerita/pemantik video/diskusi interaktif terkait sub-topik, kosakata baru, apersepsi).
       3. Penjelasan aturan bermain dan mengenalkan ragam main inti.
    
    D. KEGIATAN INTI (Estimasi 60 Menit)
       (Rancang minimal 3-4 pilihan kegiatan bermain yang merdeka, berpusat pada anak, dan berbasis STEAM/Loose parts yang menyenangkan sesuai model {data.model_belajar}. Berikan instruksi singkat cara mainnya).
    
    E. ISTIRAHAT, SNACK TIME & BERMAIN BEBAS (Estimasi 30 Menit)
       (SOP mencuci tangan dengan sabun, doa sebelum/sesudah makan, makan bekal bersama, bermain bebas di luar/dalam ruangan secara aman).
    
    F. KEGIATAN PENUTUP & RECALLING (Estimasi 30 Menit)
       1. Kegiatan Recalling (Guru menanyakan perasaan anak, mempersilakan anak menceritakan hasil karya atau pengalaman bermainnya hari ini).
       2. Refleksi & Penguatan (Guru memberikan pijakan moral/konsep bermakna dari apa yang dipelajari hari ini).
       3. SOP Penutupan (Informasi kegiatan esok hari, doa pulang, salam).
    
    G. RENCANA ASESMEN / PENILAIAN HARIAN
       (Sebutkan indikator penilaian apa yang akan diamati dan rekomendasikan teknik asesmen harian yang paling cocok untuk kegiatan ini, seperti Catatan Anekdot, Hasil Karya, atau Ceklis Perkembangan).
    
    💡 PERTANYAAN PEMANTIK GURU (HOTS):
       (Tuliskan 2-3 contoh pertanyaan terbuka tingkat tinggi yang bisa diajukan guru saat mendampingi anak bermain untuk merangsang nalar kritis mereka).
    """
    
    # SISTEM FALLBACK AI OTOMATIS
    try:
        # Mencoba server utama (Gemini 2.5 Flash - Kuota Longgar & Cepat)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_sistem
        )
        return {"status": "sukses", "hasil": response.text}
    except Exception as e_utama:
        try:
            # Jika server utama sibuk, otomatis dialihkan ke server cadangan (Gemini 2.0 Flash)
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt_sistem
            )
            return {"status": "sukses", "hasil": response.text}
        except Exception as e_cadangan:
            # Jika kedua server Google sedang over-capacity
            raise HTTPException(status_code=500, detail="Semua jalur server AI sedang padat. Silakan coba klik tombol sekali lagi.")
