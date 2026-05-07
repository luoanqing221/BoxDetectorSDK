# BoxDetectorSDK

用于箱子检测的 SDK，支持通过 ONNX Runtime 进行推理。

## 快速开始

### C# 使用

**1. 添加文件**

将 `BoxDetectorSDK.cs` 添加到您的 C# 项目中。

**2. 复制运行时文件**

将以下 DLL 文件复制到程序输出目录：
- `BoxDetectorSDK.dll`
- `opencv_world490.dll`
- `onnxruntime.dll`

**3. 调用示例**

```csharp
using BoxDetectorSDK;

var result = BoxDetector.Detect(
    "model.onnx",    // ONNX模型路径
    "image.jpg",     // 输入图片路径
    0.5f,            // 置信度阈值（可选，默认0.5）
    "./output"       // 输出目录（可选，默认./output）
);

if (result.Success) {
    foreach (var box in result.Boxes) {
        // box.index - 箱子索引
        // box.x, box.y - 左上角坐标
        // box.width, box.height - 尺寸
        // box.confidence - 置信度
    }
} else {
    Console.WriteLine($"检测失败: {result.Error}");
}
```

## API 说明

### 函数签名

```csharp
AnalyzeResult Detect(string modelPath, string imagePath, float confidence = 0.5f, string outputDir = "")
```

### 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| modelPath | string | ONNX 模型文件路径 |
| imagePath | string | 输入图片路径 |
| confidence | float | 置信度阈值（默认 0.5） |
| outputDir | string | 结果输出目录（默认 ./output） |

### 返回值结构

```csharp
public struct BoxInfo {
    public int index;         // 箱子索引（从0开始）
    public double x;          // 左上角X坐标（像素）
    public double y;          // 左上角Y坐标（像素）
    public double width;      // 宽度（像素）
    public double height;     // 高度（像素）
    public double confidence; // 置信度（0-1之间）
}

public class AnalyzeResult {
    public bool Success;           // 是否成功
    public string Error;           // 错误信息（空表示无错误）
    public int ImageWidth;         // 图片宽度（像素）
    public int ImageHeight;        // 图片高度（像素）
    public List<BoxInfo> Boxes;    // 检测到的箱子列表
    public string ResultImagePath; // 结果图片路径（保存后才有值）
    public double AnalysisTimeMs;  // 分析耗时（毫秒）
    public string ImagePath;       // 原始图片路径
}
```

### JSON 返回值示例

```json
{
    "success": true,
    "error": "",
    "imageWidth": 1920,
    "imageHeight": 1280,
    "boxes": [
        {
            "index": 0,
            "x": 759,
            "y": 450,
            "width": 568,
            "height": 462,
            "confidence": 0.9661096334457397
        }
    ],
    "resultImagePath": "",
    "analysisTimeMs": 0,
    "imagePath": "/path/to/image.jpg"
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| success | bool | 检测是否成功 |
| error | string | 错误信息（空字符串表示无错误） |
| imageWidth | int | 图片宽度（像素） |
| imageHeight | int | 图片高度（像素） |
| boxes | array | 检测到的箱子列表 |
| boxes[].index | int | 箱子索引（从0开始） |
| boxes[].x | int | 左上角X坐标（像素） |
| boxes[].y | int | 左上角Y坐标（像素） |
| boxes[].width | int | 箱子宽度（像素） |
| boxes[].height | int | 箱子高度（像素） |
| boxes[].confidence | float | 置信度（0-1之间，越接近1越可信） |
| resultImagePath | string | 结果图片路径（保存后才有值） |
| analysisTimeMs | float | 分析耗时（毫秒） |
| imagePath | string | 原始图片路径 |

## C++ 使用

**1. 包含头文件**

```cpp
#include "BoxDetectorSDK.h"
```

**2. 链接库**

- 链接 `BoxDetectorSDK.lib`
- 运行时需要 `BoxDetectorSDK.dll`

**3. 调用示例**

```cpp
auto result = BoxDetectorSDK::BoxDetector::Analyze(
    "model.onnx",
    "image.jpg",
    0.5f,
    "./output"
);

if (result.success) {
    for (const auto& box : result.boxes) {
        // box.x, box.y - 左上角坐标
        // box.width, box.height - 尺寸
        // box.confidence - 置信度
    }
}
```

## 文件结构

```
BoxDetectorSDK/
├── include/
│   └── BoxDetectorSDK.h        # C++头文件
├── BoxDetectorSDK.cs           # C#封装类
├── README.md                   # 使用说明（本文件）
└── RUNTIME_DEPENDENCIES.md     # 运行时依赖说明
```

## 构建说明

如果需要自行编译 DLL：

### 依赖要求

- OpenCV 4.x (x64)
- ONNX Runtime (x64)
- Visual Studio 2022
- CMake 3.16+

### 构建步骤

```bash
mkdir build && cd build
cmake -G "Visual Studio 17 2022" .. ^
    -DOpenCV_DIR=C:/opencv/build ^
    -DONNXRuntime_DIR=C:/onnxruntime/lib/cmake/ONNXRuntime
cmake --build . --config Release
```

## 模型转换

使用 `convert_to_onnx.py` 将 YOLO 模型转换为 ONNX 格式：

```bash
python convert_to_onnx.py model.pt
```

## 注意事项

1. 运行时需要将 `BoxDetectorSDK.dll`、`opencv_world490.dll`、`onnxruntime.dll` 放在同一目录
2. 支持的图片格式：JPG、PNG、BMP
3. 模型必须是 ONNX 格式
4. 置信度阈值建议范围：0.3-0.7

## 技术支持

如有问题，请联系开发人员。