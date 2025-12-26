from fastapi import FastAPI
from schemas import Car, Prediction
import uvicorn
import joblib
from pathlib import Path
from datetime import date
import pandas as pd
import numpy as np

app = FastAPI()

# load model relative to repository root (one level up from api/)
MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "Ridge_model_used_cars.pkl"
model = joblib.load(MODEL_PATH)


@app.post("/")
def main():
    return {"message": "Hello"}


@app.post("/predict", response_model=Prediction)
def predict(car: Car):
    car_age = date.today().year - car.year
    df = pd.DataFrame([
        {
            "Distance": car.distance,
            "Car_age": car_age,
            "Engine_cc": car.engine_cc,
            "Type": car.type_,
            "Condition": car.condition,
            "Manufacturer": car.manufacturer,
            "Fuel_type": car.fuel_type,
            "Body_type": car.body_type,
        }
    ])
    pred_log = model.predict(df)
    pred = float(np.expm1(pred_log[0]))
    return Prediction(predicted_price=round(pred, -4))


if __name__ == "__main__":
    # quick local test without running the server
    sample = Car(
        model_name="سبورتاج",
        year=2024,
        manufacturer="كيا",
        type_="أوتوماتيك",
        condition="مستعملة",
        distance=19600.0,
        color="Gray",
        body_type="SUV",
        fuel_type="Gas",
        engine_cc=1600.0,
    )
    print("Sample prediction:", predict(sample))

    uvicorn.run(app=app, host="0.0.0.0", port=8080)

