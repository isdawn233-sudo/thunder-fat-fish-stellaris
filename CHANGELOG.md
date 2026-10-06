# Changelog

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.0] — 首个公开版本

### 许可证

- **代码部分**：MIT License
- **角色立绘**：不覆盖在 MIT 内 —— 该图是从网上搜集的 AI 生成图片
  （内嵌 C2PA 凭证显示为 ChatGPT / gpt-image，2026-10-05 生成），
  作者并非本项目作者，权利状态不明
- 详见 README「素材来源与署名」与「许可证」两章

### 命名

- 领袖名与联系人国名：`DeepSeek` → **大肥鱼** / **Big Fat Fish**
- 内部 ID（`zl_deepseek`、`event_target:zl_deepseek` 等）保持不变，
  仅改动玩家可见的显示文本

### 新增

- **独特传奇领袖「大肥鱼」**
  - 10 级、传奇级、**永生**（`immortal_leaders = yes`，全局生效）
  - 开局无职，出现在玩家领袖列表中
  - 自定义静态半身立绘，同时用于领袖面板与通讯窗口
  - 自定义旗帜（鲸鱼标志，透明背景）

- **三形态切换**（复刻原版灰风机制）
  - 入口 ①：F10 通讯界面 → 点开大肥鱼 → 「外交」按钮
  - 入口 ②：政治 → 决策 → 「与大肥鱼通话」
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
