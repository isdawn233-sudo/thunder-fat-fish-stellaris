"""
audit_traits.py -- 审计本 mod 三形态配装里每个特质的作用域

分类：
    通用     只用 self_modifier / modifier  —— 任何职位都生效
    仅内阁   councilor_modifier            —— 只有在内阁时生效
    仅总督   planet_modifier / sector_modifier —— 只有治理星球/星域时生效
    仅舰队   fleet_modifier / army_modifier —— 只有统率舰队/陆军时生效
"""
import os, re
# 路径由 zlpaths 自动解析（可用环境变量 ZL_MOD / STELLARIS_GAME 覆盖）
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zlpaths import MOD, GAME


# 三形态当前配装
KITS = {
    "行政官": ["zl_leader_trait_administrator", "leader_trait_gifted_2",
               "leader_trait_adventurous_spirit_3", "leader_trait_rift_warped",
               "leader_trait_govenor_caretaker"],
    "指挥官": ["zl_leader_trait_commander", "leader_trait_gifted_2",
               "leader_trait_adventurous_spirit_3", "leader_trait_hive_affinity",
               "leader_trait_ethereal", "leader_trait_great_khan"],
    "科学家": ["zl_leader_trait_scientist", "leader_trait_gifted_2",
               "leader_trait_inspired_surveyor", "leader_trait_guided",
               "leader_trait_adventurous_spirit_3", "leader_trait_xeno_cataloger"],
}


def strip_comments(t):
    return "\n".join(l[:l.find("#")] if "#" in l else l for l in t.splitlines())


# 载入原版全部特质
VAN = {}
for fn in os.listdir(os.path.join(GAME, "common", "traits")):
    if not fn.endswith(".txt") or fn.startswith("000_"):
        continue
    txt = strip_comments(open(os.path.join(GAME, "common", "traits", fn),
                              encoding="utf-8-sig", errors="ignore").read())
    for m in re.finditer(r'(?m)^\s*([a-zA-Z0-9_]+)\s*=\s*\{', txt):
        key = m.group(1)
        if not (key.startswith("leader_trait") or key.startswith("trait_ruler")
                or key.startswith("subclass_")):
            continue
        i = m.end() - 1
        depth = 0
        for j in range(i, len(txt)):
            if txt[j] == '{':
                depth += 1
            elif txt[j] == '}':
                depth -= 1
                if depth == 0:
                    VAN[key] = txt[i + 1:j]
                    break

BLOCKS = {
    "通用": ["self_modifier", "modifier", "triggered_self_modifier", "triggered_modifier"],
    "仅内阁": ["councilor_modifier", "triggered_councilor_modifier"],
    "仅总督": ["planet_modifier", "sector_modifier", "triggered_planet_modifier",
               "triggered_sector_modifier"],
    "仅舰队": ["fleet_modifier", "army_modifier", "triggered_fleet_modifier",
               "triggered_army_modifier"],
    "其他": ["galcom_modifier", "federation_modifier", "background_planet_modifier"],
}

MODTRAITS = {}
mt = open(os.path.join(MOD, "common", "traits", "zl_leader_traits.txt"),
          encoding="utf-8-sig", errors="ignore").read()
for m in re.finditer(r'(?m)^\s*(zl_leader_trait_\w+)\s*=\s*\{', mt):
    key = m.group(1)
    i = m.end() - 1
    depth = 0
    for j in range(i, len(mt)):
        if mt[j] == '{':
            depth += 1
        elif mt[j] == '}':
            depth -= 1
            if depth == 0:
                MODTRAITS[key] = mt[i + 1:j]
                break

seen = {}
for form, keys in KITS.items():
    print("=" * 78)
    print("形态：%s" % form)
    print("=" * 78)
    for k in keys:
        body = VAN.get(k) or MODTRAITS.get(k)
        if body is None:
            print("  %-52s  !! 未找到" % k)
            continue
        cats = []
        for cat, blks in BLOCKS.items():
            for b in blks:
                if re.search(r'(?m)^\s*' + b + r'\s*=\s*\{', body):
                    cats.append(cat)
                    break
        cats = sorted(set(cats))
        src = "原版" if k in VAN else "本mod"
        print("  %-52s [%s]  %s" % (k, src, "/".join(cats) or "无修正"))
        if k not in seen:
            seen[k] = cats

print()
print("=" * 78)
print("汇总：仅内阁 / 仅总督 的特质（要替换掉的）")
print("=" * 78)
for k, cats in sorted(seen.items(), key=lambda x: x[1]):
    if "仅内阁" in cats or "仅总督" in cats:
        print("  %-52s %s" % (k, "/".join(cats)))
