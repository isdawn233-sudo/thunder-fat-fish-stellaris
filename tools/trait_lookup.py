"""按"效果关键词"反查特质 key，方便精确挑选各职业的顶级特质。"""
import os, re, sys

GAME = r"/path/to/Steam/steamapps/common/Stellaris"
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


def blocks(txt):
    for m in re.finditer(r'(?m)^\s*([a-zA-Z0-9_]+)\s*=\s*\{', txt):
        key = m.group(1)
        i = m.end() - 1
        depth = 0
        for j in range(i, len(txt)):
            if txt[j] == '{':
                depth += 1
            elif txt[j] == '}':
                depth -= 1
                if depth == 0:
                    yield key, txt[i + 1:j]
                    break


def field(body, name):
    m = re.search(r'(?m)^\s*' + name + r'\s*=\s*\{', body)
    if m:
        i = m.end() - 1
        depth = 0
        for j in range(i, len(body)):
            if body[j] == '{':
                depth += 1
            elif body[j] == '}':
                depth -= 1
                if depth == 0:
                    return body[i + 1:j].strip()
    m = re.search(r'(?m)^\s*' + name + r'\s*=\s*([^\n{]+)', body)
    return m.group(1).strip().strip('"') if m else None


# 载入全部领袖特质
ALL = {}
for fn in os.listdir(os.path.join(GAME, "common", "traits")):
    if not fn.endswith(".txt") or fn.startswith("000_"):
        continue
    txt = strip_comments(open(os.path.join(GAME, "common", "traits", fn),
                              encoding="utf-8-sig", errors="ignore").read())
    for key, body in blocks(txt):
        if not (key.startswith("leader_trait") or key.startswith("trait_ruler")
                or key.startswith("subclass_")):
            continue
        ALL[key] = body

want_class = sys.argv[1] if len(sys.argv) > 1 else "commander"
KEYS = sys.argv[2:] if len(sys.argv) > 2 else []

if KEYS:
    for k in KEYS:
        b = ALL.get(k)
        print("=" * 76)
        if not b:
            print("%s  !! 未找到" % k)
            continue
        print("%s   (%s)" % (k, name_of(k)))
        print("   type=%-10s class=%s" % (
            (field(b, "leader_trait_type") or "basic").split()[0],
            (field(b, "leader_class") or "all").strip()))
        for f in ("self_modifier", "fleet_modifier", "army_modifier",
                  "councilor_modifier", "scientist_modifier", "planet_modifier",
                  "triggered_fleet_modifier", "triggered_councilor_modifier"):
            v = field(b, f)
            if v:
                vals = re.findall(r'([a-z_0-9]+)\s*=\s*([-0-9.]+)', v)
                if vals:
                    print("   %-26s %s" % (f, ", ".join("%s=%s" % x for x in vals)))
    sys.exit(0)

# 无参数：按类列出 veteran 里"效果最强"的（数值总和排序）
rows = []
for key, body in ALL.items():
    kt = (field(body, "leader_trait_type") or "basic").split()[0]
    lc = (field(body, "leader_class") or "all").strip()
    if want_class not in lc and lc != "all":
        continue
    eff = []
    score = 0.0
    for f in ("fleet_modifier", "army_modifier", "councilor_modifier",
              "scientist_modifier", "self_modifier", "modifier"):
        v = field(body, f)
        if not v:
            continue
        for m in re.finditer(r'([a-z_0-9]+)\s*=\s*([-0-9.]+)', v):
            name, val = m.group(1), float(m.group(2))
            if name in ("factor", "mult", "exists", "owner", "add"):
                continue
            score += abs(val)
            eff.append("%s:%s=%s" % (f[:4], name, val))
    if eff:
        rows.append((score, kt, key, name_of(key), eff))

rows.sort(reverse=True)
print("=== %s 强特质排行（按修正数值总和）===" % want_class)
for score, kt, key, nm, eff in rows[:30]:
    print("* [%s] %-26s %s" % (kt[:4], key, nm))
    print("      score=%.2f  %s" % (score, ", ".join(eff[:8])))
