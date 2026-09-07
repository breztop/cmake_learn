cmake_minimum_required(VERSION 3.28)
project(AssetLens LANGUAGES CXX)
add_executable(assetlens main.cpp)
target_compile_features(assetlens PRIVATE cxx_std_17)
