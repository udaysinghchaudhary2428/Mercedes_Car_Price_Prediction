from pydantic import BaseModel,Field,field_validator
from typing import Literal,Annotated
from config.info import valid_models

class UserInput(BaseModel):
    model : Annotated[str,Field(description="Enter the car model",examples=['A-Class','C-Class','E-Class','S-Class'],max_length=20)]
    year : Annotated[Literal[2020, 2021, 2022, 2023, 2024, 2025],Field(description ="Enter the year")]
    color : Annotated[str,Field(description="Enter the color",max_length=20)]
    fuel : Annotated[Literal['Diesel','Petrol','Hybrid','Electric'],Field(description="Enter the Fuel type")]
    horsepower : Annotated[int,Field(strict=True,description="Enter the horsepower",ge=100,le=1000)]
    turbo : Annotated[Literal['Yes','No'],Field(description="Enter the turbo (Yes or NO)")]