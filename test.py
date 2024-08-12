import subprocess
import streamlit as st
import pickle
import pandas as pd
import os
import numpy as np
import subprocess
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OrdinalEncoder
import requests
from transformers import pipeline
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from streamlit_gsheets import GSheetsConnection
import subprocess


# Establishing a google sheet connection
conn = st.experimental_connection("gsheets", type = GSheetsConnection)
# Fetch existing vendors data
existing_data = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1z7UPC-LoZDsNvsVbGv4cYsAM8D65wdIKci3xBXGMTqw/edit?usp=sharing", usecols=list(range(24)), ttl=100)


# Function to load the model from a pickle file
def load_model(file_path):
    with open(file_path, 'rb') as model_file:
        model = pickle.load(model_file)
    return model

# Load model
file_path = os.path.abspath("mlp_model_fix.pkl")
model = load_model(file_path)

# Function to categorize age
def categorize_age(age):
    if 11 <= age <= 26:
        return '11-26'
    if 27 <= age <= 42:
        return '27-42'
    if 43 <= age <= 58:
        return '43-58'
    if 59 <= age <= 68:
        return '59-68'
    else:
        return 'Tidak diketahui'

# Function to encode categorical columns
def encode_columns(df, columns_to_encode):
    encoder = OrdinalEncoder()
    df[columns_to_encode] = encoder.fit_transform(df[columns_to_encode])
    df[columns_to_encode] = df[columns_to_encode].astype(int)
    return df

