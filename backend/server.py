import json
from pydoc import describe
import pandas as pd
import uvicorn
from fastapi.responses import JSONResponse
from fastapi import FastAPI,Path,Query,HTTPException
from pydantic import BaseModel,Field,computed_field
from typing import Optional,Annotated,Literal
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pickle


app = FastAPI()

def load_encoder():
    with open(r"../model_encoder_files/label_encoders.pkl","rb") as file:
        label_encoders = pickle.load(file)
    return label_encoders

def load_model():
    with open(r"../model_encoder_files/car_predict_model.pkl","rb") as file:
        model = pickle.load(file)
    return model

encoders = load_encoder()
model = load_model()

# for encoder in encoders:
#         print((encoder))

class CarData(BaseModel):
    car_company : Annotated[Literal[
    "Jeep", "Renault", "Toyota", "Honda", "Volkswagen", "Maruti", "Mahindra",
    "Hyundai", "Nissan", "Kia", "MG", "Tata", "BMW", "Mercedes-Benz", "Datsun",
    "Volvo", "Audi", "Porsche", "Ford", "Chevrolet", "Skoda", "Lexus", "Land",
    "Mini", "Jaguar", "Mitsubishi", "Force", "Premier", "Fiat", "Maserati",
    "Bentley", "Isuzu"
    ],Field(...,description="name of the car manufacturer company")]
    
    car_name : Annotated[Optional[str],Field(description="Name of the car.")] = None

    kms_driven : Annotated[int,Field(...,ge=0,description="how many kilometers is car driven?")]

    fuel_type : Annotated[Literal["Diesel", "Petrol", "Cng", "Electric", "Lpg"],Field(...,description="fuel type of car",examples=['petrol','diesel'])]

    transmission : Annotated[Literal["Automatic","Manual"],Field(...,description="Transmission type of the car")]

    ownership : Annotated[int,Field(...,description="Ownership of the car",examples=[1,2,3])]

    manufacture_year : Annotated[int,Field(...,description="A year in which car manufactured.")]

    engine_power_in_cc : Annotated[int,Field(...,description="Engine power in cc")]

    seats : Annotated[Literal[2, 4, 5, 6, 7, 8],Field(...,description="how many seats in the car?")]


@app.get("/")
async def root():
    return {'message':'hii krish'}


@app.get("/predict")
async def root():
    return {'message':'hii krish'}

@app.post("/predict")
async def predict_car_price(car_data : CarData):
    print(car_data)
    data = pd.DataFrame([{
        'car_company'       : car_data.car_company,
        'kms_driven'        : car_data.kms_driven,
        'fuel_type'         : car_data.fuel_type,
        'transmission'      : car_data.transmission,
        'ownership'         : car_data.ownership,
        'manufacture_year'  : car_data.manufacture_year,
        'engine_power_in_cc': car_data.engine_power_in_cc,
        'seats'             : car_data.seats,

    }])

    print(data)
    for encoder in encoders:
        data.loc[:,encoder] = encoders[encoder].transform(data.loc[:,encoder])
    # print(data.loc[:,["car_company","fuel_type","transmission"]])
    # print(model.predict(np.array(data)))
    car_price = model.predict(np.array(data))[0]
    # car_price = 0.1
    if car_price<1:
        car_price*=100000
        return JSONResponse(status_code=200,content={'car_price':f"{round(car_price,2)}"})
    return JSONResponse(status_code=200,content={'car_price':f"{round(car_price,2)} Lakhs"})
    