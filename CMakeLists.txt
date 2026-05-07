cmake_minimum_required(VERSION 3.16)

project(BoxDetectorSDK)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W3")
else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra")
endif()

set(OpenCV_DIR "C:/opencv/build/x64/vc16/lib" CACHE PATH "OpenCV directory")
find_package(OpenCV REQUIRED)

set(ONNXRUNTIME_INCLUDE_DIR "C:/onnxruntime/include" CACHE PATH "ONNX Runtime include directory")
set(ONNXRUNTIME_LIB_DIR "C:/onnxruntime/lib" CACHE PATH "ONNX Runtime lib directory")

message(STATUS "OpenCV found: ${OpenCV_INCLUDE_DIRS}")
message(STATUS "OpenCV libs: ${OpenCV_LIBS}")
message(STATUS "ONNX Runtime include: ${ONNXRUNTIME_INCLUDE_DIR}")
message(STATUS "ONNX Runtime lib: ${ONNXRUNTIME_LIB_DIR}")

if(WIN32)
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
    add_definitions(-DBOXDETECTORSDK_EXPORTS)
    add_definitions(-D_CRT_SECURE_NO_WARNINGS)
endif()

add_library(BoxDetectorSDK SHARED
    BoxDetectorSDK.cpp
)

target_include_directories(BoxDetectorSDK PRIVATE
    ${OpenCV_INCLUDE_DIRS}
    ${ONNXRUNTIME_INCLUDE_DIR}
)

target_link_libraries(BoxDetectorSDK PRIVATE
    ${OpenCV_LIBS}
    ${ONNXRUNTIME_LIB_DIR}/onnxruntime.lib
)

install(TARGETS BoxDetectorSDK
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)

install(FILES BoxDetectorSDK.h DESTINATION include)

add_executable(BoxDetectorExample
    BoxDetectorExample.cpp
)

target_link_libraries(BoxDetectorExample PRIVATE
    BoxDetectorSDK
)