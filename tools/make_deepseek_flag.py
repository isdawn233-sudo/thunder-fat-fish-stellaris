"""
make_deepseek_flag.py -- 用 DeepSeek 官方 logo（resources/icon.png 里的鲸鱼）
生成 mod 的国家旗帜。

做法：
    1. 从 icon.png 里提取鲸鱼剪影（深色像素 -> 遮罩）
    2. 把遮罩分别渲染成几种配色方案
    3. 输出原版规格的旗帜 DDS（未压缩 BGRA8，无 mipmap）
       flags/special/<name>.dds            256x256
       flags/special/map/<name>.dds        256x256
       flags/special/small/<name>.dds       24x24
"""
import os, struct
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC = r"/path/to/whale.png"
OUT = r"/path/to/Documents/Paradox Interactive/Stellaris/mod/zl_unique_administrator\flags\special"
FRAMES = r"/path/to/frames"

# DeepSeek 品牌蓝（取自其品牌色）
BRAND_BLUE = (77, 107, 254)
DARK_NAVY = (16, 24, 56)
WHITE = (255, 255, 255)


def write_flag_dds(path, img):
    """未压缩 BGRA8，无 mipmap，字段对齐原版 flags/special/*.dds"""
    w, h = img.size
    hdr = bytearray(128)
    hdr[0:4] = b"DDS "
    struct.pack_into("<I", hdr, 4, 124)
    struct.pack_into("<I", hdr, 8, 0x00100F)
    struct.pack_into("<I", hdr, 12, h)
    struct.pack_into("<I", hdr, 16, w)
    struct.pack_into("<I", hdr, 20, w * 4)
    struct.pack_into("<I", hdr, 28, 0)
    pf = 76
    struct.pack_into("<I", hdr, pf, 32)
    struct.pack_into("<I", hdr, pf + 4, 0x41)
    struct.pack_into("<I", hdr, pf + 8, 0)
    struct.pack_into("<I", hdr, pf + 12, 32)
    struct.pack_into("<I", hdr, pf + 16, 0x00FF0000)
    struct.pack_into("<I", hdr, pf + 20, 0x0000FF00)
    struct.pack_into("<I", hdr, pf + 24, 0x000000FF)
    struct.pack_into("<I", hdr, pf + 28, 0xFF000000)
    struct.pack_into("<I", hdr, 108, 0x1000)
    a = np.asarray(img.convert("RGBA"), np.uint8)
    bgra = np.empty_like(a)
    bgra[:, :, 0] = a[:, :, 2]
    bgra[:, :, 1] = a[:, :, 1]
    bgra[:, :, 2] = a[:, :, 0]
    bgra[:, :, 3] = a[:, :, 3]
    open(path, "wb").write(bytes(hdr) + bgra.tobytes())


def extract_whale(icon_path):
    """从 app 图标里提取鲸鱼剪影，返回 (alpha遮罩 float 0..1, 包围盒)"""
    im = Image.open(icon_path).convert("RGBA")
    a = np.asarray(im).astype(float)
    rgb = a[:, :, :3]
    alpha = a[:, :, 3]

    # 图标是浅色圆角底 + 深色鲸鱼：取"明显偏暗且不透明"的像素
    lum = rgb.mean(axis=2)
    mask = (lum < 140) & (alpha > 128)

    # 裁到包围盒
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        raise RuntimeError("没找到鲸鱼像素，检查图标")
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    m = mask[y0:y1, x0:x1]
    print("  鲸鱼包围盒: x %d..%d  y %d..%d  -> %dx%d  像素 %d"
          % (x0, x1, y0, y1, x1 - x0, y1 - y0, m.sum()))
    return m


