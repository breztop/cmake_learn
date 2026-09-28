cmake_minimum_required(VERSION 3.28)
project(AssetLens VERSION 1.0.0 LANGUAGES CXX)
add_library(assetlens_core STATIC src/scanner.cpp src/report.cpp)
add_library(AssetLens::core ALIAS assetlens_core)
target_include_directories(assetlens_core PUBLIC include)
target_compile_features(assetlens_core PUBLIC cxx_std_17)
add_executable(assetlens app/main.cpp)
target_link_libraries(assetlens PRIVATE AssetLens::core)
set(schema "${CMAKE_CURRENT_BINARY_DIR}/generated/assetlens/schema.hpp")
add_custom_command(OUTPUT "${schema}"
  COMMAND "${CMAKE_COMMAND}" -DINPUT=${CMAKE_CURRENT_SOURCE_DIR}/data/schema.txt
    -DOUTPUT=${schema} -P "${CMAKE_CURRENT_SOURCE_DIR}/cmake/GenerateSchema.cmake"
  DEPENDS data/schema.txt cmake/GenerateSchema.cmake VERBATIM)
target_sources(assetlens PRIVATE "${schema}")
target_include_directories(assetlens PRIVATE "${CMAKE_CURRENT_BINARY_DIR}/generated")
target_compile_definitions(assetlens PRIVATE ASSETLENS_HAS_SCHEMA)
