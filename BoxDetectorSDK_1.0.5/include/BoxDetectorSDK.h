#pragma once

#ifdef _WIN32
    #ifdef BOXDETECTORSDK_EXPORTS
        #define BOXDETECTORSDK_API __declspec(dllexport)
    #else
        #define BOXDETECTORSDK_API __declspec(dllimport)
    #endif
#else
    #define BOXDETECTORSDK_API
#endif

#include <vector>
#include <string>
#include <memory>

namespace BoxDetectorSDK {

struct BOXDETECTORSDK_API BoxInfo {
    int index;
    double x;
    double y;
    double width;
    double height;
    double confidence;

    BoxInfo() : index(0), x(0), y(0), width(0), height(0), confidence(0) {}
    BoxInfo(int idx, double x_, double y_, double w_, double h_, double conf_)
        : index(idx), x(x_), y(y_), width(w_), height(h_), confidence(conf_) {}
};

struct BOXDETECTORSDK_API AnalyzeResult {
    bool success;
    std::string error;
    int imageWidth;
    int imageHeight;
    std::vector<BoxInfo> boxes;
    std::string resultImagePath;
    double analysisTimeMs;
    std::string imagePath;

    AnalyzeResult() : success(false), imageWidth(0), imageHeight(0), analysisTimeMs(0) {}
};

class BOXDETECTORSDK_API BoxDetector {
public:
    BoxDetector();
    ~BoxDetector();

    static bool LoadModel(const std::string& modelPath);
    
    static void UnloadModel();
    
    static bool IsModelLoaded();

    static AnalyzeResult Detect(const std::string& imagePath, 
                                float confidence = 0.5f, 
                                const std::string& outputDir = "");

    static AnalyzeResult Analyze(const std::string& modelPath, const std::string& imagePath, 
                                  float confidence = 0.5f, const std::string& outputDir = "");

    static AnalyzeResult AnalyzeAsync(const std::string& modelPath, const std::string& imagePath,
                                      float confidence = 0.5f, const std::string& outputDir = "");

    static std::vector<AnalyzeResult> BatchAnalyze(const std::string& modelPath, 
                                                    const std::vector<std::string>& imagePaths,
                                                    float confidence = 0.5f, 
                                                    const std::string& outputDir = "");

    static std::vector<AnalyzeResult> BatchDetect(const std::vector<std::string>& imagePaths,
                                                   float confidence = 0.5f,
                                                   const std::string& outputDir = "");

private:
    class Impl;
    std::unique_ptr<Impl> pImpl;
};

} // namespace BoxDetectorSDK