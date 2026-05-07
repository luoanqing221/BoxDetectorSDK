FROM mcr.microsoft.com/devcontainers/dotnet:6.0-windowsservercore-ltsc2022

# 安装 CMake
RUN choco install cmake --installargs 'ADD_CMAKE_TO_PATH=System' -y

# 创建依赖目录
RUN mkdir C:\deps

# 下载并安装 OpenCV
RUN powershell -Command "Invoke-WebRequest -Uri 'https://github.com/opencv/opencv/releases/download/4.9.0/opencv-4.9.0-windows.exe' -OutFile 'C:\deps\opencv.exe'; Start-Process -FilePath 'C:\deps\opencv.exe' -ArgumentList '-oC:\deps\opencv -y' -Wait -NoNewWindow"

# 下载并解压 ONNX Runtime
RUN powershell -Command "Invoke-WebRequest -Uri 'https://github.com/microsoft/onnxruntime/releases/download/v1.17.0/onnxruntime-win-x64-1.17.0.zip' -OutFile 'C:\deps\onnxruntime.zip'; Expand-Archive -Path 'C:\deps\onnxruntime.zip' -DestinationPath 'C:\deps' -Force; Rename-Item -Path 'C:\deps\onnxruntime-win-x64-1.17.0' -NewName 'onnxruntime'"

# 设置环境变量
ENV OpenCV_DIR=C:\deps\opencv\build\x64\vc16\lib
ENV ONNXRUNTIME_DIR=C:\deps\onnxruntime

# 设置工作目录
WORKDIR /workspace