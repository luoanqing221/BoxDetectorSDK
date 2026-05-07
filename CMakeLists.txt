cmake_minimum_required(VERSION 3.16)

project(BoxDetectorSDK)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(OpenCV REQUIRED)
find_package(ONNXRuntime REQUIRED)

if(WIN32)
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
    add_definitions(-DBOXDETECTORSDK_EXPORTS)
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