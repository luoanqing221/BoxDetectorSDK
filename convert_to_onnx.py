import sys
from ultralytics import YOLO

def convert_to_onnx(model_path, output_path):
    model = YOLO(model_path)
    model.export(format='onnx', opset=13, simplify=True)
    print(f"模型已转换为 ONNX 格式: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python convert_to_onnx.py <model_path> [output_path]")
        sys.exit(1)
    
    model_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else model_path.replace('.pt', '.onnx')
    
    convert_to_onnx(model_path, output_path)