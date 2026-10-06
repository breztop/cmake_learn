include(FetchContent)
function(assetlens_fetch_fmt)
  set(FMT_TEST OFF CACHE BOOL "" FORCE)
  set(FMT_INSTALL ON CACHE BOOL "" FORCE)
  FetchContent_Declare(fmt
    URL https://codeload.github.com/fmtlib/fmt/zip/refs/tags/10.2.1
    URL_HASH SHA256=d368f9c39a33a3aef800f5be372ec1df1c12ad57ada1f60adc62f24c0e348469
    DOWNLOAD_EXTRACT_TIMESTAMP TRUE)
  FetchContent_MakeAvailable(fmt)
endfunction()
function(assetlens_fetch_gtest)
  set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)
  set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
  FetchContent_Declare(googletest
    URL https://codeload.github.com/google/googletest/zip/refs/tags/v1.14.0
    URL_HASH SHA256=1f357c27ca988c3f7c6b4bf68a9395005ac6761f034046e9dde0896e3aba00e4
    DOWNLOAD_EXTRACT_TIMESTAMP TRUE)
  FetchContent_MakeAvailable(googletest)
endfunction()
