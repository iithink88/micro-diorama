# 风格包与词库

## 一、12 个风格包

`category` 列的值即 `scripts/build_prompt.py --category` 的参数名。

| category | 风格 | 典型主体 | 配色 | 材质词 | 必写环境元素 | 光线 |
|---|---|---|---|---|---|---|
| `chinese-palace` | 中式宫殿 | 故宫、天坛、布达拉宫 | 金黄＋朱红＋汉白玉白 | 琉璃瓦、宫墙、汉白玉台基、彩画额枋 | 中轴线宫殿群、广场、角楼、城墙、古树 | 柔和阳光，庄重华丽 |
| `chinese-garden` | 江南园林 | 苏州园林、拙政园、留园 | 白墙黛瓦＋青绿 | 灰瓦、木廊柱、太湖石、卵石铺地 | 月洞门、曲折回廊、池塘、拱桥、假山、窗棂 | 柔和自然光，雅致清新 |
| `chinese-pavilion` | 中式楼阁 | 黄鹤楼、岳阳楼、滕王阁 | 黄琉璃＋红柱＋灰石 | 飞檐、木构斗拱、朱漆立柱、石阶高台 | 高台、亭廊、苍松、江面与船只、远山 | 柔和金色阳光 |
| `ink-landscape` | 山水湖泊 | 西湖、千岛湖、桂林 | 青绿＋黛青＋雾白 | 水面波纹、垂柳、荷叶、山石层理 | 堤岸、断桥、湖心岛、远山层叠、薄雾 | 柔和晨光，薄雾缭绕 |
| `modern-city` | 现代都市 | 陆家嘴、深圳、香港维港 | 冷蓝＋暖橙 | 玻璃幕墙、钢结构、沥青路面、铝板 | 塔楼群、江岸、车流、天桥、绿带、码头 | 蓝调时刻＋暖色窗光 |
| `natural-wonder` | 自然奇观 | 张家界、九寨沟、大峡谷 | 青灰＋翠绿 | 岩石层理、苔藓、松针、溪流水花 | 峰林石柱、峡谷、栈道、瀑布、云雾 | 清晨侧逆光，薄雾 |
| `coast-island` | 海滨岛屿 | 三亚、鼓浪屿、马尔代夫 | 浅青绿＋米白＋深蓝 | 珊瑚砂、海水折射、椰木、白墙 | 弧形海湾、浪线、椰林、度假建筑、帆船 | 正午通透高光 |
| `snow-mountain` | 雪山高原 | 玉龙雪山、珠峰、长白山 | 冷白＋松绿＋岩灰 | 积雪、冰川、裸岩、针叶林 | 雪峰脊线、冰川舌、盘山路、高山湖、经幡 | 清冷高原日照，蓝紫阴影 |
| `desert-ruins` | 沙漠遗迹 | 莫高窟、敦煌、楼兰 | 土黄＋赭红 | 砾岩崖壁、风蚀岩面、细沙、夯土 | 洞窟崖面、栈道、沙丘、胡杨、驼队 | 炽烈顶光，浓重阴影 |
| `japanese-garden` | 日式庭院 | 金阁寺、清水寺、枯山水 | 墨绿＋浅金＋灰白 | 金箔、桧皮葺、黑松、白砂砾、苔藓 | 镜湖池、石灯笼、竹篱、置石、碎石小径 | 柔和侧光，克制高光 |
| `european-oldtown` | 欧洲古城 | 布拉格、佛罗伦萨、爱丁堡 | 砖红＋赭石＋暖灰 | 陶瓦、石材砌块、铸铁灯柱、彩绘玻璃 | 密集街区、石桥、雕像、钟楼、广场市集 | 黄昏暖光斜照 |
| `campus-life` | 校园／生活场景 | 校园、村落、街区、厂房 | 砖红＋草绿＋米白 | 红砖、涂料墙面、塑胶跑道、钢构 | 教学楼、操场、升旗台、车棚、行道树、微小人物 | 上午柔和阳光，长阴影 |

补充：`scifi-fantasy`（科幻童话）— 配色青紫＋霓虹，材质金属与全息发光，环境写悬浮平台、能量管线、奇异植被，光线暗场＋发光体，氛围超现实但结构精巧。

## 二、词库

### 基座样式（Step 3 第 5 段，必选其一）

| 键（`--base`） | 写法 |
|---|---|
| `floating` | 模型底部呈现自然的地形切面，仿佛整座景点被浓缩成一座悬浮于纯净背景中的微缩岛屿 |
| `section` | 底部为整齐的剖面切面，露出岩层／土层的分层结构，像从大地上切下的一块 |
| `wood` | 坐落于深色胡桃木圆形底座上，底座边缘有轻微倒角，如同博物馆展品 |
| `acrylic` | 罩在透明亚克力方罩内，罩体边缘有细微反光，呈展示柜质感 |
| `plate` | 底座是一块浅色哑光展示板，边缘干净利落，投影柔和 |

### 材质搭配三连（颜色＋材质成对写，信息量翻倍）

- 建筑：金黄琉璃瓦／朱红宫墙／汉白玉台基／灰瓦白墙／青砖／夯土／红砂岩／米色涂料
- 金属：铸铁／青铜／拉丝不锈钢／黄铜／金箔
- 自然：花岗岩／太湖石／层理砂岩／苔藓／腐叶土／细珊瑚砂／火山岩
- 水：清透浅水／镜面静水／湍急溪流／薄冰／湿润反光地面
- 植被：垂柳／黑松／银杏／杨树／椰林／针叶林／高山草甸／荷叶
- 人工物：石板路／卵石铺地／沥青路面／木质栈道／玻璃幕墙／竹篱

### 光线与氛围

- 时段：柔和晨光／上午斜阳／金色黄昏／蓝调时刻／清冷高原日照／夜晚灯火
- 天气：薄雾缭绕／晴空通透／细雨湿润／初雪覆盖／沙尘微茫
- 氛围对子（收尾用）：壮观但精巧／梦幻而不失真实／雅致清新／庄重华丽／古朴典雅／静谧而生动

### 英文锚点（末段固定，可微调顺序）

```
photorealistic 3D miniature diorama, isometric view, ultra detailed, tilt-shift depth of field, clean background, no text, no watermark, high resolution render
```

风格替换时保留 `miniature diorama` 与 `isometric view` 两个核心词，其余可换：

| 风格 | 英文替换 |
|---|---|
| 黏土 | claymation diorama, handmade clay texture, matte surface, soft studio light |
| 纸艺 | papercraft diorama, layered paper cut, visible paper grain, crisp folded edges |
| 木质 | wooden architectural model, basswood, laser-cut edges, workshop lighting |
| 水彩 | watercolor diorama illustration, soft edge bleeding, grainy paper texture |
| 微缩真人感 | tilt-shift photography of a real miniature set, shallow depth of field, macro lens |

### 负面约束（每次必带）

中文：`画面干净，无文字，无水印，高清画质`
英文：`no text, no watermark, no logo, clean background, high resolution`

需要避免的写法：
- ✗ "cute""toy""卡通" → 会被拉向塑料玩具
- ✗ "aerial view""drone shot""鸟瞰航拍" → 会被拉向实景航拍
- ✗ 同时给两个以上"视觉中心" → 画面失焦
- ✗ 罗列超过 8 个细节元素 → 糊成一团