# Streamlit app
def main():
    st.title("Prediksi Kesehatan Mental Karyawan")
    st.markdown("""<div style="text-align: justify;">
                    Apps ini hanyalah sebuah model prediksi dan tidak boleh dianggap sebagai pengganti nasihat profesional.
                    Hasil yang diberikan oleh model ini mungkin saja tidak akurat atau tidak sesuai dengan keadaan individual.
                    Apabila anda mengalami potensi permasalahan kesehatan mental atau memiliki kekhawatiran terkait  dengan kesejahteraan psikologis,
                    segera konsultasikan dengan tenaga kesehatan mental atau profesional terkait.<br><br>
                    <strong> Catatan: Apps ini akan merekam hasil data kuesioner yang diisi oleh pengguna dan akan terjamin kerahasiaannya
                    </div>
                    """, unsafe_allow_html=True)
    st.markdown("""---""")
    
    st.subheader("Identitas")

    # Pertanyaan Nama
    Nama = st.text_input("Masukan nama/inisial anda?")

    # Pertanyaan Usia
    Age = st.slider("Berapa usia Anda?", min_value=11, max_value=68, value=25)

    # Pertanyaan Jenis Kelamin
    Gender_options = ["Laki-laki", "Perempuan"]
    Gender = st.selectbox("Jenis kelamin Anda apa?", Gender_options)

    st.markdown("""---""")

    st.subheader("Riwayat Kesehatan Mental")
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
    st.markdown("""Rentang nilai: 0 (Tidak Penting Sama Sekali) - 10 (Sangat Penting)""")
    Employer_mental_health_importance2 = st.slider("Seberapa penting menurut Anda perusahaan Anda menghargai kesehatan mental?", min_value=0, max_value=10, value=1)
    
    st.markdown("""Rentang nilai: 0 (Tidak Penting Sama Sekali) - 10 (Sangat Penting)""")
    Employer_physical_health_importance1 = st.slider("Seberapa penting menurut Anda perusahaan Anda dalam menghargai kesehatan fisik?", min_value=0, max_value=10, value=1)

    st.markdown("""Rentang nilai: 1 (Sangat Tidak Didukung) - 5 (Sangat Didukung)""")
    Tech_industry_support = st.slider("Bagaimana menurut Anda dukungan yang diberikan perusahaan Anda kepada karyawan yang memiliki gangguan kesehatan mental?", min_value=0, max_value=5, value=1)
    
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

    # Membuat dataframe
    data = [[Nama, Age,
            Gender,
           Past_disorder,
           Family_history,
           Mental_health_treatment,
           Employer_mental_health_importance2,
           Tech_industry_support,
           Employer_physical_health_importance1,
           Health_benefits,
           Previous_benefits,
           Mental_health_options,
           Share_mental_illness,
           Supervisor_comfort,
           Coworker_mental_health_discussion1,
           Coworker_mental_health_discussion2,
           Employer_mental_health_discussion,
           Employees_count,
           Medical_leave_ease,
           Health_disclosure,
           Emotions
          ]]

    df_x = pd.DataFrame(data, columns=['Nama','Age','Gender','Past_disorder',
                                 'Family_history','Mental_health_treatment',
                                'Employer_mental_health_importance2','Tech_industry_support',
                                'Employer_physical_health_importance1','Health_benefits','Previous_benefits',
                                'Mental_health_options','Share_mental_illness','Supervisor_comfort',
                                'Coworker_mental_health_discussion1','Coworker_mental_health_discussion2',
                                'Employer_mental_health_discussion','Employees_count','Medical_leave_ease',
                                'Health_disclosure','Emotions'])

    # Menambah tombol "Submit"
    submit_button = st.button("Submit")
    
    # Menambah keadaan apabila tombol ditekan
    if submit_button:
        st.subheader("""Rangkuman Data Karyawan""")
        st.markdown(f"Nama: {Nama}")
        st.markdown(f"Umur: {Age}")
        st.markdown(f"Jenis kelamin: {Gender}")
        st.markdown(f"Memiliki pengalaman masa lalu terhadap kesehatan mental: {Past_disorder}")
        st.markdown(f"Memiliki latar belakang keluarga yang memiliki gangguan kesehatan mental: {Family_history}")
        st.markdown(f"Pernah mencari penanganan kesehatan mental: {Mental_health_treatment}")
        st.markdown(f"Nilai akan pentingnya kesehatan mental: {Employer_mental_health_importance2}")
        st.markdown(f"Nilai akan pentingnya dukungan teknologi industri: {Tech_industry_support}")
        st.markdown(f"Nilai akan pentingnya kesehatan fisik: {Employer_physical_health_importance1}")
        st.markdown(f"Perusahaan saat ini menyediakan manfaat kesehatan: {Health_benefits}")
        st.markdown(f"Perusahaan sebelumnya menyediakan manfaat kesehatan: {Previous_benefits}")
        st.markdown(f"Mengetahui opsi perawatan kesehatan mental: {Mental_health_options}")
        st.markdown(f"Bersedia membagikan cerita tentang kesehatan mental: {Share_mental_illness}")
        st.markdown(f"Pernah membagikan cerita tentang kesehatan mental ke atasan: {Employer_mental_health_discussion}")
        st.markdown(f"Merasa nyaman ketika bercerita dengan atasan: {Supervisor_comfort}")
        st.markdown(f"Pernah membagikan cerita tentang kesehatan mental ke rekan kerja: {Coworker_mental_health_discussion2}")
        st.markdown(f"Merasa nyaman ketika bercerita dengan rekan kerja: {Coworker_mental_health_discussion1}")
        st.markdown(f"Jumlah karyawan di perusahaan: {Employees_count}")
        st.markdown(f"Mudah mendapatkan izin sakit: {Medical_leave_ease}")
        st.markdown(f"Bersedia berdiskusi mengenai permasalahan kesehatan mental dengan pemberi kerja: {Health_disclosure}")
        if Emotions != "":
            st.markdown(f"Perasaan hari ini: {Emotions}")
        else:
            st.warning("Semua pertanyaan harus terisi. Mohon isi pertanyaan tentang perasaan hari ini.")
        # Stop execution if Emotions is null
            st.stop()
           
    st.markdown("""---""")
    
    # Menambah tombol "Predict"
    predict_button = st.button("Predict")

    # Membuat fungsi if apabila tombol predict ditekan
    if predict_button:
        df_x['Gender'] = df_x['Gender'].replace({
                            'Laki-laki':'Male',
                            'Perempuan' : 'Female'})

        df_x['Past_disorder'] = df_x['Past_disorder'].replace({
                                'Iya': 'Yes',
                                'Tidak': 'No',
                                'Tidak tahu': "I don't know"})

        df_x['Family_history'] = df_x['Family_history'].replace({
                                'Iya': 'Yes',
                                'Tidak': 'No',
                                'Tidak tahu': "I don't know"})

        df_x['Mental_health_treatment'] = df_x['Mental_health_treatment'].replace({
                                        'Iya': 1,
                                        'Tidak': 0})

        df_x['Health_benefits'] = df_x['Health_benefits'].replace({
                                    'Iya': 'Yes',
                                    'Tidak': 'No',
                                    'Tidak tahu': "I don't know"})

        df_x['Previous_benefits'] = df_x['Previous_benefits'].replace({
                                    'Iya': 'Yes',
                                    'Tidak': 'No',
                                    'Tidak tahu': "I don't know"})

        df_x['Mental_health_options'] = df_x['Mental_health_options'].replace({
                                        'Iya': 'Yes',
                                        'Tidak': 'No',
                                        'Tidak tahu': "I don't know"})

        df_x['Share_mental_illness'] = df_x['Share_mental_illness'].replace({
                                        'Tidak berlaku untuk saya' : 'Not applicable to me (I do not have a mental illness)',
                                        'Tidak terbuka sama sekali' : 'Not open at all',
                                        'Netral' : 'Neutral',
                                        'Agak tidak terbuka' : 'Somewhat not open',
                                        'Agak terbuka' : 'Somewhat open',
                                        'Sangat terbuka' : 'Very open'})

        df_x['Supervisor_comfort'] = df_x['Supervisor_comfort'].replace({
                                    'Iya': 'Yes',
                                    'Tidak': 'No',
                                    'Mungkin': 'Maybe'})

        df_x['Coworker_mental_health_discussion1'] = df_x['Coworker_mental_health_discussion1'].replace({
                                                    'Iya': 'Yes',
                                                    'Tidak': 'No',
                                                    'Mungkin': 'Maybe'})

        df_x['Coworker_mental_health_discussion2'] = df_x['Coworker_mental_health_discussion2'].replace({
                                                    'Iya': 1,
                                                    'Tidak': 0})

        df_x['Employer_mental_health_discussion'] = df_x['Employer_mental_health_discussion'].replace({
                                                    'Iya': 1,
                                                    'Tidak': 0})

        df_x['Medical_leave_ease'] = df_x['Medical_leave_ease'].replace({
            'Sulit' : 'Difficult',
            'Saya tidak tahu' : "I don't know",
            'Agak sulit': 'Somewhat difficult',
            'Agak mudah': 'Somewhat easy',
            'Sangat mudah' : 'Very easy'
        })

        df_x['Health_disclosure'] = df_x['Health_disclosure'].replace({
            'Iya': 'Yes',
            'Tidak': 'No',
            'Mungkin': 'Maybe'
        })

        df_x['Employees_count'] = df_x['Employees_count'].replace({
            '1-100': 0,
            '100-1000': 1,
            'Lebih dari 1000': 2
        })

        df_x['Age'] = df_x['Age'].astype('int')
        df_x['Category_age'] = df_x['Age'].apply(categorize_age)

        df_x['Employer_physical_health_importance1'] = df_x['Employer_physical_health_importance1'].astype('float')
        df_x['Employer_mental_health_importance2'] = df_x['Employer_mental_health_importance2'].astype('float')
        df_x['Tech_industry_support'] = df_x['Tech_industry_support'].astype('float')
        df_x['Employer_mental_health_discussion'] = df_x['Employer_mental_health_discussion'].astype('float')
        df_x['Mental_health_treatment'] = df_x['Mental_health_treatment'].astype('int')
        df_x['Coworker_mental_health_discussion2'] = df_x['Coworker_mental_health_discussion2'].astype('float')

        df_x['Age'] = df_x['Age'].replace({
            '11-26' : 0,
            '27-42' : 1,
            '43-58' : 2,
            '59-68' : 3
        })

        list_columns = ['Gender', 'Past_disorder', 'Family_history',
                        'Health_benefits', 'Previous_benefits',
                        'Mental_health_options', 'Share_mental_illness', 'Supervisor_comfort',
                        'Coworker_mental_health_discussion1',
                        'Medical_leave_ease', 'Health_disclosure', 'Emotions']

        encoded_data = pd.get_dummies(df_x, columns=list_columns)
        encoded_data.replace(True, 1, inplace=True)

        # List of top features
        top_feature_list = ['Past_disorder_No',
                            'Past_disorder_Yes',
                            'Family_history_No',
                            'Mental_health_treatment',
                            'Family_history_Yes',
                            'Share_mental_illness_Not applicable to me (I do not have a mental illness)',
                            "Past_disorder_I don't know",
                            'Employees_count',
                            'Tech_industry_support',
                            'Age',
                            'Share_mental_illness_Very open',
                            'Gender_Male']

        # Set all other dummy columns to 0
        for column in top_feature_list:
            if column not in encoded_data.columns:
                encoded_data[column] = 0

        # Reorder columns to match top_feature_list order
        encoded_data = encoded_data[top_feature_list]

        text_input = df_x.loc[0, 'Emotions']
        emotion = pipeline('sentiment-analysis', model='StevenLimcorn/indonesian-roberta-base-emotion-classifier')
        emotion_result = emotion(text_input)

        prediction = model.predict(encoded_data)

        # st.dataframe(encoded_data)
        st.write(f"Hasil Prediksi kesehatan mental menunjukkan bahwa saudara memiliki probabilitas <b>{prediction[0]}</b>. Hasil tersebut didapatkan dari kuesioner yang sudah anda kerjakan.", unsafe_allow_html=True)
        st.write(f"Sedangkan berdasarkan hasil emosi yang dimiliki oleh anda hari ini menunjukkan emosi <b>{emotion_result[0]['label']}<b>.")

        df_x['result'] = prediction[0]
        df_x['emotion_detection'] = emotion_result[0]['label']

        updated_data = pd.concat([existing_data, df_x], ignore_index=True)

        conn.update(spreadsheet="https://docs.google.com/spreadsheets/d/1z7UPC-LoZDsNvsVbGv4cYsAM8D65wdIKci3xBXGMTqw/edit?usp=sharing",data=updated_data)
        
        st.warning("Data telah direkam dalam database.")

    st.caption("Created by: Irvan Zidny (225221004).")

if __name__ == "__main__":
    main()


