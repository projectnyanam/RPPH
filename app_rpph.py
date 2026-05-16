import streamlit as st
from google import genai

# ==========================================
# 1. KONFIGURASI API & CLIENT
# ==========================================
API_KEY = st.secrets["GEMINI_API_KEY"] 
client = genai.Client(api_key=API_KEY)

# ==========================================
# 2. PENGATURAN TAMPILAN HALAMAN (UI)
# ==========================================
st.set_page_config(
    page_title="Pembuat RPPH PAUD - Sentra Tumbuh Anak", 
    page_icon="📝", 
    layout="wide" # Menggunakan layout wide karena RPPH formatnya memanjang
)

st.title("📝 Generator RPPH PAUD Kurikulum Merdeka")
st.write("Susun Rencana Pelaksanaan Pembelajaran Harian (RPPH) secara instan, lengkap dengan muatan literasi, STEAM, dan rencana asesmen.")
st.markdown("---")

# ==========================================
# 3. FORMULIR INPUT GURU
# ==========================================
with st.form("form_rpph"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        topik = st.text_input("Topik / Sub-Topik", placeholder="Contoh: Alam Semesta / Benda Langit")
        usia = st.selectbox("Kelompok Usia", ["Kelompok Bermain (3-4 Tahun)", "TK A (4-5 Tahun)", "TK B (5-6 Tahun)"])
        
    with col2:
        model_belajar = st.selectbox("Model Pembelajaran", ["Sentra", "Area", "Kelompok dengan Kegiatan Pengaman", "Project Based Learning"])
        waktu = st.text_input("Alokasi Waktu", value="07.30 - 10.30 WIB")
        
    with col3:
        tujuan_khusus = st.text_area("Tujuan Khusus / Titik Berat (Opsional)", placeholder="Contoh: Fokus pada pengenalan huruf hijaiyah dan motorik halus menggunting.")

    submit_button = st.form_submit_button(label="Susun RPPH Sekarang 🚀")

# ==========================================
# 4. LOGIKA AI (DENGAN FALLBACK)
# ==========================================
if submit_button:
    if not topik:
        st.error("Mohon isi Topik / Sub-Topik terlebih dahulu.")
    else:
        with st.spinner("Merancang draf RPPH sesuai standar Kurikulum Merdeka..."):
            
            prompt_sistem = f"""
            Anda adalah seorang Asesor PAUD dan Kepala Sekolah yang ahli dalam menyusun perangkat ajar Kurikulum Merdeka.
            Buatkan Rencana Pelaksanaan Pembelajaran Harian (RPPH) yang terstruktur, praktis, dan kreatif berdasarkan data berikut:
            - Topik / Sub-Topik: {topik}
            - Usia Anak: {usia}
            - Model Pembelajaran: {model_belajar}
            - Alokasi Waktu: {waktu}
            - Catatan/Tujuan Khusus: {tujuan_khusus if tujuan_khusus else 'Buatkan tujuan umum yang holistik.'}
            
            Format jawaban harus persis seperti kerangka berikut (Gunakan Markdown tebal dan rapi):
            
            ## RENCANA PELAKSANAAN PEMBELAJARAN HARIAN (RPPH)
            **Topik/Sub Topik:** {topik} | **Kelompok:** {usia} | **Model:** {model_belajar}
            
            ### A. TUJUAN KEGIATAN (CAPAIAN PEMBELAJARAN)
            *(Buatkan 3 poin tujuan turunan dari elemen: 1. Nilai Agama & Budi Pekerti, 2. Jati Diri, 3. Dasar Literasi & STEAM)*
            
            ### B. ALAT DAN BAHAN
            *(Daftar logistik yang dibutuhkan, bagi menjadi bahan alam/loose parts dan alat tulis)*
            
            ### C. KEGIATAN PEMBUKAAN (Estimasi 30 Menit)
            1. (SOP Pembukaan: Salam, doa, presensi)
            2. (Pijakan Awal: Pemantik diskusi, apersepsi topik, menyanyi/baca buku)
            3. (Penjelasan aturan main)
            
            ### D. KEGIATAN INTI (Estimasi 60 Menit)
            *(Rancang 3-4 aktivitas bermain yang bermakna sesuai dengan {model_belajar}. Jelaskan secara ringkas cara mainnya)*
            
            ### E. ISTIRAHAT & MAKAN BERSAMA (Estimasi 30 Menit)
            *(SOP cuci tangan, doa makan, bermain bebas)*
            
            ### F. KEGIATAN PENUTUP (Estimasi 30 Menit)
            1. (Recalling / Menanyakan perasaan dan pengalaman anak saat bermain)
            2. (Penguatan konsep dan pesan moral)
            3. (SOP Penutupan: Doa, salam, informasi esok hari)
            
            ### G. RENCANA ASESMEN
            *(Berikan rekomendasi teknik asesmen yang cocok untuk hari ini, misalnya Catatan Anekdot, Hasil Karya, atau Ceklis)*
            
            ### 💡 TIPS GURU:
            *(Berikan 2 kalimat pertanyaan pemantik tingkat tinggi (HOTS) yang bisa ditanyakan guru saat mendampingi anak di Kegiatan Inti).*
            """
            
            try:
                # Coba Gemini 2.5 Flash
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt_sistem
                )
                st.success("✨ RPPH Berhasil Disusun!")
                st.markdown(response.text)
                
            except Exception as e1:
                st.info("Sistem utama sibuk, beralih ke server cadangan...")
                try:
                    # Fallback ke Gemini 2.0 Flash
                    response = client.models.generate_content(
                        model='gemini-2.0-flash',
                        contents=prompt_sistem
                    )
                    st.success("✨ RPPH Berhasil Disusun! (Server Cadangan)")
                    st.markdown(response.text)
                except Exception as e2:
                    st.error("Mohon maaf, server AI sedang penuh. Silakan coba sebentar lagi.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 12px;'>Dikembangkan untuk mendukung administrasi pendidik yang efisien.</p>", unsafe_allow_html=True)
