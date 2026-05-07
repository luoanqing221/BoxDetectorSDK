@echo off
chcp 65001 >nul
setlocal

echo ================================
echo BoxDetectorSDK Build Script
echo ================================

set "CMAKE_GENERATOR=Visual Studio 17 2022"
set "BUILD_DIR=build"
set "CONFIG=Release"

if not exist "%BUILD_DIR%" (
    mkdir "%BUILD_DIR%"
)

cd "%BUILD_DIR%"

echo Configuring CMake...
cmake -G "%CMAKE_GENERATOR%" .. ^
    -DOpenCV_DIR=C:/opencv/build ^
    -DONNXRuntime_DIR=C:/onnxruntime/lib/cmake/ONNXRuntime ^
    -DCMAKE_INSTALL_PREFIX=../dist

if %errorlevel% neq 0 (
    echo CMake configuration failed!
    pause
    exit /b 1
)

echo Building...
cmake --build . --config %CONFIG% --target install

if %errorlevel% neq 0 (
    echo Build failed!
    pause
    exit /b 1
)

echo Copying runtime dependencies...
copy "C:\opencv\build\x64\vc16\bin\opencv_world490.dll" ..\dist\bin\
copy "C:\onnxruntime\lib\onnxruntime.dll" ..\dist\bin\

echo Build completed successfully!
echo Output directory: dist/

pause