cmake_minimum_required(VERSION 3.28)
project(AssetLens VERSION 1.0.0 LANGUAGES CXX)
include(GNUInstallDirs)
include(CMakePackageConfigHelpers)
include(CTest)
option(ASSETLENS_ENABLE_JSON "Enable JSON report output" ON)
option(ASSETLENS_USE_FMT "Format reports with fmt" OFF)
option(ASSETLENS_USE_GTEST "Build GoogleTest tests" OFF)
option(ASSETLENS_GENERATE_SCHEMA "Generate schema header during build" ON)
option(ASSETLENS_FETCH_DEPS "Fetch missing fmt and GoogleTest sources" ON)
include(cmake/ProjectOptions.cmake)
configure_file(cmake/config.hpp.in generated/assetlens/config.hpp @ONLY)

if(ASSETLENS_USE_FMT)
  if(ASSETLENS_FETCH_DEPS)
    include(cmake/Dependencies.cmake)
    assetlens_fetch_fmt()
  else()
    find_package(fmt 10.2.1 CONFIG REQUIRED)
  endif()
endif()
if(ASSETLENS_GENERATE_SCHEMA)
  set(schema_header "${CMAKE_CURRENT_BINARY_DIR}/generated/assetlens/schema.hpp")
  add_custom_command(OUTPUT "${schema_header}"
    COMMAND "${CMAKE_COMMAND}" -DINPUT=${CMAKE_CURRENT_SOURCE_DIR}/data/schema.txt
      -DOUTPUT=${schema_header} -P "${CMAKE_CURRENT_SOURCE_DIR}/cmake/GenerateSchema.cmake"
    DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/data/schema.txt" "${CMAKE_CURRENT_SOURCE_DIR}/cmake/GenerateSchema.cmake"
    COMMENT "Generate report schema header" VERBATIM)
  add_custom_target(assetlens_schema DEPENDS "${schema_header}")
endif()
add_subdirectory(src)
add_subdirectory(app)
if(BUILD_TESTING)
  add_subdirectory(tests)
endif()

install(TARGETS assetlens_core assetlens
  EXPORT AssetLensTargets
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/generated/assetlens/config.hpp"
  DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/assetlens")
install(DIRECTORY data/ DESTINATION "${CMAKE_INSTALL_DATADIR}/assetlens")
install(EXPORT AssetLensTargets FILE AssetLensTargets.cmake NAMESPACE AssetLens::
  DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/AssetLens")
configure_package_config_file(cmake/AssetLensConfig.cmake.in
  "${CMAKE_CURRENT_BINARY_DIR}/AssetLensConfig.cmake"
  INSTALL_DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/AssetLens")
write_basic_package_version_file("${CMAKE_CURRENT_BINARY_DIR}/AssetLensConfigVersion.cmake"
  VERSION ${PROJECT_VERSION} COMPATIBILITY SameMajorVersion)
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/AssetLensConfig.cmake"
  "${CMAKE_CURRENT_BINARY_DIR}/AssetLensConfigVersion.cmake"
  DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/AssetLens")
