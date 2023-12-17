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

# Function to query API
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Function to load the model from a pickle file
def load_model(file_path):
    with open(file_path, 'rb') as model_file:
        model = pickle.load(model_file)
    return model

# Constants
API_URL = "your_api_url_here"
headers = {"Content-Type": "application/json"}

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
    st.markdown("""---""")
    
    # ... (Rest of your code)

    # Menambah tombol "Submit"
    submit_button = st.button("Submit")
    
    # Check if the button is clicked
    if submit_button:
        st.dataframe(df_x)
    
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
        df_x['Age'] = df_x['Age'].apply(categorize_age)

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

        st.dataframe(encoded_data)
        st.write(prediction)
        st.write(emotion_result)

if __name__ == "__main__":
    main()
