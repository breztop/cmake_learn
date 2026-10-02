add_library(assetlens_core scanner.cpp report.cpp)
add_library(AssetLens::core ALIAS assetlens_core)
set_target_properties(assetlens_core PROPERTIES EXPORT_NAME core WINDOWS_EXPORT_ALL_SYMBOLS ON)
target_compile_features(assetlens_core PUBLIC cxx_std_17)
target_include_directories(assetlens_core PUBLIC
  $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)
target_include_directories(assetlens_core PRIVATE "${PROJECT_BINARY_DIR}/generated")
target_compile_definitions(assetlens_core PRIVATE ASSETLENS_HAS_CONFIG)
assetlens_warnings(assetlens_core)
if(ASSETLENS_USE_FMT)
  target_link_libraries(assetlens_core PRIVATE fmt::fmt)
  target_compile_definitions(assetlens_core PRIVATE ASSETLENS_USE_FMT)
endif()
