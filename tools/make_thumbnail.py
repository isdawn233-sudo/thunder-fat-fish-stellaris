"""
make_thumbnail.py —— 生成创意工坊封面

输入：thumbnail-source.png（用户提供的原图）
输出：thumbnail.png

── 规格（按 Steam 工坊要求）────────────────────────────────────────────
必须【正方形 512x512】。

踩过的坑（重要，别再改回横向）:
  一开始做成横向 717x512（理由是想匹配启动器 Mod 卡片的显示框），
  结果上传时报 k_EResultFileNotFound。

  查 Steam 工坊错误码文档后确认:
      k_EResultFileNotFound (#9) = Steam 无法读取【预览图】，
      或该条目的工坊页面已不存在 —— 预览图路径是最常见的原因。
      原文: "Steam could not read the preview image, or the item's
             Workshop entry is gone. Check the preview image path..."
      并特别注明: "k_EResultFileNotFound points at a path, not at your
                  mod's contents. The preview image is the usual culprit."

  即: 预览图不符合 Steam 要求的正方形 512x512 时，Steam 无法建立
  工坊条目；启动器只好每次自己编一个新的 item id，表现为
  「上传失败 / 找不到文件」，而且永远无法成功。

构图:
  · 整图等比缩放到宽度铺满（不裁切内容 —— 气泡文字、手、角色全保留）
  · 上下留白居中（原图本就是白底，衔接自然）
  · 不要把标题画进图片: 启动器旁边本来就显示 mod 名字
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.dirname(HERE)
SRC = os.path.join(MOD, "thumbnail-source.png")
OUT = os.path.join(MOD, "thumbnail.png")

SIZE = 512             # Steam 工坊预览图要求的边长（必须是正方形）
CROP_BOTTOM = 42       # 裁掉原图底部纯白
SAFE_BOTTOM = 10       # 底部至少保留的空白


def main():
    if not os.path.isfile(SRC):
        raise SystemExit("找不到原图: %s" % SRC)

    im = Image.open(SRC).convert("RGB")
    print("原图: %dx%d  (%.3f)" % (im.width, im.height, im.width / im.height))

    if CROP_BOTTOM > 0 and im.height - CROP_BOTTOM > 100:
        im = im.crop((0, 0, im.width, im.height - CROP_BOTTOM))
    W, H = im.size
    print("裁掉底部白边后: %dx%d  (%.3f)" % (W, H, W / H))

    # 等比缩放到【宽度铺满】，不裁切内容
    scale = SIZE / W
    nw, nh = SIZE, int(round(H * scale))
    if nh > SIZE:                       # 万一太高，改为按高度缩放
        scale = SIZE / H
        nw, nh = int(round(W * scale)), SIZE
    im = im.resize((nw, nh), Image.LANCZOS)
    print("缩放后: %dx%d" % (nw, nh))

    # 上下留白居中
    free = SIZE - nh
    top = max(0, min(free - SAFE_BOTTOM, free // 2))
    if SIZE - (top + nh) < SAFE_BOTTOM:
        top = max(0, SIZE - nh - SAFE_BOTTOM)

    canvas = Image.new("RGB", (SIZE, SIZE), (255, 255, 255))
    canvas.paste(im, ((SIZE - nw) // 2, top))
    canvas.save(OUT, "PNG")

    kb = os.path.getsize(OUT) / 1024
    print("输出: %s" % OUT)
    print("  %dx%d  %.1f KB   图片区 %dx%d  top=%d"
          % (canvas.width, canvas.height, kb, nw, nh, top))
    assert canvas.size == (SIZE, SIZE), "必须是正方形"
    assert os.path.getsize(OUT) < 1024 * 1024, "必须 < 1MB"


if __name__ == "__main__":
    main()
