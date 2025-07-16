import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load("air_quality_rf_model.pkl")  

# Title
st.title("Air Quality Index (AQI) Predictor")
st.markdown("Predict AQI based on user inputs like date, state, and pollutant.")

# User Inputs
col1, col2 = st.columns(2)

with col1:
    year = st.selectbox("Year", list(range(2000, 2024)))
    month = st.selectbox("Month", list(range(1, 13)))
    day = st.selectbox("Day", list(range(1, 32)))
    weekday = st.selectbox("Weekday", list(range(7)), format_func=lambda x: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][x])

with col2:
    pollutant = st.selectbox("Pollutant", ['PM2.5', 'Ozone', 'NO2', 'PM10', 'CO'])
    category = st.selectbox("AQI Category", ['Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', 'Very Unhealthy', 'Hazardous'])
    state = st.selectbox("State", [
        'California', 'Texas', 'Florida', 'New York', 'Illinois', 'Arizona', 'Georgia', 'Ohio', 'Michigan', 'North Carolina'
    ])  # Add more states as needed
    season = st.selectbox("Season", ['Winter', 'Spring', 'Summer', 'Fall'])

# Categorical Encoding
pollutant_code = {'PM2.5': 3, 'Ozone': 2, 'NO2': 1, 'PM10': 4, 'CO': 0}[pollutant]
category_code = {
    'Good': 0,
    'Moderate': 1,
    'Unhealthy for Sensitive Groups': 2,
    'Unhealthy': 3,
    'Very Unhealthy': 4,
    'Hazardous': 5
}[category]
state_code = {
    'California': 0, 'Texas': 1, 'Florida': 2, 'New York': 3, 'Illinois': 4,
    'Arizona': 5, 'Georgia': 6, 'Ohio': 7, 'Michigan': 8, 'North Carolina': 9
}[state]
season_code = {'Winter': 3, 'Spring': 2, 'Summer': 1, 'Fall': 0}[season]

# Prediction Button
if st.button("Predict AQI"):
    input_data = pd.DataFrame({
        'Year': [year],
        'Month': [month],
        'Day': [day],
        'Weekday': [weekday],
        'Pollutant_Code': [pollutant_code],
        'Category_Code': [category_code],
        'State_Code': [state_code],
        'Season_Code': [season_code]
    })

    prediction = model.predict(input_data)[0]
    st.success(f"✅ Predicted AQI: {prediction:.2f}")

    # Display Category from AQI
    def aqi_label(aqi):
        if aqi <= 50: return 'Good'
        elif aqi <= 100: return 'Moderate'
        elif aqi <= 150: return 'Unhealthy for Sensitive Groups'
        elif aqi <= 200: return 'Unhealthy'
        elif aqi <= 300: return 'Very Unhealthy'
        else: return 'Hazardous'

    st.info(f"Category: {aqi_label(prediction)}")
