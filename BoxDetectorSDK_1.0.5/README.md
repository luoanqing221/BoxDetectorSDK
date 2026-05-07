# BoxDetectorSDK

用于箱子检测的 SDK，通过 ONNX Runtime 进行高效推理。

## 编译

请参考 [BUILD.md](BUILD.md) 中的编译指南。

## 文件结构

```
BoxDetectorSDK/
├── include/
│   └── BoxDetectorSDK.h      # C++头文件
├── examples/
│   └── BoxDetectorExample.cpp # C++使用示例
├── BoxDetectorSDK.cpp         # C++实现
├── BoxDetectorSDK.cs          # C#封装类
├── CMakeLists.txt             # CMake构建配置
├── BUILD.md                   # 编译指南
└── build_windows.bat          # Windows编译脚本
```

## C# 使用

### 1. 添加文件
- 将 `BoxDetectorSDK.cs` 添加到 C# 项目

### 2. 复制 DLL
- 将编译产生的 DLL 复制到程序输出目录
- 需要的 DLL：`BoxDetectorSDK.dll`, `opencv_world490.dll`, `onnxruntime.dll`

### 3. 完整调用示例

#### 基础用法（同步）

```csharp
using BoxDetectorSDK;
using System.Collections.Generic;

// ============================================================================
// 第一步：加载模型（同步操作，阻塞线程）
// 说明：模型只需加载一次，建议在程序启动时调用
// 耗时：约 500ms - 2000ms（取决于模型大小）
// ============================================================================
bool loadSuccess = BoxDetector.LoadModel("model.onnx");
if (!loadSuccess) {
    Console.WriteLine("模型加载失败！");
    return;
}

try {
    // ========================================================================
    // 第二步：检测图片（同步操作，阻塞线程）
    // 说明：推理过程是同步的，但结果图保存是异步的
    // 耗时：约 30ms - 100ms/张（取决于图片大小和GPU性能）
    // ========================================================================
    
    // 方式A：不保存结果图（更快）
    var images = new List<string> { "image1.jpg", "image2.jpg", "image3.jpg" };
    var results = BoxDetector.Detect(images, 0.5f);  // outputDir=null，跳过绘制保存
    
    // 遍历检测结果
    foreach (var result in results) {
        if (result.Success) {
            Console.WriteLine($"图片: {result.ImagePath}");
            Console.WriteLine($"尺寸: {result.ImageWidth}x{result.ImageHeight}");
            Console.WriteLine($"箱子数量: {result.Boxes.Count}");
            Console.WriteLine($"推理耗时: {result.AnalysisTimeMs}ms");
            
            foreach (var box in result.Boxes) {
                Console.WriteLine($"  箱子{box.Index}: 位置({box.X}, {box.Y}), 尺寸 {box.Width}x{box.Height}, 置信度 {box.Confidence:F2}");
            }
        } else {
            Console.WriteLine($"图片: {result.ImagePath} - 检测失败: {result.Error}");
        }
    }
    
    // 方式B：保存结果图（带异步保存）
    var resultsWithSave = BoxDetector.Detect(images, 0.5f, "./output");
    // 注意：Detect 返回时，图片可能还在后台保存中
    // 如需等待保存完成，可检查 result.ResultImagePath 是否为空
}
finally {
    // ========================================================================
    // 第三步：卸载模型（同步操作，阻塞线程）
    // 说明：释放模型占用的内存，建议在程序退出时调用
    // ========================================================================
    BoxDetector.UnloadModel();
}
```

#### 完整示例（带异步保存说明）

```csharp
using BoxDetectorSDK;
using System.Collections.Generic;
using System.IO;

// 加载模型
BoxDetector.LoadModel("model.onnx");

try {
    // 检测并保存结果图
    var images = new List<string> { "test.jpg" };
    var results = BoxDetector.Detect(images, 0.5f, "./output");
    
    if (results[0].Success) {
        Console.WriteLine($"检测完成，耗时: {results[0].AnalysisTimeMs}ms");
        
        // 结果图路径（异步保存，可能尚未写入磁盘）
        string outputPath = results[0].ResultImagePath;
        
        // 如果需要等待图片保存完成，可轮询检查文件是否存在
        if (!string.IsNullOrEmpty(outputPath)) {
            int waitCount = 0;
            while (!File.Exists(outputPath) && waitCount < 100) {
                System.Threading.Thread.Sleep(10);
                waitCount++;
            }
            Console.WriteLine($"结果图已保存: {outputPath}");
        }
    }
}
finally {
    BoxDetector.UnloadModel();
}
```

### API 说明

| 方法 | 同步/异步 | 说明 |
|------|----------|------|
| `LoadModel(modelPath)` | **同步** | 加载模型到内存（只需调用一次） |
| `UnloadModel()` | **同步** | 卸载模型，释放内存 |
| `IsModelLoaded()` | **同步** | 检查模型是否已加载 |
| `Detect(imagePaths, confidence, outputDir)` | **同步推理，异步保存** | 检测图片列表 |

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `imagePaths` | `List<string>` | - | 图片路径列表（支持单张或多张） |
| `confidence` | `float` | 0.5f | 置信度阈值（0.0-1.0） |
| `outputDir` | `string` | null | 输出目录（为null/空时不保存结果图） |

