from PIL import Image, ImageDraw, ImageFont

# 基本設定
width, height = 280, 80
font_size = 28
text = "DesignStudio 35mm"
font_path = "C:/Windows/Fonts/msgothic.ttc"  # MSゴシック（標準）

font = ImageFont.truetype(font_path, font_size)

# 色設定
bg_color = (250, 245, 230)  # あたたかいベージュ
text_color = (60, 50, 40)   # ややコーヒー色っぽい濃いグレー
num_frames = 8

# テキスト位置（中央寄せ）
temp_img = Image.new("RGB", (1, 1))
temp_draw = ImageDraw.Draw(temp_img)
bbox = temp_draw.textbbox((0, 0), text, font=font)
text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
x = (width - text_w) // 2
y = (height - text_h) // 2

frames = []
for i in range(num_frames):
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # 透明度（アルファ）をアニメ的に変化させる
    alpha = int(255 * (0.5 + 0.5 * (i / (num_frames - 1))))  # 0.5〜1.0の範囲
    text_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_layer)
    text_draw.text((x, y), text, font=font, fill=text_color + (alpha,))
    img = Image.alpha_composite(img.convert("RGBA"), text_layer)
    frames.append(img.convert("RGB"))

# GIF保存
frames[0].save(
    "ds35mm.gif",
    save_all=True,
    append_images=frames[1:],
    loop=0,
    duration=180
)
