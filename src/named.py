import math
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def process_image_to_a4(image_path, title_text):
    
    img = Image.open(image_path)
    img.load()
        
    W, H = img.size
    a4_ratio = math.sqrt(2)
    target_H = int(W * a4_ratio)
    strip_H = target_H - H

    if strip_H <= 50: 
        strip_H = int(W * 0.15) 
        target_H = H + strip_H 

    background_color = (30, 30, 30)
    new_img = Image.new("RGB", (W, target_H), background_color)
    new_img.paste(img, (0, strip_H))

    draw = ImageDraw.Draw(new_img)
    text_color = (255, 255, 255)
    
    text_x = W / 2
    text_y = strip_H / 2

    font_size = int(strip_H * 0.60)
    spacing = 15
    font_path = "C:/Windows/Fonts/arial.ttf"

    while font_size >= 12:
        font = ImageFont.truetype(font_path, font_size)

        char_width = font.getlength("A")
        max_chars_per_line = max(10, int((W * 0.9) / char_width))
        wrapped_text = textwrap.fill(title_text, width=max_chars_per_line)
        lines = wrapped_text.split('\n')

        total_height = (len(lines) * font_size) + ((len(lines) - 1) * spacing)

        if total_height <= (strip_H * 0.80):
            break

        font_size -= 2

    draw.multiline_text(
        (text_x, text_y),
        wrapped_text,
        fill=text_color,
        font=font,
        anchor="mm",
        align="center",
        spacing=spacing
    )
    
    base_name = os.path.basename(image_path)
        
    new_img.save('../coverArticle/' + base_name, quality=95)

if __name__ == "__main__":
    IMAGE_PATH = 'D:/Project/ArticleCover/images/student/1712.02779v3.png'
    TITLE = "A Rotation and a Translation Suffice: Fooling CNNs with Simple Transformations"
    
    process_image_to_a4(IMAGE_PATH, TITLE)