from schema.userinput import UserInput
from fastapi.responses import JSONResponse
from fastapi import FastAPI,HTTPException
from model.predict import model,predict_output,MODEL_VERSION

app = FastAPI(title="Mercedes Price Prediction API",
              description="Predict base price of mercedes cars",
              version="1.0.0")
    
@app.get("/",tags=["General"])
def home():
    return {"message":"Mercedes Car base price prediction (USD)"}

@app.get("/health",tags=["Monitoring"])
def health():
    return {
        "status": "OK",
        "version" : MODEL_VERSION,
        "model_loaded" : model is not None
    }

@app.post("/predict",tags=["Prediction"])
def predict(data : UserInput) -> JSONResponse:
        
    features = {
        "Model": data.model,
        "Year": data.year,
        "Color": data.color,
        "Fuel Type": data.fuel,
        "Horsepower": data.horsepower,
        "Turbo": data.turbo,
    }
    
    try: 
        prediction = predict_output(features)
        return JSONResponse(status_code=200,content={"Predicted Car Base Price (USD)" : round(float(prediction),2)})
    
    except Exception as e:
        return HTTPException(status_code=500,detail="Prediction failed")