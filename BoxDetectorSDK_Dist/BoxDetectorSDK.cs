using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Text;

namespace BoxDetectorSDK
{
    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi)]
    public struct BoxInfo
    {
        public int index;
        public double x;
        public double y;
        public double width;
        public double height;
        public double confidence;
    }

    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi)]
    public struct AnalyzeResultInternal
    {
        [MarshalAs(UnmanagedType.I1)]
        public bool success;
        
        [MarshalAs(UnmanagedType.LPStr)]
        public string error;
        
        public int imageWidth;
        public int imageHeight;
        
        public IntPtr boxes;
        public int boxesCount;
        
        [MarshalAs(UnmanagedType.LPStr)]
        public string resultImagePath;
        
        public double analysisTimeMs;
        
        [MarshalAs(UnmanagedType.LPStr)]
        public string imagePath;
    }

    public class AnalyzeResult
    {
        public bool Success { get; set; }
        public string Error { get; set; }
        public int ImageWidth { get; set; }
        public int ImageHeight { get; set; }
        public List<BoxInfo> Boxes { get; set; } = new List<BoxInfo>();
        public string ResultImagePath { get; set; }
        public double AnalysisTimeMs { get; set; }
        public string ImagePath { get; set; }
    }

    public static class BoxDetector
    {
        private const string DllPath = "BoxDetectorSDK.dll";

        [DllImport(DllPath, CallingConvention = CallingConvention.Cdecl)]
        private static extern IntPtr Analyze([MarshalAs(UnmanagedType.LPStr)] string modelPath,
                                             [MarshalAs(UnmanagedType.LPStr)] string imagePath,
                                             float confidence,
                                             [MarshalAs(UnmanagedType.LPStr)] string outputDir);

        [DllImport(DllPath, CallingConvention = CallingConvention.Cdecl)]
        private static extern void FreeResult(IntPtr result);

        public static AnalyzeResult Detect(string modelPath, string imagePath, float confidence = 0.5f, string outputDir = "")
        {
            var result = new AnalyzeResult();
            
            IntPtr nativeResult = Analyze(modelPath, imagePath, confidence, outputDir);
            
            if (nativeResult == IntPtr.Zero)
            {
                result.Success = false;
                result.Error = "调用失败";
                return result;
            }

            try
            {
                AnalyzeResultInternal native = Marshal.PtrToStructure<AnalyzeResultInternal>(nativeResult);
                
                result.Success = native.success;
                result.Error = native.error;
                result.ImageWidth = native.imageWidth;
                result.ImageHeight = native.imageHeight;
                result.ResultImagePath = native.resultImagePath;
                result.AnalysisTimeMs = native.analysisTimeMs;
                result.ImagePath = native.imagePath;

                if (native.boxes != IntPtr.Zero && native.boxesCount > 0)
                {
                    int boxSize = Marshal.SizeOf<BoxInfo>();
                    for (int i = 0; i < native.boxesCount; i++)
                    {
                        IntPtr boxPtr = new IntPtr(native.boxes.ToInt64() + i * boxSize);
                        BoxInfo box = Marshal.PtrToStructure<BoxInfo>(boxPtr);
                        result.Boxes.Add(box);
                    }
                }
            }
            finally
            {
                FreeResult(nativeResult);
            }

            return result;
        }
    }
}