#!/usr/bin/env python3
import sys
import os
import json
import time
import argparse

def detect(model_path, image_path, confidence=0.5, output_dir=""):
    start_time = time.time()
    
    if not os.path.exists(model_path):
        return {
            "success": False,
            "error": f"模型文件不存在: {model_path}",
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
        from ultralytics import YOLO
        
        model = YOLO(model_path)
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
            
            filename = "analyzed_" + os.path.basename(image_path)
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

def main():
    parser = argparse.ArgumentParser(description='Box Detector CLI')
    parser.add_argument('--model', required=True, help='Model path (.pt or .onnx)')
    parser.add_argument('--image', required=True, help='Image path')
    parser.add_argument('--confidence', type=float, default=0.5, help='Confidence threshold')
    parser.add_argument('--output', default='', help='Output directory')
    
    args = parser.parse_args()
    
    result = detect(args.model, args.image, args.confidence, args.output)
    print(json.dumps(result))

if __name__ == '__main__':
    main()