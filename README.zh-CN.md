# Image To Shape-Safe SVG

语言：[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

将幻灯片截图、流程图、业务图表、信息图和页面截图重建为更适合在 PowerPoint 中“转换为形状”的可编辑 SVG。

这是一个 Codex skill。它的目标不是把位图描摹成一张复杂路径图，而是用文本、路径、线条、多边形、图标和简单形状重新搭建页面结构，让输出文件更容易在 Office 中编辑。

## 适合做什么

- 把 PPT 截图或设计稿截图重建成结构化 SVG。
- 提升 PowerPoint convert-to-shapes 的兼容性。
- 避免嵌入原图、`foreignObject`、SVG transform、marker 箭头和未展开的图标占位符。
- 将箭头头部烘焙为 polygon，降低 Office 转换后丢失箭头的风险。
- 尽量保持文本为独立 SVG text 节点，方便后续编辑。
- 对说明性小段文字允许有限的多行文本块，并用 `data-text-role="explanatory-block"` 标记。
- 内置语义图标库和自动关键词匹配工具，可按 automation、data、risk、workflow、数据、自动化、风险等语义匹配可编辑 SVG primitives。
- 默认减少装饰性图标，优先用编号圆点、普通圆点、胶囊标签、色块和状态徽章替代重复小图标。

## 输出要求

最终交付的 SVG 应通过这些硬性检查：

```text
image = 0
data_icon = 0
transform = 0
marker_end = 0
marker_defs = 0
tspan = 0，但允许已标记的说明性文本块例外
foreign_object = 0
```

默认输出目录：

```text
svg_shape_safe/
```

## 目录结构

```text
.
|-- SKILL.md
|-- config.yaml
|-- agents/
|-- assets/
|   `-- icons/
|-- docs/
|   |-- icon-matching.md
|   |-- map-complexity-policy.md
|   `-- troubleshooting.md
|-- examples/
|   |-- basic_usage.md
|   `-- web_usage.md
|-- references/
|   |-- local-batch-workflow.md
|   `-- web-workflow.md
|-- tests/
|   `-- test_validate_shape_safe_svg.py
`-- tools/
    |-- match_shape_safe_icon.py
    `-- validate_shape_safe_svg.py
```

## 安装

克隆仓库到你的 Codex skills 目录，或复制到项目的 `.agents/skills` 目录：

```bash
git clone https://github.com/perpetualhui/image-to-shape-safe-svg.git
```

如果使用项目级 skill，推荐路径：

```text
.agents/skills/image-to-shape-safe-svg/
```

## 使用示例

在 Codex 中按 skill 名称调用：

```text
Use $image-to-shape-safe-svg to convert these three slide screenshots into editable SVG.
Only deliver svg_shape_safe. Make sure icons and arrowheads survive PowerPoint convert-to-shapes.
```

中文提示也可以：

```text
使用 $image-to-shape-safe-svg，把这 3 张中文业务流程图截图重建为可编辑 SVG。
输出放到 svg_shape_safe。箭头不要用 marker，要用 polygon 烘焙箭头头部。
```

图标较多时：

```text
使用 $image-to-shape-safe-svg 转换这张信息图。
先做 preflight，判断图标数量和文字密度。如果图标过多，采用 balanced 策略，只保留模块级图标，其他改成编号圆点或状态标签。
```

批量页面：

```text
使用 $image-to-shape-safe-svg 处理这 5 张仪表盘截图。
先选一页作为样式锚点，统一颜色、字号、卡片圆角和间距。最终只交付通过验证的 svg_shape_safe。
```

图标自动匹配：

```powershell
py tools\match_shape_safe_icon.py "自动化审批流程" --x 120 --y 80 --size 48 --color "#5A0FB4"
```

这会从内置图标库输出已展开的 SVG primitives，不会生成 `<image>`、`transform`、`marker`、`foreignObject` 或 `data-icon`。

本地批处理工作流见：

```text
references/local-batch-workflow.md
```

浏览器或 Web 应用工作流见：

```text
references/web-workflow.md
```

## 推荐流程

1. 检查源图尺寸和页面结构。
2. 先写简短 preflight：复杂度、图标数量、文字密度风险、布局策略和视觉模型调用预算。
3. 如果需要明显改版、减少图标、拆页或改变结构，先让用户选择。
4. 用可编辑 SVG primitives 重建页面。
5. 控制图标预算，只保留真正有信息价值的图标。
6. 箭头用 line/path 加 polygon 箭头头部绘制。
7. 用内置工具验证 SVG。
8. 渲染预览并检查错位、遮挡、箭头缺失和 Office 转换风险。

## 验证

验证单个文件或目录：

```bash
python tools/validate_shape_safe_svg.py path/to/svg_shape_safe
```

Windows 上如果 `python` 指向 Microsoft Store 占位程序，可用：

```powershell
py tools\validate_shape_safe_svg.py path\to\svg_shape_safe
```

输出 JSON：

```bash
python tools/validate_shape_safe_svg.py --json path/to/svg_shape_safe
```

安装 `pytest` 后运行测试：

```bash
python -m pytest tests
```

## 设计原则

目标是可编辑重建，不是像素级描摹。好的输出应该保留源页面的结构、层级、间距、色彩意图和主要信息，同时避开 PowerPoint 转换形状时容易出问题的 SVG 特性。

对于复杂业务图，默认优先考虑清晰度和可编辑性。重复小图标、装饰符号和密集标记通常应简化为更稳定的可编辑形状。

## 协议

MIT License。详见 [LICENSE](LICENSE)。
