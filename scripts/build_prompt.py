#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""结构化拼装微缩景观提示词（micro-diorama）。

把「主体 + 类别 + 标志元素 + 光线 + 底座」拼成六段式提示词，
保证每次输出都带齐五个硬锚点：微缩定性、45度俯视、地形切面、
真实质感与光影、无文字无水印。

用法示例：
    python build_prompt.py --name "黄鹤楼" --category chinese-pavilion \
        --elements "飞檐,黄琉璃瓦,朱漆立柱,高台,长江,江船"

    python build_prompt.py --name "西湖" --category ink-landscape --ratio 1:1 --json

    python build_prompt.py --name "莫高窟" --category desert-ruins \
        --elements "九层楼阁,洞窟崖面,栈道,沙丘,驼队" --base wood --variant 夜景

无第三方依赖，Python 3.8+。
"""

import argparse
import json
import sys

# ---------------------------------------------------------------- 风格包
STYLES = {
    "chinese-palace": {
        "world": "紫禁城宫殿",
        "palette": "金黄与朱红、汉白玉",
        "materials": "金黄琉璃瓦、朱红宫墙、汉白玉台基、彩画额枋",
        "env": "中轴线排列的宫殿群、宽阔石板广场、角楼与城墙、庭院古树",
        "light": "柔和阳光，庄重华丽",
    },
    "chinese-garden": {
        "world": "江南庭院",
        "palette": "白墙黛瓦与青绿",
        "materials": "灰瓦、木质廊柱、太湖石、卵石铺地",
        "env": "曲折回廊、月洞门、池塘拱桥、假山置石、岸边垂柳",
        "light": "柔和自然光，雅致清新",
    },
    "chinese-pavilion": {
        "world": "楼阁江天",
        "palette": "黄琉璃与朱红、古朴典雅",
        "materials": "层层飞檐、木构斗拱、朱漆立柱、石阶高台",
        "env": "高台亭廊、苍松景观道、蜿蜒江面与微型船只、远方山峦",
        "light": "柔和金色阳光",
    },
    "ink-landscape": {
        "world": "江南山水",
        "palette": "清新淡雅的青绿",
        "materials": "细腻水面波纹、垂柳荷叶、山石层理",
        "env": "蜿蜒堤岸、跨水石桥、湖心小岛、层叠远山与薄雾",
        "light": "柔和晨光，薄雾缭绕",
    },
    "modern-city": {
        "world": "都市天际",
        "palette": "冷蓝与暖橙对比",
        "materials": "玻璃幕墙、钢结构、沥青路面、金属铝板",
        "env": "高低错落塔楼群、江岸码头、微小车流、环形天桥、滨江绿带",
        "light": "蓝调时刻的城市灯火与暖色窗光",
    },
    "natural-wonder": {
        "world": "云雾峰林",
        "palette": "青灰与翠绿",
        "materials": "岩石层理、苔藓、松针、溪流水花",
        "env": "垂直石柱峰林、幽深峡谷、悬空栈道、瀑布与云雾山影",
        "light": "清晨侧逆光，薄雾",
    },
    "coast-island": {
        "world": "热带海滨",
        "palette": "浅青绿与米白",
        "materials": "珊瑚细沙、通透海水、椰木、白墙建筑",
        "env": "弧形海湾与白色浪线、成排椰林、度假建筑与泳池、帆船游艇",
        "light": "正午通透高光",
    },
    "snow-mountain": {
        "world": "高原雪山",
        "palette": "冷白与松绿",
        "materials": "积雪、冰川、裸岩、针叶林",
        "env": "连绵雪峰脊线、冰川舌、之字形盘山路、高山湖泊倒影",
        "light": "清冷高原日照，雪面蓝紫阴影",
    },
    "desert-ruins": {
        "world": "丝路荒漠",
        "palette": "土黄与赭红",
        "materials": "砾岩崖壁、风蚀岩面、细沙、夯土",
        "env": "密布洞窟的崖面、层叠栈道、起伏沙丘、胡杨与驼队",
        "light": "炽烈正午顶光与浓重阴影",
    },
    "japanese-garden": {
        "world": "日式禅意庭院",
        "palette": "墨绿与浅金",
        "materials": "金箔墙面、桧皮葺屋顶、黑松、白砂砾、苔藓",
        "env": "镜面水池倒影、石灯笼、竹篱、置石小岛、碎石小径",
        "light": "柔和侧光，高光克制",
    },
    "european-oldtown": {
        "world": "欧洲古城",
        "palette": "砖红与赭石",
        "materials": "陶瓦屋顶、石材砌块、铸铁灯柱、彩绘玻璃",
        "env": "密集红瓦街区、石桥雕像、教堂钟楼、广场市集",
        "light": "黄昏暖光斜照",
    },
    "campus-life": {
        "world": "青春校园",
        "palette": "砖红与草绿",
        "materials": "红砖墙面、塑胶跑道、钢构车棚、玻璃窗格",
        "env": "围合式教学楼、环形操场、升旗台与花坛、行道树与微小人物",
        "light": "上午柔和阳光与长阴影",
    },
    "scifi-fantasy": {
        "world": "超现实未来",
        "palette": "青紫与霓虹",
        "materials": "抛光金属、全息发光体、能量管线、奇异晶体植被",
        "env": "悬浮平台、环形结构、发光脉络、层叠天空之城",
        "light": "暗场环境光与自发光体",
    },
}

BASES = {
    "floating": "模型底部呈现自然的地形切面，仿佛整座景点被浓缩成一座悬浮于纯净背景中的微缩立体岛屿",
    "section": "模型底部为整齐的剖面切面，露出岩层与土层的分层结构，像从大地上切下的一块",
    "wood": "整座模型坐落于深色胡桃木圆形底座之上，底座边缘有轻微倒角，如同博物馆展品",
    "acrylic": "整座模型罩在透明亚克力方罩内，罩体边缘有细微反光，呈展示柜质感",
    "plate": "模型立于一块浅色哑光展示板上，边缘干净利落，投影柔和",
}

ANCHOR_CN = "画面干净，无文字，无水印，高清画质"
ANCHOR_EN = (
    "photorealistic 3D miniature diorama, isometric view, ultra detailed, "
    "tilt-shift depth of field, clean background, no text, no watermark, "
    "high resolution render"
)

VARIANTS = {
    "夜景": "夜间场景，建筑内部透出暖黄窗光，路灯形成柔和光斑，天空呈深蓝带星，地面湿润反光",
    "雪景": "覆盖一层薄雪，屋顶与树梢积雪，暖黄窗光与冷蓝环境色对比，空气中隐约有呼气白雾",
    "春季": "春季，新绿与花树点缀，花瓣散落在步道与水面上",
    "秋景": "秋季，落叶乔木转为金黄与橙红，地面铺满落叶",
    "雨天": "细雨，地面湿润反光，水洼倒映建筑，空气清透带雾",
}

SIZE_MAP = {
    "3:2": "1536x1024",
    "16:9": "1536x1024",
    "4:3": "1536x1024",
    "1:1": "1024x1024",
    "2:3": "1024x1536",
    "9:16": "1024x1536",
}


def build(args):
    style = STYLES.get(args.category)
    if style is None:
        style = {
            "world": "",
            "palette": "自然真实",
            "materials": "",
            "env": "近景、中景与远景层层递进的景观",
            "light": args.light or "柔和自然光",
        }

    palette = args.palette or style["palette"]
    light = args.light or style["light"]
    world = args.world or style["world"]
    base = BASES.get(args.base, BASES["floating"])

    elements = [e.strip() for e in (args.elements or "").split(",") if e.strip()]
    if len(elements) > 8:
        elements = elements[:8]  # 超过 8 个细节会糊成一团

    # 材质词若已被元素覆盖，就不再重复罗列
    keep_materials = []
    for m in [x.strip() for x in style["materials"].split("、") if x.strip()]:
        if any(m in e or e in m for e in elements):
            continue
        keep_materials.append(m)

    detail_bits = []
    if elements:
        detail_bits.append("、".join(elements) + "清晰可见")
    if keep_materials:
        detail_bits.append("材质上保留" + "、".join(keep_materials))
    detail = "，".join(detail_bits) if detail_bits else "建筑与地形细节完整可辨"

    env = args.env or style["env"] or "近景、中景与远景层层递进的环境细节"
    center = args.center or args.name

    variant = VARIANTS.get(args.variant, args.variant or "")

    parts = []
    if world:
        parts.append(
            "将{}制作成精致的微缩立体模型，呈现一个浓缩的{}世界".format(args.name, world)
        )
    else:
        parts.append(
            "将{}制作成精致的微缩立体模型，呈现一座完整的微缩世界".format(args.name)
        )
    parts.append("45度俯视视角，紧凑精巧的立体沙盘构图，{}".format(detail))
    parts.append("{}作为整个微缩世界的视觉中心，周围{}共同构成丰富的空间层次".format(center, env))
    parts.append(base)
    if variant:
        parts.append(variant)
    if args.text:
        parts.append(args.text)
    parts.append(
        "{light}，{palette}配色，精致的3D微缩模型质感，真实的材质细节，细腻阴影，电影级渲染".format(
            light=light, palette=palette
        )
    )
    parts.append(ANCHOR_EN)
    parts.append(ANCHOR_CN)

    prompt = "。".join(parts) + "。"

    anchors = {
        "微缩定性": "微缩立体模型" in prompt and "diorama" in prompt,
        "45度俯视": "45度俯视" in prompt and "isometric view" in prompt,
        "基座切面": any(k in prompt for k in ("地形切面", "剖面切面", "底座", "亚克力", "展示板")),
        "质感光影": "photorealistic" in prompt and ("光线" in prompt or "阳光" in prompt or "光" in prompt),
        "负面约束": "无文字" in prompt and "no watermark" in prompt,
    }

    return {
        "name": args.name,
        "category": args.category,
        "prompt": prompt,
        "size": SIZE_MAP.get(args.ratio, "1536x1024"),
        "ratio": args.ratio,
        "anchors": anchors,
        "passed": all(anchors.values()),
        "element_count": len(elements),
    }


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    p = argparse.ArgumentParser(description="拼装微缩景观（micro-diorama）提示词")
    p.add_argument("--name", required=True, help="景点或场景名称，如 黄鹤楼")
    p.add_argument("--category", default="generic", choices=sorted(STYLES) + ["generic"],
                   help="风格包，默认 generic")
    p.add_argument("--elements", default="", help="标志元素，逗号分隔，最多保留 8 个")
    p.add_argument("--center", default="", help="视觉中心，默认同 --name")
    p.add_argument("--env", default="", help="自定义环境层次描述，覆盖风格包")
    p.add_argument("--world", default="", help="覆盖世界定性词，如 江南山水")
    p.add_argument("--palette", default="", help="覆盖配色描述")
    p.add_argument("--light", default="", help="覆盖光线描述")
    p.add_argument("--base", default="floating", choices=sorted(BASES), help="底座样式")
    p.add_argument("--variant", default="", help="季节/时段变体：夜景 雪景 春季 秋景 雨天，或自定义短句")
    p.add_argument("--text", default="", help="追加的额外风格描述，如 黏土手工质感")
    p.add_argument("--ratio", default="3:2", choices=sorted(SIZE_MAP), help="画幅比例")
    p.add_argument("--json", action="store_true", help="输出 JSON 结构化结果")

    args = p.parse_args()
    result = build(args)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["prompt"])
        print()
        print("建议尺寸: {}".format(result["size"]))
        missing = [k for k, v in result["anchors"].items() if not v]
        print("硬锚点自检: {}".format("全部通过" if not missing else "缺 " + "、".join(missing)))

    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
