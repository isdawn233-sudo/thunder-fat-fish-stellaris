"""
verify_mod.py -- 本 mod 的完整静态校验
    1. 括号平衡 / BOM 规则（.txt/.gfx/.mod 不能有 BOM；.yml 必须有）
    2. modifier 名是否在原版存在
    3. 事件 / 特质 / 效果 / country_type / on_action 的交叉引用
    4. 本地化键是否齐全
"""
import os, re, struct, sys
# 路径由 zlpaths 自动解析（可用环境变量 ZL_MOD / STELLARIS_GAME 覆盖）
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zlpaths import MOD, GAME


fails = []
warns = []


def read(p):
    return open(p, encoding="utf-8-sig", errors="ignore").read()


# ---------------------------------------------------------------- 1) 结构
print("=" * 78)
print("1) 括号平衡 / BOM")
print("=" * 78)
for root, _, files in os.walk(MOD):
    for fn in files:
        p = os.path.join(root, fn)
        rel = p.replace(MOD + "\\", "")
        if fn.endswith((".txt", ".gfx", ".mod", ".asset")):
            t = read(p)
            o, c = t.count("{"), t.count("}")
            b = open(p, "rb").read()
            bom = b[:3] == b"\xef\xbb\xbf"
            st = "OK" if (o == c and not bom) else "FAIL"
            if st == "FAIL":
                fails.append("%s: 括号 %d/%d BOM=%s" % (rel, o, c, bom))
            print("  %-4s %-62s {%d }%d BOM=%s" % (st, rel, o, c, bom))
        elif fn.endswith(".yml"):
            b = open(p, "rb").read()
            bom = b[:3] == b"\xef\xbb\xbf"
            if not bom:
                fails.append("%s: 本地化必须有 BOM" % rel)
            # 引号成对
            bad = 0
            for line in read(p).splitlines():
                if re.match(r'^\s*[A-Za-z0-9_.\-]+:\d*\s+"', line):
                    if line.count('"') % 2 != 0:
                        bad += 1
                        fails.append("%s: 引号不成对 -> %s" % (rel, line[:70]))
            print("  %-4s %-62s BOM=%s 引号异常=%d" % ("OK" if bom and not bad else "FAIL", rel, bom, bad))

# ---------------------------------------------------------------- 2) modifier
print()
print("=" * 78)
print("2) modifier 名对照原版")
print("=" * 78)
valid = set()
for sub in ("common", "events"):
    for root, _, files in os.walk(os.path.join(GAME, sub)):
        for fn in files:
            if not fn.endswith(".txt"):
                continue
            try:
                t = read(os.path.join(root, fn))
            except Exception:
                continue
            for m in re.finditer(r'(?m)^\s*([a-z][a-z_0-9]{3,})\s*=\s*[-0-9]', t):
                valid.add(m.group(1))

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
        t = read(p)
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
                            for mm in re.finditer(r'([a-z][a-z_0-9]{3,})\s*=\s*([-0-9.]+)', t[i+1:j]):
                                used.setdefault(mm.group(1), []).append(fn)
                            break
bad_mods = [k for k in used if k not in valid]
print("  使用 %d 个 modifier 名，原版库 %d 个" % (len(used), len(valid)))
if bad_mods:
    for k in sorted(bad_mods):
        fails.append("无效 modifier: %s (%s)" % (k, ",".join(set(used[k]))))
        print("  FAIL  %s" % k)
else:
    print("  OK    全部有效")

# ---------------------------------------------------------------- 3) 交叉引用
print()
print("=" * 78)
print("3) 交叉引用")
print("=" * 78)
ev_p = os.path.join(MOD, "events", "zl_unique_administrator_events.txt")
tr_p = os.path.join(MOD, "common", "traits", "zl_leader_traits.txt")
ef_p = os.path.join(MOD, "common", "scripted_effects", "zl_unique_administrator_effects.txt")
oa_p = os.path.join(MOD, "common", "on_actions", "zl_unique_administrator_on_actions.txt")
ct_p = os.path.join(MOD, "common", "country_types", "zl_deepseek_country_type.txt")
yg_p = os.path.join(MOD, "gfx", "portraits", "portraits", "zl_unique_administrator_portraits.txt")
gf_p = os.path.join(MOD, "interface", "zl_leader_trait_icons.gfx")

ev, tr, ef, oa, ct = read(ev_p), read(tr_p), read(ef_p), read(oa_p), read(ct_p)

