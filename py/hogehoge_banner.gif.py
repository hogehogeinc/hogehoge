from PIL import Image, ImageDraw, ImageFont
import math

# 設定
width, height = 140, 40
font_size = 12
text = "株式会社hogehoge"
num_frames = 12
font_path = "C:/Windows/Fonts/meiryo.ttc"
font = ImageFont.truetype(font_path, font_size)

text_color = "#FF00FF"
bg_color = "white"
character_color = "#FFAAFF"

# テキスト位置（下段中央）
temp_img = Image.new("RGB", (1, 1))
temp_draw = ImageDraw.Draw(temp_img)
bbox = temp_draw.textbbox((0, 0), text, font=font)
text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
text_x = (width - text_w) // 2
text_y = height - text_h - 2  # 下から少し余白

# キャラクターサイズ・位置
start_x = -30
start_y = 4  # 上の段
character_spacing = 26  # 顔と顔の距離

frames = []
for frame in range(num_frames):
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    dx = int((width + 60) * frame / num_frames) + start_x
    dy = start_y

    for i in range(2):
        x = dx + i * character_spacing

        # 目（・・）
        draw.ellipse((x, dy, x + 3, dy + 3), fill=character_color)
        draw.ellipse((x + 6, dy, x + 9, dy + 3), fill=character_color)

        # 口（◯）白抜き
        draw.ellipse((x, dy + 6, x + 12, dy + 16), fill=None, outline=character_color, width=1)

    # テキスト
    draw.text((text_x, text_y), text, font=font, fill=text_color)

    frames.append(img)

# 保存
frames[0].save(
    "hogehoge_banner.gif",
    save_all=True,
    append_images=frames[1:],
    loop=0,
    duration=120
)
