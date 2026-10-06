"""
find_universal.py -- 列出【纯通用】特质的候选池

纯通用 = 只含 self_modifier / modifier / triggered_self_modifier
        （不含 councilor_* / planet_* / sector_* / fleet_* / army_*）
这类特质不管领袖担任什么职位都生效，正是需求要的"正常的"特质。
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


BAD_BLOCKS = ["councilor_modifier", "triggered_councilor_modifier",
              "planet_modifier", "sector_modifier", "triggered_planet_modifier",
              "triggered_sector_modifier", "fleet_modifier", "army_modifier",
              "triggered_fleet_modifier", "triggered_army_modifier",
              "galcom_modifier", "federation_modifier", "background_planet_modifier"]
GOOD_BLOCKS = ["self_modifier", "modifier", "triggered_self_modifier", "triggered_modifier"]

want_class = sys.argv[1] if len(sys.argv) > 1 else "official"

rows = []
for fn in os.listdir(os.path.join(GAME, "common", "traits")):
    if not fn.endswith(".txt") or fn.startswith("000_"):
        continue
    txt = strip_comments(open(os.path.join(GAME, "common", "traits", fn),
                              encoding="utf-8-sig", errors="ignore").read())
    for m in re.finditer(r'(?m)^\s*([a-zA-Z0-9_]+)\s*=\s*\{', txt):
        key = m.group(1)
        if not (key.startswith("leader_trait") or key.startswith("trait_ruler")):
            continue
        i = m.end() - 1
        depth = 0
        for j in range(i, len(txt)):
            if txt[j] == '{':
                depth += 1
            elif txt[j] == '}':
                depth -= 1
                if depth == 0:
                    body = txt[i + 1:j]
                    break
        else:
            continue

        # 过滤：有任何一个"位置限定"块就排除
        if any(re.search(r'(?m)^\s*' + b + r'\s*=\s*\{', body) for b in BAD_BLOCKS):
            continue
        # 必须至少有一个通用块
        if not any(re.search(r'(?m)^\s*' + b + r'\s*=\s*\{', body) for b in GOOD_BLOCKS):
            continue
        # 职业过滤
        lc = re.search(r'leader_class\s*=\s*\{([^}]*)\}', body)
        classes = lc.group(1).split() if lc else ["all"]
        if want_class not in classes and classes != ["all"]:
            continue
        ty = re.search(r'leader_trait_type\s*=\s*(\w+)', body)
        kt = ty.group(1) if ty else "basic"

        # 抽效果
        eff = []
        for b in GOOD_BLOCKS:
            mm = re.search(r'(?ms)^\s*' + b + r'\s*=\s*\{(.*?)\n\s*\}', body)
            if mm:
                vals = re.findall(r'([a-z_0-9]+)\s*=\s*([-0-9.]+)', mm.group(1))
                for a, c in vals:
                    if a not in ("factor", "mult", "exists", "owner", "add", "value"):
                        eff.append("%s=%s" % (a, c))
        if eff:
            rows.append((kt, key, name_of(key), eff))

print("=== 纯通用（任何职位都生效）特质 —— 职业 %s 可用，共 %d 个 ===" % (want_class, len(rows)))
print()
order = {"basic": 0, "veteran": 1, "destiny": 2, "subclass": 3, "negative": 4}
for kt, key, nm, eff in sorted(rows, key=lambda x: (order.get(x[0], 9), x[1])):
    print("* [%-8s] %-30s %s" % (kt, key, nm))
    print("             %s" % ", ".join(eff[:8]))
