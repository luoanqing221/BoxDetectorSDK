#!/usr/bin/env python3
import subprocess
import json
import os

def test_cli():
    model_path = "/Users/luoanqing/Desktop/样本 1/best.onnx"
    image_path = "/Users/luoanqing/Desktop/样本 1/Image_20260429170036016.bmp"
    output_dir = "/Users/luoanqing/Desktop/输出"
    confidence = 0.5
    
    print("=== 验证 CLI 接口 ===")
    print(f"模型: {model_path}")
    print(f"图片: {image_path}")
    print(f"输出目录: {output_dir}")
    print()
    
    cmd = [
        "/Users/luoanqing/Library/Python/3.9/bin/python3",
        "/Users/luoanqing/Desktop/Model inference C++/box_detector_cli.py",
        "--model", model_path,
        "--image", image_path,
        "--confidence", str(confidence),
        "--output", output_dir
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"CLI 调用失败: {result.stderr}")
        return None
    
    output_lines = result.stdout.strip().split('\n')
    json_line = None
    for line in output_lines:
        if line.strip().startswith('{'):
            json_line = line.strip()
            break
    
    if not json_line:
        print("无法找到 JSON 输出")
        return None
    
    cli_result = json.loads(json_line)
    print("CLI 返回结果:")
    print(json.dumps(cli_result, indent=2, ensure_ascii=False))
    print()
    
    return cli_result

def test_gui_logic():
    model_path = "/Users/luoanqing/Desktop/样本 1/best.onnx"
    image_path = "/Users/luoanqing/Desktop/样本 1/Image_20260429170036016.bmp"
    confidence = 0.5
    
    print("=== 验证测试工具逻辑 ===")
    print()
    
    script_content = '''
import sys
import json
import time
from ultralytics import YOLO

start_time = time.time()

model = YOLO("%s")
results = model.predict("%s", conf=%f, verbose=False)

elapsed_ms = (time.time() - start_time) * 1000

boxes_info = []
img_width = 0
img_height = 0

import cv2
image = cv2.imread("%s")
if image is not None:
    img_height, img_width = image.shape[:2]

for result in results:
    boxes = result.boxes
    for idx, box in enumerate(boxes):
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = box.conf[0].item()
        boxes_info.append({
            "index": idx,
            "x": int(x1),
            "y": int(y1),
            "width": int(x2 - x1),
            "height": int(y2 - y1),
            "confidence": float(conf)
        })

result_dict = {
    "success": True,
    "error": "",
    "imageWidth": img_width,
    "imageHeight": img_height,
    "boxes": boxes_info,
    "resultImagePath": "",
    "analysisTimeMs": round(elapsed_ms, 2),
    "imagePath": "%s"
}

print(json.dumps(result_dict))
''' % (model_path, image_path, confidence, image_path, image_path)
    
    result = subprocess.run(["/Users/luoanqing/Library/Python/3.9/bin/python3", "-c", script_content], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"测试工具逻辑调用失败: {result.stderr}")
        return None
    
    output_lines = result.stdout.strip().split('\n')
    json_line = None
    for line in output_lines:
        if line.strip().startswith('{'):
            json_line = line.strip()
            break
    
    if not json_line:
        print("无法找到 JSON 输出")
        return None
    
    gui_result = json.loads(json_line)
    print("测试工具逻辑返回结果:")
    print(json.dumps(gui_result, indent=2, ensure_ascii=False))
    print()
    
    return gui_result

def compare_results(cli_result, gui_result):
    print("=== 结果对比 ===")
    
    if cli_result is None or gui_result is None:
        print("❌ 无法进行对比")
        return False
    
    # 比较 success
    if cli_result['success'] != gui_result['success']:
        print("❌ success 不一致")
        return False
    
    # 比较图片尺寸
    if cli_result['imageWidth'] != gui_result['imageWidth'] or cli_result['imageHeight'] != gui_result['imageHeight']:
        print("❌ 图片尺寸不一致")
        return False
    
    # 比较箱子数量
    cli_boxes = cli_result.get('boxes', [])
    gui_boxes = gui_result.get('boxes', [])
    
    if len(cli_boxes) != len(gui_boxes):
        print(f"❌ 箱子数量不一致: CLI={len(cli_boxes)}, GUI={len(gui_boxes)}")
        return False
    
    # 比较每个箱子
    for i, (cli_box, gui_box) in enumerate(zip(cli_boxes, gui_boxes)):
        if cli_box['index'] != gui_box['index']:
            print(f"❌ 箱子 {i} index 不一致")
            return False
        if cli_box['x'] != gui_box['x'] or cli_box['y'] != gui_box['y']:
            print(f"❌ 箱子 {i} 位置不一致")
            return False
        if cli_box['width'] != gui_box['width'] or cli_box['height'] != gui_box['height']:
            print(f"❌ 箱子 {i} 尺寸不一致")
            return False
        if abs(cli_box['confidence'] - gui_box['confidence']) > 0.0001:
            print(f"❌ 箱子 {i} 置信度不一致")
            return False
    
    print("✅ 所有结果一致！")
    return True

if __name__ == "__main__":
    cli_result = test_cli()
    gui_result = test_gui_logic()
    compare_results(cli_result, gui_result)