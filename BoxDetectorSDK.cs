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

        [DllImport(DllPath, CallingConvention = CallingConvention.Cdecl, EntryPoint = "LoadModel")]
        [return: MarshalAs(UnmanagedType.I1)]
        private static extern bool NativeLoadModel([MarshalAs(UnmanagedType.LPStr)] string modelPath);

        [DllImport(DllPath, CallingConvention = CallingConvention.Cdecl, EntryPoint = "UnloadModel")]
        private static extern void NativeUnloadModel();

        [DllImport(DllPath, CallingConvention = CallingConvention.Cdecl, EntryPoint = "IsModelLoaded")]
        [return: MarshalAs(UnmanagedType.I1)]
        private static extern bool NativeIsModelLoaded();

        [DllImport(DllPath, CallingConvention = CallingConvention.Cdecl, EntryPoint = "Detect")]
        private static extern IntPtr NativeDetect([MarshalAs(UnmanagedType.LPStr)] string imagePath,
                                                   float confidence,
                                                   [MarshalAs(UnmanagedType.LPStr)] string outputDir);

        [DllImport(DllPath, CallingConvention = CallingConvention.Cdecl, EntryPoint = "Analyze")]
        private static extern IntPtr NativeAnalyze([MarshalAs(UnmanagedType.LPStr)] string modelPath,
                                                   [MarshalAs(UnmanagedType.LPStr)] string imagePath,
                                                   float confidence,
                                                   [MarshalAs(UnmanagedType.LPStr)] string outputDir);

        [DllImport(DllPath, CallingConvention = CallingConvention.Cdecl, EntryPoint = "BatchDetect")]
        private static extern int NativeBatchDetect([MarshalAs(UnmanagedType.LPArray, ArraySubType = UnmanagedType.LPStr)] string[] imagePaths,
                                                     int count,
                                                     float confidence,
                                                     [MarshalAs(UnmanagedType.LPStr)] string outputDir,
                                                     IntPtr[] results);

        [DllImport(DllPath, CallingConvention = CallingConvention.Cdecl)]
        private static extern void FreeResult(IntPtr result);

        private static AnalyzeResult ConvertResult(IntPtr nativeResult)
        {
            var result = new AnalyzeResult();
            
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

        public static bool LoadModel(string modelPath)
        {
            return NativeLoadModel(modelPath);
        }

        public static void UnloadModel()
        {
            NativeUnloadModel();
        }

        public static bool IsModelLoaded()
        {
            return NativeIsModelLoaded();
        }

        public static List<AnalyzeResult> Detect(List<string> imagePaths, float confidence = 0.5f, string outputDir = null)
        {
            var results = new List<AnalyzeResult>();
            
            if (imagePaths == null || imagePaths.Count == 0)
                return results;

            IntPtr[] resultArray = new IntPtr[imagePaths.Count];
            string[] imageArray = imagePaths.ToArray();
            
            int ret = NativeBatchDetect(imageArray, imageArray.Length, confidence, outputDir, resultArray);
            
            for (int i = 0; i < resultArray.Length; i++)
            {
                results.Add(ConvertResult(resultArray[i]));
            }

            return results;
        }

        public static AnalyzeResult Analyze(string modelPath, string imagePath, float confidence = 0.5f, string outputDir = "")
        {
            IntPtr nativeResult = NativeAnalyze(modelPath, imagePath, confidence, outputDir);
            return ConvertResult(nativeResult);
        }
    }
}
