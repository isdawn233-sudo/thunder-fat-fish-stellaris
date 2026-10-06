"""
fix_bom.py -- 修正本地化文件的 UTF-8 BOM

群星规则：
    .yml 本地化文件 【必须】带 UTF-8 BOM，否则中文乱码
    .txt / .gfx / .mod / .asset 【不能】带 BOM，否则解析报 Unexpected token

编辑工具常常会丢掉 BOM，所以在每次改完本地化后跑一遍本脚本。
用法：  python fix_bom.py
"""
import os, sys
# 路径由 zlpaths 自动解析（可用环境变量 ZL_MOD / STELLARIS_GAME 覆盖）
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zlpaths import MOD, GAME

BOM = b"\xef\xbb\xbf"

fixed = 0
for root, _, files in os.walk(MOD):
    for fn in files:
        p = os.path.join(root, fn)
        rel = p.replace(MOD + "\\", "")
        data = open(p, "rb").read()
        has_bom = data[:3] == BOM

        if fn.endswith(".yml"):
            if not has_bom:
                open(p, "wb").write(BOM + data)
                print("  ADD BOM   %s" % rel)
                fixed += 1
            else:
                print("  OK        %s" % rel)
        elif fn.endswith((".txt", ".gfx", ".mod", ".asset")):
            if has_bom:
                open(p, "wb").write(data[3:])
                print("  DEL BOM   %s" % rel)
                fixed += 1

print()
print("修正 %d 个文件" % fixed)
sys.exit(0)
