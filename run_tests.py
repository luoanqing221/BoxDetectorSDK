#!/usr/bin/env python3
import subprocess
import json
import sys
import os

def test_detection():
    model_path = "/Users/luoanqing/Desktop/样本 1/best.onnx"
    test_images = [
        "/Users/luoanqing/Desktop/样本 1/Image_20260429170036016.bmp",
        "/Users/luoanqing/Desktop/样本 1/Image_20260429170134802.bmp",
        "/Users/luoanqing/Desktop/样本 1/Image_20260429170235958.bmp"
    ]
    conf_threshold = 0.5
    
    print("=== 接口测试工具自动测试 ===")
    print()
    
    all_passed = True
    
    for image_path in test_images:
        print(f"测试图片: {os.path.basename(image_path)}")
        
        script_content = '''
import sys
import json
from ultralytics import YOLO

model = YOLO("%s")
results = model.predict("%s", conf=%f, verbose=False)

boxes_info = []
for result in results:
    boxes = result.boxes
    for idx, box in enumerate(boxes):
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = box.conf[0].item()
        boxes_info.append({
            "index": idx,
            "x1": int(x1),
            "y1": int(y1),
            "x2": int(x2),
            "y2": int(y2),
            "confidence": float(conf)
        })

print(json.dumps(boxes_info))
''' % (model_path, image_path, conf_threshold)

        result = subprocess.run([sys.executable, "-c", script_content], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"  ❌ 检测失败: {result.stderr}")
            all_passed = False
            continue
            
        output_lines = result.stdout.strip().split('\n')
        json_line = None
        for line in output_lines:
            if line.strip().startswith('{') or line.strip().startswith('['):
                json_line = line.strip()
                break
        
        if not json_line:
            print(f"  ❌ 无法找到 JSON 输出")
            all_passed = False
            continue
            
        try:
            boxes_info = json.loads(json_line)
            print(f"  ✅ 检测成功，找到 {len(boxes_info)} 个箱子")
            for box in boxes_info:
                print(f"    - 箱子 {box['index']}: 位置({box['x1']},{box['y1']}), 尺寸 {box['x2']-box['x1']}x{box['y2']-box['y1']}, 置信度 {box['confidence']:.2f}")
        except Exception as e:
            print(f"  ❌ JSON 解析失败: {e}")
            all_passed = False
            
        print()
    
    if all_passed:
        print("=== 所有测试通过！===")
    else:
        print("=== 部分测试失败 ===")
    
    return all_passed

if __name__ == "__main__":
    success = test_detection()
    sys.exit(0 if success else 1)