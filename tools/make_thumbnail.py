"""
make_thumbnail.py —— 生成创意工坊封面

输入：thumbnail-source.png（用户提供的原图）
输出：thumbnail.png（横向 717x512）

── 设计约束（都是实测定下来的）────────────────────────────────────────
1) 启动器 Mod 库的显示框是【横向】的（约 1.400:1）。
   用正方形会被裁切，所以按 1.400 出图。

2) 【不要把标题画进图片】—— 启动器旁边本来就显示 mod 名字，
   画进去既多余、又会被裁掉。

3) 【不裁切内容】—— 原图内容横向几乎铺满（x=0..789），
   横向裁切会切掉气泡文字或角色。
   原图比例 1.954 比目标 1.400 更宽，所以只能纵向留白。

4) 留白要【上下居中】，并且底部保证 SAFE_BOTTOM 以上的空白，
   这样：
     · 启动器无论从哪边裁，都不会切到内容
     · 图片下缘不会出现被裁掉一半的文字
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.dirname(HERE)
SRC = os.path.join(MOD, "thumbnail-source.png")
OUT = os.path.join(MOD, "thumbnail.png")

HEIGHT = 512
ASPECT = 1.40          # 匹配启动器显示框
CROP_BOTTOM = 42       # 裁掉原图底部纯白
SAFE_BOTTOM = 24       # 底部至少保留的空白（防止贴边被裁）


def main():
    if not os.path.isfile(SRC):
        raise SystemExit("找不到原图: %s" % SRC)

    im = Image.open(SRC).convert("RGB")
    print("原图: %dx%d  (%.3f)" % (im.width, im.height, im.width / im.height))

    if CROP_BOTTOM > 0 and im.height - CROP_BOTTOM > 100:
        im = im.crop((0, 0, im.width, im.height - CROP_BOTTOM))
    W, H = im.size
    print("裁掉底部白边后: %dx%d  (%.3f)" % (W, H, W / H))

    target_w = int(round(HEIGHT * ASPECT))
    # 等比缩放到【宽度铺满】（不裁切内容）
    scale = target_w / W
    nw, nh = target_w, int(round(H * scale))
    if nh > HEIGHT:                     # 万一高度超出，改为按高度缩放
        scale = HEIGHT / H
        nw, nh = int(round(W * scale)), HEIGHT
    im = im.resize((nw, nh), Image.LANCZOS)
    print("缩放后: %dx%d" % (nw, nh))

    # 垂直居中，保证上下留白尽量均匀、且底部不小于 SAFE_BOTTOM
    free = HEIGHT - nh
    top = max(0, min(free - SAFE_BOTTOM, free))
    top = free // 2 if free - SAFE_BOTTOM >= 0 else 0
    # 若居中后底部不足 SAFE_BOTTOM，则上移
    if HEIGHT - (top + nh) < SAFE_BOTTOM:
        top = max(0, HEIGHT - nh - SAFE_BOTTOM)

    canvas = Image.new("RGB", (target_w, HEIGHT), (255, 255, 255))
    canvas.paste(im, ((target_w - nw) // 2, top))
    canvas.save(OUT, "PNG")

    kb = os.path.getsize(OUT) / 1024
    print("输出: %s" % OUT)
    print("  %dx%d  (%.3f)  %.1f KB" % (canvas.width, canvas.height,
                                        canvas.width / canvas.height, kb))
    print("  图片区 %dx%d  top=%d  上留白=%d  下留白=%d"
          % (nw, nh, top, top, HEIGHT - top - nh))
    assert canvas.height >= 512 and canvas.width >= 512
    assert os.path.getsize(OUT) < 1024 * 1024
    assert HEIGHT - top - nh >= SAFE_BOTTOM, "底部留白不足"


if __name__ == "__main__":
    main()



if __name__ == "__main__":
    main()
