# BoxDetectorSDK

用于箱子检测的 SDK，通过 ONNX Runtime 进行高效推理。

## 自动编译

本项目使用 GitHub Actions 自动编译 Windows DLL，无需手动配置编译环境。

### 使用方法

**1. Fork 或上传本项目到 GitHub**

**2. 触发编译**
- 方式一：推送代码到 `main` 分支
- 方式二：在 GitHub 仓库页面点击 `Actions` → `Build Windows DLL` → `Run workflow`
- 方式三：创建 tag（如 `v1.0.0`）会自动创建 Release

**3. 下载编译产物**
- 编译完成后，在 `Actions` → 对应的 workflow → `Artifacts` 中下载 `BoxDetectorSDK-Windows-x64.zip`
- 如果创建了 tag，会在 `Releases` 页面自动发布

## 分发包内容

```
BoxDetectorSDK-Windows-x64/
├── bin/
│   ├── BoxDetectorSDK.dll    # 核心库
│   ├── opencv_world490.dll   # OpenCV 运行时
│   └── onnxruntime.dll       # ONNX Runtime 运行时
├── lib/
│   └── BoxDetectorSDK.lib    # 导入库（C++使用）
├── include/
│   └── BoxDetectorSDK.h      # C++头文件
├── BoxDetectorSDK.cs         # C#封装类
└── README.md                 # 使用说明
```

## C# 使用

**1. 添加文件**
- 将 `BoxDetectorSDK.cs` 添加到 C# 项目

**2. 复制 DLL**
- 将 `bin/` 目录中的所有 DLL 复制到程序输出目录

**3. 调用示例**

```csharp
using BoxDetectorSDK;

var result = BoxDetector.Detect(
    "model.onnx",    // ONNX模型路径
    "image.jpg",     // 输入图片路径
    0.5f,            // 置信度阈值
    "./output"       // 输出目录
);

if (result.Success) {
    foreach (var box in result.Boxes) {
        Console.WriteLine($"箱子 {box.index}: 位置({box.x}, {box.y}), 尺寸 {box.width}x{box.height}");
    }
}
```

## 模型转换

使用 `convert_to_onnx.py` 将 YOLO 模型转换为 ONNX 格式：

```bash
python convert_to_onnx.py model.pt
```

## 本地测试

```bash
# 安装依赖
pip install ultralytics opencv-python onnxruntime PyQt5

# 运行测试工具
python test_gui.py

# 运行模型转换工具
python convert_gui.py
```

## 项目结构

```
├── .github/workflows/build.yml  # GitHub Actions 编译配置
├── BoxDetectorSDK.cpp           # C++ 实现
├── BoxDetectorSDK.h             # C++ 头文件
├── BoxDetectorSDK.cs            # C# 封装
├── CMakeLists.txt               # CMake 配置
├── convert_to_onnx.py           # 模型转换工具
├── convert_gui.py               # 模型转换 GUI
├── test_gui.py                  # 测试工具 GUI
└── dist/                        # 分发文件
    ├── README.md
    ├── BoxDetectorSDK.cs
    └── include/BoxDetectorSDK.h
```