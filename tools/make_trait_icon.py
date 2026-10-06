"""
make_trait_icon.py -- 生成群星领袖特性图标

原版规格（从 legendary_leader.dds / eager.dds 实测）：
    尺寸 29 x 29
    格式 DXT5
    内容【纯黑图形】+ 透明背景
        因为引擎用 layer 的 color 做乘法上色，
        trait_icon_default = { 0 0 0 191 } => 黑色 = 保持黑
    底板 / 稀有度光晕 / 边框 / 议会标记 都由引擎另外叠加，
    所以图标本身【不要】画圆圈底板或边框。

用法：
    python make_trait_icon.py --out xxx.dds [--glyph pillar|seal|fish|star]
"""
import argparse, struct
import numpy as np
from PIL import Image, ImageDraw

# ---------------------------------------------------------------- DXT5
def _dxt5_block(blk):
    r = blk[:, 0].astype(int); g = blk[:, 1].astype(int)
    b = blk[:, 2].astype(int); a = blk[:, 3].astype(int)
    amin, amax = int(a.min()), int(a.max())
    ab = bytearray(8); ab[0], ab[1] = amax, amin
    if amax != amin:
        pal = [amax, amin] + [int(round((((7-i)*amax) + (i*amin))/7.0)) for i in range(1, 7)]
        bits = 0
        for i in range(16):
            best, bd = 0, 1 << 30
            for p in range(8):
                d = abs(a[i]-pal[p])
                if d < bd: bd, best = d, p
            bits |= best << (3*i)
        for i in range(6):
            ab[2+i] = (bits >> (8*i)) & 0xFF
    lum = 2*r + 3*g + b
    imax, imin = int(lum.argmax()), int(lum.argmin())
    c0 = (r[imax], g[imax], b[imax]); c1 = (r[imin], g[imin], b[imin])
    cp = [c0, c1,
          ((2*c0[0]+c1[0])//3, (2*c0[1]+c1[1])//3, (2*c0[2]+c1[2])//3),
          ((c0[0]+2*c1[0])//3, (c0[1]+2*c1[1])//3, (c0[2]+2*c1[2])//3)]
    bits2 = 0
    for i in range(16):
        best, bd = 0, 1 << 30
        for p in range(4):
            d = (r[i]-cp[p][0])**2 + (g[i]-cp[p][1])**2 + (b[i]-cp[p][2])**2
            if d < bd: bd, best = d, p
        bits2 |= best << (2*i)
    # RGB565 打包：DXT 规定 R 在高 5 位、G 在中 6 位、B 在低 5 位
    # （原先误写成 B 在高位、R 在低位，会导致红蓝通道互换。2026-10-06 修正）
    rgb0 = ((c0[0] >> 3) << 11) | ((c0[1] >> 2) << 5) | (c0[2] >> 3)
    rgb1 = ((c1[0] >> 3) << 11) | ((c1[1] >> 2) << 5) | (c1[2] >> 3)
    out = bytearray(16); out[0:8] = ab
    struct.pack_into("<H", out, 8, rgb0)
    struct.pack_into("<H", out, 10, rgb1)
    struct.pack_into("<I", out, 12, bits2)
    return bytes(out)

def encode_dxt5(img):
    w, h = img.size
    arr = np.asarray(img.convert("RGBA"), np.uint8)
    out = bytearray()
    for by in range(h // 4):
        for bx in range(w // 4):
            blk = arr[by*4:(by+1)*4, bx*4:(bx+1)*4, :].reshape(16, 4)
            out += _dxt5_block(blk)
    return bytes(out)

def write_dds_bgra(path, img, mipmaps=True):
    """写成【未压缩 BGRA8】，与原版图标逐字段一致。

    原版图标实测（legendary_leader.dds / eager.dds / adaptable.dds ...）：
        29x29  mips=5  caps=0xFF000000
        pfFlags=0x41 (DDPF_RGB|DDPF_ALPHAPIXELS)  rgbBits=32
        masks  R=0x00FF0000 G=0x0000FF00 B=0x000000FF A=0xFF000000
    即内存顺序为 B,G,R,A。
    """
    w, h = img.size
    levels = [img]
    if mipmaps:
        cw, ch, cur = w, h, img
        while cw > 1 or ch > 1:
            nw, nh = max(1, cw // 2), max(1, ch // 2)
            cur = cur.resize((nw, nh), Image.LANCZOS)
            levels.append(cur)
            cw, ch = nw, nh

    hdr = bytearray(128)
    hdr[0:4] = b"DDS "
    struct.pack_into("<I", hdr, 4, 124)
    # 与原版逐字段一致：0x0002100F = CAPS|HEIGHT|WIDTH|PITCH|PIXELFORMAT
    struct.pack_into("<I", hdr, 8, 0x0002100F)
    struct.pack_into("<I", hdr, 12, h)
    struct.pack_into("<I", hdr, 16, w)
    struct.pack_into("<I", hdr, 20, w * 4)          # pitch
    struct.pack_into("<I", hdr, 28, len(levels))    # mip count
    pf = 76
    struct.pack_into("<I", hdr, pf, 32)             # pf size
    struct.pack_into("<I", hdr, pf + 4, 0x41)       # RGB | ALPHAPIXELS
    struct.pack_into("<I", hdr, pf + 8, 0)          # fourCC = 0 (未压缩)
    struct.pack_into("<I", hdr, pf + 12, 32)        # rgb bit count
    struct.pack_into("<I", hdr, pf + 16, 0x00FF0000)   # R
    struct.pack_into("<I", hdr, pf + 20, 0x0000FF00)   # G
    struct.pack_into("<I", hdr, pf + 24, 0x000000FF)   # B
    struct.pack_into("<I", hdr, pf + 28, 0xFF000000)   # A
    # caps1（偏移 108）：0x401008 = TEXTURE|MIPMAP|COMPLEX
    struct.pack_into("<I", hdr, 108, 0x401008 if len(levels) > 1 else 0x1000)

    body = bytearray()
    for lv in levels:
        a = np.asarray(lv.convert("RGBA"), np.uint8)
        bgra = np.empty_like(a)
        bgra[:, :, 0] = a[:, :, 2]      # B
        bgra[:, :, 1] = a[:, :, 1]      # G
        bgra[:, :, 2] = a[:, :, 0]      # R
        bgra[:, :, 3] = a[:, :, 3]      # A
        body += bgra.tobytes()
    open(path, "wb").write(bytes(hdr) + bytes(body))
    return len(hdr) + len(body), len(levels)


def write_dds(path, img, mipmaps=True):
    w, h = img.size
    levels = [img]
    if mipmaps:
        cw, ch, cur = w, h, img
        while cw > 1 or ch > 1:
            nw, nh = max(1, cw//2), max(1, ch//2)
            cur = cur.resize((nw, nh), Image.LANCZOS)
            levels.append(cur); cw, ch = nw, nh
    hdr = bytearray(128)
    hdr[0:4] = b"DDS "
    struct.pack_into("<I", hdr, 4, 124)
    struct.pack_into("<I", hdr, 8, 0x00081007)
    struct.pack_into("<I", hdr, 12, h)
    struct.pack_into("<I", hdr, 16, w)
    struct.pack_into("<I", hdr, 20, w*4)
    struct.pack_into("<I", hdr, 28, len(levels))
    pf = 76
    struct.pack_into("<I", hdr, pf, 32)
    struct.pack_into("<I", hdr, pf+4, 0x4)
    hdr[pf+8:pf+12] = b"DXT5"
    struct.pack_into("<I", hdr, 104, 0x401008 if len(levels) > 1 else 0x1000)
    body = bytearray()
    for lv in levels:
        lw, lh = lv.size
        pw, ph = (lw+3)//4*4, (lh+3)//4*4
        if (pw, ph) != (lw, lh):
            c = Image.new("RGBA", (pw, ph), (0, 0, 0, 0)); c.paste(lv, (0, 0)); lv = c
        body += encode_dxt5(lv)
    open(path, "wb").write(bytes(hdr) + bytes(body))
    return len(hdr) + len(body), len(levels)

# ---------------------------------------------------------------- 图形
def draw_glyph(size, kind):
    """在透明背景上画一个纯黑剪影（放大 8 倍绘制再缩小，边缘更干净）"""
    SS = size * 8
    img = Image.new("L", (SS, SS), 0)        # 0 = 透明
    d = ImageDraw.Draw(img)
    BLK = 255
    if kind == "pillar":
        # 立柱 + 横梁 + 顶部圆点（稳固/行政感）
        d.rectangle([SS*0.44, SS*0.30, SS*0.56, SS*0.78], fill=BLK)
        d.rectangle([SS*0.20, SS*0.44, SS*0.80, SS*0.54], fill=BLK)
        d.ellipse([SS*0.34, SS*0.10, SS*0.66, SS*0.34], fill=BLK)
        d.rectangle([SS*0.28, SS*0.78, SS*0.72, SS*0.87], fill=BLK)
    elif kind == "seal":
        # 圆环 + 中心方块
        d.ellipse([SS*0.12, SS*0.12, SS*0.88, SS*0.88], outline=BLK, width=int(SS*0.09))
        d.rectangle([SS*0.38, SS*0.38, SS*0.62, SS*0.62], fill=BLK)
    elif kind == "fish":
        # 抽象鱼形（呼应"大肥鱼"）
        d.ellipse([SS*0.16, SS*0.34, SS*0.74, SS*0.72], fill=BLK)
        d.polygon([(SS*0.70, SS*0.36), (SS*0.90, SS*0.24), (SS*0.90, SS*0.80), (SS*0.70, SS*0.68)], fill=BLK)
        d.ellipse([SS*0.30, SS*0.46, SS*0.38, SS*0.54], fill=0)
    else:  # star
        d.polygon([(SS*0.5, SS*0.08), (SS*0.62, SS*0.40), (SS*0.95, SS*0.40),
                   (SS*0.68, SS*0.60), (SS*0.78, SS*0.92), (SS*0.50, SS*0.72),
                   (SS*0.22, SS*0.92), (SS*0.32, SS*0.60), (SS*0.05, SS*0.40),
                   (SS*0.38, SS*0.40)], fill=BLK)
    small = img.resize((size, size), Image.LANCZOS)
    # 黑色 + 该 alpha
    rgba = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    a = np.asarray(small)
    arr = np.zeros((size, size, 4), np.uint8)
    arr[:, :, 3] = a
    return Image.fromarray(arr, "RGBA")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", type=int, default=29, help="原版是 29")
    ap.add_argument("--glyph", default="pillar",
                    choices=["pillar", "seal", "fish", "star"])
    ap.add_argument("--no-mipmaps", action="store_true")
    ap.add_argument("--dxt5", action="store_true",
                    help="输出 DXT5 压缩（默认输出未压缩 BGRA8，与原版图标一致）")
    ap.add_argument("--preview", default="")
    a = ap.parse_args()

    # 尺寸必须是 4 的倍数才能直接编码 DXT5；29 -> 用 32 画布再裁
    canvas = a.size if a.size % 4 == 0 else ((a.size + 3)//4*4)
    img = draw_glyph(a.size, a.glyph)
    if canvas != a.size:
        c = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
        c.paste(img, ((canvas-a.size)//2, (canvas-a.size)//2))
        img = c
    # 裁回目标尺寸（居中裁）
    if canvas != a.size:
        off = (canvas - a.size)//2
        img = img.crop((off, off, off+a.size, off+a.size))

    if a.dxt5:
        n, mips = write_dds(a.out, img, mipmaps=not a.no_mipmaps)
        fmt = "DXT5"
    else:
        n, mips = write_dds_bgra(a.out, img, mipmaps=not a.no_mipmaps)
        fmt = "BGRA8 (uncompressed, vanilla format)"
    arr = np.asarray(img)[:, :, 3]
    print("glyph  : %s" % a.glyph)
    print("format : %s" % fmt)
    print("size   : %dx%d  mips=%d" % (a.size, a.size, mips))
    print("alpha  : transparent=%d  opaque=%d  semi=%d"
          % (int((arr == 0).sum()), int((arr == 255).sum()), int(((arr > 0) & (arr < 255)).sum())))
    print("wrote  : %s  %d bytes" % (a.out, n))
    if a.preview:
        big = img.resize((img.width*8, img.height*8), Image.NEAREST)
        bg = Image.new("RGBA", big.size, (255, 0, 255, 255))
        bg.alpha_composite(big)
        bg.convert("RGB").save(a.preview)
        print("preview: %s" % a.preview)


if __name__ == "__main__":
    main()
