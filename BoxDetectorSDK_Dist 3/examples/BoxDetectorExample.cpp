#include "BoxDetectorSDK.h"
#include <iostream>

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "用法: BoxDetectorExample <模型路径> <图片路径> [置信度] [输出目录]" << std::endl;
        return 1;
    }

    std::string modelPath = argv[1];
    std::string imagePath = argv[2];
    float confidence = (argc > 3) ? std::stof(argv[3]) : 0.5f;
    std::string outputDir = (argc > 4) ? argv[4] : "";

    std::cout << "开始分析图片: " << imagePath << std::endl;
    
    auto result = BoxDetectorSDK::BoxDetector::Analyze(modelPath, imagePath, confidence, outputDir);
    
    if (result.success) {
        std::cout << "分析成功!" << std::endl;
        std::cout << "图片尺寸: " << result.imageWidth << " x " << result.imageHeight << std::endl;
        std::cout << "检测到箱子数量: " << result.boxes.size() << std::endl;
        std::cout << "分析耗时: " << result.analysisTimeMs << " ms" << std::endl;
        std::cout << "结果图片路径: " << result.resultImagePath << std::endl;
        
        for (const auto& box : result.boxes) {
            std::cout << "箱子 " << box.index << ":" << std::endl;
            std::cout << "  位置: (" << box.x << ", " << box.y << ")" << std::endl;
            std::cout << "  尺寸: " << box.width << " x " << box.height << std::endl;
            std::cout << "  置信度: " << box.confidence << std::endl;
        }
    } else {
        std::cerr << "分析失败: " << result.error << std::endl;
        return 1;
    }

    return 0;
}