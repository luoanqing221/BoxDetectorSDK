#!/usr/bin/env python3
import sys
import os
import threading
import time
from flask import Flask, request, jsonify
from ultralytics import YOLO

app = Flask(__name__)
model = None
model_path = ""

def load_model(path):
    global model
    global model_path
    if model is None or model_path != path:
        model = YOLO(path)
        model_path = path
        print(f"模型加载完成: {path}")

@app.route('/detect', methods=['POST'])
def detect():
    try:
        data = request.get_json()
        image_path = data.get('image_path')
        confidence = data.get('confidence', 0.5)
        output_dir = data.get('output_dir', '')
        
        if not image_path:
            return jsonify({"success": False, "error": "缺少 image_path 参数"}), 400
            
        if not os.path.exists(image_path):
            return jsonify({"success": False, "error": f"图片文件不存在: {image_path}"}), 400
            
        if model is None:
            return jsonify({"success": False, "error": "模型未加载"}), 500
            
        results = model.predict(image_path, conf=confidence, verbose=False)
        
        boxes_info = []
        img_width = 0
        img_height = 0
        
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
            if hasattr(result, "orig_shape"):
                img_height, img_width = result.orig_shape
        
        result_dict = {
            "success": True,
            "error": "",
            "imageWidth": img_width,
            "imageHeight": img_height,
            "boxes": boxes_info,
            "resultImagePath": "",
            "analysisTimeMs": 0,
            "imagePath": image_path
        }
        
        return jsonify(result_dict)
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/load_model', methods=['POST'])
def load_model_api():
    try:
        data = request.get_json()
        model_path_param = data.get('model_path')
        
        if not model_path_param:
            return jsonify({"success": False, "error": "缺少 model_path 参数"}), 400
            
        if not os.path.exists(model_path_param):
            return jsonify({"success": False, "error": f"模型文件不存在: {model_path_param}"}), 400
            
        load_model(model_path_param)
        
        return jsonify({"success": True, "error": "", "message": "模型加载成功"})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "model_loaded": model is not None,
        "model_path": model_path,
        "status": "running"
    })

def start_server(host='127.0.0.1', port=5000, initial_model_path=None):
    if initial_model_path and os.path.exists(initial_model_path):
        load_model(initial_model_path)
    
    print(f"服务启动: http://{host}:{port}")
    app.run(host=host, port=port, threaded=True, debug=False, use_reloader=False)

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5000
    initial_model = None
    
    for arg in sys.argv[1:]:
        if arg.startswith('--host='):
            host = arg.split('=')[1]
        elif arg.startswith('--port='):
            port = int(arg.split('=')[1])
        elif arg.startswith('--model='):
            initial_model = arg.split('=')[1]
    
    start_server(host, port, initial_model)