#include "BoxDetectorSDK.h"
#include <opencv2/opencv.hpp>
#include <onnxruntime_cxx_api.h>
#include <algorithm>
#include <filesystem>
#include <thread>
#include <future>
#include <chrono>
#include <cstring>
#include <sstream>

#ifdef _WIN32
    #define EXPORT extern "C" __declspec(dllexport)
#else
    #define EXPORT extern "C"
#endif

namespace BoxDetectorSDK {

namespace fs = std::filesystem;

struct NativeBoxInfo {
    int index;
    double x;
    double y;
    double width;
    double height;
    double confidence;
};

struct NativeAnalyzeResult {
    bool success;
    char* error;
    int imageWidth;
    int imageHeight;
    NativeBoxInfo* boxes;
    int boxesCount;
    char* resultImagePath;
    double analysisTimeMs;
    char* imagePath;
};

class InferenceEngine {
public:
    Ort::Env env{ORT_LOGGING_LEVEL_ERROR, "BoxDetector"};
    std::unique_ptr<Ort::Session> session = nullptr;
    Ort::SessionOptions session_options;
    std::vector<int64_t> input_shape;

    InferenceEngine() {
        session_options.SetIntraOpNumThreads(1);
        session_options.SetGraphOptimizationLevel(Ort::GraphOptimizationLevel::ORT_ENABLE_BASIC);
    }

    bool LoadModel(const std::string& modelPath) {
        try {
            session = std::make_unique<Ort::Session>(env, modelPath.c_str(), session_options);
            Ort::AllocatorWithDefaultOptions allocator;
            Ort::TypeInfo input_type_info = session->GetInputTypeInfo(0);
            auto input_tensor_info = input_type_info.GetTensorTypeAndShapeInfo();
            input_shape = input_tensor_info.GetShape();
            return true;
        } catch (const Ort::Exception&) {
            return false;
        }
    }

