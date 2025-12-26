import streamlit as st
from pathlib import Path
import pandas as pd
import os
from datetime import date
import joblib
import numpy as np

today = date.today()


# data lists
data_path = Path(__file__).resolve().parents[2] / "data" / "lists"
model = joblib.load("../../models/Ridge_model_used_cars.pkl")

car_brands = []
car_names = []
body_types = []
engine_cc = []
with open(data_path / "car_brands.txt", 'r', encoding='utf-8-sig') as f:
    for line in f:
        car_brands.append(line.strip())

with open(data_path / "engine_cc.txt", 'r', encoding='utf') as f:
    for line in f:
        engine_cc.append(line.strip())




st.title("Used Cars Price Prediction")

# Introduction section
st.header("Introduction")
st.write("Welcome to the Cars Price Prediction app, in this app we will utilize" \
"a Machine Learning model to predict the prices of a Car in a local market, the model is not perfect yet but it's doable")
st.write("here is some facts about the model:")
st.markdown("- The model is built using Ridge Regression algorithm.")
st.markdown("- The model is trained on 3000+ data on local shop.")
st.markdown("- The model R2 score is : 0.78")
st.markdown("- The model MAPE score is : 0.21")

# End of Introduction section

# App section
st.header("Let's begin:")
st.subheader("Fill the input fields")

manufacturer = st.selectbox("Select Car Brand:", options=car_brands, key="brand", index=16)
if manufacturer:
    with open(data_path / f"{manufacturer}" / f"{manufacturer}.txt", 'r', encoding='utf-8-sig') as f:
        for line in f:
            car_names.append(line.split(":", 1)[0].strip())

model_name = st.selectbox("Select Car Model:", options=car_names, key="model")
year = st.number_input("Enter Car Year:", min_value=1990, max_value=today.year, value=2020, step=1, key="year")
car_age = today.year - year

type_ = st.checkbox("Is the car Automatic?", value=True, key="type")
car_type = "أوتوماتيك"
if not type_:
    car_type = "مانيوال"

condition = st.selectbox("Select Car Condition:", options=["مستعملة", "جديدة"], index=1 ,key="condition")
distance = 0.0
if condition == "مستعملة":
    distance = st.number_input("Enter Distance Driven (in KM):", min_value=0.0, step=100.0, key="distance")

color = st.color_picker("Pick Car Color:", value="#ffffff", key="color")
if model_name:
    with open(data_path / f"{manufacturer}" / f"{manufacturer}.txt", 'r', encoding='utf-8-sig') as f:
        for line in f:
            name, body_types_str = line.split(":", 1)
            if model_name == name.strip():
                body_types_str = body_types_str.strip()
                body_types = [bt.strip() for bt in body_types_str.split(",")]
            else:
                continue

body_type = st.selectbox("Select Body Type:", options=body_types)
fuel_type = st.selectbox("Select Fuel Type:", options=["Gas", "Electric", "Hybird"]).strip()
engine_cc_val = float(st.select_slider("Engine_cc", options=sorted(engine_cc)))

input_data = pd.DataFrame({
    'Manufacturer': [manufacturer],
    'Car_age': [car_age],
    'Type': [car_type],
    'Condition': [condition],
    'Distance': [distance],
    'Body_type': [body_type],
    'Fuel_type': [fuel_type],
    'Engine_cc': [engine_cc_val]
})

for col in input_data.select_dtypes(include=['object']).columns:
    input_data[col] = input_data[col].str.strip()
    input_data[col] = input_data[col].astype('category')

if st.button("Predict Price"):

    predicted_price = model.predict(input_data)
    st.success(f"The predicted price of the car is : {round(np.expm1(predicted_price[0]), -4)}")
else:
    st.info("Fill all the input fields and click on Predict Price.")