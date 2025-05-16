from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel
from u2net_model import remove_background, load_model

class InputData(BaseModel):
    model_image: str

net = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global net 
    net = load_model()
    yield
    del net
    
app = FastAPI(lifespan=lifespan)

@app.post("/process-image")
async def process_image(input_data: InputData):
    processed_image = remove_background(input_data.model_image, net)
    
    return processed_image

    
    
