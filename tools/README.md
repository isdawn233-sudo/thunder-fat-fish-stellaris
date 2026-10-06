# tools —— Stellaris Mod 开发校验工具

这些是开发《ZL - 天枢执政》时写的脚本。
它们对写**任何** Stellaris mod 的人都有用，所以一并开源。

---

## 前置

```bash
pip install pillow
```

脚本里的游戏路径常量（默认 `/path/to/Steam/steamapps/common/Stellaris`）
请改成你自己的安装位置。

---

## 校验类

### `verify_mod.py` —— 综合校验

```bash
python verify_mod.py
```

检查内容：

- 目录结构是否完整（必备文件夹/文件是否缺失）
- **BOM 是否正确**（`.mod`/`.txt`/`.gfx` 不能有；`.yml` 必须有）
- 所有 `modifier` 名是否在原版合法列表中
- 交叉引用：事件里引用的特质/本地化键是否存在
- 本地化键是否中英双语齐全

### `verify_traits.py` —— 领袖特质校验

```bash
python verify_traits.py
```

- 引用的原版特质名是否真实存在
- **槽位上限**是否超限（`MAX_BASIC_TRAITS = 2`、`MAX_VETERAN_TRAITS = 3`）
- `leader_trait_type` 是否合法（只有 `basic`/`veteran`/`subclass`/`destiny`/`negative`）

> ⚠️ `leader_trait_type` **缺省即 `basic`**。漏写会导致 basic 槽位超限，
> 这个脚本能抓到。

### `verify_modifiers.py` —— modifier 名校验

```bash
python verify_modifiers.py
```

对照 `modifier_names.txt`（从原版提取的 **2193 个**合法名）逐个检查。
写错的名字会被游戏静默忽略，这个脚本能提前发现。

### `fix_bom.py` —— 自动修 BOM

```bash
python fix_bom.py
```

按文件类型自动加/去 UTF-8 BOM：

| 文件类型 | 处理 |
|---|---|
| `descriptor.mod` / `.mod` / `.txt` / `.gfx` / `.asset` | **去掉** BOM |
| `.yml`（localisation） | **加上** BOM |

`.mod` 带 BOM 会让启动器报 `Unexpected token` 并**跳过整个 mod**。
建议每次改完本地化都跑一次。

### `audit_traits.py` —— 特质作用域审计

```bash
python audit_traits.py
```

把配装里的每个特质分类：

```
通用     只用 self_modifier / modifier          —— 任何职位都生效
仅内阁   councilor_modifier
仅总督   planet_modifier / sector_modifier
仅舰队   fleet_modifier / army_modifier
```

想在"任何职位都生效"和"限定本职"之间做取舍时很有用。

### `find_universal.py` / `list_universal_by_type.py` —— 找通用特质

```bash
python find_universal.py official          # 行政官可用的纯通用特质
python list_universal_by_type.py veteran   # 按类型列出纯通用特质
```

### `trait_lookup.py` —— 查特质详情

```bash
python trait_lookup.py official leader_trait_gifted leader_trait_resilient
```

打印特质的类型、适用职业、修正块与数值。

---

## 资源生成类

### `portrait_dds.py` —— PNG → 立绘 DDS

```bash
python portrait_dds.py --src 输入.png --out 输出.dds --height 323 --gain 1.1 --preview
```

产出群星立绘用的 **DXT5** DDS（500×323、mips=1、caps=0x1000）。

参数：`--crop`（裁剪）、`--size`、`--height`、`--gain`（亮度）、
`--sat`（饱和度）、`--tint R G B`、`--preview`

> 注意：DXT5 编码里 RGB 通道顺序是 565/555，**写反会让蓝色变橙色**。
> 本脚本已修正。

### `make_trait_icon.py` —— 特质图标

```bash
python make_trait_icon.py --glyph fish --out 输出.dds
```

产出原版格式的 **29×29 未压缩 BGRA8** DDS
（`flags=0x0002100F`、`mips=5`、`caps1=0x401008`）。
这是原版特质图标实际使用的格式 —— 用 DXT5 会显示异常。

`--glyph` 可选：`fish` / `pillar` / `seal` / `star`

### `make_deepseek_flag.py` —— 帝国旗帜

```bash
python make_deepseek_flag.py
```

生成旗帜三件套：

```
flags/<名>.dds            256×256 主旗（未压缩 BGRA8）
flags/<名>/map/<名>.dds   256×256 地图旗
flags/<名>/small/<名>.dds 24×24   小旗
```

脚本内包含**透明背景**方案（抠出图案、去除黑底）。

---

## 参考数据

| 文件 | 内容 |
|---|---|
| `modifier_names.txt` | 从原版 `common/` 提取的 2193 个合法 modifier 名 |
| `valid_modifier_blocks.txt` | 合法的修正块名（`self_modifier` / `councilor_modifier` / `planet_modifier` …） |

---

## 典型工作流

```bash
# 改完 mod 后
python fix_bom.py          # 1. 先修 BOM
python verify_modifiers.py # 2. 检查 modifier 名
python verify_traits.py    # 3. 检查特质与槽位
python verify_mod.py       # 4. 综合校验
```

全部通过后再进游戏测试。
