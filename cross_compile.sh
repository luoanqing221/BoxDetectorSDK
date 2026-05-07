#!/bin/bash
# Mac 交叉编译 Windows DLL 脚本

set -e

echo "=== Mac 交叉编译 Windows DLL ==="
echo ""

# 检查是否安装了 mingw-w64
if ! command -v x86_64-w64-mingw32-g++ &> /dev/null; then
    echo "安装 mingw-w64 交叉编译器..."
    brew install mingw-w64
fi

# 创建工作目录
WORK_DIR="$(pwd)/cross_compile"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

# 下载 OpenCV Windows 版本
if [ ! -d "opencv" ]; then
    echo "下载 OpenCV Windows 版本..."
    curl -L -o opencv.exe https://github.com/opencv/opencv/releases/download/4.9.0/opencv-4.9.0-windows.exe
    7z x opencv.exe -oopencv -y
fi

# 下载 ONNX Runtime Windows 版本
if [ ! -d "onnxruntime" ]; then
    echo "下载 ONNX Runtime Windows 版本..."
    curl -L -o onnxruntime.zip https://github.com/microsoft/onnxruntime/releases/download/v1.17.0/onnxruntime-win-x64-1.17.0.zip
    unzip onnxruntime.zip
    mv onnxruntime-win-x64-1.17.0 onnxruntime
fi

# 创建 CMake 工具链文件
cat > toolchain-mingw.cmake << 'EOF'
set(CMAKE_SYSTEM_NAME Windows)
set(CMAKE_SYSTEM_PROCESSOR x86_64)

set(CMAKE_C_COMPILER x86_64-w64-mingw32-gcc)
set(CMAKE_CXX_COMPILER x86_64-w64-mingw32-g++)
set(CMAKE_RC_COMPILER x86_64-w64-mingw32-windres)

set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)
EOF

# 创建构建目录
mkdir -p build
cd build

# 配置 CMake
echo "配置 CMake..."
cmake ../.. \
    -DCMAKE_TOOLCHAIN_FILE=../toolchain-mingw.cmake \
    -DOpenCV_DIR="$WORK_DIR/opencv/build/x64/vc16/lib" \
    -DONNXRuntime_DIR="$WORK_DIR/onnxruntime/lib/cmake/onnxruntime" \
    -DCMAKE_BUILD_TYPE=Release

# 编译
echo "编译..."
make -j$(sysctl -n hw.ncpu)

echo ""
echo "=== 编译完成 ==="
echo "输出文件: build/libBoxDetectorSDK.dll"