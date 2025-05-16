from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Verilen input verisi için Pydantic modelini oluştur
class InputData(BaseModel):
    model_image: str

# API endpointi oluştur
@app.post("/process-image")
async def process_image(input_data: InputData):
    #remove_background(input_data.model_image)
    pass

    
    
