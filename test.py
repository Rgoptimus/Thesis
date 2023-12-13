import streamlit as st

def main():
    st.title("Prediksi Kesehatan Mental Karyawan")
    
    st.subheader("Usia dan Identitas")

    # Pertanyaan Usia
    Age = st.slider("Berapa usia Anda?", min_value=0, max_value=100, value=25)

    # Pertanyaan Jenis Kelamin
    Gender_options = ["Laki-laki", "Perempuan"]
    Gender = st.selectbox("Jenis kelamin Anda apa?", Gender_options)

    st.subheader("Permasalahan Kesehatan Mental Sebelumnya")
    # Pertanyaan Masalah Kesehatan Sebelumnya
    Past_disorder_options = ["Iya","Tidak","Tidak tahu"]
    Past_disorder = st.selectbox("Pernahkah Anda mengalami gangguan kesehatan mental sebelumnya?", Past_disorder_options)

    Family_history_options = ["Iya", "Tidak", "Tidak tahu"]
    Family_history = st.selectbox("Apakah ada riwayat gangguan kesehatan mental dalam keluarga Anda?", Family_history_options)

    Mental_health_treatment_options = ["Iya", "Tidak"]
    Mental_health_treatment = st.selectbox("Pernahkah Anda mencari perawatan dari profesional kesehatan mental untuk gangguan kesehatan mental?", Mental_health_treatment_options)

    st.subheader("Pentingnya Kesehatan Mental di Tempat Kerja")
    # Pertanyaan Pentingnya Kesehatan Mental di Tempat Kerja
    Employer_mental_health_importance2 = st.slider("Seberapa penting menurut Anda perusahaan Anda menghargai kesehatan mental?", min_value=0, max_value=10, value=1)
    Tech_industry_support = st.slider("Bagaimana menurut Anda dukungan yang diberikan perusahaan Anda kepada karyawan yang memiliki permasalahan kesehatan mental?", min_value=0, max_value=5, value=1)
    Employer_physical_health_importance1 = st.slider("Seberapa penting menurut Anda perusahaan Anda dalam menghargai kesehatan fisik?", min_value=0, max_value=10, value=1)
    
    st.subheader("Manfaat Kesehatan Mental di Tempat Kerja")
    # Pertanyaan Manfaat Kesehatan Mental di Tempat Kerja
    Health_benefits_options = ["Iya","Tidak","Tidak tahu"]
    Health_benefits = st.selectbox("Apakah perusahaan Anda menyediakan manfaat kesehatan mental sebagai bagian dari cakupan perawatan kesehatan mental?", Health_benefits_options)
    
    Previous_benefits_options = ["Iya","Tidak","Tidak tahu"]
    Previous_benefits = st.selectbox("Apakah perusahaan – perusahaan sebelumnya Anda menyediakan manfaat kesehatan mental?", Previous_benefits_options)

    Mental_health_options_options = ["Iya","Tidak","Tidak tahu"]
    Mental_health_options = st.selectbox("Apakah Anda mengetahui opsi perawatan kesehatan mental yang disediakan oleh perusahaan – perusahaan sebelumnya tempat Anda bekerja?", Mental_health_options_options)
    
    st.subheader("Kenyamanan Berbicara tentang Kesehatan Mental")
    # Pertanyaan Kenyamanan Berbicara tertang Kesehatan Mental
    Share_mental_illness_options = ["Tidak berlaku untuk saya","Tidak terbuka sama sekali","Netral","Agak tidak terbuka","Agak terbuka","Sangat terbuka"]
    Share_mental_illness = st.selectbox("Seberapa bersedia Anda untuk berbicara kepada teman dan keluarga bahwa Anda memiliki masalah kesehatan mental?", Share_mental_illness_options)

    Supervisor_comfort_options = ["Iya","Tidak","Mungkin"]
    Supervisor_comfort = st.selectbox("Apakah Anda merasa nyaman untuk berbicara tentang masalah kesehatan mental dengan atasan langsung Anda?", Supervisor_comfort_options)

    Coworker_mental_health_discussion1_options = ["Iya","Tidak","Mungkin"]
    Coworker_mental_health_discussion1 = st.selectbox("Apakah Anda merasa nyaman untuk berbicara tentang masalah kesehatan mental dengan rekan kerja Anda?", Coworker_mental_health_discussion1_options)

    Coworker_mental_health_discussion2_options = ["Iya","Tidak"]
    Coworker_mental_health_discussion2 = st.selectbox("Pernahkah Anda membicarakan masalah kesehatan mental dengan rekan kerja Anda?", Coworker_mental_health_discussion2_options)

    Employer_mental_health_discussion_options = ["Iya","Tidak"]
    Employer_mental_health_discussion = st.selectbox("Pernahkah Anda membicarakan masalah kesehatan mental dengan atasan Anda?", Employer_mental_health_discussion_options)
    
    st.subheader("Faktor – Faktor Tambahan")
    # Pertanyaan Faktor - Faktor Tambahan


    # Menampilkan hasil
    st.write(f"Usia: {usia} tahun")
    st.write(f"Jenis Kelamin: {jenis_kelamin}")

if __name__ == "__main__":
    main()
