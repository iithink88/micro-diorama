# micro-diorama · 微缩景观生成技能

把一个景点、建筑或任意场景，缩小成一座可以捧在手里的立体小世界，并直接出图。

> 输入「黄鹤楼」，输出一段结构化提示词 + 一张 3D 微缩沙盘图。
> 灵感来自公众号文章《如果把中国的著名景点，缩小成一个精致的微观世界》（爱云画AI，2026-10-19）。

![示例](https://img.shields.io/badge/WorkBuddy-Skill-blue) ![License](https://img.shields.io/badge/license-MIT-green)

## 效果

输入：`把保定大慈阁缩小成微观世界`

输出：三层歇山顶楼阁立在石栏高台上，四周青砖灰瓦的老街、古槐与银杏，整块地形被切成一座悬浮的圆形沙盘，45° 俯视，移轴景深。

## 安装

这个技能运行在 [WorkBuddy](https://www.workbuddy.cn) 里，依赖它的对话与出图能力。

### 方式一：解压到用户级技能目录（推荐）

技能对所有工作区生效。

1. 解压 `micro-diorama.zip`，得到 `micro-diorama` 文件夹
2. 放进用户技能目录：
   - Windows：`C:\Users\<你的用户名>\.workbuddy\skills\`
   - macOS / Linux：`~/.workbuddy/skills/`
3. 重启 WorkBuddy，在对话框输入「把西湖缩小成微观世界」即可触发

最终结构应为：

```
~/.workbuddy/skills/micro-diorama/
├── SKILL.md
├── references/
│   ├── prompt-cookbook.md
│   └── style-lexicon.md
└── scripts/
    ├── build_prompt.py
    └── trim_watermark.py
```

### 方式二：装到单个项目

把 `micro-diorama` 文件夹放进项目根目录的 `.workbuddy/skills/` 下，只在该项目内生效，适合团队共享。

## 用法

不需要记命令，直接说人话：

| 你说 | 它做 |
|---|---|
| 把黄山缩小成微观世界 | 直接给提示词并出图 |
| 把西湖做成微缩景观，秋天版，木质底座 | 套江南山水风格包 + 秋景变体 + 胡桃木底座 |
| 给我故宫、敦煌、鼓浪屿三个的微缩提示词 | 先出三条提示词，确认后再逐张出图 |
| 换成黏土手工质感 | 只替换渲染风格段，构图与配色保持 |

### 命令行拼装（批量用）

```bash
python scripts/build_prompt.py --name "黄鹤楼" --category chinese-pavilion \
  --elements "飞檐,黄琉璃瓦,朱漆立柱,高台,长江,江船" --base floating

python scripts/build_prompt.py --name "西湖" --category ink-landscape --ratio 1:1 --json
```

`--category` 可选值：`chinese-palace` `chinese-garden` `chinese-pavilion` `ink-landscape` `modern-city` `natural-wonder` `coast-island` `snow-mountain` `desert-ruins` `japanese-garden` `european-oldtown` `campus-life` `scifi-fantasy` `generic`

`--base` 可选值：`floating`（悬浮地形切面，默认） `section`（剖面） `wood`（胡桃木底座） `acrylic`（亚克力罩） `plate`（展示板）

脚本自带五个硬锚点自检，缺项会以退出码 1 报错，方便批量流水线里卡质量。

### 裁掉水印

出图工具会在右下角强制叠加「AI生成」标识，提示词里的 `no watermark` 对它无效：

```bash
python scripts/trim_watermark.py 图片路径 --keep-ratio
```

默认从底部裁 7% 并补回原比例，裁切线落在沙盘虚化的边缘，不伤主体。

## 原理：六段公式

| 段 | 内容 |
|---|---|
| 1 转化指令 | 将「X」制作成精致的微缩立体模型，呈现一个浓缩的……世界 |
| 2 视角构图 | 45 度俯视视角，紧凑精巧的立体沙盘构图 |
| 3 主体细节 | 材质＋颜色＋结构，只给一个视觉中心 |
| 4 环境层次 | 近—中—远三层：水系、植被、道路、云雾、远山 |
| 5 基座处理 | 地形切面／悬浮岛／木底座／亚克力罩——决定「模型感」的关键 |
| 6 质感光影 | 3D miniature diorama, isometric view, photorealistic, ultra detailed ＋ 光线 ＋ 配色 ＋ 无文字无水印 |

五个硬锚点缺一不可：**微缩定性词、45° 俯视、地形切面、真实质感光影、负面约束**。

更多范例见 `references/prompt-cookbook.md`，风格包与词库见 `references/style-lexicon.md`。

## 依赖

- WorkBuddy（提供对话与出图能力）
- Python 3.8+（仅命令行拼装需要；`trim_watermark.py` 需要 pillow）
- 无其他第三方依赖

## 许可

MIT。随意修改、二次分发，保留出处即可。
