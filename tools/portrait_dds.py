# ============================================================================
#  portrait_dds.py -- 立绘 -> 群星用 DXT5 DDS（纯 Python 实现）
#
#  流程：
#     1. 裁切（支持非正方形）
#     2. 去白底（从四边 flood fill，保留角色内部白色）
#     3. 等比缩放居中到 512x512（不变形；背景透明）
#     4. 边缘收缩（防 DXT5 压缩出白边）
#     5. 手写 DXT5 (BC3) 编码，无 mipmap
#
#  用法：
#     python portrait_dds.py --src bigfish.png --out x.dds ^
#         --crop 0,20,941,941 [--preview x.png] [--no-bg] [--mipmaps]
# ============================================================================
import argparse, struct, sys
from PIL import Image
import numpy as np

# ------------------------------------------------ DXT5 编码
def _dxt5_block(block_rgba):
    """block_rgba: (16,4) uint8 -> 16 bytes"""
    r = block_rgba[:, 0].astype(int)
    g = block_rgba[:, 1].astype(int)
    b = block_rgba[:, 2].astype(int)
    a = block_rgba[:, 3].astype(int)

    # ---- alpha：8 级调色板 ----
    amin, amax = int(a.min()), int(a.max())
    ab = bytearray(8)
    ab[0], ab[1] = amax, amin
    if amax != amin:
        pal = [amax, amin] + [int(round((((7 - i) * amax) + (i * amin)) / 7.0)) for i in range(1, 7)]
        bits = 0
        for i in range(16):
            best, bd = 0, 1 << 30
            for p in range(8):
                d = abs(a[i] - pal[p])
                if d < bd:
                    bd, best = d, p
            bits |= best << (3 * i)
        for i in range(6):
            ab[2 + i] = (bits >> (8 * i)) & 0xFF

    # ---- 颜色：RGB565 端点 + 4 级调色板 ----
    lum = 2 * r + 3 * g + b
    i_max, i_min = int(lum.argmax()), int(lum.argmin())
    r0, g0, b0 = r[i_max], g[i_max], b[i_max]
    r1, g1, b1 = r[i_min], g[i_min], b[i_min]
    cp = [(r0, g0, b0), (r1, g1, b1),
          ((2 * r0 + r1) // 3, (2 * g0 + g1) // 3, (2 * b0 + b1) // 3),
          ((r0 + 2 * r1) // 3, (g0 + 2 * g1) // 3, (b0 + 2 * b1) // 3)]
    bits2 = 0
    for i in range(16):
        best, bd = 0, 1 << 30
        for p in range(4):
            d = (r[i] - cp[p][0]) ** 2 + (g[i] - cp[p][1]) ** 2 + (b[i] - cp[p][2]) ** 2
            if d < bd:
                bd, best = d, p
        bits2 |= best << (2 * i)
    # RGB565 打包：DXT 规定 R 在高 5 位、G 在中 6 位、B 在低 5 位
    # （原先误写成 B 在高位、R 在低位，导致红蓝通道互换：
    #   蓝发会被存成橙发。2026-10-06 修正）
    rgb0 = ((r0 >> 3) << 11) | ((g0 >> 2) << 5) | (b0 >> 3)
    rgb1 = ((r1 >> 3) << 11) | ((g1 >> 2) << 5) | (b1 >> 3)

    out = bytearray(16)
    out[0:8] = ab
    struct.pack_into("<H", out, 8, rgb0)
    struct.pack_into("<H", out, 10, rgb1)
    struct.pack_into("<I", out, 12, bits2)
    return bytes(out)

def encode_dxt5(img):
    """img: RGBA PIL Image，宽高须为 4 的倍数"""
    w, h = img.size
    assert w % 4 == 0 and h % 4 == 0, (w, h)
    arr = np.asarray(img.convert("RGBA"), dtype=np.uint8)
    bw, bh = w // 4, h // 4
    out = bytearray()
    for by in range(bh):
        for bx in range(bw):
            blk = arr[by*4:(by+1)*4, bx*4:(bx+1)*4, :].reshape(16, 4)
            out += _dxt5_block(blk)
    return bytes(out)

def write_dds(path, img, mipmaps=False):
    """写 DXT5 DDS。mipmaps=False -> mip 数 1、caps=TEXTURE（与原版立绘一致）"""
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
    struct.pack_into("<I", hdr, 8, 0x00081007)     # CAPS|HEIGHT|WIDTH|PIXELFORMAT|PITCH
    struct.pack_into("<I", hdr, 12, h)
    struct.pack_into("<I", hdr, 16, w)
    struct.pack_into("<I", hdr, 20, w * 4)
    struct.pack_into("<I", hdr, 28, len(levels))   # mip count
    pf = 76
    struct.pack_into("<I", hdr, pf, 32)
    struct.pack_into("<I", hdr, pf + 4, 0x4)       # DDPF_FOURCC
    hdr[pf + 8:pf + 12] = b"DXT5"
    caps = 0x401008 if len(levels) > 1 else 0x1000
    struct.pack_into("<I", hdr, 104, caps)

    body = bytearray()
    for lv in levels:
        lw, lh = lv.size
        pad_w = (lw + 3) // 4 * 4
        pad_h = (lh + 3) // 4 * 4
        if (pad_w, pad_h) != (lw, lh):
            canvas = Image.new("RGBA", (pad_w, pad_h), (0, 0, 0, 0))
            canvas.paste(lv, (0, 0))
            lv = canvas
        body += encode_dxt5(lv)

    with open(path, "wb") as f:
        f.write(hdr)
        f.write(body)
    return len(hdr) + len(body), len(levels)

# ------------------------------------------------ 去白底
def remove_white_bg(im, thr=242, tol=16):
    """从四边 flood fill 清除近白背景，返回 RGBA"""
    rgba = np.asarray(im.convert("RGBA")).copy()
    h, w = rgba.shape[:2]
    rgb = rgba[:, :, :3].astype(int)
    mx = rgb.max(axis=2)
    mn = rgb.min(axis=2)
    is_bg = (mx >= thr) & ((mx - mn) <= tol)

    visited = np.zeros((h, w), dtype=bool)
    from collections import deque
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if is_bg[y, x] and not visited[y, x]:
                visited[y, x] = True
                q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if is_bg[y, x] and not visited[y, x]:
                visited[y, x] = True
                q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx] and is_bg[ny, nx]:
                visited[ny, nx] = True
                q.append((ny, nx))
    rgba[visited, 3] = 0
    return Image.fromarray(rgba, "RGBA"), int(visited.sum())

def erode_alpha(im, factor=0.55):
    """边缘像素 alpha 收缩，避免 DXT5 压缩白边"""
    a = np.asarray(im).copy()
    al = a[:, :, 3].astype(int)
    trans = al < 128
    edge = np.zeros_like(trans)
    edge[1:, :] |= trans[:-1, :]
    edge[:-1, :] |= trans[1:, :]
    edge[:, 1:] |= trans[:, :-1]
    edge[:, :-1] |= trans[:, 1:]
    edge &= ~trans & (al > 0)
    a[:, :, 3] = np.where(edge, (al * factor).astype(np.uint8), a[:, :, 3])
    return Image.fromarray(a, "RGBA"), int(edge.sum())

# ------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--crop", default="", help="x,y,w,h（省略则自动顶部居中正方形）")
    ap.add_argument("--size", type=int, default=512, help="目标宽度")
    ap.add_argument("--height", type=int, default=0, help="目标高度（0=与宽度相同，即正方形）")
    ap.add_argument("--gain", type=float, default=1.0,
                    help="RGB 预乘系数。游戏着色器提亮约 1.94 倍，"
                         "静态立绘建议 1/1.94≈0.515")
    ap.add_argument("--sat", type=float, default=1.0,
                    help="饱和度预乘系数。游戏渲染后饱和度约 x0.805，"
                         "建议 1/0.805≈1.24")
    ap.add_argument("--tint", type=float, nargs=3, default=[1.0, 1.0, 1.0],
                    metavar=("R", "G", "B"),
                    help="逐通道缩放，抵消引擎的通道偏移。"
                         "实测游戏会注入绿色、压制蓝色，可试 1.00 0.88 1.18")
    ap.add_argument("--no-bg", action="store_true", help="（保留兼容，等同不处理）")
    ap.add_argument("--remove-white", action="store_true",
                    help="仅当原图是不透明白底时才用：删掉近白背景")
    ap.add_argument("--mipmaps", action="store_true")
    ap.add_argument("--preview", default="")
    a = ap.parse_args()

    im = Image.open(a.src).convert("RGBA")
    W, H = im.size
    print(f"source : {W} x {H}")

    if a.crop:
        x, y, w, h = [int(v) for v in a.crop.split(",")]
    else:
        side = min(W, int(H * 0.45))
        x, y, w, h = (W - side) // 2, int(H * 0.02), side, side
    x, y = max(0, x), max(0, y)
    w, h = min(w, W - x), min(h, H - y)
    print(f"crop   : x={x} y={y} w={w} h={h}")
    im = im.crop((x, y, x + w, y + h))

    # ---- 背景处理 ----
    # 注意：若原图本身已经是带透明通道的 PNG（人物 A=255、背景 A=0），
    # 就【绝对不要】再去"删白底" —— 那会把角色身上的白色部分
    # （白围裙、蕾丝、高光）当成背景删掉，导致背景从人物里透出来。
    # 只有原图是不透明白底时，才需要 --remove-white。
    if a.remove_white:
        im, n = remove_white_bg(im)
        print(f"bg     : removed near-white {n} px ({100.0*n/(w*h):.1f}%)")
    else:
        al = np.asarray(im.convert("RGBA"))[:, :, 3]
        n_t = int((al == 0).sum())
        n_o = int((al == 255).sum())
        print(f"bg     : kept source alpha (transparent={n_t}, opaque={n_o})")

    # ---- 颜色补偿 ----
    # 群星静态立绘走 PdxMeshPortrait 着色器，渲染后：
    #     亮度  ≈ 贴图亮度 × 1.94      -> 需要预压暗 gain≈0.515
    #     饱和度 ≈ 贴图饱和度 × 0.805  -> 需要预加饱和 sat≈1.24
    # (实测自游戏截图与贴图的像素统计，通道比值 R/G/B 均 ≈1:1)
    if (a.gain and abs(a.gain - 1.0) > 1e-6) or (a.sat and abs(a.sat - 1.0) > 1e-6) \
       or any(abs(t - 1.0) > 1e-6 for t in a.tint):
        arr0 = np.asarray(im.convert("RGBA")).astype(np.float32)
        rgb0 = np.clip(arr0[:, :, :3] * a.gain, 0, 255)
        if abs(a.sat - 1.0) > 1e-6:
            lum = rgb0 @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
            rgb0 = np.clip(lum[:, :, None] + (rgb0 - lum[:, :, None]) * a.sat, 0, 255)
        # 逐通道缩放（抵消引擎注入的通道偏移）
        rgb0 = np.clip(rgb0 * np.array(a.tint, dtype=np.float32)[None, None, :], 0, 255)
        arr0[:, :, :3] = rgb0
        im = Image.fromarray(arr0.astype(np.uint8), "RGBA")
        print(f"color  : gain x {a.gain:.3f}, sat x {a.sat:.3f}, tint R/G/B = "
              f"{a.tint[0]:.3f}/{a.tint[1]:.3f}/{a.tint[2]:.3f}")

    S = a.size
    SH = a.height if a.height else a.size      # 目标高（默认正方形）
    # ---- 缩放：premultiply 后 LANCZOS，避免透明区颜色渗进人物 ----
    arr = np.asarray(im.convert("RGBA")).astype(np.float32)
    alpha = arr[:, :, 3:4] / 255.0
    premul = np.concatenate([arr[:, :, :3] * alpha, arr[:, :, 3:4]], axis=2)
    pm_img = Image.fromarray(np.clip(premul, 0, 255).astype(np.uint8), "RGBA")

    scale = min(S / im.width, SH / im.height)
    dw, dh = max(1, round(im.width * scale)), max(1, round(im.height * scale))
    ox, oy = (S - dw) // 2, (SH - dh) // 2

    small = np.asarray(pm_img.resize((dw, dh), Image.LANCZOS)).astype(np.float32)
    a_small = small[:, :, 3:4] / 255.0
    with np.errstate(divide="ignore", invalid="ignore"):
        rgb = np.where(a_small > 0, small[:, :, :3] / np.maximum(a_small, 1e-6), 0)
    out = np.zeros((SH, S, 4), dtype=np.uint8)
    out[oy:oy+dh, ox:ox+dw, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    out[oy:oy+dh, ox:ox+dw, 3] = np.clip(small[:, :, 3], 0, 255).astype(np.uint8)
    canvas = Image.fromarray(out, "RGBA")
    print(f"fit    : {im.width}x{im.height} -> {dw}x{dh} on {S}x{SH} (premultiplied)")

    if a.preview:
        canvas.save(a.preview)
        print(f"preview: {a.preview}")

    size, mips = write_dds(a.out, canvas, mipmaps=a.mipmaps)
    print(f"wrote  : {a.out}  {S}x{SH} DXT5  mips={mips}  {size} bytes")

if __name__ == "__main__":
    main()
