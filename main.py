import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# Set Streamlit page configuration
st.set_page_config(page_title="Health Assistant",
                   layout="wide",
                   page_icon="🧑‍⚕️")

# Load saved machine learning models
working_dir = os.path.dirname(os.path.abspath(__file__))

try:
    diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes_model.sav', 'rb'))
    heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))
    parkinsons_model = pickle.load(open(f'{working_dir}/saved_models/parkinsons_model.sav', 'rb'))
except FileNotFoundError:
    st.error("Error: One or more model files not found. Please check the directory.")
    st.stop()

# Sidebar navigation
with st.sidebar:
    selected = option_menu("Multiple Disease Prediction System",
                           ["Diabetes Prediction",
                            "Heart Disease Prediction",
                            "Parkinson's Prediction"],
                           menu_icon="hospital-fill",
                           icons=["activity", "heart", "person"],
                           default_index=0)

# Diabetes Prediction Page
if selected == "Diabetes Prediction":
    st.title("🩺 Diabetes Prediction using Machine Learning")

    with st.container():
        st.markdown("### Enter Patient Details:")
        col1, col2, col3 = st.columns(3)

        with col1:
            Pregnancies = st.number_input("Number of Pregnancies", min_value=0, step=1, value=0)

        with col2:
            Glucose = st.number_input("Glucose Level", min_value=0, step=1, value=100)

        with col3:
            BloodPressure = st.number_input("Blood Pressure (mmHg)", min_value=0, step=1, value=80)

        with col1:
            SkinThickness = st.number_input("Skin Thickness (mm)", min_value=0, step=1, value=20)

        with col2:
            Insulin = st.number_input("Insulin Level", min_value=0, step=1, value=80)

        with col3:
            BMI = st.number_input("BMI", min_value=0.0, format="%.1f", value=25.0)

        with col1:
            DiabetesPedigreeFunction = st.number_input("Diabetes Pedigree Function", min_value=0.0, format="%.3f", value=0.5)

        with col2:
            Age = st.number_input("Age", min_value=1, step=1, value=30)

    # Prediction
    if st.button("🔍 Get Diabetes Test Result"):
        user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
        diab_prediction = diabetes_model.predict([user_input])

        result = "✅ The person is **not diabetic**." if diab_prediction[0] == 0 else "⚠️ The person **has diabetes**."
        st.success(result)

# Heart Disease Prediction Page
elif selected == "Heart Disease Prediction":
    st.title("❤️ Heart Disease Prediction using Machine Learning")

    with st.container():
        st.markdown("### Enter Patient Details:")
        col1, col2, col3 = st.columns(3)

        with col1:
            age = st.number_input("Age", min_value=1, step=1, value=30)

        with col2:
            sex = st.selectbox("Sex", [0, 1], format_func=lambda x: "Male" if x == 1 else "Female")

        with col3:
            cp = st.number_input("Chest Pain Type", min_value=0, max_value=3, step=1, value=1)

        with col1:
            trestbps = st.number_input("Resting Blood Pressure (mmHg)", min_value=0, step=1, value=120)

        with col2:
            chol = st.number_input("Serum Cholesterol (mg/dl)", min_value=0, step=1, value=200)

        with col3:
            fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

        with col1:
            restecg = st.number_input("Resting ECG Results", min_value=0, max_value=2, step=1, value=1)

        with col2:
            thalach = st.number_input("Max Heart Rate Achieved", min_value=0, step=1, value=150)

        with col3:
            exang = st.selectbox("Exercise-Induced Angina", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

        with col1:
            oldpeak = st.number_input("ST Depression Induced by Exercise", min_value=0.0, format="%.2f", value=1.0)

        with col2:
            slope = st.number_input("Slope of Peak Exercise ST Segment", min_value=0, max_value=2, step=1, value=1)

        with col3:
            ca = st.number_input("Major Vessels Colored by Fluoroscopy", min_value=0, max_value=4, step=1, value=0)

        with col1:
            thal = st.number_input("Thalassemia", min_value=0, max_value=3, step=1, value=1)

    # Prediction
    if st.button("🔍 Get Heart Disease Test Result"):
        user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
        heart_prediction = heart_disease_model.predict([user_input])

        result = "✅ The person **does not have heart disease**." if heart_prediction[0] == 0 else "⚠️ The person **has heart disease**."
        st.success(result)

# Parkinson's Prediction Page
elif selected == "Parkinson's Prediction":
    st.title("🧠 Parkinson's Disease Prediction using Machine Learning")

    with st.container():
        st.markdown("### Enter Voice Analysis Data:")
        cols = st.columns(5)
        parkinsons_features = [
            "MDVP:Fo(Hz)", "MDVP:Fhi(Hz)", "MDVP:Flo(Hz)", "MDVP:Jitter(%)", "MDVP:Jitter(Abs)",
            "MDVP:RAP", "MDVP:PPQ", "Jitter:DDP", "MDVP:Shimmer", "MDVP:Shimmer(dB)",
            "Shimmer:APQ3", "Shimmer:APQ5", "MDVP:APQ", "Shimmer:DDA", "NHR", "HNR",
            "RPDE", "DFA", "spread1", "spread2", "D2", "PPE"
        ]
        user_input = []
        for i, feature in enumerate(parkinsons_features):
            with cols[i % 5]:
                user_input.append(st.number_input(feature, value=0.0, format="%.4f"))

    if st.button("🔍 Get Parkinson's Test Result"):
        parkinsons_prediction = parkinsons_model.predict([user_input])

        result = "✅ The person **does not have Parkinson's disease**." if parkinsons_prediction[0] == 0 else "⚠️ The person **has Parkinson's disease**."
        st.success(result)
