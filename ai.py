import requests
import uuid
import os

TEMP_DIR = "temp"

def generate_image(prompt: str) -> str:
    os.makedirs(TEMP_DIR, exist_ok=True)

    image_id = str(uuid.uuid4())
    output_path = f"{TEMP_DIR}/{image_id}.png"

    url = f"https://image.pollinations.ai/prompt/{prompt}"

    try:
        response = requests.get(url, timeout=20)
    except requests.exceptions.Timeout:
        raise Exception("AI lagi lemot 😭 coba lagi bentar")


    if response.status_code != 200:
        raise Exception("Gagal generate gambar dari Pollinations")

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path
