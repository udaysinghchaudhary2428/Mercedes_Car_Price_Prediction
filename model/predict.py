import pandas as pd
import joblib

with open("model/model",'rb') as file:
    model = joblib.load(file)
    
MODEL_VERSION = "1.0.0"

def predict_output(user_input : dict):
    
    data = pd.DataFrame([user_input])
    output = model.predict(data)
    return output