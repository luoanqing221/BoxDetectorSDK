#!/usr/bin/env python3
import subprocess
import os

os.chdir("/Users/luoanqing/Desktop/Model inference C++")

commands = [
    ["git", "init"],
    ["git", "add", "."],
    ["git", "commit", "-m", "Initial commit: BoxDetectorSDK"],
    ["git", "remote", "add", "origin", "https://ghp_HQ692i6Elx8tvAFS77DZuHqsbHAabS1gTT@github.com/luoanqing221/BoxDetectorSDK.git"],
    ["git", "push", "-u", "origin", "main"]
]

for cmd in commands:
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("STDOUT:", result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    if result.returncode != 0:
        print(f"Command failed with code {result.returncode}")
        break
    print()