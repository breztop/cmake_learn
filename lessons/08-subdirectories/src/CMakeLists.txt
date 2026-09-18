add_library(assetlens_core scanner.cpp report.cpp)
target_include_directories(assetlens_core PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/../include")
target_compile_features(assetlens_core PUBLIC cxx_std_17)
