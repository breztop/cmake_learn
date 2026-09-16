                #ifndef ASSETLENS_CONTRACT_VERSION
                #error Public contract did not propagate
                #endif
                #ifdef ASSETLENS_INTERNAL_BUILD
                #error Private definition leaked into consumer
                #endif

#include "assetlens/scanner.hpp"
#include <exception>
#include <fstream>
#include <iostream>
#include <string>
#ifdef ASSETLENS_HAS_CONFIG
#include "assetlens/config.hpp"
#endif
#ifdef ASSETLENS_HAS_SCHEMA
#include "assetlens/schema.hpp"
#endif

int main(int argc, char** argv) {
    try {
        if (argc == 2 && std::string(argv[1]) == "--version") {
#ifdef ASSETLENS_HAS_CONFIG
            std::cout << ASSETLENS_VERSION << '\n';
#else
            std::cout << "0.1.0\n";
#endif
#ifdef ASSETLENS_HAS_SCHEMA
            std::cout << "schema=" << ASSETLENS_SCHEMA_REVISION << '\n';
#endif
            return 0;
        }
        if (argc < 2) {
            std::cerr << "usage: assetlens DIRECTORY [--ext .txt] [--json FILE]\n";
            return 2;
        }
        std::string extension, output;
        for (int i = 2; i < argc; ++i) {
            std::string option = argv[i];
            if (option == "--ext" && i + 1 < argc) extension = argv[++i];
            else if (option == "--json" && i + 1 < argc) output = argv[++i];
            else { std::cerr << "invalid argument: " << option << '\n'; return 2; }
        }
        const auto snapshot = assetlens::scan(std::filesystem::u8path(argv[1]), extension);
        std::cout << assetlens::summarize(snapshot);
        if (!output.empty()) {
#if defined(ASSETLENS_HAS_CONFIG) && !ASSETLENS_ENABLE_JSON
            std::cerr << "JSON output is disabled in this build\n";
            return 2;
#else
            std::ofstream file(std::filesystem::u8path(output), std::ios::binary);
            if (!file) { std::cerr << "cannot open report file\n"; return 3; }
            file << assetlens::to_json(snapshot);
            file.close();
            if (!file) { std::cerr << "cannot write report file\n"; return 3; }
#endif
        }
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "assetlens: " << error.what() << '\n';
        return 1;
    }
}
