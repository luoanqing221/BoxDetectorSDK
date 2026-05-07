@echo off
chcp 65001 >nul
echo ==========================================
echo   BoxDetectorSDK 一键编译脚本
echo ==========================================
echo.

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [错误] 请以管理员身份运行此脚本！
    echo 右键点击此文件，选择"以管理员身份运行"
    pause
    exit /b 1
)

:: 设置安装目录
set INSTALL_DIR=C:\BoxDetectorSDK
set OPENCV_DIR=%INSTALL_DIR%\opencv
set ONNXRUNTIME_DIR=%INSTALL_DIR%\onnxruntime

echo [1/6] 创建安装目录...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo [2/6] 下载 OpenCV 4.9.0...
if not exist "%OPENCV_DIR%" (
    powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/opencv/opencv/releases/download/4.9.0/opencv-4.9.0-windows.exe' -OutFile '%INSTALL_DIR%\opencv.exe'}"
    echo 正在解压 OpenCV...
    %INSTALL_DIR%\opencv.exe -o"%OPENCV_DIR%" -y
)

echo [3/6] 下载 ONNX Runtime 1.17.0...
if not exist "%ONNXRUNTIME_DIR%" (
    powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/microsoft/onnxruntime/releases/download/v1.17.0/onnxruntime-win-x64-1.17.0.zip' -OutFile '%INSTALL_DIR%\onnxruntime.zip'}"
    echo 正在解压 ONNX Runtime...
    powershell -Command "& {Expand-Archive -Path '%INSTALL_DIR%\onnxruntime.zip' -DestinationPath '%INSTALL_DIR%' -Force}"
    rename "%INSTALL_DIR%\onnxruntime-win-x64-1.17.0" onnxruntime
)

echo [4/6] 配置 CMake...
if not exist build mkdir build
cd build
cmake -G "Visual Studio 17 2022" -A x64 ^
    -DOpenCV_DIR=%OPENCV_DIR%\build\x64\vc16\lib ^
    -DONNXRUNTIME_INCLUDE_DIR=%ONNXRUNTIME_DIR%\include ^
    -DONNXRUNTIME_LIB_DIR=%ONNXRUNTIME_DIR%\lib ^
    ..

if %errorLevel% neq 0 (
    echo [错误] CMake 配置失败！
    pause
    exit /b 1
)

echo [5/6] 编译项目...
cmake --build . --config Release

if %errorLevel% neq 0 (
    echo [错误] 编译失败！
    pause
    exit /b 1
)

echo [6/6] 准备发布文件...
if not exist dist\bin mkdir dist\bin
if not exist dist\lib mkdir dist\lib
if not exist dist\include mkdir dist\include

copy Release\BoxDetectorSDK.dll dist\bin\
copy Release\BoxDetectorSDK.lib dist\lib\
copy ..\BoxDetectorSDK.h dist\include\
copy ..\BoxDetectorSDK.cs dist\
copy ..\README.md dist\
copy ..\BUILD.md dist\
copy %OPENCV_DIR%\build\x64\vc16\bin\opencv_world490.dll dist\bin\
copy %ONNXRUNTIME_DIR%\lib\onnxruntime.dll dist\bin\

echo.
echo ==========================================
echo   编译成功！
echo   输出目录: %cd%\dist
echo ==========================================
echo.
echo 包含的文件:
dir dist\bin\*.dll
echo.
echo 用户只需将 dist 目录发给对方即可！
pause
