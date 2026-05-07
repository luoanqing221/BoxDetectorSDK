#!/bin/bash
# GitHub 推送修复脚本

echo "=== 修复 GitHub 推送问题 ==="
echo ""

# 1. 配置 Git 用户信息
echo "1. 配置 Git 用户信息..."
git config --global user.email "luoanqing221@users.noreply.github.com"
git config --global user.name "luoanqing221"
echo "   ✅ 配置完成"
echo ""

# 2. 初始化仓库（如果需要）
if [ ! -d ".git" ]; then
    echo "2. 初始化 Git 仓库..."
    git init
    echo "   ✅ 初始化完成"
    echo ""
fi

# 3. 添加所有文件
echo "3. 添加文件..."
git add .
echo "   ✅ 添加完成"
echo ""

# 4. 提交
echo "4. 提交代码..."
git commit -m "Initial commit: BoxDetectorSDK - Box Detection SDK"
echo "   ✅ 提交完成"
echo ""

# 5. 设置远程仓库（使用 Token 认证）
echo "5. 设置远程仓库..."
git remote remove origin 2>/dev/null || true
git remote add origin https://ghp_HQ692i6Elx8tvAFS77DZuHqsbHAabS1gTT@github.com/luoanqing221/BoxDetectorSDK.git
echo "   ✅ 设置完成"
echo ""

# 6. 推送
echo "6. 推送代码..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "=== ✅ 推送成功 ==="
    echo ""
    echo "下一步："
    echo "1. 访问 Actions 页面查看编译进度："
    echo "   https://github.com/luoanqing221/BoxDetectorSDK/actions"
    echo ""
    echo "2. 编译完成后下载："
    echo "   BoxDetectorSDK-Windows-x64.zip"
else
    echo ""
    echo "=== ❌ 推送失败 ==="
    echo ""
    echo "请检查："
    echo "1. 仓库是否已创建：https://github.com/luoanqing221/BoxDetectorSDK"
    echo "2. Token 是否有效（可能已过期）"
    echo "3. 网络连接是否正常"
fi