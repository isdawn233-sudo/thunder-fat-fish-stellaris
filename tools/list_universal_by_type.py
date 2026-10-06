"""
list_universal_by_type.py -- 按 leader_trait_type 列出纯通用特质（含职业适用性）
"""
import os, re, sys
# 路径由 zlpaths 自动解析（可用环境变量 ZL_MOD / STELLARIS_GAME 覆盖）
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zlpaths import MOD, GAME


LOC = {}
d = os.path.join(GAME, "localisation", "simp_chinese")
for fn in os.listdir(d):
    if not fn.endswith(".yml"):
        continue
    try:
        t = open(os.path.join(d, fn), encoding="utf-8-sig", errors="ignore").read()
    except Exception:
        continue
    for line in t.splitlines():
        m = re.match(r'^\s*([A-Za-z0-9_.\-]+):\d*\s*"(.*)"\s*$', line)
        if m:
            LOC[m.group(1)] = m.group(2)


def resolve(s, dep=0):
    if not s or dep > 8:
        return s
    return re.sub(r'\$([A-Za-z0-9_.\-]+)\$',
                  lambda m: resolve(LOC.get(m.group(1), m.group(0)), dep + 1), s)


def name_of(key):
    nm = resolve(LOC.get(key) or LOC.get("trait_" + key) or "")
    if not nm:
        m = re.match(r'^(.*)_(\d+)$', key)
        if m:
            b = LOC.get(m.group(1)) or LOC.get("trait_" + m.group(1))
            if b:
                nm = resolve(b) + " " + {2: "II", 3: "III", 4: "IV"}.get(int(m.group(2)), m.group(2))
    return nm or key


def strip_comments(t):
    return "\n".join(l[:l.find("#")] if "#" in l else l for l in t.splitlines())


BAD = ["councilor_modifier", "triggered_councilor_modifier", "planet_modifier",
       "sector_modifier", "triggered_planet_modifier", "triggered_sector_modifier",
       "fleet_modifier", "army_modifier", "triggered_fleet_modifier",
       "triggered_army_modifier", "galcom_modifier", "federation_modifier",
       "background_planet_modifier"]
GOOD = ["self_modifier", "modifier", "triggered_self_modifier", "triggered_modifier"]

want = sys.argv[1] if len(sys.argv) > 1 else "veteran"
rows = []
for fn in os.listdir(os.path.join(GAME, "common", "traits")):
    if not fn.endswith(".txt") or fn.startswith("000_") or fn.startswith("30_"):
        continue
    txt = strip_comments(open(os.path.join(GAME, "common", "traits", fn),
                              encoding="utf-8-sig", errors="ignore").read())
    for m in re.finditer(r'(?m)^\s*([a-zA-Z0-9_]+)\s*=\s*\{', txt):
        key = m.group(1)
        if not (key.startswith("leader_trait") or key.startswith("trait_ruler")):
            continue
        i = m.end() - 1
        depth = 0
        body = None
        for j in range(i, len(txt)):
            if txt[j] == '{':
                depth += 1
            elif txt[j] == '}':
                depth -= 1
                if depth == 0:
                    body = txt[i + 1:j]
                    break
        if body is None:
            continue
        if any(re.search(r'(?m)^\s*' + b + r'\s*=\s*\{', body) for b in BAD):
            continue
        if not any(re.search(r'(?m)^\s*' + b + r'\s*=\s*\{', body) for b in GOOD):
            continue
        ty = re.search(r'leader_trait_type\s*=\s*(\w+)', body)
        kt = ty.group(1) if ty else "basic"
        if kt != want:
            continue
        lc = re.search(r'leader_class\s*=\s*\{([^}]*)\}', body)
        classes = lc.group(1).split() if lc else ["all"]
        # 排除 crisis / 特殊来源
        vals = [x for x in re.findall(r'([a-z_0-9]+)\s*=\s*([-0-9.]+)', body)
                if x[0] not in ("factor", "mult", "exists", "owner", "add", "value", "cost")]
        if not vals:
            continue
        rows.append((key, name_of(key), classes, vals, fn))

print("=== 纯通用 【%s】 特质（共 %d 个）===" % (want, len(rows)))
print()
for key, nm, classes, vals, fn in sorted(rows):
    cc = "通用" if classes == ["all"] else "/".join(classes)
    print("* %-44s %-22s [%s]" % (key, nm, cc))
    print("      %s" % ", ".join("%s=%s" % v for v in vals[:8]))
    print("      来源 %s" % fn)
