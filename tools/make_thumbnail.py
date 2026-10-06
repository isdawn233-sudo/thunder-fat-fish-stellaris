"""
make_thumbnail.py —— 生成创意工坊封面（512x512）

输入：thumbnail-source.png（用户提供的原图）
输出：thumbnail.png

要点（踩过的坑）：
  · 工坊要求 thumbnail.png、>=512x512、< 1MB
  · 原图自带白底，且下方有大片空白 —— 必须裁掉，
    否则合成到方形画布后整体构图偏上、底部空一大块
  · 图片区域放大一点、标题下移，整体才平衡
"""
import os
from PIL import Image, ImageDraw, ImageFont


HERE = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.dirname(HERE)
SRC = os.path.join(MOD, "thumbnail-source.png")
OUT = os.path.join(MOD, "thumbnail.png")

CANVAS = 512
SCALE = 1.05          # 图片放大系数（>1 表示裁掉更多留白）
TITLE = "ZL - 大肥鱼天枢执政"

# 裁剪设置：原图下方空白多，切掉一些
CROP_BOTTOM = 40      # 从底部裁掉的像素
TOP_MARGIN = 14       # 图片上方留白（太小会显得贴边）

FONTS = [
    r"C:\Windows\Fonts\msyhbd.ttc",
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
]


def load_font(size):
    for f in FONTS:
        if os.path.isfile(f):
            try:
                return ImageFont.truetype(f, size)
            except Exception:
                pass
    return ImageFont.load_default()


def main():
    if not os.path.isfile(SRC):
        raise SystemExit("找不到原图: %s" % SRC)

    im = Image.open(SRC).convert("RGB")
    W, H = im.size
    print("原图: %dx%d" % (W, H))

    # 1) 底部裁掉一些空白
    if CROP_BOTTOM > 0 and H - CROP_BOTTOM > 100:
        im = im.crop((0, 0, W, H - CROP_BOTTOM))
    W, H = im.size
    print("裁剪后: %dx%d" % (W, H))

    # 2) 缩放（SCALE 越大，留白越少）
    nw = int(W * SCALE)
    nh = int(H * SCALE)
    im = im.resize((nw, nh), Image.LANCZOS)
    print("放大后: %dx%d" % (nw, nh))

    # 3) 在 512 高的画布里，图片占约 63%，标题占剩下的部分
    IMG_AREA = int(CANVAS * 0.63)
    if nh > IMG_AREA:                      # 太高就等比缩回去
        k = IMG_AREA / nh
        nw, nh = int(nw * k), IMG_AREA
        im = im.resize((nw, nh), Image.LANCZOS)
    if nw > CANVAS:                        # 太宽就裁中间
        left = (nw - CANVAS) // 2
        im = im.crop((left, 0, left + CANVAS, nh))
        nw = CANVAS

    canvas = Image.new("RGB", (CANVAS, CANVAS), (255, 255, 255))
    # 图片顶部留一点，避免气泡贴边；其余空间给标题
    top = TOP_MARGIN
    canvas.paste(im, ((CANVAS - nw) // 2, top))
    print("图片放置: (%d, %d)  %dx%d" % ((CANVAS - nw) // 2, top, nw, nh))

    # 4) 标题：垂直居中在图片下方的空白里
    d = ImageDraw.Draw(canvas)
    space_top = top + nh
    space_h = CANVAS - space_top
    size = 34
    font = load_font(size)
    bbox = d.textbbox((0, 0), TITLE, font=font)
    tw = bbox[2] - bbox[0]
    while tw > CANVAS - 40 and size > 16:
        size -= 2
        font = load_font(size)
        bbox = d.textbbox((0, 0), TITLE, font=font)
        tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    ty = space_top + (space_h - th) // 2 - bbox[1]
    d.text(((CANVAS - tw) // 2 - bbox[0], ty), TITLE, font=font, fill=(28, 38, 66))
    print("标题: y=%d  字号=%d  下方空间=%dpx" % (ty, size, space_h))

    canvas.save(OUT, "PNG")
    kb = os.path.getsize(OUT) / 1024
    print("输出: %s  %.1f KB  %dx%d" % (OUT, kb, canvas.width, canvas.height))
    assert canvas.size == (CANVAS, CANVAS)
    assert os.path.getsize(OUT) < 1024 * 1024


if __name__ == "__main__":
    main()
