#include "assetlens/scanner.hpp"
#include <iostream>
#include <stdexcept>
#include <string>
int main(int argc, char** argv) {
    if (argc != 2) return 2;
    auto all = assetlens::scan(argv[1]);
    if (all.files.size() != 3 || all.total_bytes != 22 || all.by_extension[".txt"] != 2) {
        std::cerr << "fixture count/size/extension mismatch\n"; return 1;
    }
    auto txt = assetlens::scan(argv[1], ".txt");
    if (txt.files.size() != 2 || txt.total_bytes != 10) return 1;
    if (all.files[0].relative_path.generic_string() != "config.json") return 1;
    if (assetlens::to_json(all).find("\"count\":3") == std::string::npos) return 1;
    assetlens::Snapshot escaped;
    escaped.files.push_back({"quote\"tab\t.txt", 0});
    if (assetlens::to_json(escaped).find("quote\\\"tab\\t.txt") == std::string::npos) return 1;
    try { (void)assetlens::scan(std::filesystem::path(argv[1]) / "missing"); }
    catch (const std::runtime_error&) { return 0; }
    return 1;
}
