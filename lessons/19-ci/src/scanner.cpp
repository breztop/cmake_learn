#include "assetlens/scanner.hpp"
#include <algorithm>
#include <stdexcept>
#include <system_error>

namespace assetlens {
Snapshot scan(const std::filesystem::path& root, const std::string& extension) {
    std::error_code ec;
    if (!std::filesystem::is_directory(root, ec) || ec) {
        throw std::runtime_error("scan root must be an existing directory");
    }
    Snapshot result;
    // Directory symlinks are not followed. File symlinks are skipped as well.
    std::filesystem::recursive_directory_iterator it(
        root, std::filesystem::directory_options::skip_permission_denied, ec), end;
    if (ec) throw std::runtime_error("cannot enumerate scan root: " + ec.message());
    while (it != end) {
        const auto entry = *it;
        auto status = entry.symlink_status(ec);
        if (ec) { ++result.skipped; ec.clear(); }
        else if (std::filesystem::is_regular_file(status)) {
            auto ext = entry.path().extension().string();
            if (extension.empty() || extension == ext) {
                const auto size = entry.file_size(ec);
                if (ec) { ++result.skipped; ec.clear(); }
                else {
                    result.files.push_back({entry.path().lexically_relative(root), size});
                    ++result.by_extension[ext.empty() ? "[none]" : ext];
                    result.total_bytes += size;
                }
            }
        }
        it.increment(ec);
        if (ec) { ++result.skipped; ec.clear(); }
    }
    std::sort(result.files.begin(), result.files.end(), [](const Entry& a, const Entry& b) {
        return a.relative_path.generic_string() < b.relative_path.generic_string();
    });
    return result;
}
}
