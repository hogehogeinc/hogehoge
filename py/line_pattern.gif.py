from PIL import Image, ImageDraw

# 画像サイズ
width, height = 100, 100

# 線の間隔と色
line_spacing = 10
line_color = (255, 128, 255)  # FF00FF と FFFFFF の中間色

# 背景は透明
image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
draw = ImageDraw.Draw(image)

# 横線を描画
for y in range(0, height, line_spacing):
    draw.line([(0, y), (width, y)], fill=line_color, width=1)

# RGBA → Pモードに変換し透明色を指定してGIF保存
gif_image = image.convert('P', palette=Image.ADAPTIVE)
gif_image.save('line_pattern.gif', transparency=0)
