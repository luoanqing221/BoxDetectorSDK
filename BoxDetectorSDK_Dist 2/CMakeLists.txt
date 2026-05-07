cmake_minimum_required(VERSION 3.16)

project(BoxDetectorSDK)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W3")
else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra")
endif()

find_package(OpenCV REQUIRED PATHS "C:/opencv/build")
find_package(ONNXRuntime REQUIRED PATHS "C:/onnxruntime-win-x64-1.17.0")

message(STATUS "OpenCV found: ${OpenCV_INCLUDE_DIRS}")
message(STATUS "ONNX Runtime found: ${ONNXRuntime_INCLUDE_DIRS}")

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
    ${ONNXRuntime_INCLUDE_DIRS}
)

target_link_libraries(BoxDetectorSDK PRIVATE
    ${OpenCV_LIBS}
    ${ONNXRuntime_LIBRARIES}
)

add_executable(BoxDetectorExample
    BoxDetectorExample.cpp
)

target_link_libraries(BoxDetectorExample PRIVATE
    BoxDetectorSDK
)

install(TARGETS BoxDetectorSDK
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
)

install(FILES BoxDetectorSDK.h DESTINATION include)

set(CPACK_GENERATOR "ZIP")
set(CPACK_PACKAGE_NAME "BoxDetectorSDK")
set(CPACK_PACKAGE_VERSION "1.0.0")
set(CPACK_PACKAGE_DESCRIPTION "Box Detection SDK using ONNX Runtime")
include(CPack)