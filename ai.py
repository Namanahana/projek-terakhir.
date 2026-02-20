import openai
import uuid
import os
import base64
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

TEMP_DIR = "temp"

def generate_image(prompt: str) -> str:
    os.makedirs(TEMP_DIR, exist_ok=True)

    image_id = str(uuid.uuid4())
    output_path = f"{TEMP_DIR}/{image_id}.png"

    response = openai.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    image_base64 = response.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    with open(output_path, "wb") as f:
        f.write(image_bytes)

    return output_path
