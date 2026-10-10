cmake_minimum_required(VERSION 3.28)
project(MissingLink LANGUAGES CXX)
add_library(core STATIC core.cpp)
target_include_directories(core PUBLIC include)
add_executable(client main.cpp)
target_include_directories(client PRIVATE include)
# Exercise: link client to core after observing the unresolved symbol.
