#!/usr/bin/env python3
import os
import shutil
import zipfile
from datetime import datetime

def create_distribution():
    source_dir = "/Users/luoanqing/Desktop/Model inference C++"
    dist_dir = os.path.join(source_dir, "dist")
    output_dir = "/Users/luoanqing/Desktop"
    
    version = "1.0.0"
    timestamp = datetime.now().strftime("%Y%m%d")
    zip_name = f"BoxDetectorSDK_v{version}_{timestamp}"
    zip_path = os.path.join(output_dir, zip_name)
    
    print(f"创建分发包: {zip_name}.zip")
    print()
    
    with zipfile.ZipFile(f"{zip_path}.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
        files_to_include = [
            ("README.md", "README.md"),
            ("RUNTIME_DEPENDENCIES.md", "RUNTIME_DEPENDENCIES.md"),
            ("BoxDetectorSDK.cs", "BoxDetectorSDK.cs"),
            ("include/BoxDetectorSDK.h", "include/BoxDetectorSDK.h"),
        ]
        
        for src, dst in files_to_include:
            src_path = os.path.join(dist_dir, src)
            if os.path.exists(src_path):
                arcname = os.path.join(zip_name, dst)
                zipf.write(src_path, arcname)
                print(f"  ✅ 添加: {dst}")
            else:
                print(f"  ❌ 缺失: {dst}")
        
        placeholder_dirs = ["bin", "lib"]
        for d in placeholder_dirs:
            arcname = os.path.join(zip_name, d, ".gitkeep")
            zipf.writestr(arcname, "")
            print(f"  📁 创建目录: {d}/")
    
    print()
    print(f"✅ 分发包创建成功!")
    print(f"   路径: {zip_path}.zip")
    print()
    print("分发内容:")
    print(f"  - {zip_name}/")
    print(f"    - README.md              # 使用说明")
    print(f"    - RUNTIME_DEPENDENCIES.md # 运行时依赖说明")
    print(f"    - BoxDetectorSDK.cs      # C#封装类")
    print(f"    - include/")
    print(f"      - BoxDetectorSDK.h     # C++头文件")
    print(f"    - bin/                   # DLL文件目录（待填充）")
    print(f"    - lib/                   # 导入库目录（待填充）")
    print()
    print("注意: bin/ 和 lib/ 目录需要在 Windows 环境下构建后填充")

if __name__ == "__main__":
    create_distribution()