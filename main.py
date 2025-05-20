from fastapi import FastAPI, File, UploadFile , HTTPException,Request
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
from PIL import Image
from io import BytesIO
from u2net_model import remove_background, load_model
import matplotlib.pyplot as plt

net = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global net 
    net = load_model()
    yield
    del net
    
app = FastAPI(lifespan=lifespan)

@app.get("/hello")
async def root():
    print("Hello World")
    return {"message": "Hello World"}

@app.post("/process-image")
async def process_image(
    photo: UploadFile = File(...),
    clothing: UploadFile = File(...),
):
    contents = await photo.read()
    img = Image.open(BytesIO(contents))

    # Placeholder: apply background removal logic here
    processed_image = remove_background(img, net)
  
    buf = BytesIO()
    rgb_image = processed_image.convert("RGB")
    rgb_image.save(buf, format="JPEG")
    buf.seek(0)
    plt.imshow(rgb_image)
    plt.axis('off')

    plt.show()

    return StreamingResponse(buf, media_type="image/jpeg")
    
