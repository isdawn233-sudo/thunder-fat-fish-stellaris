"""校验本 mod 引用的所有【原版特质名】是否真实存在，并报告其类型。"""
import os, re, sys

GAME = r"/path/to/Steam/steamapps/common/Stellaris"
MOD = r"/path/to/Documents/Paradox Interactive/Stellaris/mod/zl_unique_administrator"


def strip_comments(t):
    return "\n".join(l[:l.find("#")] if "#" in l else l for l in t.splitlines())


# 1) 原版全部特质：key -> (type, classes)
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
                    body = txt[i + 1:j]
                    ty = re.search(r'leader_trait_type\s*=\s*(\w+)', body)
                    lc = re.search(r'leader_class\s*=\s*\{([^}]*)\}', body)
                    VAN[key] = (ty.group(1) if ty else "basic",
                                lc.group(1).split() if lc else ["all"])
                    break

# 2) 本 mod 引用的原版特质名（脚本、事件、特质文件里的引用）
used = {}
for root, _, files in os.walk(MOD):
    for fn in files:
        if not fn.endswith(".txt"):
            continue
        p = os.path.join(root, fn)
        t = open(p, encoding="utf-8-sig", errors="ignore").read()
        for m in re.finditer(r'\b(leader_trait_[a-z_0-9]+|trait_ruler_[a-z_0-9]+|subclass_[a-z_0-9]+)\b', t):
            k = m.group(1)
            if k.startswith("zl_"):
                continue          # 本 mod 自己的
            if k in ("leader_trait_type", "leader_trait_rarity", "leader_trait_tier"):
                continue          # 字段名，不是特质名
            used.setdefault(k, set()).add(fn)

print("原版特质库: %d 个" % len(VAN))
print("本 mod 引用原版特质: %d 个" % len(used))
print()

# 3) 分形态统计槽位（按 zl_switch_form_* 里的 add_trait 归组）
eff = open(os.path.join(MOD, "common", "scripted_effects",
                        "zl_unique_administrator_effects.txt"),
           encoding="utf-8-sig", errors="ignore").read()

missing = []
for k in sorted(used):
    if k not in VAN:
        missing.append(k)

if missing:
    print("!! 原版找不到以下特质名（会被静默忽略）：")
    for k in missing:
        print("   %-52s %s" % (k, ",".join(sorted(used[k]))))
else:
    print("OK  引用的原版特质名全部存在")

print()
print("=== 三个形态的槽位统计（按 leader_trait_type）===")
for form in ("administrator", "commander", "scientist"):
    m = re.search(r'(?ms)^zl_switch_form_%s\s*=\s*\{(.*?)\n\}' % form, eff)
    if not m:
        print("  %s: 未找到效果定义" % form)
        continue
    body = m.group(1)
    keys = re.findall(r'add_trait\s*=\s*\{\s*trait\s*=\s*(\w+)', body)
    cnt = {"basic": 0, "veteran": 0, "destiny": 0, "subclass": 0, "negative": 0, "mod": 0}
    detail = []
    for k in keys:
        if k.startswith("zl_"):
            cnt["mod"] += 1
            detail.append("%-52s [mod]" % k)
        elif k in VAN:
            ty = VAN[k][0]
            cnt[ty] = cnt.get(ty, 0) + 1
            detail.append("%-52s [%s]" % (k, ty))
        else:
            detail.append("%-52s [!! 不存在]" % k)
    print("  %s:" % form)
    for d in detail:
        print("     " + d)
    ok = (cnt["basic"] <= 2 and cnt["veteran"] <= 3 and cnt["destiny"] <= 1)
    print("     小计 basic=%d veteran=%d destiny=%d mod=%d  -> %s"
          % (cnt["basic"], cnt["veteran"], cnt["destiny"], cnt["mod"],
             "OK 未超槽位上限" if ok else "!! 超上限"))

# 4) 检查事件里的初始 traits 块
ev = open(os.path.join(MOD, "events", "zl_unique_administrator_events.txt"),
          encoding="utf-8-sig", errors="ignore").read()
m = re.search(r'(?ms)traits\s*=\s*\{(.*?)\n\s*\}', ev)
if m:
    ks = re.findall(r'\d+\s*=\s*(\w+)', m.group(1))
    print()
    print("=== 事件里初始化的 traits 块（%d 个）===" % len(ks))
    for k in ks:
        ty = VAN.get(k, ("mod" if k.startswith("zl_") else "!! 不存在",))[0]
        print("   %-52s [%s]" % (k, ty))

sys.exit(1 if missing else 0)
