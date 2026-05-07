#!/usr/bin/env python3
import sys
import os
import json
import time
import argparse
from typing import List, Dict, Optional

_model_cache = {}

def load_model(model_path: str) -> bool:
    """加载模型到缓存"""
    global _model_cache
    
    if not os.path.exists(model_path):
        return False
    
    try:
        from ultralytics import YOLO
        _model_cache['model'] = YOLO(model_path)
        _model_cache['path'] = model_path
        return True
    except Exception as e:
        print(f"模型加载失败: {e}", file=sys.stderr)
        return False

def unload_model():
    """卸载模型"""
    global _model_cache
    _model_cache.clear()

def is_model_loaded() -> bool:
    """检查模型是否已加载"""
    return 'model' in _model_cache

def detect_single(image_path: str, confidence: float = 0.5, output_dir: str = "") -> Dict:
    """检测单张图片"""
    start_time = time.time()
    
    if not is_model_loaded():
        return {
            "success": False,
            "error": "模型未加载，请先调用 load_model()",
            "imageWidth": 0,
            "imageHeight": 0,
            "boxes": [],
            "resultImagePath": "",
            "analysisTimeMs": 0,
            "imagePath": image_path
        }
    
    if not os.path.exists(image_path):
        return {
            "success": False,
            "error": f"图片文件不存在: {image_path}",
            "imageWidth": 0,
            "imageHeight": 0,
            "boxes": [],
            "resultImagePath": "",
            "analysisTimeMs": 0,
            "imagePath": image_path
        }
    
    try:
        import cv2
        
        model = _model_cache['model']
        results = model.predict(image_path, conf=confidence, verbose=False)
        
        boxes_info = []
        img_width = 0
        img_height = 0
        
        image = cv2.imread(image_path)
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
        
        result_image_path = ""
        
        if output_dir and image is not None:
            os.makedirs(output_dir, exist_ok=True)
            
            result_img = image.copy()
            for box in boxes_info:
                x, y = box['x'], box['y']
                w, h = box['width'], box['height']
                conf = box['confidence']
                
                cv2.rectangle(result_img, (x, y), (x + w, y + h), (74, 144, 217), 2)
                label = f"({x},{y}) W={w} H={h} Conf={conf:.2f}"
                cv2.putText(result_img, label, (x, max(0, y - 10)),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            ext = os.path.splitext(image_path)[1]
            timestamp = int(time.time())
            filename = f"{base_name}_detected_{len(boxes_info)}_boxes_{timestamp}{ext}"
            result_image_path = os.path.abspath(os.path.join(output_dir, filename))
            cv2.imwrite(result_image_path, result_img)
        
        elapsed_ms = (time.time() - start_time) * 1000
        
        return {
            "success": True,
            "error": "",
            "imageWidth": img_width,
            "imageHeight": img_height,
            "boxes": boxes_info,
            "resultImagePath": result_image_path,
            "analysisTimeMs": round(elapsed_ms, 2),
            "imagePath": image_path
        }
        
    except Exception as e:
        elapsed_ms = (time.time() - start_time) * 1000
        return {
            "success": False,
            "error": str(e),
            "imageWidth": 0,
            "imageHeight": 0,
            "boxes": [],
            "resultImagePath": "",
            "analysisTimeMs": round(elapsed_ms, 2),
            "imagePath": image_path
        }

def batch_detect(image_paths: List[str], confidence: float = 0.5, output_dir: str = "") -> List[Dict]:
    """批量检测多张图片"""
    results = []
    for image_path in image_paths:
        result = detect_single(image_path, confidence, output_dir)
        results.append(result)
    return results

def main():
    parser = argparse.ArgumentParser(description='Box Detector CLI - 模拟C++接口')
    parser.add_argument('--model', required=True, help='模型路径 (.pt 或 .onnx)')
    parser.add_argument('--images', required=True, nargs='+', help='图片路径列表（支持多张）')
    parser.add_argument('--confidence', type=float, default=0.5, help='置信度阈值 (默认: 0.5)')
    parser.add_argument('--output', default='', help='输出目录（为空则不保存结果图）')
    
    args = parser.parse_args()
    
    load_start = time.time()
    if not load_model(args.model):
        result = {
            "success": False,
            "error": f"模型加载失败: {args.model}",
            "imageWidth": 0,
            "imageHeight": 0,
            "boxes": [],
            "resultImagePath": "",
            "analysisTimeMs": 0,
            "imagePath": ""
        }
        print(json.dumps([result]))
        return
    
    load_time = (time.time() - load_start) * 1000
    
    results = batch_detect(args.images, args.confidence, args.output)
    
    output = {
        "modelLoadTimeMs": round(load_time, 2),
        "results": results
    }
    
    print(json.dumps(output, indent=2, ensure_ascii=False))
    
    unload_model()

if __name__ == '__main__':
    main()
