#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""去掉出图工具叠加在右下角的「AI生成」标识。

提示词里的 no watermark / 无水印 对平台强制叠加的标识无效，
只能靠裁切处理。默认从底部裁掉 7%，并自动补回原比例。

用法：
    python trim_watermark.py 图片路径
    python trim_watermark.py 图片路径 --percent 0.08
    python trim_watermark.py 图片路径 --keep-ratio
    python trim_watermark.py 图片路径 --box 830,960,250,64   # 精确指定水印区域

依赖 pillow。
"""

import argparse
import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("缺少 pillow，请先安装：pip install pillow")


def parse_box(text):
    try:
        x, y, w, h = [int(v) for v in text.split(",")]
    except Exception:
        sys.exit("--box 格式应为 x,y,w,h，例如 830,960,250,64")
    return x, y, w, h


def main():
    p = argparse.ArgumentParser(description="裁掉右下角 AI 生成水印")
    p.add_argument("image", help="待处理图片路径")
    p.add_argument("--percent", type=float, default=0.07,
                   help="从底部裁掉的百分比，默认 0.07")
    p.add_argument("--keep-ratio", action="store_true",
                   help="裁切后从左右补裁，保持原图宽高比")
    p.add_argument("--box", default="",
                   help="精确水印区域 x,y,w,h；给出时只裁到该区域下沿")
    p.add_argument("--out", default="", help="输出路径，默认在原文件名后加 _clean")
    args = p.parse_args()

    if not os.path.isfile(args.image):
        sys.exit("找不到图片：{}".format(args.image))

    img = Image.open(args.image).convert("RGB")
    w, h = img.size

    if args.box:
        _x, y, _w, bh = parse_box(args.box)
        cut = max(0, h - (y + bh)) + 4  # 多留 4px 余量
    else:
        cut = int(round(h * args.percent))

    cut = min(cut, int(h * 0.25))  # 保护性上限，别把画面裁没了

    box = (0, 0, w, h - cut)
    out_img = img.crop(box)

    if args.keep_ratio:
        target_h = h - cut
        target_w = int(round(target_h * (w / h)))
        if target_w < w:
            left = (w - target_w) // 2
            out_img = out_img.crop((left, 0, left + target_w, target_h))

    if args.out:
        out_path = args.out
    else:
        root, ext = os.path.splitext(args.image)
        out_path = root + "_clean" + (ext or ".png")

    out_img.save(out_path, quality=95)
    print("已裁掉底部 {}px，输出：{}（{}x{}）".format(
        cut, out_path, out_img.size[0], out_img.size[1]))


if __name__ == "__main__":
    main()