    std::vector<NativeBoxInfo> RunInference(const cv::Mat& image, float conf_threshold) {
        std::vector<NativeBoxInfo> results;
        if (!session) return results;

        int input_h = static_cast<int>(input_shape[2]);
        int input_w = static_cast<int>(input_shape[3]);

        cv::Mat resized, normalized;
        cv::resize(image, resized, cv::Size(input_w, input_h));
        resized.convertTo(normalized, CV_32F, 1.0f / 255.0f);
        cv::cvtColor(normalized, normalized, cv::COLOR_BGR2RGB);

        std::vector<cv::Mat> channels(3);
        cv::split(normalized, channels);

        std::vector<float> input_tensor_values(input_w * input_h * 3);
        int idx = 0;
        for (int c = 0; c < 3; ++c) {
            for (int y = 0; y < input_h; ++y) {
                for (int x = 0; x < input_w; ++x) {
                    input_tensor_values[idx++] = channels[c].at<float>(y, x);
                }
            }
        }

        Ort::AllocatorWithDefaultOptions allocator;
        const char* input_names[] = {session->GetInputName(0, allocator)};
        const char* output_names[] = {session->GetOutputName(0, allocator)};

        std::vector<Ort::Value> input_tensors;
        std::vector<int64_t> input_shape_vec = {1, 3, input_h, input_w};
        input_tensors.push_back(Ort::Value::CreateTensor<float>(
            allocator, input_tensor_values.data(), input_tensor_values.size(),
            input_shape_vec.data(), input_shape_vec.size()));

        try {
            auto output_tensors = session->Run(Ort::RunOptions{nullptr},
                                               input_names, input_tensors.data(), 1,
                                               output_names, 1);

            float* output_data = output_tensors[0].GetTensorMutableData<float>();
            Ort::TypeInfo output_type_info = session->GetOutputTypeInfo(0);
            auto output_tensor_info = output_type_info.GetTensorTypeAndShapeInfo();
            std::vector<int64_t> output_shape = output_tensor_info.GetShape();

            int num_detections = static_cast<int>(output_shape[1]);
            int detection_size = static_cast<int>(output_shape[2]);

            float scale_x = static_cast<float>(image.cols) / input_w;
            float scale_y = static_cast<float>(image.rows) / input_h;

            for (int i = 0; i < num_detections; ++i) {
                float* det = output_data + i * detection_size;
                float conf = det[4];

                if (conf >= conf_threshold) {
                    NativeBoxInfo box;
                    box.index = i;
                    box.x = det[0] * scale_x;
                    box.y = det[1] * scale_y;
                    box.width = (det[2] - det[0]) * scale_x;
                    box.height = (det[3] - det[1]) * scale_y;
                    box.confidence = conf;
                    results.push_back(box);
                }
            }
        } catch (const Ort::Exception&) {
            return results;
        }

        return results;
    }
};

char* strdup_c(const char* str) {
    if (!str) return nullptr;
    size_t len = strlen(str) + 1;
    char* copy = new char[len];
    strcpy(copy, str);
    return copy;
}

NativeAnalyzeResult* CreateNativeResult() {
    NativeAnalyzeResult* result = new NativeAnalyzeResult();
    result->success = false;
    result->error = nullptr;
    result->imageWidth = 0;
    result->imageHeight = 0;
    result->boxes = nullptr;
    result->boxesCount = 0;
    result->resultImagePath = nullptr;
    result->analysisTimeMs = 0;
    result->imagePath = nullptr;
    return result;
}

void FreeNativeResult(NativeAnalyzeResult* result) {
    if (!result) return;
    if (result->error) delete[] result->error;
    if (result->boxes) delete[] result->boxes;
    if (result->resultImagePath) delete[] result->resultImagePath;
    if (result->imagePath) delete[] result->imagePath;
    delete result;
}

EXPORT NativeAnalyzeResult* Analyze(const char* modelPath, const char* imagePath,
                                     float confidence, const char* outputDir) {
    NativeAnalyzeResult* result = CreateNativeResult();

    if (!modelPath || !imagePath) {
        result->error = strdup_c("参数为空");
        return result;
    }

    if (!fs::exists(modelPath)) {
        result->error = strdup_c("模型文件不存在");
        return result;
    }

    if (!fs::exists(imagePath)) {
        result->error = strdup_c("图片文件不存在");
        return result;
    }

    auto start_time = std::chrono::high_resolution_clock::now();

    cv::Mat image = cv::imread(imagePath);
    if (image.empty()) {
        result->error = strdup_c("无法读取图片");
        return result;
    }

    result->imageWidth = image.cols;
    result->imageHeight = image.rows;
    result->imagePath = strdup_c(imagePath);

    InferenceEngine engine;
    if (!engine.LoadModel(modelPath)) {
        result->error = strdup_c("加载模型失败");
        return result;
    }

    std::vector<NativeBoxInfo> boxes = engine.RunInference(image, confidence);

    result->boxesCount = static_cast<int>(boxes.size());
    if (result->boxesCount > 0) {
        result->boxes = new NativeBoxInfo[result->boxesCount];
        for (int i = 0; i < result->boxesCount; ++i) {
            result->boxes[i] = boxes[i];
        }
    }

    std::string out_dir = outputDir && outputDir[0] ? outputDir : "./output";
    fs::create_directories(out_dir);

    cv::Mat result_image = image.clone();
    cv::Scalar blue_color(74, 144, 217);

    for (const auto& box : boxes) {
        int x1 = static_cast<int>(box.x);
        int y1 = static_cast<int>(box.y);
        int x2 = static_cast<int>(box.x + box.width);
        int y2 = static_cast<int>(box.y + box.height);

        cv::rectangle(result_image, cv::Point(x1, y1), cv::Point(x2, y2), blue_color, 2);

        std::stringstream ss;
        ss << "W=" << static_cast<int>(box.width) << ", H=" << static_cast<int>(box.height);
        std::string label = ss.str();
        int label_y = std::max(0, y1 - 10);
        cv::putText(result_image, label, cv::Point(x1, label_y),
                    cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(255, 255, 255), 1);
    }

    std::string filename = "analyzed_" + fs::path(imagePath).filename().string();
    std::string result_path = (fs::path(out_dir) / filename).string();
    cv::imwrite(result_path, result_image);
    result->resultImagePath = strdup_c(result_path.c_str());

    auto end_time = std::chrono::high_resolution_clock::now();
    result->analysisTimeMs = std::chrono::duration<double, std::milli>(end_time - start_time).count();

    result->success = true;
    return result;
}

EXPORT void FreeResult(NativeAnalyzeResult* result) {
    FreeNativeResult(result);
}

BoxDetector::BoxDetector() {}
BoxDetector::~BoxDetector() {}

AnalyzeResult BoxDetector::Analyze(const std::string& modelPath, const std::string& imagePath,
                                    float confidence, const std::string& outputDir) {
    AnalyzeResult result;
    result.success = false;

    NativeAnalyzeResult* native = ::Analyze(modelPath.c_str(), imagePath.c_str(),
                                             confidence, outputDir.c_str());

    if (!native) {
        result.error = "调用失败";
        return result;
    }

    try {
        result.success = native->success;
        result.error = native->error ? native->error : "";
        result.imageWidth = native->imageWidth;
        result.imageHeight = native->imageHeight;
        result.resultImagePath = native->resultImagePath ? native->resultImagePath : "";
        result.analysisTimeMs = native->analysisTimeMs;
        result.imagePath = native->imagePath ? native->imagePath : "";

        for (int i = 0; i < native->boxesCount; ++i) {
            const auto& box = native->boxes[i];
            result.boxes.emplace_back(box.index, box.x, box.y,
                                      box.width, box.height, box.confidence);
        }
    } catch (...) {
        FreeResult(native);
        throw;
    }
    FreeResult(native);

    return result;
}

AnalyzeResult BoxDetector::AnalyzeAsync(const std::string& modelPath, const std::string& imagePath,
                                        float confidence, const std::string& outputDir) {
    auto future = std::async(std::launch::async, Analyze, modelPath, imagePath, confidence, outputDir);
    return future.get();
}

std::vector<AnalyzeResult> BoxDetector::BatchAnalyze(const std::string& modelPath,
                                                      const std::vector<std::string>& imagePaths,
                                                      float confidence,
                                                      const std::string& outputDir) {
    std::vector<AnalyzeResult> results;
    for (const auto& imagePath : imagePaths) {
        results.push_back(Analyze(modelPath, imagePath, confidence, outputDir));
    }
    return results;
}

} // namespace BoxDetectorSDK