"""
zlpaths.py —— 路径解析（所有工具共用）

目的：不把任何机器相关的绝对路径写死在代码里。

解析规则（按优先级）

  MOD（本 mod 文件夹，必须含 common/ 与 events/）
    1. 环境变量 ZL_MOD
    2. 从本文件位置向上找：tools/ 的父目录
    3. 当前工作目录向上找
    4. <用户文档>/Paradox Interactive/Stellaris/mod/zl_unique_administrator

  GAME（Stellaris 安装目录，必须含 common/defines）
    1. 环境变量 STELLARIS_GAME
    2. 常见 Steam 安装位置（多盘符 + 库文件夹）
    3. 从 MOD 反推（若 mod 恰好在游戏目录下的 mod/）

找不到时给出清晰的报错提示，而不是静默用错路径。
"""
import os


def _looks_like_mod(p):
    return (os.path.isfile(os.path.join(p, "descriptor.mod"))
            and os.path.isdir(os.path.join(p, "common"))
            and os.path.isdir(os.path.join(p, "events")))


def _looks_like_game(p):
    return os.path.isfile(os.path.join(p, "common", "defines", "00_defines.txt"))


def _walk_up_for(start, predicate, limit=8):
    cur = os.path.abspath(start)
    for _ in range(limit):
        if predicate(cur):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    return None


def find_mod():
    # 1) 环境变量
    env = os.environ.get("ZL_MOD")
    if env and _looks_like_mod(env):
        return os.path.abspath(env)

    # 2) 从本文件位置向上找（工具在 <mod>/tools/ 下）
    here = os.path.dirname(os.path.abspath(__file__))
    found = _walk_up_for(here, _looks_like_mod)
    if found:
        return found

    # 3) 从当前工作目录向上找
    found = _walk_up_for(os.getcwd(), _looks_like_mod)
    if found:
        return found

    # 4) 默认用户文档目录
    docs = os.path.join(os.path.expanduser("~"), "Documents")
    cand = os.path.join(docs, "Paradox Interactive", "Stellaris", "mod",
                        "zl_unique_administrator")
    if _looks_like_mod(cand):
        return cand

    raise SystemExit(
        "找不到 mod 文件夹。请设置环境变量 ZL_MOD 指向它，例如：\n"
        r'    set ZL_MOD=C:\Users\<你>\Documents\Paradox Interactive\Stellaris\mod\zl_unique_administrator'
    )


def find_game():
    # 1) 环境变量
    env = os.environ.get("STELLARIS_GAME")
    if env and _looks_like_game(env):
        return os.path.abspath(env)

    # 2) 常见 Steam 位置
    roots = []
    for drive in ("C:", "D:", "E:", "F:", "G:"):
        roots += [
            os.path.join(drive + os.sep, "Steam", "steamapps", "common", "Stellaris"),
            os.path.join(drive + os.sep, "SteamLibrary", "steamapps", "common", "Stellaris"),
            os.path.join(drive + os.sep, "Program Files (x86)", "Steam",
                         "steamapps", "common", "Stellaris"),
            os.path.join(drive + os.sep, "Games", "Steam", "steamapps", "common", "Stellaris"),
        ]
    for p in roots:
        if _looks_like_game(p):
            return os.path.abspath(p)

    # 3) Steam 库文件夹记录（libraryfolders.vdf）
    for drive in ("C:", "D:", "E:", "F:", "G:"):
        vdf = os.path.join(drive + os.sep, "Steam", "steamapps", "libraryfolders.vdf")
        if os.path.isfile(vdf):
            try:
                txt = open(vdf, encoding="utf-8", errors="ignore").read()
                for m in __import__("re").finditer(r'"path"\s*"([^"]+)"', txt):
                    p = os.path.join(m.group(1).replace("\\\\", os.sep),
                                     "steamapps", "common", "Stellaris")
                    if _looks_like_game(p):
                        return os.path.abspath(p)
            except Exception:
                pass

    raise SystemExit(
        "找不到 Stellaris 安装目录。请设置环境变量 STELLARIS_GAME 指向它，例如：\n"
        r'    set STELLARIS_GAME=/path/to/Steam/steamapps/common/Stellaris'
    )


MOD = find_mod()
GAME = find_game()
