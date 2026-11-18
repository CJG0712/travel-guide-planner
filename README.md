<h1 align="center">travel-guide-planner</h1>

<p align="center">
  <em>通用图文旅游攻略与 4 页手账画册式 PDF 路书规划 Skill</em>
</p>

<p align="center">
  <a href="./VERSION"><img src="https://img.shields.io/badge/version-1.1.0-2B6D7A?style=flat-square" alt="Version"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-4E8B78?style=flat-square" alt="License: MIT"></a>
  <a href="./SKILL.md"><img src="https://img.shields.io/badge/works%20with-Agent%20Skills%20%2F%20Antigravity%20%2F%20Claude%20Code%20%2F%20Codex-B64632?style=flat-square" alt="Agent Skills"></a>
</p>

<p align="center">
  简体中文 | <a href="./readmes/README.en.md">English</a>
</p>

> **不设定任何既定城市，拒绝模板化“AI 腔”与冗长文字堆砌。**
> 先问清出发地与目的地、精确抵离时刻、预算与饮食底线，再联网核实实时票价、闭馆日与门店地址，遵循**“优先网上真实美观实拍、缺失杂乱时再合理生图补位”**的配图原则，输出手账质感满满、字阶清晰、间距匀称的 4 页 A4 图文路书。

---

## 实测成品效果预览（v1.1.0 手账精修版示例）

以下为本 Skill 实际运行导出的一组 4 页 A4 全出血手账路书截图（技能本身完全通用，不绑定制城市；示例为按用户“不爬山、完全不吃辣、学生预算”约束实测生成）：

<table>
  <tr>
    <td align="center" width="50%">
      <img src="./assets/demo_page_1.png" alt="第1页：拍立得封面、车票票根、天气便签与蜡笔预算条" width="100%"><br>
      <sub><b>Page 1 · 拍立得封面 + 票根与预算</b>：和纸胶带相框、车票票根、便签提醒、蜡笔预算条与选站理由</sub>
    </td>
    <td align="center" width="50%">
      <img src="./assets/demo_page_2.png" alt="第2页：2×2与1×3拍立得拼贴相册与省力原则" width="100%"><br>
      <sub><b>Page 2 · 地标与街区手账相册</b>：舒朗留白、价格黄标与省腿动线原则底栏，不拥挤不堆字</sub>
    </td>
  </tr>
  <tr>
    <td align="center" width="50%">
      <img src="./assets/demo_page_3.png" alt="第3页：手绘海岸路线SVG地图与双日虚线时间轴" width="100%"><br>
      <sub><b>Page 3 · 手绘路线图 + 双栏手账轴</b>：手绘水系轮廓、防遮挡文字、日夜航切换及口碑公交贴士</sub>
    </td>
    <td align="center" width="50%">
      <img src="./assets/demo_page_4.png" alt="第4页：当地特色美食图鉴、核实地址与行前勾选单" width="100%"><br>
      <sub><b>Page 4 · 美食小本本 + 行前勾选单</b>：0 辣真实美食大图、门牌实价卡片、邮戳印章与点单暗号</sub>
    </td>
  </tr>
</table>

---

## v1.1.0 核心能力升级

- **通用零地域预设**：不写死任何既定出发地或目的地城市；先收集或核对**出发城市、目标城市、抵离窗口、证件优惠（并核查公交/轮渡等无半价真相）、辣度忌口与体力底线**再规划。
- **双渠道真实感图片原则**：
  1. **第一优先（真实网络实拍）**：优先检索并下载目标景点与本地美食的真实、干净、无水印高清实拍图，逐张 `read_file` 过检后再入版；
  2. **第二优先（按需真实感生图补位）**：仅当搜不到合规图、原图杂乱带水印或拼盘菜品需要统一美观画风时生成配图；严格遵守现实地理与食材认知，绝不虚构不存在的建筑或违背忌口（如“不吃辣”绝不出现红椒辣油）。
- **彻底去 AI 味 + 手作手账排版**：摒弃僵硬公文套话与后台面板方框，改用米白点阵手账纸、斜角和纸胶带拍立得、票根、荧光标记与自然人话短句；正文字阶采用清晰易读的等线/幼圆配华文新魏/华文中宋大标，并禁止 `space-between` 拉出页间空洞。
- **独立隔离导出与逐页视觉验收**：内置 [export_pdf.py](./scripts/export_pdf.py) 采用 `--headless=new --user-data-dir=<temp>` 隔离编译，自动捕获目标 PDF 占用锁定，并导出 `160 dpi` 逐页 `.png` 供 Agent 目视验收。

---

## 30 秒快速安装

```bash
npx skills add CJG0712/travel-guide-planner -g
```

或手动克隆到你的 Agent 技能目录：

- **Antigravity（全局）**：`git clone https://github.com/CJG0712/travel-guide-planner.git ~/.gemini/config/skills/travel-guide-planner`
- **Claude Code（全局）**：`git clone https://github.com/CJG0712/travel-guide-planner.git ~/.claude/skills/travel-guide-planner`
- **项目级共享**：克隆至项目根目录 `.agents/skills/travel-guide-planner/`

---

## 本地体验模板导出

```bash
pip install -r requirements.txt
python scripts/export_pdf.py --html examples/lookbook-template.html --out tmp/sample.pdf --preview-dir previews --dpi 160
```

> 运行依赖：本机需安装 Microsoft Edge 或 Chrome/Chromium 用于无头 PDF 打印；`PyMuPDF`（AGPL-3.0 协议）与 `python-docx` 为可选辅助依赖。

---

## 仓库目录与协议

- 完整工作流规范见 [SKILL.md](./SKILL.md)，版式细则见 [visual-pdf-blueprint.md](./references/visual-pdf-blueprint.md) 与 [itinerary-template.md](./references/itinerary-template.md)，通用 HTML 样板见 [lookbook-template.html](./examples/lookbook-template.html)。
- 本项目代码与文档基于 [MIT License](./LICENSE) 开源。
