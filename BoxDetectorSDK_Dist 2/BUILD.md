# BoxDetectorSDK 编译指南

## 环境要求

| 软件 | 版本 | 说明 |
|------|------|------|
| Windows | 10/11 | 64位系统 |
| Visual Studio | 2022 | 带 C++ 开发工具 |
| CMake | 3.16+ | 构建工具 |
| OpenCV | 4.9.0 | 图像处理库 |
| ONNX Runtime | 1.17.0 | 推理引擎 |

---

## 安装步骤

### 1. 安装 Visual Studio 2022

1. 下载：https://visualstudio.microsoft.com/zh-hans/downloads/
2. 安装时选择「使用 C++ 的桌面开发」工作负载

### 2. 安装 CMake

1. 下载：https://cmake.org/download/
2. 安装时勾选「Add CMake to system PATH」

### 3. 安装 OpenCV 4.9.0

1. 下载：https://github.com/opencv/opencv/releases/download/4.9.0/opencv-4.9.0-windows.exe
2. 运行安装程序，安装到 `C:\opencv`

### 4. 安装 ONNX Runtime

1. 下载：https://github.com/microsoft/onnxruntime/releases/download/v1.17.0/onnxruntime-win-x64-1.17.0.zip
2. 解压到 `C:\onnxruntime-win-x64-1.17.0`

---

## 编译步骤

### 方法一：使用命令行

```cmd
@echo off
setlocal

:: 设置环境变量
set OpenCV_DIR=C:\opencv\build\x64\vc16\lib
set ONNXRuntime_DIR=C:\onnxruntime-win-x64-1.17.0\lib\cmake\onnxruntime

:: 创建构建目录
mkdir build
cd build

:: 配置 CMake
cmake -G "Visual Studio 17 2022" -A x64 ^
  -DOpenCV_DIR=%OpenCV_DIR% ^
  -DONNXRuntime_DIR=%ONNXRuntime_DIR% ^
  ..

:: 编译
cmake --build . --config Release

:: 复制运行时库
mkdir dist\bin
copy Release\BoxDetectorSDK.dll dist\bin\
copy C:\opencv\build\x64\vc16\bin\opencv_world490.dll dist\bin\
copy C:\onnxruntime-win-x64-1.17.0\lib\onnxruntime.dll dist\bin\

echo 编译完成！输出文件在 dist\bin\ 目录下
endlocal
```

### 方法二：使用 Visual Studio

1. 打开 `build/BoxDetectorSDK.sln`
2. 在解决方案资源管理器中右键点击项目
3. 选择「生成」或按 Ctrl+Shift+B

---

## 编译输出

```
build/
├── Release/
│   ├── BoxDetectorSDK.dll    # 核心库
│   ├── BoxDetectorSDK.lib    # 导入库
│   └── BoxDetectorExample.exe # 示例程序
└── dist/
    └── bin/
        ├── BoxDetectorSDK.dll
        ├── opencv_world490.dll
        └── onnxruntime.dll
```

---

## 常见问题

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
set ONNXRuntime_DIR=C:\onnxruntime-win-x64-1.17.0\lib\cmake\onnxruntime
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

---

## 使用示例

### C++

```cpp
#include "BoxDetectorSDK.h"

int main() {
    auto result = BoxDetectorSDK::BoxDetector::Analyze(
        "model.onnx",
        "image.jpg",
        0.5f,
        "./output"
    );
    
    if (result.success) {
        for (const auto& box : result.boxes) {
            std::cout << "Box: x=" << box.x << ", y=" << box.y 
                      << ", width=" << box.width << ", height=" << box.height << std::endl;
        }
    }
    return 0;
}
```

### C#

```csharp
using BoxDetectorSDK;

var result = BoxDetector.Detect("model.onnx", "image.jpg", 0.5f, "./output");

if (result.Success) {
    foreach (var box in result.Boxes) {
        Console.WriteLine($"Box: x={box.x}, y={box.y}, width={box.width}, height={box.height}");
    }
}
```

---

## 技术支持

如果遇到问题，请检查：
1. 所有依赖版本是否正确
2. 环境变量是否设置正确
3. Visual Studio 是否安装了 C++ 工具