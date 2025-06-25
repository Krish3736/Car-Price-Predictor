import streamlit as st
import requests
import json
import datetime

API_URL = "http://127.0.0.1:8000/predict"

st.title("Car Price Predictor : apni car apne dam")

st.markdown("Enter your details below: ")

def load_data():
    with open("../data/data.json","r") as file:
        data = json.load(file)
    return data


data = load_data()
    
#Input Fields

car_company = st.selectbox("Car Manufacturer Company: ",options = data["car_company"])

car_name = st.text_input("Car name: ")

kms_driven = st.number_input("Car driven (in Kilometers): ",min_value=0,value=1000)

fuel_type = st.selectbox("Fuel type of your car: ",options=data["fuel_type"])

transmission = st.radio("Select Gender", options=data["transmission_type"])

ownership = st.number_input("ownership (valid from 1 to 5): ",min_value=1,max_value=5,step=1)

years = list(range(1990, datetime.datetime.now().year + 1))
manufacture_year = st.selectbox("Year of manufacture of car: ", years, index=years.index(2018))

engine_power_in_cc = st.number_input("engine power (in cc): ",min_value=768,max_value=6000,value=1399)

seats = st.number_input("Number of seats (valid range : 2 to 8): ",min_value=2,max_value=8)

if st.button("Predict Price"):
    
    input_data = {
        'car_company'       : car_company,
        'kms_driven'        : kms_driven,
        'fuel_type'         : fuel_type,
        'transmission'      : transmission,
        'ownership'         : ownership,
        'manufacture_year'  : manufacture_year,
        'engine_power_in_cc': engine_power_in_cc,
        'seats'             : seats
    }
    if car_company == "Select a company":
        st.warning("Please choose a valid company !!!")
    
    elif fuel_type == "Select a fuel type":
        st.warning("Please choose a valid fuel type !!!")
    else:

        print(input_data)
        try:
            response = requests.post(API_URL,json = input_data)
            if response.status_code == 200:
                result = response.json()
                st.success(f"Predicted Car Price : {result["car_price"]}")
            else:
                st.error(f"API Error : {response.status_code} -{response.text}")
            
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the FastAPI server. Make sure it's running on the port 8000.")