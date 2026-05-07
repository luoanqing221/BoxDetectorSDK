#include "BoxDetectorSDK.h"
#include <iostream>
#include <vector>
#include <chrono>

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "用法: BoxDetectorExample <模型路径> <图片路径1> [图片路径2] [图片路径3] ..." << std::endl;
        std::cout << "示例: BoxDetectorExample model.onnx image1.jpg image2.jpg image3.jpg" << std::endl;
        return 1;
    }

    std::string modelPath = argv[1];
    
    std::vector<std::string> imagePaths;
    for (int i = 2; i < argc; i++) {
        imagePaths.push_back(argv[i]);
    }

    std::cout << "==========================================" << std::endl;
    std::cout << "BoxDetectorSDK 测试程序" << std::endl;
    std::cout << "==========================================" << std::endl;

    // 1. 加载模型
    std::cout << "\n[1/3] 正在加载模型: " << modelPath << std::endl;
    auto start = std::chrono::high_resolution_clock::now();
    
    bool loaded = BoxDetectorSDK::BoxDetector::LoadModel(modelPath);
    
    auto end = std::chrono::high_resolution_clock::now();
    auto loadTime = std::chrono::duration<double, std::milli>(end - start).count();
    
    if (!loaded) {
        std::cout << "模型加载失败！" << std::endl;
        return -1;
    }
    std::cout << "模型加载成功！耗时: " << loadTime << "ms" << std::endl;

    // 2. 检测图片（不保存结果图）
    std::cout << "\n[2/3] 正在检测图片（不保存结果图）..." << std::endl;
    start = std::chrono::high_resolution_clock::now();
    
    auto results = BoxDetectorSDK::BoxDetector::BatchDetect(imagePaths, 0.5f, "");
    
    end = std::chrono::high_resolution_clock::now();
    auto detectTime = std::chrono::duration<double, std::milli>(end - start).count();
    
    std::cout << "检测完成！总耗时: " << detectTime << "ms" << std::endl;
    std::cout << "平均耗时: " << detectTime / imagePaths.size() << "ms/张" << std::endl;
    
    for (size_t i = 0; i < results.size(); i++) {
        const auto& result = results[i];
        std::cout << "\n图片 " << i+1 << ": " << imagePaths[i] << std::endl;
        if (result.success) {
            std::cout << "  状态: 成功" << std::endl;
            std::cout << "  耗时: " << result.analysisTimeMs << "ms" << std::endl;
            std::cout << "  尺寸: " << result.imageWidth << "x" << result.imageHeight << std::endl;
            std::cout << "  箱子数量: " << result.boxes.size() << std::endl;
            for (const auto& box : result.boxes) {
                std::cout << "    箱子 " << box.index << ": (" << box.x << "," << box.y << ") "
                          << box.width << "x" << box.height 
                          << " 置信度: " << box.confidence << std::endl;
            }
        } else {
            std::cout << "  状态: 失败" << std::endl;
            std::cout << "  错误: " << result.error << std::endl;
        }
    }

    // 3. 检测图片（保存结果图）
    std::cout << "\n[3/3] 正在检测图片（保存结果图）..." << std::endl;
    start = std::chrono::high_resolution_clock::now();
    
    auto resultsWithSave = BoxDetectorSDK::BoxDetector::BatchDetect(imagePaths, 0.5f, "./output");
    
    end = std::chrono::high_resolution_clock::now();
    detectTime = std::chrono::duration<double, std::milli>(end - start).count();
    
    std::cout << "检测完成！总耗时: " << detectTime << "ms" << std::endl;
    std::cout << "平均耗时: " << detectTime / imagePaths.size() << "ms/张" << std::endl;
    
    for (size_t i = 0; i < resultsWithSave.size(); i++) {
        const auto& result = resultsWithSave[i];
        if (result.success && !result.resultImagePath.empty()) {
            std::cout << "  结果图片: " << result.resultImagePath << std::endl;
        }
    }

    // 4. 卸载模型
    std::cout << "\n[完成] 正在卸载模型..." << std::endl;
    BoxDetectorSDK::BoxDetector::UnloadModel();
    std::cout << "模型已卸载！" << std::endl;

    std::cout << "\n==========================================" << std::endl;
    std::cout << "测试完成！" << std::endl;
    std::cout << "==========================================" << std::endl;

    return 0;
}