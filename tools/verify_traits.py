"""校验本 mod 引用的所有【原版特质名】是否真实存在，并报告其类型。"""
import os, re, sys

GAME = r"/path/to/Steam/steamapps/common/Stellaris"
MOD = r"/path/to/Documents/Paradox Interactive/Stellaris/mod/zl_unique_administrator"


def strip_comments(t):
    return "\n".join(l[:l.find("#")] if "#" in l else l for l in t.splitlines())


def is_trait_key(key):
    """判断一个 key 是不是领袖特质名。

    注意本 mod 的特质是 zl_leader_trait_*（带 zl_ 前缀），
    所以必须同时接受 zl_leader_trait 开头。
    """
    return (key.startswith("leader_trait")
            or key.startswith("zl_leader_trait")
            or key.startswith("trait_ruler")
            or key.startswith("subclass_"))


def load_traits(path, skip_doc=True):
    """从 traits 目录载入 key -> (type, classes)。

    只有领袖特质才算；其它块（inline_script / leader_class /
    self_modifier 等）跳过。
    """
    out = {}
    if not os.path.isdir(path):
        return out
    for fn in os.listdir(path):
        if not fn.endswith(".txt"):
            continue
        if skip_doc and fn.startswith("000_"):
            continue
        txt = strip_comments(open(os.path.join(path, fn),
                                  encoding="utf-8-sig", errors="ignore").read())
        for m in re.finditer(r'(?m)^\s*([a-zA-Z0-9_]+)\s*=\s*\{', txt):
            key = m.group(1)
            if not is_trait_key(key):
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
                        out[key] = (ty.group(1) if ty else "basic",
                                    lc.group(1).split() if lc else ["all"])
                        break
    return out


# 1) 原版全部特质
VAN = load_traits(os.path.join(GAME, "common", "traits"))

# 1b) 本 mod 自己的特质（放在同一个表里，槽位统计才有意义）
MYTRAITS = load_traits(os.path.join(MOD, "common", "traits"))
VAN.update(MYTRAITS)

# 2) 本 mod 引用的原版特质名（脚本、事件、特质文件里的引用）
#    跳过的两类：
#      · 字段名：它们以 leader_trait_ 开头但不是特质
#      · tools/ 下的参考数据：modifier_names.txt 里全是 modifier 名，
#        里面恰好有 leader_trait_selection_options_add 这种
#        以 leader_trait_ 开头的 modifier，扫进来会误报
FIELD_NAMES = {
    "leader_trait_type",
    "leader_trait_rarity",
    "leader_trait_tier",
    "leader_trait_selection_options_add",
    "leader_trait_selection_options",
}

used = {}
for root, _, files in os.walk(MOD):
    # tools/ 只放脚本和参考数据，不是 mod 内容，跳过
    if os.sep + "tools" in root + os.sep:
        continue
    for fn in files:
        if not fn.endswith(".txt"):
            continue
        p = os.path.join(root, fn)
        raw = open(p, encoding="utf-8-sig", errors="ignore").read()
        # 先去掉注释行，否则注释里举例写的特质名会被误当成真实引用
        t = strip_comments(raw)
        for m in re.finditer(r'\b(leader_trait_[a-z_0-9]+|trait_ruler_[a-z_0-9]+|subclass_[a-z_0-9]+)\b', t):
            k = m.group(1)
            if k.startswith("zl_"):
                continue          # 本 mod 自己的
            if k in FIELD_NAMES:
                continue          # 字段名 / modifier 名，不是特质名
            used.setdefault(k, set()).add(fn)

print("原版特质库: %d 个" % (len(VAN) - len(MYTRAITS)))
print("本 mod 特质: %d 个" % len(MYTRAITS))
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
    cnt = {"basic": 0, "veteran": 0, "destiny": 0, "subclass": 0, "negative": 0}
    detail = []
    for k in keys:
        if k in VAN:
            ty = VAN[k][0]
            cnt[ty] = cnt.get(ty, 0) + 1
            src = "mod" if k in MYTRAITS else "原版"
            detail.append("%-52s [%-8s %s]" % (k, ty, src))
        else:
            detail.append("%-52s [!! 不存在]" % k)
    print("  %s:" % form)
    for d in detail:
        print("     " + d)
    # 说明：这里的槽位上限只约束"升级时还能选什么"。
    # 通过 add_trait 显式给特质时可以超上限 —— 原版自己也这么做，
    # 例如 shroud_events.txt 的 Chosen 领袖是 8 级 8 特质，其中 basic=3（超 2）。
    # 真正要保证的是【特质总数 == 等级】，否则 UI 会提示「请选择特质」。
    over = []
    if cnt["basic"] > 2:
        over.append("basic %d>2" % cnt["basic"])
    if cnt["veteran"] > 3:
        over.append("veteran %d>3" % cnt["veteran"])
    if cnt["destiny"] > 1:
        over.append("destiny %d>1" % cnt["destiny"])
    print("     小计 basic=%d/2 veteran=%d/3 destiny=%d/1 subclass=%d  共 %d 个"
          % (cnt["basic"], cnt["veteran"], cnt["destiny"], cnt["subclass"], len(keys)))
    if over:
        print("     注: 超出常规槽位（%s）—— 显式给特质时属正常，"
              "原版 Chosen 领袖同样超限" % ", ".join(over))
    print("     关键: 特质总数 %d 个，对应 %s"
          % (len(keys), "10 级所需，OK" if len(keys) == 10 else "!! 与 10 级不匹配"))

# 4) 检查事件里的初始 traits 块
ev = open(os.path.join(MOD, "events", "zl_unique_administrator_events.txt"),
          encoding="utf-8-sig", errors="ignore").read()
m = re.search(r'(?ms)traits\s*=\s*\{(.*?)\n\s*\}', ev)
if m:
    ks = re.findall(r'\d+\s*=\s*(\w+)', m.group(1))
    print()
    print("=== 事件里初始化的 traits 块（%d 个）===" % len(ks))
    for k in ks:
        ty = VAN.get(k, ("!! 不存在",))[0]
        print("   %-52s [%s]" % (k, ty))

sys.exit(1 if missing else 0)