checks = [
    ("events 定义 zl_leader.1/2/99/100",
     all(("id = zl_leader.%s" % n) in ev for n in ("1", "2", "99", "100"))),
    ("events 含 create_country type=zl_deepseek", "type = zl_deepseek" in ev),
    ("events 含 establish_communications", "establish_communications_no_message" in ev),
    ("events 菜单用 diplomatic = yes", "diplomatic = yes" in ev),
    ("events 菜单挂在 on_custom_diplomacy", "on_custom_diplomacy" in oa and "zl_leader.100" in oa),
    ("events 的 3 个形态选项齐全",
     all(("zl_leader.100.%s" % c) in ev for c in "abc")),
    ("traits 定义了 3 个特质",
     all(("\n%s = {" % k) in tr for k in
         ("zl_leader_trait_administrator", "zl_leader_trait_commander", "zl_leader_trait_scientist"))),
    ("traits 无非法 leader_trait_type",
     not re.search(r'leader_trait_type\s*=\s*(paragon|basic_)', tr)),
    ("effects 定义 3 个切换效果 + 清理段",
     all(k in ef for k in ("zl_clear_forms_effect", "zl_switch_form_administrator",
                           "zl_switch_form_commander", "zl_switch_form_scientist"))),
    ("effects 用 change_leader_class", "change_leader_class" in ef),
    ("country_type 名叫 zl_deepseek", re.search(r'(?m)^zl_deepseek\s*=\s*\{', ct) is not None),
    ("country_type 有 show_in_contacts_list", "show_in_contacts_list = yes" in ct),
    ("country_type 有 custom_diplomacy", "custom_diplomacy = yes" in ct),
    ("country_type contact_rule on_action_only", "contact_rule = on_action_only" in ct),
    ("旗帜文件 3 个齐全",
     all(os.path.isfile(os.path.join(MOD, "flags", "special", s, "zl_deepseek.dds"))
         for s in ("", "map", "small"))),
    ("图标 dds + gfx 存在",
     os.path.isfile(os.path.join(MOD, "gfx", "interface", "icons", "traits",
                                 "zl_leader_trait_administrator.dds"))
     and "GFX_leader_trait_zl_administrator" in read(gf_p)),
    ("portrait 定义用 texturefile", "texturefile" in read(yg_p)),
]
for label, ok in checks:
    print("  %-4s %s" % ("OK" if ok else "FAIL", label))
    if not ok:
        fails.append("[交叉引用] " + label)

# ---------------------------------------------------------------- 4) 本地化
print()
print("=" * 78)
print("4) 本地化键完整性")
print("=" * 78)
LOC_REQ = ["NAME_zl_administrator", "NAME_zl_administrator_short",
           "NAME_zl_deepseek_country",
           "zl_administrator_desc", "zl_administrator_catch_phrase",
           "zl_leader.1.name", "zl_leader.1.desc",
           "zl_leader.1.a", "zl_leader.1.a.response",
           "zl_leader.1.b", "zl_leader.1.b.response",
           "zl_leader.100.name", "zl_leader.100.desc",
           "zl_leader.100.a", "zl_leader.100.a.response",
           "zl_leader.100.b", "zl_leader.100.b.response",
           "zl_leader.100.c", "zl_leader.100.c.response",
           "zl_leader.100.d", "zl_leader.100.d.response",
           "decision_zl_deepseek_call", "decision_zl_deepseek_call_desc",
           "decision_zl_deepseek_call_tt"]

# 自动从本 mod 的特质定义推导需要哪些本地化键：
#   每个特质必须有 <key> 与 <key>_desc
#   若 traits 文件里写了 custom_tooltip_with_modifiers = X，则还要 X
# 这样以后增删特质不必再来改这个脚本。
tr_p = os.path.join(MOD, "common", "traits", "zl_leader_traits.txt")
tr_t = read(tr_p)
for m in re.finditer(r'(?m)^\s*(zl_leader_trait_\w+)\s*=\s*\{', tr_t):
    k = m.group(1)
    LOC_REQ.append(k)
    LOC_REQ.append(k + "_desc")
for m in re.finditer(r'custom_tooltip_with_modifiers\s*=\s*(\w+)', tr_t):
    LOC_REQ.append(m.group(1))

# 事件与决策里引用的 title/desc/name/custom_tooltip 键
for rel in (("events", "zl_unique_administrator_events.txt"),
            ("common", "decisions", "zl_unique_administrator_decisions.txt")):
    p = os.path.join(MOD, *rel)
    if not os.path.exists(p):
        continue
    et = read(p)
    for pat in (r'(?:title|desc|name|custom_tooltip)\s*=\s*"([a-zA-Z0-9_.]+)"',
                r'(?:title|desc|name)\s*=\s*(zl_\w+\.\d+\.[a-z]+)'):
        for m in re.finditer(pat, et):
            LOC_REQ.append(m.group(1))

LOC_REQ = sorted(set(LOC_REQ))

for lang in ("simp_chinese", "english"):
    p = os.path.join(MOD, "localisation", lang,
                     "zl_unique_administrator_l_%s.yml" % lang)
    t = read(p)
    missing = [k for k in LOC_REQ if not re.search(r'(?m)^\s*' + re.escape(k) + r':', t)]
    print("  %-4s %-14s 需 %d 键, 缺失 %d 个"
          % ("OK" if not missing else "FAIL", lang, len(LOC_REQ), len(missing)))
    for k in missing:
        fails.append("[本地化 %s] 缺 %s" % (lang, k))
        print("        缺: %s" % k)

# ---------------------------------------------------------------- 汇总
print()
print("=" * 78)
if fails:
    print("校验未通过，共 %d 项：" % len(fails))
    for f in fails:
        print("  - " + f)
    sys.exit(1)
else:
    print("全部校验通过")
