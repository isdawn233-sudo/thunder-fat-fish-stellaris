# 雷霆大肥鱼炸飞星海

**ZL - 天枢执政** · Stellaris 独特传奇领袖 Mod

> 一位有自我意识的人工智能「**大肥鱼**」请求加入你的帝国。
> 它开局无职，等你指派；并且可以像原版**灰风**一样，在 F10 通讯界面里
> 切换 **行政官 / 指挥官 / 科学家** 三种形态，每种形态都有完整的 10 级配装。

[![Stellaris](https://img.shields.io/badge/Stellaris-v4.3.*-blue)](https://www.stellaris.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![AI Generated](https://img.shields.io/badge/AI--Generated-Yes-orange)](#关于-ai-生成)

---

## 关于 AI 生成

> ### 🤖 本项目由 AI 制作
>
> **本 mod 的代码、文档与美术素材均借助 AI 完成。**
>
> | 部分 | 制作方式 |
> |---|---|
> | **代码**（`common/` `events/` `tools/` 等） | 由 **AI 编程助手**（DeepSeek Harness）编写 |
> | **文档**（README、CHANGELOG、本说明等） | 由 **AI** 生成 |
> | **角色立绘** | **AI 生成** —— ChatGPT / `gpt-image`（有内嵌 C2PA 凭证为证，见 [ASSET-NOTICE.md](ASSET-NOTICE.md)） |
> | **角色形象设定** | 参考 DeepSeek 社区拟人角色「鲸鱼娘」 |
>
> ### ⚠️ 请知悉
>
> - 本项目是 **AI 辅助开发**的产物，作者对内容做了设计与审查，但**不保证**
>   不存在错误、遗漏或与官方设定冲突之处
> - AI 生成的内容可能包含**不受著作权保护**或**权利状态不明**的部分
>   （尤其是立绘，详见 [ASSET-NOTICE.md](ASSET-NOTICE.md)）
> - 如果你所在地区或平台对 AI 生成内容有特殊要求，请自行评估后再使用
> - **欢迎指出任何问题** —— 提交 Issue 即可

---

## 目录

- [关于 AI 生成](#关于-ai-生成)
- [特性](#特性)
- [安装](#安装)
- [上传到创意工坊](#上传到创意工坊)
- [玩法说明](#玩法说明)
- [领袖特质一览](#领袖特质一览)
- [兼容性](#兼容性)
- [给 Mod 开发者的工具](#给-mod-开发者的工具)
- [已知的技术坑](#已知的技术坑)
- [素材来源与署名](#素材来源与署名)
- [许可证](#许可证)
- [关于 DeepSeek 的声明](#关于-deepseek-的声明)

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

### 方法一：手动安装

Stellaris 的 mod 采用**「一个文件夹 + 一个同名 .mod 文件」**的结构（详见
[官方 wiki](https://stellaris.paradoxwikis.com/Modding#File_and_folder_structure)）。

1. 下载本仓库（`Code` → `Download ZIP`，或 `git clone`）
2. 把 `zl_unique_administrator` 文件夹整个放到 mod 目录：

   ```
   %USERPROFILE%\Documents\Paradox Interactive\Stellaris\mod\
   ```

   放好后应该是：
   ```
   ...\Stellaris\mod\zl_unique_administrator\descriptor.mod
   ...\Stellaris\mod\zl_unique_administrator\common\...
   ```

3. **在同级目录**（也就是 `mod\` 里面，不是 mod 文件夹里面）新建一个
   文本文件 `zl_unique_administrator.mod`，内容如下：

   ```
   version="1.0.0"
   tags={
       "Gameplay"
       "Leaders"
       "Character"
       "Anime"
   }
   name="ZL - 大肥鱼天枢执政 (独特传奇领袖·三形态)"
   picture="thumbnail.png"
   supported_version="v4.3.*"
   path="C:/Users/YOUR_USERNAME/Documents/Paradox Interactive/Stellaris/mod/zl_unique_administrator"
   ```

   > ⚠️ **只需改 `path` 一行** —— 把 `YOUR_USERNAME` 换成你自己的 Windows 用户名。
   >
   > - 路径必须用**正斜杠 `/`**，不能用反斜杠 `\`
   > - 也可以写成相对路径：`path="mod/zl_unique_administrator"`
   > - 路径写错 → 启动器**直接忽略**这个 mod，且不报错（最难排查的一步）

   > 💡 `descriptor.mod`（在 mod 文件夹**里面**）**不需要** `path=` 一行，
   > 这是官方 wiki 明确说明的。本仓库提供的 `descriptor.mod` 已符合该格式。

   仓库里也附了两个模板可直接改：
   [descriptor.mod.template](descriptor.mod.template) 与
   [zl_unique_administrator.mod.template](zl_unique_administrator.mod.template)

4. 确认编码正确（**这一步最容易忽略**）：

   | 文件 | 编码 |
   |---|---|
   | `.mod` / `.txt` / `.gfx` | UTF-8 **不带** BOM |
   | `.yml`（localisation） | UTF-8 **带** BOM |

   > `.mod` 带 BOM 会让启动器报 `Unexpected token` 并**跳过整个 mod**。

5. 启动器 → **所有已安装的 Mod** → 启用《ZL - 大肥鱼天枢执政》
   → 加入播放集 → 开始游戏

### 方法二：Steam 创意工坊

见 [上传到创意工坊](#上传到创意工坊) 一节。
（如果你是通过工坊订阅的，**不要**再保留本地的 `.mod` 文件，否则会冲突。）

---

## 上传到创意工坊

> 本节步骤依据 [官方 wiki · Uploading and updating a mod](https://stellaris.paradoxwikis.com/Modding#Uploading_and_updating_a_mod)。

### 上传前检查

| 检查项 | 要求 | 本 mod |
|---|---|---|
| `descriptor.mod` 里有 `name` | 必须 | ✅ |
| `picture="thumbnail.png"` | 必须，且名字固定 | ✅ |
| `thumbnail.png` | PNG、≥512×512、**< 1 MB** | ✅ 512×512、155 KB |
| `descriptor.mod` 里有 `path=` | **不需要**（会被忽略） | ✅ 已移除 |
| `tags` | ≤ 10 个（建议用预定义标签） | ✅ 4 个 |
| 所有文件编码 | 见上方表格 | ✅ 已用 `tools/fix_bom.py` 校验 |

### 上传步骤（Paradox 启动器 v2）

```
1. 启动 Paradox Launcher（不用先进游戏）
2. 左侧选「Mods」页
3. 点「Upload a Mod」
4. 从列表里选中「ZL - 大肥鱼天枢执政」
5. 选择发布站台（Steam Workshop / Paradox Mods，可同时选）
6. 填写描述（会显示在工坊页面，见下方草稿）
7. 点「Upload Mod」
8. 等待完成提示
```

上传成功后，启动器会往 `descriptor.mod` 里写入 `remote_file_id=`，
并把 mod 复制到：

```
...\Steam\steamapps\workshop\content\281990\<remote_file_id>\
```

### 更新已上传的 mod

**流程完全相同** —— 再走一次上面的步骤即可覆盖。
注意：**第 6 步填写的描述会完全替换掉工坊页面上的旧描述**，
所以更新时要重新粘贴完整描述。

### 上传后

- 到 [创意工坊页面](https://steamcommunity.com/app/281990/workshop/) →
  右侧「Your Files」→「Files you've posted」找到你的 mod
- 检查可见性是否为 **Public**（有时默认是 Friends Only）
- 建议补上：截图、更新说明、以及 README 里的重要信息

> ⚠️ **注意**：上传后如果你同时保留本地的 `.mod` 文件**并订阅**工坊版，
> 官方 wiki 说"上传的版本很可能无法工作"。请二选一：
> 要么保留本地版、要么只用工坊版（删掉 `mod\zl_unique_administrator.mod`）。


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

每个形态 **正好 10 个特质**，对应 10 级：

```
subclass 4 + basic 2 + veteran 3 + destiny 1 = 10
```

**其中只有 1 个是本 mod 自定义的**（形态 destiny 特质：不朽、绿色框、自定义图标），
其余 9 个全部是**原版特质**。

### 本 mod 自定义的 3 个特质（每形态各一个）

| 特质 | 适用形态 | 效果 |
|---|---|---|
| **大肥鱼** | 行政官 | 影响力 +15%、凝聚力 +10%、法令经费 +30、帝国规模 -10<br>**治理星球**：稳定 +10、犯罪 -25、舒适 +10、凝聚力 +15%、建筑花费 -20%、建造速度 +20%<br>**治理星域**：减半 |
| **深海鲸落** | 指挥官 | 海军容量 +10%<br>**统率舰队**：武器伤害 +15%、船体 +10%、航速 +10% |
| **万卷归流** | 科学家 | 勘测 +25%、异常研究 +25%、考古 +25% |

三者都带 `immortal_leaders = yes` —— **全局生效的永生**，不依赖职位。

### 原版特质（三形态共用，共 5 个）

| 特质 | 类型 | 效果 |
|---|---|---|
| 天赋异禀 II | basic | 领袖特质选项 +2 |
| 知识分子 | basic | 研究所产出 +10% |
| 冒险精神 | veteran | 领袖维护费 -10% |
| 科学外交 III | veteran | 科技外交权重 +20%、研究速度 +10% |
| 军事知识 III | veteran | 指挥上限 +20、海军容量 +15% |

### 子职业（每形态 4 个，全部原版）

用 4 个原版子职业把数量补到 10 个 —— **subclass 不占 basic/veteran/destiny 额度**，
所以在满足"10 个特质"的同时不会触发任何超限清理。

| 形态 | 4 个子职业 |
|---|---|
| 行政官 | 产业专员 / 帝国代表 / 国务顾问 / 外交顾问 |
| 指挥官 | 舰队司令 / 陆军司令 / 督管专员 / 舰队顾问 |
| 科学家 | 前沿学者 / 探索者 / 分析专员 / 科学顾问 |

### 为什么必须正好 10 个特质

这是这个 mod 最核心的一条规则，踩了很多次才摸清：

**规则 A —— 10 级需要 10 次特质选择**

```
LEADER_TRAIT_SELECTION_LEVELS = { 1 2 3 4 5 6 7 8 9 10 }
```

**规则 B —— `add_skill_without_trait_selection` 不消耗选择机会**

原版给自己新领袖初始化时就是这么写的
（`events/leader_events_2.txt:569` 的 `leader.200`），
所以**原版新领袖照样有待选特质** —— 那是设计意图。

> ⚠️ 这意味着：**没有任何 effect 能"清空"待选特质**。
> 想要零待选，唯一办法是让**特质总数等于等级**。
> 原版 Chosen 领袖就是 8 级配 8 个特质。

**规则 C —— 槽位上限**

```
MAX_BASIC_TRAITS   = 2
MAX_VETERAN_TRAITS = 3
```
外加 destiny 1 个。（subclass 在 defines 里**没有上限定义**）

**三条规则的交集 → `2 + 3 + 1 + 4 = 10`**

用 4 个原版子职业补足数量，是这个约束下唯一可行的解法。
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

> 📄 **完整声明见 [`ASSET-NOTICE.md`](ASSET-NOTICE.md)** ——
> 该文件逐项说明每份素材的来源、权利状态、本项目所做的修改，
> 以及权利人的移除请求渠道。本节是其摘要。

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
| 鲸鱼图形（用于帝国旗帜） | [DeepSeek 官方品牌素材](https://github.com/deepseek-ai/awesome-deepseek-integration/blob/main/docs/logo-svg/guidelines.md) | 受官方使用规范约束，非商业粉丝用途；详见[关于 DeepSeek 的声明](#关于-deepseek-的声明) |
| 原版游戏贴图（子职业图标等） | Paradox Interactive | Stellaris 游戏资源，未随本仓库分发 |

---

## 许可证

本项目的**代码部分**采用 **MIT License**，完整条款见 [LICENSE](LICENSE)。
**非代码素材的完整权利说明见 [ASSET-NOTICE.md](ASSET-NOTICE.md)。**

```
SPDX-License-Identifier: MIT
```

**适用范围**：本仓库中由本项目作者创作的部分 ——
`common/` `events/` `gfx/portraits/portraits/` `interface/` `localisation/`
`tools/` 以及各 `.md` 文档。

**例外一 —— 角色立绘不在 MIT 覆盖范围内**：

```
gfx/models/portraits/zl_leader/zl_unique_administrator_leader.dds
thumbnail.png
```

该立绘是从网上搜集的 AI 生成图片，本项目作者并非其创作者，也未取得明示
授权，权利状态不明。

**例外二 —— 鲸鱼图形属于 DeepSeek 官方品牌素材**：

```
flags/special/zl_deepseek.dds
flags/special/map/zl_deepseek.dds
flags/special/small/zl_deepseek.dds
```

该图形取自 DeepSeek 官方品牌素材，其使用受官方规范约束（见下节），
**不在 MIT 许可范围内**。

| | 说明 |
|---|---|
| ✅ **代码部分** | MIT —— 自由使用、修改、再分发，甚至商用 |
| ⚠️ **角色立绘** | 权利状态不明，**不在 MIT 范围内**；再分发时请自行评估 |
| ⚠️ **鲸鱼图形** | DeepSeek 官方品牌素材，受其使用规范约束 |

如果你打算以宽松协议复用本仓库的代码，建议**先移除上述两类素材文件**，
就可以完全按 MIT 处理。

---

## 关于 DeepSeek 的声明

**本 mod 是一个非商业的粉丝作品，与 DeepSeek 官方没有任何关联。**

- 本 mod **不是** DeepSeek 官方产品，也**未获得** DeepSeek 官方的赞助、
  授权或背书
- 本 mod **不包含、不调用、也不依赖** DeepSeek 的任何模型或 API；
  「DeepSeek」在本 mod 中仅作为**虚构角色的名字**出现
- 帝国旗帜使用的鲸鱼图形取自 **DeepSeek 官方品牌素材**，
  依据其公开的
  [DeepSeek 品牌素材使用规范](https://github.com/deepseek-ai/awesome-deepseek-integration/blob/main/docs/logo-svg/guidelines.md)
  使用
- 使用目的为**非商业的粉丝致敬**，不涉及任何形式的销售、付费墙或商业推广
- 本 mod 完全免费，作者不从中获取任何商业利益

> ⚠️ **规范中明确要求"请在实际接入 DeepSeek 的模型或 API 的前提下使用"**，
> 而本 mod 是游戏模组，并不满足该前提。因此本 mod 对鲸鱼图形的使用属于
> **灰色地带** —— 作者已尽量做到明确声明、非商业使用、可随时移除。
>
> **若 DeepSeek 官方认为本 mod 的使用方式不妥，请提交 Issue，
> 作者会立即移除相关图形。**


---

## 致谢

- **Paradox Interactive** — Stellaris
- 机制灵感来自原版**灰风（Gray / Distant Stars）**的形态切换设计
- 「鲸鱼娘」形象的社区创作者们


