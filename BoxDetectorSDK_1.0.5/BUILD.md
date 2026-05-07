# BoxDetectorSDK 编译指南

## 📋 环境要求

| 软件 | 版本 | 说明 |
|------|------|------|
| Windows | 10/11 | 64位系统 |
| Visual Studio | 2022 | 带 C++ 开发工具 |
| CMake | 3.16+ | 构建工具 |
| OpenCV | 4.9.0 | 图像处理库 |
| ONNX Runtime | 1.17.0 | 推理引擎 |

---

## 🚀 安装步骤

### 1. 安装 Visual Studio 2022

1. 下载：https://visualstudio.microsoft.com/zh-hans/downloads/
2. 安装时选择「使用 C++ 的桌面开发」工作负载
3. 确保勾选了 MSVC v143 构建工具

### 2. 安装 CMake

1. 下载：https://cmake.org/download/
2. 安装时勾选「Add CMake to system PATH」

### 3. 安装 OpenCV 4.9.0

1. **下载**：
   - 官网：https://opencv.org/releases/（选择 Windows 版本）
   - 国内镜像：https://repo.huaweicloud.com/opencv/
2. **安装**：运行安装程序，安装到 `C:\opencv`
3. **验证**：确保路径存在 `C:\opencv\build\x64\vc16\lib`

### 4. 安装 ONNX Runtime

1. **下载**：https://github.com/microsoft/onnxruntime/releases/download/v1.17.0/onnxruntime-win-x64-1.17.0.zip
2. **解压**：解压到 `C:\onnxruntime-win-x64-1.17.0`
3. **验证**：确保路径存在 `C:\onnxruntime-win-x64-1.17.0\lib` 和 `C:\onnxruntime-win-x64-1.17.0\include`

---

## 🔧 编译步骤

### 方法一：使用一键脚本（推荐）

1. 解压 `BoxDetectorSDK_Dist.zip`
2. 双击运行 `build_windows.bat`
3. 等待编译完成
4. 输出文件在 `dist/bin/` 目录下

### 方法二：手动编译（高级用户）

打开 **x64 Native Tools Command Prompt for VS 2022**，执行以下命令：

```cmd
:: 1. 设置环境变量
set OpenCV_DIR=C:\opencv\build\x64\vc16\lib
set ONNXRUNTIME_DIR=C:\onnxruntime-win-x64-1.17.0

:: 2. 创建构建目录
mkdir build
cd build

:: 3. 配置 CMake
cmake -G "Visual Studio 17 2022" -A x64 ^
    -DOpenCV_DIR=%OpenCV_DIR% ^
    -DONNXRUNTIME_INCLUDE_DIR=%ONNXRUNTIME_DIR%\include ^
    -DONNXRUNTIME_LIB_DIR=%ONNXRUNTIME_DIR%\lib ^
    ..

:: 4. 编译
cmake --build . --config Release

:: 5. 复制运行时库
mkdir dist\bin
copy Release\BoxDetectorSDK.dll dist\bin\
copy %OpenCV_DIR%\..\bin\opencv_world490.dll dist\bin\
copy %ONNXRUNTIME_DIR%\lib\onnxruntime.dll dist\bin\

echo 编译完成！输出文件在 dist\bin\ 目录下
```

### 方法三：使用 Visual Studio IDE

1. 执行方法二中的步骤 1-3
2. 打开 `build/BoxDetectorSDK.sln`
3. 在解决方案资源管理器中右键点击项目
4. 选择「生成」或按 Ctrl+Shift+B

---

## 📦 编译输出

```
build/
├── Release/
│   ├── BoxDetectorSDK.dll    # 核心库（必需）
│   ├── BoxDetectorSDK.lib    # 导入库（链接时用）
│   └── BoxDetectorExample.exe # 示例程序
└── dist/
    └── bin/
        ├── BoxDetectorSDK.dll      # 核心库
        ├── opencv_world490.dll     # OpenCV 运行时
        └── onnxruntime.dll         # ONNX Runtime 运行时
```

---

## ❗ 常见问题