def render_flag(mask, size, bg, fg, pad_ratio=0.14, round_corners=False,
                label=None, label_color=None, font_path=r"C:\Windows\Fonts\arialbd.ttf",
                transparent_bg=False):
    """把鲸鱼遮罩渲染成方形旗帜。

    transparent_bg=True 时底色全透明（alpha=0），只保留鲸鱼与字标 ——
    与原版灰风旗帜一样（gray_goo.dds 有 61% 全透明像素）。
    """
    SS = size * 4
    if transparent_bg:
        canvas = Image.new("RGBA", (SS, SS), (0, 0, 0, 0))
    else:
        canvas = Image.new("RGBA", (SS, SS), tuple(bg) + (255,))

    # 有字标时，logo 占上半部分，给文字留出下方空间
    if label:
        avail = SS * 0.62
        top_ratio = 0.10
    else:
        avail = SS * (1 - 2 * pad_ratio)
        top_ratio = None

    mh, mw = mask.shape
    scale = min(avail / mw, avail / mh)
    nw, nh = max(1, int(mw * scale)), max(1, int(mh * scale))
    mimg = Image.fromarray((mask * 255).astype(np.uint8), "L").resize((nw, nh), Image.LANCZOS)

    fg_layer = Image.new("RGBA", (nw, nh), tuple(fg) + (255,))
    fg_layer.putalpha(mimg)

    if label:
        ox = (SS - nw) // 2
        oy = int(SS * top_ratio)
    else:
        ox, oy = (SS - nw) // 2, (SS - nh) // 2
    canvas.alpha_composite(fg_layer, (ox, oy))

    # ---- 字标 ----
    if label:
        d = ImageDraw.Draw(canvas)
        fs = int(SS * 0.155)
        try:
            font = ImageFont.truetype(font_path, fs)
        except Exception:
            font = ImageFont.load_default()
        col = tuple(label_color or fg) + (255,)
        bbox = d.textbbox((0, 0), label, font=font)
        tw = bbox[2] - bbox[0]
        maxw = SS * 0.88
        if tw > maxw:
            fs = int(fs * maxw / tw)
            font = ImageFont.truetype(font_path, fs)
            bbox = d.textbbox((0, 0), label, font=font)
            tw = bbox[2] - bbox[0]
        tx = (SS - tw) // 2 - bbox[0]
        ty = oy + nh + int(SS * 0.045)
        # 透明底时给文字加一圈深色描边，保证在任何背景上都看得清
        if transparent_bg:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx or dy:
                        d.text((tx + dx, ty + dy), label, font=font, fill=(10, 16, 40, 255))
        d.text((tx, ty), label, font=font, fill=col)

    return canvas.resize((size, size), Image.LANCZOS)


if __name__ == "__main__":
    print("提取 DeepSeek 鲸鱼 logo ...")
    mask = extract_whale(SRC)

    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, "map"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "small"), exist_ok=True)

    # ---- 配色方案 ----
    # bg=None 表示【透明底】，只保留鲸鱼与字标
    # （原版灰风旗帜就是透明底：gray_goo.dds 有 61% 全透明像素）
    schemes = {
        "T1_透明底_品牌蓝鲸":  dict(bg=None, fg=BRAND_BLUE, transparent=True),
        "T2_透明底_白鲸":      dict(bg=None, fg=WHITE,      transparent=True),
        "T3_透明底_亮蓝鲸":    dict(bg=None, fg=(120, 190, 255), transparent=True),
        "A_蓝底白鲸":          dict(bg=BRAND_BLUE, fg=WHITE,  transparent=False),
        "B_深蓝底蓝鲸":        dict(bg=DARK_NAVY,  fg=BRAND_BLUE, transparent=False),
    }

    # 预览：透明底用洋红做衬底，方便看清抠图效果
    previews = []
    for name, sc in schemes.items():
        big = render_flag(mask, 256, sc["bg"], sc["fg"], label="DeepSeek",
                          label_color=sc["fg"], transparent_bg=sc["transparent"])
        prev = os.path.join(FRAMES, "flag_%s.png" % name)
        if sc["transparent"]:
            board = Image.new("RGBA", big.size, (255, 0, 255, 255))
            board.alpha_composite(big)
            board.convert("RGB").save(prev)
        else:
            big.convert("RGB").save(prev)
        previews.append((name, big))

    # ---- 正式采用：T2 透明底 + 白鲸（最清晰，且不带底框）----
    chosen = schemes["T2_透明底_白鲸"]
    for size, sub in ((256, ""), (256, "map"), (24, "small")):
        # 小旗 24x24 放不下字标，只放鲸鱼
        lab = None if size <= 32 else "DeepSeek"
        img = render_flag(mask, size, chosen["bg"], chosen["fg"],
                          label=lab, label_color=chosen["fg"],
                          transparent_bg=chosen["transparent"])
        p = os.path.join(OUT, sub, "zl_deepseek.dds")
        write_flag_dds(p, img)
        b = open(p, "rb").read()
        a = np.asarray(img.convert("RGBA"))[:, :, 3]
        print("  wrote %-46s %3dx%-3d %d B  label=%-9s 全透明像素=%d"
              % (p.replace(OUT, "flags/special"), size, size, len(b),
                 lab or "-", int((a == 0).sum())))

    # ---- 拼对比图 ----
    W = 256
    canvas = Image.new("RGB", (W * len(previews) + 10 * (len(previews) - 1), W), (60, 60, 70))
    for i, (nm, im) in enumerate(previews):
        board = Image.new("RGBA", im.size, (255, 0, 255, 255))
        board.alpha_composite(im)
        canvas.paste(board.convert("RGB"), (i * (W + 10), 0))
    canvas.save(os.path.join(FRAMES, "flag_schemes.png"))
    print()
    print("配色对比图: frames/flag_schemes.png")
    print("  顺序: " + " | ".join(n for n, _ in previews))
