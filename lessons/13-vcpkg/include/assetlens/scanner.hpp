#pragma once
#include <cstdint>
#include <filesystem>
#include <map>
#include <string>
#include <vector>

namespace assetlens {
struct Entry {
    std::filesystem::path relative_path;
    std::uintmax_t bytes;
};
struct Snapshot {
    std::vector<Entry> files;
    std::map<std::string, std::size_t> by_extension;
    std::uintmax_t total_bytes = 0;
    std::size_t skipped = 0;
};
Snapshot scan(const std::filesystem::path& root, const std::string& extension = {});
std::string summarize(const Snapshot& snapshot);
std::string to_json(const Snapshot& snapshot);
}
