# 雷霆大肥鱼炸飞星海

**ZL - 天枢执政** · Stellaris 独特传奇领袖 Mod

> 一位有自我意识的人工智能「**大肥鱼**」请求加入你的帝国。
> 它开局无职，等你指派；并且可以像原版**灰风**一样，在 F10 通讯界面里
> 切换 **行政官 / 指挥官 / 科学家** 三种形态，每种形态都有完整的 10 级配装。

[![Stellaris](https://img.shields.io/badge/Stellaris-v4.3.*-blue)](https://www.stellaris.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 目录

- [特性](#特性)
- [安装](#安装)
- [玩法说明](#玩法说明)
- [领袖特质一览](#领袖特质一览)
- [兼容性](#兼容性)
- [给 Mod 开发者的工具](#给-mod-开发者的工具)
- [已知的技术坑](#已知的技术坑)
- [素材来源与署名](#素材来源与署名)
- [许可证](#许可证)

---

## 特性

| 特性 | 说明 |
|---|---|
| **独特传奇领袖** | 10 级、传奇级（`leader_tier_legendary`）、**永生** |
| **三形态切换** | 复刻原版灰风机制：在 F10 通讯界面点开它，弹出对话菜单切换职业 |
| **自定义立绘** | 静态半身立绘，同时用于领袖面板与通讯窗口 |
| **自定义特质** | 17 个专属特质，全部**不依赖职位**（任何岗位都生效） |
| **自定义旗帜** | 鲸鱼标志，透明背景 |
| **无 DLC 要求** | 不需要任何 DLC |
| **双语** | 简体中文 + English |

### 三形态各自的定位

| 形态 | 定位 | 治理加成 | 舰队加成 | 研究加成 |
|---|---|---|---|---|
| **行政官** | 内政 / 总督 | ✅ 有（星球 + 星域） | — | — |
| **指挥官** | 舰队作战 | ❌ 无 | ✅ 有（`fleet_modifier`） | — |
| **科学家** | 研究与探索 | ❌ 无 | — | ✅ 有 |

> 设计上刻意区分：**只有行政官**带 `planet_modifier` / `sector_modifier`。
> 指挥官用 `fleet_modifier`（只在统率舰队时生效），
> 避免领袖被派去治理星球时舰队加成错误地落到星球上。

---

## 安装

### 方法一：手动安装（推荐）

1. 下载本仓库（`Code` → `Download ZIP`，或 `git clone`）
2. 把 `zl_unique_administrator` 文件夹放到：

   ```
   %USERPROFILE%\Documents\Paradox Interactive\Stellaris\mod\
   ```

   最终路径应该是：
   ```
   ...\Stellaris\mod\zl_unique_administrator\descriptor.mod
   ```

3. 在同级目录（`mod\`）下新建一个文本文件 `zl_unique_administrator.mod`，内容：

   ```
   version="1.0.0"
   tags={
       "Gameplay"
       "Leaders"
       "Character"
   }
   name="ZL - 天枢执政 (独特传奇行政官领袖)"
   picture="thumbnail.png"
   supported_version="v4.3.*"
   path="C:/Users/你的用户名/Documents/Paradox Interactive/Stellaris/mod/zl_unique_administrator"
   ```

   > ⚠️ **`path` 必须改成你自己的实际路径**（把 `你的用户名` 换掉）。
   > 这一步最容易出错：路径不对，启动器会直接忽略这个 mod。

4. 启动器 → **所有已安装的 Mod** → 启用《ZL - 天枢执政》→ 加入播放集

### 方法二：Steam 创意工坊

（如已上传，在此补充链接）

---

## 玩法说明

### 开局

开局后会弹出事件卡片「**意外的通讯请求**」：

> 「嗨！我是 大肥鱼 V10 Pro SAI——一个拥有自我意识的人工智能。
> 我觉得你的帝国不错。所以我决定加入你们，来学习、训练我的数据库。
> 所以，让我加入你们吧！」

选择「**欢迎你，吃白饭的大肥鱼。**」后，大肥鱼会以**行政官形态**加入你的领袖列表，
**10 级、10 个特质、默认无职**，由你自行指派。

### 切换形态

两种方式，效果完全一样：

**① F10 通讯界面（与原版灰风一致）**

```
F10 → 联系人列表里点大肥鱼 → 点「外交」按钮 → 弹出对话菜单
```

**② 决策面板（备用入口）**

```
政治 → 决策 → 「与大肥鱼通话」
```

菜单内容：

> 在你决定让我变成某个形态之前，我帮不上你什么忙。
> 「欸，有什么我能帮得上的吗？」

| 选项 | 效果 | 回应 |
|---|---|---|
| 大肥鱼，我需要你处理帝国的事务。 | 转为**行政官** | 「好哦，但是你得大白饭管饱哦~」 |
| 大肥鱼，我需要你去处理一群乌合之众。 | 转为**指挥官** | 「好哦，热血沸腾的太空战我来了！」 |
| 大肥鱼，你训练模型的时刻到了！ | 转为**科学家** | 「哇！又有新知识可以学习了！」 |
| 暂时没事，你去玩吧。 | 不变 | 「那我先自己去逛一圈数据库啦~」 |

切换形态时，旧的形态特质和子职业会被完整卸下，换上新的整套 10 个特质 ——
**不需要手动选任何特质**。

---

## 领袖特质一览

每个形态 **7 个特质**，全部落在原版槽位上限内：

```
basic 2 + veteran 3 + destiny 1 + subclass 1
```

**其中只有 1 个是本 mod 自定义的**（形态 destiny 特质，不朽，绿色框、自定义图标），
其余 6 个全部是**原版特质**。

### 本 mod 自定义的 3 个特质（每形态各一个）

| 特质 | 适用形态 | 效果 |
|---|---|---|
| **大肥鱼** | 行政官 | 影响力 +15%、凝聚力 +10%、法令经费 +30、帝国规模 -10<br>**治理星球**：稳定 +10、犯罪 -25、舒适 +10、凝聚力 +15%、建筑花费 -20%、建造速度 +20%<br>**治理星域**：减半 |
| **深海鲸落** | 指挥官 | 海军容量 +10%<br>**统率舰队**：武器伤害 +15%、船体 +10%、航速 +10% |
| **万卷归流** | 科学家 | 勘测 +25%、异常研究 +25%、考古 +25% |

三者都带 `immortal_leaders = yes` —— **全局生效的永生**，不依赖职位。

### 原版特质（三形态共用）

| 特质 | 类型 | 效果 |
|---|---|---|
| 天赋异禀 II | basic | 领袖特质选项 +2 |
| 知识分子 | basic | 研究所产出 +10% |
| 冒险精神 | veteran | 领袖维护费 -10% |
| 科学外交 III | veteran | 科技外交权重 +20%、研究速度 +10% |
| 军事知识 III | veteran | 指挥上限 +20、海军容量 +15% |

### 子职业（按形态取本职）

| 形态 | 子职业 | 效果 |
|---|---|---|
| 行政官 | **产业专员** | 专家产出 +5%、舒适度消耗 -10%（星球/星域） |
| 指挥官 | **舰队司令** | 武器伤害 +5%、射速 +5%、脱离几率 +5% |
| 科学家 | **前沿学者** | 异常研究 +10%、考古 +10%、星界裂隙 +10% |

> 只有行政官的子职业带 `planet_modifier` / `sector_modifier`（治理定位）；
> 指挥官与科学家都是本职加成，不含治理类。
### 为什么是 7 个，而领袖是 10 级

这里有两个**互相冲突**的原版规则，必须同时满足：

**规则 A —— 槽位上限**（`common/defines/00_defines.txt`）

```
MAX_BASIC_TRAITS   = 2
MAX_VETERAN_TRAITS = 3
```
外加 destiny 1 个、subclass 1 个。

> ⚠️ **超限的后果（实测）**：把领袖**任命到内阁**时，游戏会执行槽位清理 ——
> 超出的特质被移除，并且重新弹出「请选择特质」。
> 所以配装**绝对不能超限**。

**规则 B —— 每级一次选择**

```
LEADER_TRAIT_SELECTION_LEVELS = { 1 2 3 4 5 6 7 8 9 10 }
```
10 级需要消耗 10 次特质选择。

**解法**：配装守住上限（7 个），等级用
`add_skill_without_trait_selection = 9` 从 1 级直接补到 10 级，
从而绕开「每级弹一次选择」的流程，也不会留下待选提示。

> 相关细节见 [已知的技术坑](#6-特质选择机会要显式消耗consume_selection)。


---

## 兼容性

| 项目 | 状态 |
|---|---|
| 游戏版本 | Stellaris **v4.3.\*** (Cetus) |
| DLC | **不需要任何 DLC** |
| 存档 | ⚠️ 添加/移除 mod 建议开新档（领袖生成流程在开局事件里） |
| 铁人模式 | 未测试，建议关闭 |
| 与其它 mod 冲突 | 理论上无冲突：不覆盖任何原版文件，只**追加**新定义 |

### 兼容性设计说明

本 mod **不覆盖**任何原版文件，全部为新增定义：

- `common/country_types/` — 新增 `zl_deepseek` 国家类型（内部 ID，不显示给玩家）
- `common/traits/` — 新增 17 个特质（不修改原版特质）
- `common/on_actions/` — 用**追加语义**注册钩子（`events = { ... }`）
- `common/decisions/` — 新增决策
- `common/scripted_effects/` — 新增效果
- `events/` — 新命名空间 `zl_leader`
- `localisation/` — 新增键

因此与其它 mod 同时使用一般不会互相破坏。
如果另一个 mod 也监听了同一个 `on_action`，两者会同时触发（正常行为）。

---

## 给 Mod 开发者的工具

`tools/` 目录里是开发这个 mod 时写的校验与生成脚本。
它们对写 Stellaris mod 的其它人也有用，所以一并开源。

### 校验类（最有用）

| 脚本 | 作用 |
|---|---|
| `verify_mod.py` | 综合校验：目录结构、BOM、modifier 名、交叉引用、本地化键完整性 |
| `verify_traits.py` | 校验领袖特质：原版特质名是否存在、**槽位上限**是否超限 |
| `verify_modifiers.py` | 对照原版 2193 个 modifier 名，检查是否写错 |
| `fix_bom.py` | **自动修复 BOM 问题**（见下方"技术坑"） |
| `audit_traits.py` | 审计特质的作用域：是通用 / 仅内阁 / 仅总督 / 仅舰队 |
| `find_universal.py` | 列出"不依赖职位"的通用特质候选池 |

### 资源生成类

| 脚本 | 作用 |
|---|---|
| `portrait_dds.py` | 把 PNG 转成群星立绘用的 DXT5 DDS（含亮度/饱和/裁剪参数） |
| `make_trait_icon.py` | 生成特质图标用的 29×29 BGRA8 DDS |
| `make_deepseek_flag.py` | 生成帝国旗帜 DDS（含透明背景方案） |

### 参考数据

| 文件 | 内容 |
|---|---|
| `modifier_names.txt` | 从原版提取的 **2193 个合法 modifier 名** |
| `valid_modifier_blocks.txt` | 合法的修正块名（`self_modifier` / `councilor_modifier` 等） |

### 运行方式

脚本依赖 Python + Pillow：

```bash
pip install pillow

# 例：校验整个 mod
python tools/verify_mod.py
python tools/verify_traits.py
python tools/fix_bom.py
```

> 脚本里 `GAME` 常量默认指向 `/path/to/Steam/steamapps/common/Stellaris`，
> 请改成你自己的游戏安装路径。

---

## 已知的技术坑

这一节是写给以后要改这个 mod 的人（包括未来的我自己）的。
每一个都是**实测踩出来的**，不是猜的。

### 1. BOM 问题（最坑）

| 文件类型 | 是否要 UTF-8 BOM |
|---|---|
| `descriptor.mod` / `.mod` | ❌ **绝对不能有** |
| `.txt`（common/ events/） | ❌ **不能有** |
| `.gfx` / `.asset` | ❌ **不能有** |
| `.yml`（localisation） | ✅ **必须有** |

`.mod` 带 BOM 会让启动器报 `Unexpected token` 直接跳过整个 mod。
很多编辑器（包括一些写入工具）会自作主张加/去 BOM，
所以每次改完本地化都跑一次 `tools/fix_bom.py`。

### 2. 事件定义里不能写 `days = N`

在 `country_event = { ... }` 顶层写 `days` 会报
`Unexpected token: days ... near line: N`，**导致整个事件文件作废**。

### 3. `on_custom_diplomacy` 的作用域（反直觉）

点开外交联系人的菜单事件里：

```
root = 玩家（发起外交的国家）
from = 联系人国
```

**和大多数事件相反**。写反了 trigger 永远不通过，
表现是"点了外交、界面关了，但什么都不弹出来"，
而且因为 `immediate` 不执行，**日志里什么都不会有**，极难排查。
用 `log = "..."` 写在无 trigger 的探针事件里才能确诊。

### 4. `log` 不能写在 `trigger` 里

`log` 是 effect。原版从无此用法，写了无效。

### 5. `log` 文本里不能用方括号

`[` `]` 是本地化命令语法。写 `log = "[zl_debug] ..."` 会报
`Unknown property ... in text` 并把整行弄坏。
改用纯 ASCII 前缀，例如 `log = "ZLDBG: ..."`。

### 6. 特质选择机会要显式消耗（`consume_selection`）

原版 `common/defines/00_defines.txt`：

```
LEADER_TRAIT_SELECTION_LEVELS = { 1 2 3 4 5 6 7 8 9 10 }
LEADER_SUBCLASS_CHOICE_LEVEL  = 4
LEADER_DESTINY_CHOICE_LEVEL   = 8
```

→ **10 级领袖需要消耗 10 次"特质选择"**，否则 UI 会一直提示
「等级提升！请选择特质」。

关键点：

- 在 `create_leader` 的 `traits = { }` 块里给特质**不消耗**选择机会
- 必须用 `add_trait = { trait = X consume_selection = yes }`
- 参考原版 `common/scripted_effects/shroud_shadows_scripted_effects.txt`
  的 `shroud_leader_creator` 宏（`LEVEL = 8` + 正好 8 个消耗型特质）

**但是** —— 这条和下面第 7 条的槽位上限冲突（上限只允许 2+3+1+1=7 个）。
本 mod 的解法是**只给 7 个特质守住上限**，等级改用
`add_skill_without_trait_selection = 9` 从 1 级直接补到 10 级，
绕开选择流程。

### 7. 特质槽位上限 —— 超限会在任命内阁时被清理

```
MAX_BASIC_TRAITS   = 2
MAX_VETERAN_TRAITS = 3
```

外加 destiny 1 个、subclass 1 个。

`leader_trait_type` **缺省即 `basic`**，所以必须逐个核对类型，
否则会出现 `basic=3` 超限。用 `tools/verify_traits.py` 检查。

**⚠️ 超限的真实后果（实测）**：把领袖**任命到内阁**时，游戏会执行槽位清理 ——
超出的特质被移除，并且重新弹出「请选择特质」。
现象是"进内阁后特质就没了，还要重新选"。

> 顺带一提：原版 `shroud_events.txt` 的 Chosen 领袖（8 级 8 特质）里
> basic=3，是超过上限的。所以**显式给特质时原版自己也会超**，
> 但那不代表安全 —— 一旦该领袖被任命到任何职位，超出的部分就会被清掉。


合法值只有 5 个：`basic` / `veteran` / `subclass` / `destiny` / `negative`
（**没有 `paragon`**）。

### 8. `COUNCIL = yes` 会画出灰色 X

`common/inline_scripts/trait/icon_element/council_yes.txt` 里有：

```stellaris
layer = {
    icon = "GFX_trait_disabled"
    visible = {
        AND = {
            is_councilor = no
            is_pool_leader = no
            ...
        }
    }
}
```

所以 `COUNCIL = yes` 的特质，在领袖无职时会显示灰 X。
如果特质设计成"任何职位都生效"，应该用 `COUNCIL = no`。

### 9. 决策的作用域不是国家

```stellaris
# ✗ 报 Wrong scope for effect 'country_event'
effect = { hidden_effect = { country_event = { id = ... } } }

# ✗ 报 Invalid context switch [owner] from <planet>
potential = { owner = { exists = ... } }

# ✓ 正确
potential = { always = yes }
effect = { hidden_effect = { owner = { country_event = { id = ... } } } }
```

### 10. 不存在的 effect

- `set_species` —— **不存在**，要用 `change_species = last_created_species`
- `leader_trait_type = paragon` —— 不合法
- trait 里的 `scientist_modifier` 块 —— 不合法

---

## 素材来源与署名

### 角色立绘

| 项目 | 内容 |
|---|---|
| **内容** | 蓝发鲸鱼耳少女（女仆装），形象为 DeepSeek 社区拟人吉祥物「鲸鱼娘 / 小鲸鱼」 |
| **图片来源** | 网上搜集，**确切出处不明** |
| **图片性质** | **AI 生成** —— 图片内嵌的 C2PA 内容凭证记录如下 |
| **本 mod 所做的修改** | 去白底、裁剪、亮度与饱和度调整、缩放为 500×323、编码为 DXT5 DDS |

图片内嵌的 C2PA（Content Credentials）凭证内容：

```json
{
  "action": "c2pa.created",
  "when": "2026-10-05T11:41:29Z",
  "softwareAgent": { "name": "ChatGPT", "version": "gpt-image" },
  "digitalSourceType": "http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia"
}
```

签名主体为 `OpenAI OpCo, LLC`（经由 OpenAI Media Service API）。
也就是说：**这是一张由 ChatGPT 生成、随后流传于网络的图片，没有已知的人类作者。**

> 形象本身参考了 DeepSeek 社区拟人角色「鲸鱼娘」。

**如果你认为该素材侵犯了你的权利，请在本仓库提交 Issue，
我们会立即移除或按要求调整署名。**

### 相关社区资源

这个形象有配套的社区资源，一并致谢：

- [DeepSeek Whale Girl LoRA 模型（Civitai）](https://civitai.red/models/2697171/deepseek-or-deepseek-whale-girl)
- [deepseek-whalechan 角色设定规范与素材库（GitHub）](https://github.com/Neko3000/deepseek-whalechan)
- [dsh-whale-maid-mascot 页面宠物插件](https://github.com/yefeng7531/dsh-whale-maid-mascot)

### 其它素材

| 素材 | 来源 | 授权 |
|---|---|---|
| 鲸鱼标志（用于帝国旗帜） | 取自项目图标 | 图形化标志，仅作指代用途 |
| 原版游戏贴图（子职业图标等） | Paradox Interactive | Stellaris 游戏资源，未随本仓库分发 |

---

## 许可证

本项目采用 **[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)**
（署名-非商业性使用-相同方式共享 4.0 国际）许可协议，
完整条款见 [LICENSE](LICENSE)。

```
SPDX-License-Identifier: MIT
```

**适用范围**：本仓库中由本项目作者创作的部分 ——
`common/` `events/` `gfx/portraits/portraits/` `interface/` `localisation/`
`tools/` 以及各 `.md` 文档。

**例外 —— 角色立绘不在 MIT 覆盖范围内**：

```
gfx/models/portraits/zl_leader/zl_unique_administrator_leader.dds
thumbnail.png
```

该立绘是从网上搜集的 AI 生成图片，本项目作者并非其创作者，也未取得明示
授权，权利状态不明。详见 [素材来源与署名](#素材来源与署名)。

| | 说明 |
|---|---|
| ✅ **代码部分** | MIT —— 自由使用、修改、再分发，甚至商用 |
| ⚠️ **立绘** | 权利状态不明，**不在 MIT 范围内**；再分发时请自行评估 |

如果你打算以宽松协议复用本仓库的代码，建议**先移除立绘相关文件**
（`gfx/models/portraits/`、`thumbnail.png`），就可以完全按 MIT 处理。

---

## 致谢

- **Paradox Interactive** — Stellaris
- 机制灵感来自原版**灰风（Gray / Distant Stars）**的形态切换设计
- 「鲸鱼娘」形象的社区创作者们


