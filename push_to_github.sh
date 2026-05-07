#!/bin/bash
# GitHub 仓库初始化脚本

GITHUB_USERNAME="luoanqing221"
REPO_NAME="BoxDetectorSDK"
TOKEN="ghp_HQ692i6Elx8tvAFS77DZuHqsbHAabS1gTT"

echo "=== 初始化 GitHub 仓库 ==="
echo ""

# 配置 Git
git config --global user.name "$GITHUB_USERNAME"
git config --global user.email "$GITHUB_USERNAME@users.noreply.github.com"

# 初始化仓库
git init
git add .
git commit -m "Initial commit: BoxDetectorSDK for box detection"

# 添加远程仓库
git remote add origin https://$TOKEN@github.com/$GITHUB_USERNAME/$REPO_NAME.git

# 推送代码
git branch -M main
git push -u origin main

echo ""
echo "=== 推送成功 ==="
echo "仓库地址: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo "请访问 Actions 页面查看编译进度: https://github.com/$GITHUB_USERNAME/$REPO_NAME/actions"