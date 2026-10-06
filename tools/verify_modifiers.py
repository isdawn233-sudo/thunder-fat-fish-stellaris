"""校验本 mod 用到的所有 modifier 名是否在原版存在。"""
import os, re
# 路径由 zlpaths 自动解析（可用环境变量 ZL_MOD / STELLARIS_GAME 覆盖）
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zlpaths import MOD, GAME


# 1) 原版所有 modifier 名（含 defines/pop 分类里的）
valid = set()
for root, _, files in os.walk(os.path.join(GAME, "common")):
    for fn in files:
        if not fn.endswith(".txt"):
            continue
        try:
            t = open(os.path.join(root, fn), encoding="utf-8-sig", errors="ignore").read()
        except Exception:
            continue
        for m in re.finditer(r'(?m)^\s*([a-z][a-z_0-9]{3,})\s*=\s*[-0-9]', t):
            valid.add(m.group(1))
# 事件/脚本里也会引用 modifier 名，一并扫
for root, _, files in os.walk(os.path.join(GAME, "events")):
    for fn in files:
        if not fn.endswith(".txt"):
            continue
        try:
            t = open(os.path.join(root, fn), encoding="utf-8-sig", errors="ignore").read()
        except Exception:
            continue
        for m in re.finditer(r'(?m)^\s*([a-z][a-z_0-9]{3,})\s*=\s*[-0-9]', t):
            valid.add(m.group(1))

print("原版 modifier 名库: %d 个" % len(valid))

# 2) 本 mod 的 modifier 块里用到的名字
BLOCKS = ("self_modifier", "modifier", "councilor_modifier", "planet_modifier",
          "fleet_modifier", "army_modifier", "sector_modifier", "system_modifier",
          "scientist_modifier", "galcom_modifier", "federation_modifier",
          "triggered_modifier", "triggered_self_modifier", "triggered_councilor_modifier")
used = {}
for root, _, files in os.walk(MOD):
    for fn in files:
        if not fn.endswith(".txt"):
            continue
        p = os.path.join(root, fn)
        t = open(p, encoding="utf-8-sig", errors="ignore").read()
        for blk in BLOCKS:
            for m in re.finditer(r'(?ms)^\s*' + blk + r'\s*=\s*\{', t):
                i = m.end() - 1
                depth = 0
                for j in range(i, len(t)):
                    if t[j] == '{':
                        depth += 1
                    elif t[j] == '}':
                        depth -= 1
                        if depth == 0:
                            inner = t[i+1:j]
                            for mm in re.finditer(r'([a-z][a-z_0-9]{3,})\s*=\s*([-0-9.]+)', inner):
                                used.setdefault(mm.group(1), set()).add(os.path.basename(p))
                            break

print("本 mod 使用: %d 个 modifier 名" % len(used))
print()
bad = {k: v for k, v in used.items() if k not in valid}
ok = {k: v for k, v in used.items() if k in valid}

print("=== [OK] valid (%d) ===" % len(ok))
for k in sorted(ok):
    print("   %-46s  %s" % (k, ",".join(sorted(ok[k]))))

if bad:
    print()
    print("=== [BAD] NOT FOUND IN VANILLA (%d) ===" % len(bad))
    for k in sorted(bad):
        print("   %-46s  %s" % (k, ",".join(sorted(bad[k]))))
else:
    print()
    print("=== all modifier names valid ===")
