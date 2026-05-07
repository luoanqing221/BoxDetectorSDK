# 运行时依赖文件说明

以下文件需要从构建环境中复制到 bin/ 目录：

## Windows 64位

### 必须文件
- **BoxDetectorSDK.dll** - 核心库（构建后生成）
- **opencv_world490.dll** - OpenCV 运行时
- **onnxruntime.dll** - ONNX Runtime 运行时

### 可选文件（调试用）
- **BoxDetectorSDK.pdb** - 调试符号

## 获取方式

1. **BoxDetectorSDK.dll**
   - 通过运行 build_windows.bat 构建生成
   - 路径：build/bin/Release/BoxDetectorSDK.dll

2. **opencv_world490.dll**
   - 安装 OpenCV 4.x 后获取
   - 路径：C:\opencv\build\x64\vc16\bin\opencv_world490.dll

3. **onnxruntime.dll**
   - 下载 ONNX Runtime
   - 路径：C:\onnxruntime\lib\onnxruntime.dll

## 分发时需要提供的文件

```
dist/
├── include/
│   └── BoxDetectorSDK.h          # C++头文件
├── lib/
│   └── BoxDetectorSDK.lib        # C++导入库（可选）
├── bin/
│   ├── BoxDetectorSDK.dll        # 核心库
│   ├── opencv_world490.dll       # OpenCV运行时
│   └── onnxruntime.dll           # ONNX Runtime
├── BoxDetectorSDK.cs             # C#封装类
└── README.md                     # 使用说明
```