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

**1. 添加文件**
- 将 `BoxDetectorSDK.cs` 添加到 C# 项目

**2. 复制 DLL**
- 将编译产生的 DLL 复制到程序输出目录

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

## C++ 使用

参考 `examples/BoxDetectorExample.cpp` 中的示例代码。