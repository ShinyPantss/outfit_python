from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
import requests
from io import BytesIO
from background_removal import remove_bg

# FastAPI uygulamasını
app = FastAPI()

# Verilen input verisi için Pydantic modelini oluştur
class InputData(BaseModel):
    model_image: str
    garment_image: str
    category: str

@app.post("/preprocess-image")
async def preprocess_image(input_data: InputData):
    # linkten download
    input_image_path = "input_image.jpg"
    with open(input_image_path, "wb") as f:
        f.write(base64.b64decode(input_data.model_image.split(",")[1]))

    # Arka plan kaldırma fonksiyonunu çağırıyoruz ve sonucu alıyoruz
    result_image = remove_bg(input_image_path)

    # Sonuç resmi Base64 formatına çeviriyoruz
    buffered = BytesIO()
    result_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Base64 formatındaki resmi döndürüyoruz
    return {"result_image": img_str}

# Fashn API'ye istek gönderme fonksiyonu
def send_to_fashn_api(model_image: str, garment_image: str, category: str) -> str:
    url = "https://api.fashn.ai/v1/run"  # Örnek URL, değişebilir
    payload = {
        "model_image": model_image,
        "garment_image": garment_image,
        "category": category
    }

    headers = {
        "Authorization": f"Bearer {your_api_key}"  # Fashn API anahtarınızı buraya ekleyin
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        return result['url']  # Geri dönen URL'yi alıyoruz
    else:
        raise HTTPException(status_code=400, detail="Fashn API'ye istek atılırken bir hata oluştu")

# API endpointi oluştur
@app.post("/process-image")
async def process_image(input_data: InputData):
    # İlk olarak background işlemi yapıyoruz
    process_background(input_data.model_image)

    # Ardından Fashn API'ye istek gönderiyoruz
    result_url = send_to_fashn_api(input_data.model_image, input_data.garment_image, input_data.category)

    # Sonuç olarak Fashn API tarafından dönen URL'yi geri döndürüyoruz
    return {"result_url": result_url}
