import subprocess
import streamlit as st

# Install the dependencies using pip
st.text("Installing dependencies...")
subprocess.run(["pip", "install", "-r", "requirements.txt"])

st.success("Dependencies installed successfully!")

import streamlit as st
import pickle
import pandas as pd
import os
import numpy as np
import subprocess
from sklearn.neural_network import MLPClassifier

# Function to load the pickle model
def load_model(file_path):
    with open(file_path, 'rb') as model_file:
        model = pickle.load(model_file)
    return model

# Get the absolute path to the file
file_path = os.path.abspath("mlp_model.pkl")

# Load the machine learning model from the pickle file
model = load_model(file_path)

def main():
    st.title("Prediksi Kesehatan Mental Karyawan")

    st.markdown("""---""")
    
    st.subheader("Usia dan Identitas")

    # Pertanyaan Usia
    Age = st.slider("Berapa usia Anda?", min_value=0, max_value=100, value=25)

    # Pertanyaan Jenis Kelamin
    Gender_options = ["Laki-laki", "Perempuan"]
    Gender = st.selectbox("Jenis kelamin Anda apa?", Gender_options)

    st.markdown("""---""")

    st.subheader("Permasalahan Kesehatan Mental Sebelumnya")
    # Pertanyaan Masalah Kesehatan Sebelumnya
    Past_disorder_options = ["Iya","Tidak","Tidak tahu"]
    Past_disorder = st.selectbox("Pernahkah Anda mengalami gangguan kesehatan mental sebelumnya?", Past_disorder_options)

    Family_history_options = ["Iya", "Tidak", "Tidak tahu"]
    Family_history = st.selectbox("Apakah ada riwayat gangguan kesehatan mental dalam keluarga Anda?", Family_history_options)

    Mental_health_treatment_options = ["Iya", "Tidak"]
    Mental_health_treatment = st.selectbox("Pernahkah Anda mencari perawatan dari profesional kesehatan mental untuk gangguan kesehatan mental?", Mental_health_treatment_options)

    st.markdown("""---""")

    st.subheader("Pentingnya Kesehatan Mental di Tempat Kerja")
    # Pertanyaan Pentingnya Kesehatan Mental di Tempat Kerja
    Employer_mental_health_importance2 = st.slider("Seberapa penting menurut Anda perusahaan Anda menghargai kesehatan mental?", min_value=0, max_value=10, value=1)
    Tech_industry_support = st.slider("Bagaimana menurut Anda dukungan yang diberikan perusahaan Anda kepada karyawan yang memiliki permasalahan kesehatan mental?", min_value=0, max_value=5, value=1)
    Employer_physical_health_importance1 = st.slider("Seberapa penting menurut Anda perusahaan Anda dalam menghargai kesehatan fisik?", min_value=0, max_value=10, value=1)

    st.markdown("""---""")
    
    st.subheader("Manfaat Kesehatan Mental di Tempat Kerja")
    # Pertanyaan Manfaat Kesehatan Mental di Tempat Kerja
    Health_benefits_options = ["Iya","Tidak","Tidak tahu"]
    Health_benefits = st.selectbox("Apakah perusahaan Anda menyediakan manfaat kesehatan mental sebagai bagian dari cakupan perawatan kesehatan mental?", Health_benefits_options)
    
    Previous_benefits_options = ["Iya","Tidak","Tidak tahu"]
    Previous_benefits = st.selectbox("Apakah perusahaan – perusahaan sebelumnya Anda menyediakan manfaat kesehatan mental?", Previous_benefits_options)

    Mental_health_options_options = ["Iya","Tidak","Tidak tahu"]
    Mental_health_options = st.selectbox("Apakah Anda mengetahui opsi perawatan kesehatan mental yang disediakan oleh perusahaan – perusahaan sebelumnya tempat Anda bekerja?", Mental_health_options_options)

    st.markdown("""---""")
    
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

    st.markdown("""---""")
    
    st.subheader("Faktor – Faktor Tambahan")
    # Pertanyaan Faktor - Faktor Tambahan
    Employees_count_options = ["1-100","100-1000","Lebih dari 1000"]
    Employees_count = st.selectbox("Berapa jumlah karyawan di perusahaan atau organisasi anda bekerja?", Employees_count_options)

    Medical_leave_ease_options = ["Sulit","Saya tidak tahu","Agak sulit","Agak mudah","Sangat mudah"]
    Medical_leave_ease = st.selectbox("Jika masalah kesehatan mental mendorong anda untuk mengajukan cuti medis dari pekerjaan, seberapa mudah atau sulitnya untuk meminta cuti tersebut?", Medical_leave_ease_options)

    Health_disclosure_options = ["Iya","Tidak","Mungkin"]
    Health_disclosure = st.selectbox("Apakah anda bersedia untuk membicarakan masalah kesehatan fisik dengan calon pemberi kerja dalam wawancara kerja?", Health_disclosure_options)

    Emotions = st.text_input("Apa yang membuat Anda merasa cemas atau stres akhir-akhir ini?")

    st.markdown("""---""")

    # Create dataframe
    df = [['Age',
          'Gender',
           'Past_disorder',
           'Family_history',
           'Mental_health_treatment',
           'Employer_mental_health_importance2',
           'Tech_industry_support',
           'Employer_physical_health_importance1',
           'Health_benefits,
           'Previous_benefits',
           'Mental_health_options',
           'Share_mental_illness',
           'Supervisor_comfort',
           'Coworker_mental_health_discussion1',
           'Coworker_mental_health_discussion2',
           'Employer_mental_health_discussion',
           'Employees_count',
           'Medical_leave_ease',
           'Health_disclosure',
           'Emotions'
          ]]

    st.dataframe(df)

    st.markdown("""---""")

    # Menampilkan hasil
    st.write(f"Usia: {Age} tahun")
    st.write(f"Jenis Kelamin: {Gender}")

if __name__ == "__main__":
    main()
