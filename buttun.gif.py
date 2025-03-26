from PIL import Image, ImageDraw, ImageFont, ImageFilter


def create_button(text="ホーム", output="button.gif"):
    # サイズ・デザイン調整
    width, height = 240, 50
    radius = 25
    font_size = 24
    line_spacing = 6
    shadow_offset = 2

    # カラー設定
    bg_color = (173, 239, 255, 255)  # 水色
    line_color = (200, 255, 255, 255)
    text_color = (0, 0, 0, 255)
    shadow_color = (0, 0, 0, 100)

    # ベース画像
    base = Image.new("RGBA", (width, height), (255, 255, 255, 0))

    # 角丸マスク
    mask = Image.new("L", (width, height), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle((0, 0, width, height), radius, fill=255)

    draw = ImageDraw.Draw(base)
    draw.rectangle((0, 0, width, height), fill=bg_color)

    # 横線を描画
    for y in range(0, height, line_spacing):
        draw.line([(0, y), (width, y)], fill=line_color)

    # 白の透明グラデ風レイヤー
    overlay = Image.new("RGBA", (width, height), (255, 255, 255, 30))
    base = Image.alpha_composite(base, overlay)

    # マスク適用
    base.putalpha(mask)

    # フォント設定
    try:
        font = ImageFont.truetype("msgothic.ttc", font_size)
    except:
        font = ImageFont.truetype("arial.ttf", font_size)

    # テキストサイズと位置
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2

    # 影レイヤー
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw_shadow = ImageDraw.Draw(shadow)
    draw_shadow.text((text_x + shadow_offset, text_y + shadow_offset), text, font=font, fill=shadow_color)
    shadow = shadow.filter(ImageFilter.GaussianBlur(1.5))

    # 文字レイヤー
    text_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw_text = ImageDraw.Draw(text_layer)
    draw_text.text((text_x, text_y), text, font=font, fill=text_color)

    # 合成
    result = Image.alpha_composite(base, shadow)
    result = Image.alpha_composite(result, text_layer)

    # GIF保存（透過設定）
    gif = result.convert("P", palette=Image.ADAPTIVE)
    transparency_index = gif.getpixel((0, 0))
    gif.save(output, format="GIF", transparency=transparency_index)

    print(f"✅ GIF保存完了: {output}")


# 実行例
# create_button("会社概要", "button_about.gif")
# create_button("事業内容", "button_services.gif")
# create_button("ニュース", "button_news.gif")
# create_button("お問い合わせ", "button_contact.gif")
