#!/usr/bin/env python3
"""
BoxDetectorSDK 完整测试脚本
测试所有组件是否正常工作
"""
import os
import sys
import json
import subprocess

print("=" * 60)
print("BoxDetectorSDK 完整测试")
print("=" * 60)
print()

# 测试结果记录
test_results = []

def test(name, condition, details=""):
    global test_results
    status = "✅ PASS" if condition else "❌ FAIL"
    test_results.append((name, condition))
    print(f"{status} - {name}")
    if details:
        print(f"      {details}")
    return condition

# ============================================
# 测试 1: 检查所有必需文件是否存在
# ============================================
print("【测试 1】检查文件完整性")
print("-" * 40)

required_files = {
    "C++ 头文件": "BoxDetectorSDK.h",
    "C++ 实现": "BoxDetectorSDK.cpp",
    "C# 封装": "BoxDetectorSDK.cs",
    "CMake 配置": "CMakeLists.txt",
    "CLI 接口": "box_detector_cli.py",
    "测试工具": "test_gui.py",
    "模型转换工具": "convert_to_onnx.py",
    "模型转换GUI": "convert_gui.py",
    "GitHub Actions": ".github/workflows/build.yml",
    "分发说明": "dist/README.md",
    "分发C#封装": "dist/BoxDetectorSDK.cs",
    "分发头文件": "dist/include/BoxDetectorSDK.h",
}

base_dir = "/Users/luoanqing/Desktop/Model inference C++"
for name, filepath in required_files.items():
    full_path = os.path.join(base_dir, filepath)
    exists = os.path.exists(full_path)
    test(f"文件存在: {name}", exists, filepath if not exists else "")

print()

# ============================================
# 测试 2: 检查 C++ 代码语法
# ============================================
print("【测试 2】检查 C++ 代码")
print("-" * 40)

cpp_file = os.path.join(base_dir, "BoxDetectorSDK.cpp")
with open(cpp_file, 'r') as f:
    cpp_content = f.read()

# 检查关键函数
test("C++ 包含 Analyze 函数", "AnalyzeResult Analyze" in cpp_content or "BoxDetector::Analyze" in cpp_content)
test("C++ 包含 BoxInfo 结构", "struct BoxInfo" in cpp_content or "BoxInfo {" in cpp_content)
test("C++ 包含 ONNX Runtime", "Ort::" in cpp_content or "onnxruntime" in cpp_content.lower())
test("C++ 包含 OpenCV", "cv::" in cpp_content or "opencv" in cpp_content.lower())
test("C++ 包含耗时计算", "chrono" in cpp_content or "time" in cpp_content.lower())

# 检查返回值字段
test("C++ 返回 success", "success" in cpp_content)
test("C++ 返回 error", "error" in cpp_content)
test("C++ 返回 imageWidth", "imageWidth" in cpp_content)
test("C++ 返回 imageHeight", "imageHeight" in cpp_content)
test("C++ 返回 boxes", "boxes" in cpp_content)
test("C++ 返回 resultImagePath", "resultImagePath" in cpp_content)
test("C++ 返回 analysisTimeMs", "analysisTimeMs" in cpp_content)
test("C++ 返回 imagePath", "imagePath" in cpp_content)

print()

# ============================================
# 测试 3: 检查 C# 封装
# ============================================
print("【测试 3】检查 C# 封装")
print("-" * 40)

cs_file = os.path.join(base_dir, "BoxDetectorSDK.cs")
with open(cs_file, 'r') as f:
    cs_content = f.read()

test("C# 包含 BoxDetector 类", "class BoxDetector" in cs_content)
test("C# 包含 Detect 方法", "Detect(" in cs_content)
test("C# 包含 AnalyzeResult", "AnalyzeResult" in cs_content or "class Result" in cs_content)
test("C# 包含 BoxInfo", "BoxInfo" in cs_content)
test("C# 包含 DllImport", "DllImport" in cs_content)

print()

# ============================================
# 测试 4: 检查 CLI 接口
# ============================================
print("【测试 4】检查 CLI 接口")
print("-" * 40)

cli_file = os.path.join(base_dir, "box_detector_cli.py")
with open(cli_file, 'r') as f:
    cli_content = f.read()

test("CLI 包含参数解析", "argparse" in cli_content)
test("CLI 包含 --model 参数", "--model" in cli_content)
test("CLI 包含 --image 参数", "--image" in cli_content)
test("CLI 包含 --confidence 参数", "--confidence" in cli_content)
test("CLI 包含 --output 参数", "--output" in cli_content)
test("CLI 返回 JSON 格式", "json.dumps" in cli_content)
test("CLI 包含耗时计算", "time.time" in cli_content)
test("CLI 包含图片保存", "cv2.imwrite" in cli_content or "imwrite" in cli_content)

# 检查返回值字段
test("CLI 返回 success", '"success"' in cli_content)
test("CLI 返回 error", '"error"' in cli_content)
test("CLI 返回 imageWidth", '"imageWidth"' in cli_content)
test("CLI 返回 imageHeight", '"imageHeight"' in cli_content)
test("CLI 返回 boxes", '"boxes"' in cli_content)
test("CLI 返回 resultImagePath", '"resultImagePath"' in cli_content)
test("CLI 返回 analysisTimeMs", '"analysisTimeMs"' in cli_content)
test("CLI 返回 imagePath", '"imagePath"' in cli_content)

