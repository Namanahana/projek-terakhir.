from PIL import Image, ImageDraw, ImageFont
import textwrap

def wrap_text(text, font, draw, max_width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]

        if line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

def draw_text(draw, text, font, image_width, y_start):
    max_width = image_width - 40
    lines = wrap_text(text, font, draw, max_width)

    y = y_start
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (image_width - text_width) // 2

        # outline hitam
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                draw.text((x + dx, y + dy), line, font=font, fill="black")

        draw.text((x, y), line, font=font, fill="white")
        y += text_height + 5

def make_meme(image_path, top_text, bottom_text):
    img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    width, height = img.size

    try:
        font = ImageFont.truetype("arial.ttf", size=int(height / 10))
    except:
        font = ImageFont.load_default()

    if top_text:
        draw_text(draw, top_text.upper(), font, width, 10)

    if bottom_text:
        draw_text(
            draw,
            bottom_text.upper(),
            font,
            width,
            height - int(height / 3)
        )

    output_path = image_path.replace(".png", "_meme.png")
    img.save(output_path)
    return output_path
