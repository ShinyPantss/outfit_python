from fastapi import FastAPI, File, UploadFile , HTTPException
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
from PIL import Image
from io import BytesIO
from u2net_model import remove_background, load_model

net = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global net 
    net = load_model()
    yield
    del net
    
app = FastAPI(lifespan=lifespan)

@app.post("/process-image")
async def process_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Please send an image")
    
    contents = await file.read()
    img = Image.open(BytesIO(contents))
    
    processed_image = remove_background(img, net)
    
    buf = BytesIO()
    processed_image.save(buf, format="jpg")
    buf.seek(0)
    
    return StreamingResponse(buf, media_type="image/jpg")

    
    
