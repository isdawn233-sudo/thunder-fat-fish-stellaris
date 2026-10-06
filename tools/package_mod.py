"""
package_mod.py —— 把 mod 打包成可发布的 zip

输出：<项目上级>/发布包/zl_unique_administrator.zip

为什么需要这个脚本
    GitHub 的 "Download ZIP" 会多套一层目录（<repo>-main/），
    解压后路径不对，玩家要手动挪文件夹，很容易装错。
    这个脚本产出的 zip 【解压即用】：
    直接解压到 Stellaris 的 mod 目录即可，不会多一层。

zip 内部结构
    zl_unique_administrator/descriptor.mod
    zl_unique_administrator/common/...
    zl_unique_administrator/events/...
    ...

排除的内容（不应该出现在发布包里）
    .git/  __pycache__/  frames/  *.pyc  *.tmp
    *.bak*（备份文件）  descriptor.mod.bak-*  thumbnail.png.bak-*
"""
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zlpaths import MOD

NAME = "zl_unique_administrator"
# 发布包输出目录：优先用环境变量 ZL_OUT，默认放在用户「文档」下的
# stellaris_mod_zl/发布包
OUT_DIR = os.environ.get(
    "ZL_OUT",
    os.path.join(os.path.expanduser("~"), "Documents", "stellaris_mod_zl", "发布包"))

SKIP_DIRS = {".git", "__pycache__", "frames", ".idea", ".vscode"}
SKIP_EXTS = {".pyc", ".tmp"}
SKIP_SUFFIX = (".bak", ".bak-old", ".bak-v1", ".bak-remotefid")


def keep(rel_path):
    parts = rel_path.replace("\\", "/").split("/")
    if any(p in SKIP_DIRS for p in parts):
        return False
    base = parts[-1]
    if base.endswith(SKIP_SUFFIX) or ".bak-" in base or ".bak." in base:
        return False
    if os.path.splitext(base)[1].lower() in SKIP_EXTS:
        return False
    return True


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    zip_path = os.path.join(OUT_DIR, NAME + ".zip")

    count = 0
    total = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for root, dirs, files in os.walk(MOD):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, MOD)
                if not keep(rel):
                    continue
                z.write(full, NAME + "/" + rel.replace("\\", "/"))
                count += 1
                total += os.path.getsize(full)

    size = os.path.getsize(zip_path)
    print("mod 目录 : %s" % MOD)
    print("输出     : %s" % zip_path)
    print("文件数   : %d" % count)
    print("原始大小 : %.2f MB" % (total / 1024 / 1024))
    print("压缩后   : %.2f MB  (压缩率 %.0f%%)"
          % (size / 1024 / 1024, size / total * 100))

    # 校验关键文件在包里
    need = ["descriptor.mod", "thumbnail.png"]
    with zipfile.ZipFile(zip_path) as z:
        names = set(z.namelist())
    print()
    print("关键文件检查:")
    for n in need:
        ok = (NAME + "/" + n) in names
        print("  %-22s %s" % (n, "OK" if ok else "!! 缺失"))
        if not ok:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
