from PIL import Image, ImageDraw
import random
import numpy as np

# アニメーションの設定
width, height = 100, 100
frames = 20
background_color = (0, 0, 20)  # 暗い青色（宇宙背景）

# GIFアニメーションの各フレームを格納するリスト
images = []

# 星の位置と特性をランダムに生成
num_stars = 50
stars = []
for _ in range(num_stars):
    x = random.randint(0, width)
    y = random.randint(0, height)
    size = random.uniform(0.5, 2)
    brightness = random.uniform(0.5, 1.0)
    twinkle_speed = random.uniform(0.05, 0.2)
    stars.append((x, y, size, brightness, twinkle_speed))

# 各フレームを生成
for frame in range(frames):
    # 新しい画像を作成
    img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(img)

    # 星を描画
    for i, (x, y, size, brightness, twinkle_speed) in enumerate(stars):
        # 星の明るさをフレームによって変化させる（瞬きの効果）
        current_brightness = brightness * (0.5 + 0.5 * np.sin(frame * twinkle_speed + i))

        # 星の色（明るさに基づく）
        star_color = (
            int(200 * current_brightness + 55),  # R
            int(200 * current_brightness + 55),  # G
            int(255 * current_brightness)        # B
        )

        # 星を描画（単純な円として）
        current_size = size * (0.8 + 0.4 * current_brightness)
        draw.ellipse(
            (x - current_size, y - current_size, x + current_size, y + current_size),
            fill=star_color
        )

    # フレームをリストに追加
    images.append(img)

# たまに流れ星を追加
for _ in range(3):
    frame_idx = random.randint(0, frames - 5)
    start_x = random.randint(0, width)
    start_y = random.randint(0, height // 3)
    length = random.randint(10, 30)
    angle = random.uniform(0.5, 1.0)

    for i in range(min(5, frames - frame_idx)):
        img = images[frame_idx + i].copy()
        draw = ImageDraw.Draw(img)

        # 流れ星の位置を計算
        current_x = start_x + int(i * length * 0.8)
        current_y = start_y + int(i * length * angle)

        if 0 <= current_x < width and 0 <= current_y < height:
            # 流れ星の頭の部分
            draw.ellipse(
                (current_x - 1, current_y - 1, current_x + 1, current_y + 1),
                fill=(255, 255, 255)
            )

            # 流れ星の尾
            for j in range(1, 5):
                tail_x = current_x - int(j * 1.5)
                tail_y = current_y - int(j * 1.5 * angle)
                if 0 <= tail_x < width and 0 <= tail_y < height:
                    alpha = (5 - j) / 5  # 尾の透明度
                    draw.point(
                        [tail_x, tail_y],
                        fill=(int(255 * alpha), int(255 * alpha), int(255 * alpha))
                    )

        images[frame_idx + i] = img

# 惑星を追加
planet_frame = random.randint(0, frames - 1)
planet_x = random.randint(width // 4, width * 3 // 4)
planet_y = random.randint(height // 4, height * 3 // 4)
planet_size = random.randint(5, 10)
planet_color = random.choice([
    (207, 117, 63),  # 木星風
    (198, 168, 78),  # 土星風
    (66, 135, 245),  # 海王星風
    (236, 91, 35)    # 火星風
])

img = images[planet_frame].copy()
draw = ImageDraw.Draw(img)
draw.ellipse(
    (planet_x - planet_size, planet_y - planet_size,
     planet_x + planet_size, planet_y + planet_size),
    fill=planet_color
)
images[planet_frame] = img

# GIFファイルとして保存
images[0].save(
    'space_animation.gif',
    save_all=True,
    append_images=images[1:],
    optimize=False,
    duration=100,  # 各フレームの表示時間（ミリ秒）
    loop=0  # 0はループを無限に繰り返す
)

print("space_animation.gif が作成されました")
