import streamlit as st

def main():
    st.title("Prediksi Kesehatan Mental Karyawan")
    
    st.subheader("Usia dan Identitas")

    # Pertanyaan Usia
    usia = st.slider("Berapa usia Anda?", min_value=0, max_value=100, value=25)

    # Pertanyaan Jenis Kelamin
    jenis_kelamin_options = ["Laki-laki", "Perempuan"]
    jenis_kelamin = st.selectbox("Jenis kelamin Anda apa?", jenis_kelamin_options)

    st.subheader("Permasalahan Kesehatan Mental Sebelumnya")
    # Pertanyaan Masalah Kesehatan Sebelumnya
    masalah_kesehatan_sebelumnya1_options = ["Iya","Tidak","Tidak tahu"]
    masalah_kesehatan1 = st.selectbox("Pernahkah Anda mengalami gangguan kesehatan mental sebelumnya?", masalah_kesehatan_sebelumnya1_options)

    masalah_kesehatan_sebelumnya2_options = ["Iya","Tidak","Tidak tahu"]
    masalah_kesehatan2 = st.selectbox("Apakah ada riwayat gangguan kesehatan mental dalam keluarga Anda?", masalah_kesehatan_sebelumnya2_options)

    masalah_kesehatan_sebelumnya3_options = ["Iya","Tidak"]
    masalah_kesehatan3 = st.selectbox("Pernahkah Anda mencari perawatan dari profesional kesehatan mental untuk gangguan kesehatan mental?", masalah_kesehatan_sebelumnya3_options)

    st.subheader("Pentingnya Kesehatan Mental di Tempat Kerja")
    st.subheader("Manfaat Kesehatan Mental di Tempat Kerja")
    st.subheader("Kenyamanaan Berbicara tentang Kesehatan Mental")
    st.subheader("Faktor – Faktor Tambahan")


    # Menampilkan hasil
    st.write(f"Usia: {usia} tahun")
    st.write(f"Jenis Kelamin: {jenis_kelamin}")

if __name__ == "__main__":
    main()
