#!/bin/bash
# BoxDetectorSDK 打包脚本 - 带版本号

# 读取版本号
if [ -f "VERSION" ]; then
    source VERSION
else
    VERSION="1.0.0"
    BUILD_DATE=$(date +%Y-%m-%d)
fi

echo "=========================================="
echo "  BoxDetectorSDK 打包脚本"
echo "  版本: ${VERSION}"
echo "  构建日期: ${BUILD_DATE}"
echo "=========================================="

# 创建分发目录
DIST_DIR="BoxDetectorSDK_${VERSION}"
rm -rf "${DIST_DIR}"
mkdir -p "${DIST_DIR}/include" "${DIST_DIR}/examples"

# 复制文件
cp BoxDetectorSDK.cpp "${DIST_DIR}/"
cp BoxDetectorSDK.cs "${DIST_DIR}/"
cp CMakeLists.txt "${DIST_DIR}/"
cp build_windows.bat "${DIST_DIR}/"
cp BoxDetectorSDK.h "${DIST_DIR}/include/"
cp BoxDetectorExample.cpp "${DIST_DIR}/examples/"
cp BUILD.md "${DIST_DIR}/"
cp README.md "${DIST_DIR}/"
cp box_detector_cli.py "${DIST_DIR}/"
cp VERSION "${DIST_DIR}/"
cp CHANGELOG.md "${DIST_DIR}/"

# 创建压缩包
ZIP_NAME="BoxDetectorSDK_${VERSION}_${BUILD_DATE}.zip"
rm -f "${ZIP_NAME}"

echo "正在创建压缩包: ${ZIP_NAME}"
zip -r "${ZIP_NAME}" "${DIST_DIR}"

if [ $? -eq 0 ]; then
    echo "=========================================="
    echo "  打包成功！"
    echo "  输出文件: ${ZIP_NAME}"
    echo "  文件大小: $(du -h "${ZIP_NAME}" | awk '{print $1}')"
    echo "=========================================="
    
    # 显示包含的文件
    echo ""
    echo "包含的文件:"
    unzip -l "${ZIP_NAME}" | grep -E "(\.cpp|\.cs|\.h|\.md|\.py|\.bat|\.txt|VERSION)"
else
    echo "打包失败！"
    exit 1
fi
