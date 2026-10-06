# Changelog

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.0] — 首个公开版本

### 新增

- **独特传奇领袖「DeepSeek」**
  - 10 级、传奇级、**永生**（`immortal_leaders = yes`，全局生效）
  - 开局无职，出现在玩家领袖列表中
  - 自定义静态半身立绘，同时用于领袖面板与通讯窗口
  - 自定义旗帜（DeepSeek 鲸鱼标志，透明背景）

- **三形态切换**（复刻原版灰风机制）
  - 入口 ①：F10 通讯界面 → 点开 DeepSeek → 「外交」按钮
  - 入口 ②：政治 → 决策 → 「与 DeepSeek 通话」
  - 形态：行政官 / 指挥官 / 科学家
  - 切换时自动卸下旧形态特质与子职业，换上完整新配装

- **17 个自定义领袖特质**
  - 全部 `COUNCIL = no`（无职时不显示灰色 X）
  - 全部不含 `leader_lifespan_add`（不朽由 `immortal_leaders` 负责）
  - 全部不含 `species_leader_exp_gain`
  - 只有行政官带 `planet_modifier` / `sector_modifier`
  - 指挥官用 `fleet_modifier`（避免舰队加成错误落到星球）

- **双语本地化**：简体中文 + English

- **`tools/` 开发工具**
  - `verify_mod.py` / `verify_traits.py` / `verify_modifiers.py` / `fix_bom.py`
  - `audit_traits.py` / `find_universal.py`
  - `portrait_dds.py` / `make_trait_icon.py` / `make_deepseek_flag.py`
  - `modifier_names.txt`（2193 个合法 modifier 名）/ `valid_modifier_blocks.txt`

### 修复（开发过程中踩过的坑）

以下问题在开发期间全部实测确认并修复，细节见 README「已知的技术坑」：

- `.mod` / `.txt` 带 UTF-8 BOM 导致启动器报 `Unexpected token` 并跳过 mod
- 事件定义里写 `days = N` 导致整个事件文件作废
- **`on_custom_diplomacy` 作用域反直觉**（`root` = 玩家，`from` = 联系人国），
  写反导致「点外交没反应」
- `log` 写在 `trigger` 里无效
- `log` 文本里的 `[ ]` 被当成本地化命令，破坏日志
- **特质选择机会未消耗**（缺 `consume_selection = yes`）导致一直提示
  「等级提升！请选择特质」
- `leader_trait_type` 缺省即 `basic`，导致 `basic` 槽位超限
- `COUNCIL = yes` 在领袖无职时显示灰色 X
- 决策作用域不是国家（`country_event` 需先 `owner = { }`）
- 不存在的 effect：`set_species`、`leader_trait_type = paragon`、
  trait 的 `scientist_modifier` 块
- DXT5 编码器 R/B 通道写反，蓝色立绘渲染成橙色
