# BoxDetectorSDK 更新日志

## [1.0.5] - 2026-05-08

### 新增
- ✨ 添加版本号管理功能
- ✨ 添加 `package.sh` 打包脚本，自动生成带版本号的压缩包
- ✨ 添加 `VERSION` 版本号配置文件
- ✨ 添加 `CHANGELOG.md` 更新日志文件
- ✨ 添加 `box_detector_cli.py` Python CLI 接口，模拟 C++ 接口行为

### 优化
- 🚀 实现模型缓存功能，模型只需加载一次
- 🚀 实现异步保存功能，结果图绘制保存在后台线程执行
- 🚀 实现线程池，复用线程减少创建销毁开销
- 🚀 优化文件名格式：`{原文件名}_detected_{箱子数量}_boxes_{时间戳}.{扩展名}`

### 改进
- 📝 更新 README.md，详细说明同步/异步操作
- 📝 更新 BUILD.md，添加完整的调用示例
- 📝 添加调用时序图，可视化展示执行流程
- 📝 添加使用场景建议

### 接口变更
- ⚠️ **Breaking Change**: 统一接口设计
  - 旧接口：`Detect(modelPath, imagePath, confidence, outputDir)`
  - 新接口：`LoadModel(modelPath)` + `Detect(imagePaths, confidence, outputDir)` + `UnloadModel()`
- ✨ 支持批量检测：一次调用处理多张图片
- ✨ 支持跳过绘制：无输出目录时不保存结果图

---

## [1.0.4] - 2026-05-07

### 新增
- ✨ 添加 GitHub Actions 自动编译配置
- ✨ 添加 C# 封装类 `BoxDetectorSDK.cs`
- ✨ 添加测试程序 `BoxDetectorExample.cpp`

### 优化
- 🚀 使用 ONNX Runtime 进行高效推理
- 🚀 支持 YOLOv8 模型格式

---

## [1.0.3] - 2026-05-06

### 新增
- ✨ 添加模型转换工具 `convert_to_onnx.py`
- ✨ 添加模型转换 GUI `convert_gui.py`
- ✨ 添加接口测试 GUI `test_gui.py`

---

## [1.0.2] - 2026-05-05

### 新增
- ✨ 初始化项目结构
- ✨ 添加 C++ 接口 `BoxDetectorSDK.h` 和 `BoxDetectorSDK.cpp`
- ✨ 添加 CMake 构建配置

---

## 版本号说明

- **主版本号**：不兼容的 API 修改
- **次版本号**：向下兼容的功能性新增
- **修订号**：向下兼容的问题修正

## 图例

- ✨ 新增功能
- 🚀 性能优化
- 📝 文档更新
- 🐛 问题修复
- ⚠️ 重要变更
- 🔒 安全相关
