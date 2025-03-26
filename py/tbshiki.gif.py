from PIL import Image, ImageDraw, ImageFont
import math

# 設定
width, height = 280, 80
font_size = 32
text = "つぶ式"
frames = []
num_frames = 8
# font_path = "C:/Windows/Fonts/msmincho.ttc"  # MS 明朝フォント（Windows標準）

font = ImageFont.truetype("msmincho.ttc", font_size)

# 中心配置用にテキストサイズを取得
temp_img = Image.new("RGB", (1, 1))
temp_draw = ImageDraw.Draw(temp_img)
bbox = temp_draw.textbbox((0, 0), text, font=font)
text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
base_x = (width - text_w) // 2
base_y = (height - text_h) // 2

# フレームごとにテキストをゆらす
for i in range(num_frames):
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    # sin波で上下に揺らす
    offset = int(math.sin(i / num_frames * 2 * math.pi) * 2)

    # テキスト描画（オレンジ）
    draw.text((base_x, base_y + offset), text, font=font, fill="orange")

    frames.append(img)

# GIFとして保存（ゆっくりめに）
frames[0].save(
    "tbshiki.gif",
    save_all=True,
    append_images=frames[1:],
    loop=0,
    duration=200  # ミリ秒（200msごとに切り替え）
)