### 返回值说明

| 属性 | 类型 | 说明 |
|------|------|------|
| `Success` | `bool` | 检测是否成功 |
| `Error` | `string` | 错误信息（失败时返回） |
| `ImagePath` | `string` | 原始图片路径 |
| `ImageWidth` | `int` | 图片宽度 |
| `ImageHeight` | `int` | 图片高度 |
| `Boxes` | `List<BoxInfo>` | 检测到的箱子列表 |
| `ResultImagePath` | `string` | 结果图路径（异步保存，可能尚未就绪） |
| `AnalysisTimeMs` | `double` | 推理耗时（毫秒） |

## C++ 使用

### 完整调用示例

```cpp
#include "BoxDetectorSDK.h"
#include <vector>
#include <iostream>

int main() {
    // ========================================================================
    // 第一步：加载模型（同步）
    // ========================================================================
    bool loaded = BoxDetectorSDK::BoxDetector::LoadModel("model.onnx");
    if (!loaded) {
        std::cerr << "模型加载失败！" << std::endl;
        return 1;
    }
    
    try {
        // ====================================================================
        // 第二步：检测图片（同步推理，异步保存）
        // ====================================================================
        std::vector<std::string> images = {"image1.jpg", "image2.jpg"};
        
        // 不保存结果图
        auto results = BoxDetectorSDK::BoxDetector::BatchDetect(images, 0.5f, "");
        
        for (const auto& result : results) {
            if (result.success) {
                std::cout << "图片: " << result.imagePath << std::endl;
                std::cout << "箱子数量: " << result.boxes.size() << std::endl;
                std::cout << "耗时: " << result.analysisTimeMs << "ms" << std::endl;
            }
        }
        
        // 保存结果图（异步）
        auto resultsWithSave = BoxDetectorSDK::BoxDetector::BatchDetect(images, 0.5f, "./output");
        
    } catch (const std::exception& e) {
        std::cerr << "检测异常: " << e.what() << std::endl;
    }
    
    // ========================================================================
    // 第三步：卸载模型（同步）
    // ========================================================================
    BoxDetectorSDK::BoxDetector::UnloadModel();
    
    return 0;
}
```

## 同步与异步说明

### 同步操作（阻塞调用线程）

| 操作 | 说明 |
|------|------|
| `LoadModel()` | 加载模型到内存，需等待完成 |
| `UnloadModel()` | 释放模型内存，需等待完成 |
| `IsModelLoaded()` | 检查模型状态，立即返回 |
| `Detect()` 推理部分 | ONNX 推理计算，需等待完成 |

### 异步操作（后台执行，不阻塞）

| 操作 | 说明 |
|------|------|
| **结果图绘制与保存** | 当指定 `outputDir` 时，绘制和保存操作在后台线程池执行 |
| **线程池复用** | 使用固定大小线程池，减少线程创建开销 |

### 关键备注

```
┌─────────────────────────────────────────────────────────────────────┐
│                        调用时序图                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   [主线程]                                                          │
│        │                                                            │
│        ▼                                                            │
│   LoadModel() ──────────────────────────► 阻塞等待模型加载完成        │
│        │                                                            │
│        ▼                                                            │
│   Detect() ─────────────────────────────► 阻塞等待推理完成           │
│        │                                                            │
│        │    [线程池]                                                │
│        │         │                                                  │
│        │         ▼                                                  │
│        │    绘制结果图 ──► 保存图片 ──► 完成（后台异步执行）          │
│        ▼                                                            │
│   返回结果（ResultImagePath 可能尚未就绪）                            │
│        │                                                            │
│        ▼                                                            │
│   UnloadModel() ────────────────────────► 阻塞等待资源释放           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 性能优化说明

| 优化项 | 说明 | 效果 |
|--------|------|------|
| **模型缓存** | 模型只需加载一次，后续调用直接使用 | 避免重复加载耗时 |
| **异步保存** | 结果图绘制保存在后台线程执行 | 不阻塞主线程，提升响应速度 |
| **跳过绘制** | 无输出目录时不绘制保存 | 减少约 10-30ms/张耗时 |
| **线程池** | 复用线程执行异步任务 | 减少线程创建销毁开销 |

## 输出文件名格式

检测结果图片命名规则：
```
{原文件名}_detected_{箱子数量}_boxes_{时间戳}.{扩展名}
```

示例：
- 输入：`test.jpg`
- 输出：`test_detected_3_boxes_1715100000.jpg`

## 使用场景建议

### 场景1：单次调用（适合几分钟调用一次）

```csharp
// 每次调用都加载/卸载模型（简单但开销较大）
BoxDetector.LoadModel("model.onnx");
var results = BoxDetector.Detect(images);
BoxDetector.UnloadModel();
```

### 场景2：多次调用（适合高频检测）

```csharp
// 程序启动时加载一次模型
BoxDetector.LoadModel("model.onnx");

// 多次检测共享模型（推荐）
for (int i = 0; i < 100; i++) {
    var results = BoxDetector.Detect(images);
    // 处理结果...
}

// 程序退出时卸载模型
BoxDetector.UnloadModel();
```

## 许可证

MIT License