### Q1: CMake 找不到 OpenCV

**错误信息：**
```
Could not find OpenCVConfig.cmake
```

**解决方案：**
确保环境变量 `OpenCV_DIR` 指向正确路径：
```cmd
set OpenCV_DIR=C:\opencv\build\x64\vc16\lib
```

### Q2: 编译时缺少 onnxruntime 头文件

**错误信息：**
```
fatal error C1083: 无法打开包括文件: "onnxruntime_cxx_api.h"
```

**解决方案：**
确保 ONNX Runtime 路径正确：
```cmd
set ONNXRUNTIME_DIR=C:\onnxruntime-win-x64-1.17.0
```

### Q3: 运行时缺少 DLL

**错误信息：**
```
找不到 opencv_world490.dll
```

**解决方案：**
将以下 DLL 复制到程序目录：
- `C:\opencv\build\x64\vc16\bin\opencv_world490.dll`
- `C:\onnxruntime-win-x64-1.17.0\lib\onnxruntime.dll`

### Q4: OpenCV_DIR 设置了还是找不到

**解决方案：**
检查 `C:\opencv\build\x64\vc16\lib` 目录下是否有 `OpenCVConfig.cmake` 文件。
如果没有，可能是安装路径不对，或需要重新安装 OpenCV。

---

## 📝 使用示例

### C++

```cpp
#include "BoxDetectorSDK.h"
#include <vector>

int main() {
    // 加载模型（只需调用一次）
    BoxDetectorSDK::BoxDetector::LoadModel("model.onnx");
    
    // 检测单张图片（不保存结果图）
    std::vector<std::string> images = {"image.jpg"};
    auto results = BoxDetectorSDK::BoxDetector::BatchDetect(images, 0.5f, "");
    
    if (results[0].success) {
        for (const auto& box : results[0].boxes) {
            std::cout << "Box: x=" << box.x << ", y=" << box.y 
                      << ", width=" << box.width << ", height=" << box.height 
                      << ", confidence=" << box.confidence << std::endl;
        }
    }
    
    // 检测并保存结果图
    auto resultsWithSave = BoxDetectorSDK::BoxDetector::BatchDetect(images, 0.5f, "./output");
    
    // 卸载模型（可选）
    BoxDetectorSDK::BoxDetector::UnloadModel();
    
    return 0;
}
```

### C#

```csharp
using BoxDetectorSDK;
using System.Collections.Generic;

// 加载模型（只需调用一次）
BoxDetector.LoadModel("model.onnx");

// 检测单张图片（不保存结果图）
var results = BoxDetector.Detect(new List<string> { "image.jpg" });

if (results[0].Success) {
    foreach (var box in results[0].Boxes) {
        Console.WriteLine($"Box: x={box.x}, y={box.y}, width={box.width}, height={box.height}, confidence={box.confidence}");
    }
}

// 检测并保存结果图
var resultsWithSave = BoxDetector.Detect(new List<string> { "image.jpg" }, 0.5f, "./output");

// 卸载模型（可选）
BoxDetector.UnloadModel();
```

### 批量检测示例

```csharp
// 批量检测多张图片
var images = new List<string> { "image1.jpg", "image2.jpg", "image3.jpg" };
var results = BoxDetector.Detect(images, 0.5f);

foreach (var result in results) {
    if (result.Success) {
        Console.WriteLine($"{result.ImagePath}: 检测到 {result.Boxes.Count} 个箱子, 耗时 {result.AnalysisTimeMs}ms");
    }
}
```

---

## 🛠️ 技术支持

如果遇到问题，请按以下顺序检查：

1. ✅ Visual Studio 是否安装了「使用 C++ 的桌面开发」工作负载
2. ✅ CMake 是否在系统 PATH 中
3. ✅ OpenCV_DIR 是否指向 `C:\opencv\build\x64\vc16\lib`
4. ✅ ONNXRUNTIME_DIR 是否指向 `C:\onnxruntime-win-x64-1.17.0`
5. ✅ 依赖库版本是否正确（OpenCV 4.9.0, ONNX Runtime 1.17.0）