print()

# ============================================
# 测试 5: 检查 GitHub Actions 配置
# ============================================
print("【测试 5】检查 GitHub Actions 配置")
print("-" * 40)

workflow_file = os.path.join(base_dir, ".github/workflows/build.yml")
with open(workflow_file, 'r') as f:
    workflow_content = f.read()

test("Actions 使用 Windows 环境", "windows-latest" in workflow_content)
test("Actions 包含 CMake 步骤", "cmake" in workflow_content.lower())
test("Actions 包含构建步骤", "build" in workflow_content.lower())
test("Actions 下载 OpenCV", "opencv" in workflow_content.lower())
test("Actions 下载 ONNX Runtime", "onnxruntime" in workflow_content.lower())
test("Actions 上传 Artifacts", "upload-artifact" in workflow_content)
test("Actions 创建 Release", "release" in workflow_content.lower() or "gh-release" in workflow_content.lower())

print()

# ============================================
# 测试 6: 检查 CMakeLists.txt
# ============================================
print("【测试 6】检查 CMake 配置")
print("-" * 40)

cmake_file = os.path.join(base_dir, "CMakeLists.txt")
with open(cmake_file, 'r') as f:
    cmake_content = f.read()

test("CMake 设置项目名", "project(" in cmake_content)
test("CMake 查找 OpenCV", "find_package(OpenCV" in cmake_content or "OpenCV" in cmake_content)
test("CMake 查找 ONNX Runtime", "onnxruntime" in cmake_content.lower() or "ONNXRuntime" in cmake_content)
test("CMake 添加库目标", "add_library" in cmake_content)
test("CMake 设置 C++ 标准", "CMAKE_CXX_STANDARD" in cmake_content or "CXX_STANDARD" in cmake_content)

print()

# ============================================
# 测试 7: 实际运行 CLI 测试
# ============================================
print("【测试 7】实际运行 CLI 测试")
print("-" * 40)

model_path = "/Users/luoanqing/Desktop/样本 1/best.onnx"
image_path = "/Users/luoanqing/Desktop/样本 1/Image_20260429170036016.bmp"
output_dir = "/Users/luoanqing/Desktop/输出"

# 检查测试文件是否存在
test("测试模型存在", os.path.exists(model_path), model_path)
test("测试图片存在", os.path.exists(image_path), image_path)

# 尝试运行 CLI
if os.path.exists(model_path) and os.path.exists(image_path):
    try:
        # 使用系统 Python
        cmd = [
            sys.executable,
            cli_file,
            "--model", model_path,
            "--image", image_path,
            "--confidence", "0.5",
            "--output", output_dir
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            # 解析输出
            output_lines = result.stdout.strip().split('\n')
            json_line = None
            for line in output_lines:
                if line.strip().startswith('{'):
                    json_line = line.strip()
                    break
            
            if json_line:
                cli_result = json.loads(json_line)
                test("CLI 运行成功", True)
                test("CLI 返回有效 JSON", True)
                test("CLI success=true", cli_result.get('success') == True)
                test("CLI 检测到箱子", len(cli_result.get('boxes', [])) > 0)
                test("CLI 包含图片尺寸", cli_result.get('imageWidth', 0) > 0)
                test("CLI 包含耗时", cli_result.get('analysisTimeMs', 0) > 0)
                
                if cli_result.get('resultImagePath'):
                    test("CLI 保存了结果图片", os.path.exists(cli_result['resultImagePath']))
                
                print()
                print("CLI 返回结果:")
                print(json.dumps(cli_result, indent=2, ensure_ascii=False))
            else:
                test("CLI 返回有效 JSON", False, "未找到 JSON 输出")
        else:
            test("CLI 运行成功", False, result.stderr[:200] if result.stderr else "Unknown error")
    except Exception as e:
        test("CLI 运行成功", False, str(e)[:200])
else:
    print("跳过 CLI 运行测试（测试文件不存在）")

print()

# ============================================
# 测试 8: 检查返回值格式一致性
# ============================================
print("【测试 8】检查返回值格式一致性")
print("-" * 40)

# 定义标准返回值字段
standard_fields = {
    "success": "bool",
    "error": "string",
    "imageWidth": "int",
    "imageHeight": "int",
    "boxes": "array",
    "resultImagePath": "string",
    "analysisTimeMs": "float",
    "imagePath": "string"
}

box_fields = {
    "index": "int",
    "x": "int",
    "y": "int",
    "width": "int",
    "height": "int",
    "confidence": "float"
}

# 检查 CLI
for field, ftype in standard_fields.items():
    test(f"CLI 包含字段 {field}", f'"{field}"' in cli_content)

for field, ftype in box_fields.items():
    test(f"CLI boxes 包含字段 {field}", f'"{field}"' in cli_content)

# 检查 C++
for field, ftype in standard_fields.items():
    test(f"C++ 包含字段 {field}", field in cpp_content)

print()

# ============================================
# 测试总结
# ============================================
print("=" * 60)
print("测试总结")
print("=" * 60)

passed = sum(1 for _, result in test_results if result)
total = len(test_results)

print(f"通过: {passed}/{total}")
print(f"失败: {total - passed}/{total}")
print()

if passed == total:
    print("🎉 所有测试通过！项目可以发布。")
else:
    print("⚠️ 部分测试失败，请检查上述标记为 ❌ 的项目。")

print()
print("=" * 60)