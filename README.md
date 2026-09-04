# CMake 实践：AssetLens

CMake 系列配套学习代码，从编译第一个 C++ 程序开始，逐步完成库、依赖管理、测试、安装和打包。

**图文教程：微信公众号「微风中的快乐」**  
**视频教程：B 站「微风中的快乐」**

在对应平台搜索「微风中的快乐」，按下方章节顺序学习。

## 示例项目

AssetLens 是一个目录扫描工具，可以统计文件数量、总字节数和扩展名分布，按扩展名筛选文件，并导出 JSON 文件清单。

- 仓库根目录：完整项目。
- `lessons/`：20 个章节的独立代码，按学习顺序逐步增加功能和构建配置。
- `examples/`：包的安装与使用示例，以及构建错误排查示例。
- `scripts/`：章节运行与代码验证脚本。

## 运行完整项目

准备 CMake 3.28 或更高版本、支持 C++17 的编译器和 Ninja。Windows 使用 MSVC 时，在 Developer PowerShell 中执行命令；使用 MinGW 时，将编译器和 Ninja 加入 PATH。

以下命令在仓库根目录执行。完整项目的默认构建使用 C++ 标准库。

```sh
cmake --preset dev
cmake --build --preset dev --parallel 2
ctest --preset dev
```

扫描随仓库提供的示例目录。Linux、macOS：

```sh
./build/dev/app/assetlens data/sample --json build/dev/report.json
```

Windows PowerShell：

```powershell
.\build\dev\app\assetlens.exe data/sample --json build/dev/report.json
```

控制台输出：

```text
files=3 bytes=22 skipped=0
.json: 1
.txt: 2
```

示例目录包含 3 个文件，共 22 字节。生成的文件清单保存在 `build/dev/report.json`。添加 `--ext .txt` 可以筛选 `.txt` 文件，扩展名匹配区分大小写。

## 章节代码

| 章节 | 内容 | 代码入口 |
| --- | --- | --- |
| 01 | 编译第一个 C++ 程序 | [01-first-build](lessons/01-first-build/CMakeLists.txt) |
| 02 | 源文件、头文件和编译选项 | [02-targets](lessons/02-targets/CMakeLists.txt) |
| 03 | 变量、列表和路径 | [03-variables](lessons/03-variables/CMakeLists.txt) |
| 04 | 缓存变量和可选功能 | [04-cache-options](lessons/04-cache-options/CMakeLists.txt) |
| 05 | 条件、循环、函数和宏 | [05-functions](lessons/05-functions/CMakeLists.txt) |
| 06 | 静态库、动态库、对象库和接口库 | [06-libraries](lessons/06-libraries/CMakeLists.txt) |
| 07 | PRIVATE、PUBLIC 和 INTERFACE | [07-usage-requirements](lessons/07-usage-requirements/CMakeLists.txt) |
| 08 | 多目录项目 | [08-subdirectories](lessons/08-subdirectories/CMakeLists.txt) |
| 09 | Debug、Release 和生成器表达式 | [09-configurations](lessons/09-configurations/CMakeLists.txt) |
| 10 | CMakePresets 构建预设 | [10-presets](lessons/10-presets/CMakeLists.txt) |
| 11 | 用 find_package 接入已安装的包 | [11-find-package](lessons/11-find-package/CMakeLists.txt) |
| 12 | 用 FetchContent 获取源码依赖 | [12-fetch-content](lessons/12-fetch-content/CMakeLists.txt) |
| 13 | 接入 vcpkg | [13-vcpkg](lessons/13-vcpkg/CMakeLists.txt) |
| 14 | 自定义命令与生成文件 | [14-custom-command](lessons/14-custom-command/CMakeLists.txt) |
| 15 | CTest 与 GoogleTest | [15-testing](lessons/15-testing/CMakeLists.txt) |
| 16 | 安装程序和库 | [16-install](lessons/16-install/CMakeLists.txt) |
| 17 | 导出可供 find_package 使用的包 | [17-export-package](lessons/17-export-package/CMakeLists.txt) |
| 18 | 用 CPack 打包 | [18-cpack](lessons/18-cpack/CMakeLists.txt) |
| 19 | 持续集成构建与测试 | [19-ci](lessons/19-ci/CMakeLists.txt) |
| 20 | 构建错误排查 | [20-diagnostics](lessons/20-diagnostics/CMakeLists.txt) |

学习某一章时，用对应目录作为源码目录。例如，构建第 1 章：

```sh
cmake -S lessons/01-first-build -B build/01 -G Ninja
cmake --build build/01
python scripts/run_lesson.py 1
```

`run_lesson.py` 使用该章的示例数据运行已经构建好的程序。Python 3 用于执行仓库脚本。

第 11 章使用 `examples/tinyreport/` 中的示例包；第 12、13 章分别通过 FetchContent 和 vcpkg 接入 fmt。依赖准备步骤见对应图文、视频教程。

## 安装与打包

完成 `dev` 构建后，可以把程序和库安装到 `install/`：

```sh
cmake --install build/dev --prefix install
```

生成 ZIP 安装包：

```sh
cpack --config build/dev/CPackConfig.cmake -B packages
```

`examples/consumer/` 演示其他项目怎样通过 `find_package(AssetLens CONFIG REQUIRED)` 使用安装后的库。

## 验证代码

在仓库根目录执行：

```sh
python scripts/verify.py --offline
```

脚本会构建第 1～11、14～20 章和完整项目，检查扫描结果、测试、安装后使用、安装目录搬迁及 ZIP 打包。第 12、13 章需要外部依赖，离线模式跳过这两章。

验证 FetchContent 路径时，可通过 `--fmt-source` 提供 fmt 10.2.1 源码；通过 `--vcpkg-root` 指定 vcpkg 目录，可验证第 13 章的包管理流程。GoogleTest 示例使用 1.14.0，完整项目可通过 `--gtest-source` 指定对应源码进行验证。
