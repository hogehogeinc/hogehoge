from PIL import Image, ImageDraw, ImageFont
import random

width, height = 280, 80
shadow_offset = 4
num_frames = 8
num_drops = 360  # 石油の粒の数

# font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font_size = 32
font = ImageFont.truetype("msgothic.ttc", font_size)
text = "石油王のホムペ"

# 茶色系パターン（石油の色ランダム感）
oil_colors = ["#996633", "#aa5522", "#bb7744", "#cc6633"]


def create_striped_background_with_shadow():
    img = Image.new("RGB", (width + shadow_offset, height + shadow_offset), "#cccc66")
    draw = ImageDraw.Draw(img)
    for y in range(0, height, 4):
        draw.line((0, y, width, y), fill="#ffff99")
    for i in range(shadow_offset):
        draw.line((width + i, 0, width + i, height + i), fill="#999933")
        draw.line((0, height + i, width + i, height + i), fill="#999933")
    return img

def draw_text_with_effects(img, text, font):
    draw = ImageDraw.Draw(img)
    temp = Image.new("RGB", (1, 1))
    bbox = ImageDraw.Draw(temp).textbbox((0, 0), text, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (width - text_w) // 2
    y = (height - text_h) // 2 - 2

    draw.text((x+2, y+2), text, font=font, fill="black")
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        draw.text((x+dx, y+dy), text, font=font, fill="blue")
    draw.text((x, y), text, font=font, fill="lime")

def draw_oil_drops(draw, frame_num):
    for _ in range(num_drops):
        # 位置はランダム＋フレームに応じて動かす（右→左）
        base_x = random.randint(0, width + 40)
        base_y = random.randint(10, height - 10)
        shift = frame_num * 2
        x = (base_x - shift) % (width + 40) - 20
        y = base_y + random.randint(-1, 1)
        size = random.choice([2, 3, 4])
        color = random.choice(oil_colors)
        draw.ellipse((x, y, x + size, y + size), fill=color)

def generate_oilflow_gif():
    frames = []
    for i in range(num_frames):
        bg = create_striped_background_with_shadow()
        draw = ImageDraw.Draw(bg)

        # 石油ドットを描画
        draw_oil_drops(draw, i)

        # テキストを重ねる
        draw_text_with_effects(bg, text, font)

        frames.append(bg)

    frames[0].save("sekiyuoh_homepage.gif", save_all=True, append_images=frames[1:], loop=0, duration=360)

generate_oilflow_gif()
