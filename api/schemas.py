from pydantic import BaseModel


class Car(BaseModel):
    model_name : str
    year : int
    manufacturer : str
    type_ : str
    condition : str
    distance : float
    color : str
    body_type : str
    fuel_type : str
    engine_cc : float


class Prediction(BaseModel):
    predicted_price: float
