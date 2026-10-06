"""
make_thumbnail.py —— 生成创意工坊封面

输入：thumbnail-source.png（用户提供的原图）
输出：thumbnail.png

── 为什么用【横向】而不是正方形 ──────────────────────────────────────
工坊虽然推荐 >=512x512，但【启动器 Mod 库里的显示框是横向的】。
实测：正方形封面会被按横向框裁切，底部内容（例如画在图里的标题）会被切掉。

因此这里输出一个横向比例（约 1.4:1）的封面：
  · 与启动器的显示框比例接近 → 不会被裁掉内容
  · 高度仍然 >= 512，满足工坊要求
  · 不把标题画进图片 —— 启动器旁边本来就会显示 mod 名字，
    画进去反而会被裁掉。

构图：整张原图直接用（气泡 + 手 + 角色一应俱全），
      只裁掉底部多余的白边。
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.dirname(HERE)
SRC = os.path.join(MOD, "thumbnail-source.png")
OUT = os.path.join(MOD, "thumbnail.png")

HEIGHT = 512
# 目标宽高比（≈ 启动器 Mod 卡片的显示框比例）
ASPECT = 1.40
# 从底部裁掉多少纯白（原图下方有约 40px）
CROP_BOTTOM = 40
# 左右各裁掉多少（可选，用于微调构图；负数表示不裁）
CROP_SIDE = 0


def main():
    if not os.path.isfile(SRC):
        raise SystemExit("找不到原图: %s" % SRC)

    im = Image.open(SRC).convert("RGB")
    print("原图: %dx%d  (宽高比 %.3f)" % (im.width, im.height, im.width / im.height))

    # 1) 裁掉底部白边
    if CROP_BOTTOM > 0 and im.height - CROP_BOTTOM > 100:
        im = im.crop((0, 0, im.width, im.height - CROP_BOTTOM))
    # 2) 可选：裁掉左右
    if CROP_SIDE > 0 and im.width - 2 * CROP_SIDE > 200:
        im = im.crop((CROP_SIDE, 0, im.width - CROP_SIDE, im.height))

    W, H = im.size
    print("裁边后: %dx%d  (%.3f)" % (W, H, W / H))

    # 3) 整图缩放，【不裁切】：
    #    先按宽度铺满，再按高度铺满，取较小的缩放比 -> 保证内容完整
    target_w = int(round(HEIGHT * ASPECT))
    scale = min(target_w / W, HEIGHT / H)
    nw, nh = int(round(W * scale)), int(round(H * scale))
    im = im.resize((nw, nh), Image.LANCZOS)

    # 4) 画布居中放置，四周不足处补白（原图本就是白底，衔接自然）
    canvas = Image.new("RGB", (target_w, HEIGHT), (255, 255, 255))
    canvas.paste(im, ((target_w - nw) // 2, (HEIGHT - nh) // 2))
    im = canvas

    im.save(OUT, "PNG")
    kb = os.path.getsize(OUT) / 1024
    print("输出: %s" % OUT)
    print("  %dx%d  (%.3f)  %.1f KB   图片区 %dx%d 居中"
          % (im.width, im.height, im.width / im.height, kb, nw, nh))
    assert im.height >= 512 and im.width >= 512
    assert os.path.getsize(OUT) < 1024 * 1024


if __name__ == "__main__":
    main()
