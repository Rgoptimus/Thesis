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
                    Informasi yang disajikan oleh model ini mungkin tidak akurat atau sesuai dengan keadaan individual. 
                    Apabila Anda mengalami potensi permasalahan kesehatan mental atau memiliki kekhawatiran terkait kesejahteraan psikologis, 
                    segera konsultasikan dengan tenaga kesehatan mental atau profesional terkait. 
                    Model ini tidak bertanggung jawab atas tindakan yang diambil berdasarkan informasi yang diberikan, 
                    dan penggunaan teks ini sepenuhnya menjadi tanggung jawab pribadi.
                    </div>
                    """, unsafe_allow_html=True)
    st.markdown("""---""")
    
    st.subheader("Identitas")

    Emotions = st.text_input("Apa yang membuat Anda merasa cemas atau stres akhir-akhir ini?")

    # Menambah tombol "Submit"
    submit_button = st.button("Submit")
    
    # Menambah keadaan apabila tombol ditekan
    if submit_button:
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
        emotion = pipeline('sentiment-analysis', model='StevenLimcorn/indonesian-roberta-base-emotion-classifier')
        emotion_result = emotion(Emotions)
        
        st.write("Hasil Emosi yang dimiliki: ", emotion_result)

    st.caption("Created by: Irvan Zidny (225221004).")

if __name__ == "__main__":
    main()


