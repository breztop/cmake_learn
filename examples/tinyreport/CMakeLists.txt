cmake_minimum_required(VERSION 3.28)
project(TinyReport VERSION 1.0.0 LANGUAGES CXX)
include(GNUInstallDirs)
include(CMakePackageConfigHelpers)
add_library(tinyreport INTERFACE)
set_target_properties(tinyreport PROPERTIES EXPORT_NAME report)
target_include_directories(tinyreport INTERFACE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)
target_compile_features(tinyreport INTERFACE cxx_std_17)
install(TARGETS tinyreport EXPORT TinyReportTargets)
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
install(EXPORT TinyReportTargets NAMESPACE TinyReport:: DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/TinyReport)
configure_package_config_file(TinyReportConfig.cmake.in "${CMAKE_CURRENT_BINARY_DIR}/TinyReportConfig.cmake"
  INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/TinyReport)
write_basic_package_version_file("${CMAKE_CURRENT_BINARY_DIR}/TinyReportConfigVersion.cmake"
  VERSION ${PROJECT_VERSION} COMPATIBILITY SameMajorVersion)
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/TinyReportConfig.cmake" "${CMAKE_CURRENT_BINARY_DIR}/TinyReportConfigVersion.cmake"
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/TinyReport)
