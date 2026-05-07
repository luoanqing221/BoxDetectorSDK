#!/usr/bin/env python3
import subprocess
import os

os.chdir("/Users/luoanqing/Desktop/Model inference C++")

commands = [
    ["git", "init"],
    ["git", "add", "."],
    ["git", "commit", "-m", "Initial commit: BoxDetectorSDK - Box Detection SDK with ONNX Runtime"],
    ["git", "remote", "add", "origin", "https://ghp_HQ692i6Elx8tvAFS77DZuHqsbHAabS1gTT@github.com/luoanqing221/BoxDetectorSDK.git"],
    ["git", "push", "-u", "origin", "main"]
]

print("=== 正在推送代码到 GitHub ===")
print()

for i, cmd in enumerate(commands, 1):
    print(f"步骤 {i}: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.stdout:
            print(f"  STDOUT: {result.stdout.strip()}")
        if result.stderr:
            print(f"  STDERR: {result.stderr.strip()}")
        
        if result.returncode != 0:
            print(f"  ❌ 命令失败")
            print()
            print("=== 手动操作步骤 ===")
            print("请在终端中运行以下命令：")
            print()
            print("cd \"/Users/luoanqing/Desktop/Model inference C++\"")
            print("git init")
            print("git add .")
            print("git commit -m \"Initial commit\"")
            print("git remote add origin https://github.com/luoanqing221/BoxDetectorSDK.git")
            print("git push -u origin main")
            print()
            print("然后访问: https://github.com/luoanqing221/BoxDetectorSDK/actions")
            break
        else:
            print(f"  ✅ 成功")
            print()
            
    except subprocess.TimeoutExpired:
        print(f"  ❌ 超时")
        break

if i == len(commands) and result.returncode == 0:
    print("=== 推送成功！===")
    print()
    print("下一步：")
    print("1. 访问 Actions 页面查看编译进度：")
    print("   https://github.com/luoanqing221/BoxDetectorSDK/actions")
    print()
    print("2. 编译完成后，在 Artifacts 中下载：")
    print("   BoxDetectorSDK-Windows-x64.zip")