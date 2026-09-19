#include "assetlens/scanner.hpp"
#include <iomanip>
#include <sstream>
#ifdef ASSETLENS_USE_FMT
#include <fmt/format.h>
#endif

namespace assetlens {
namespace {
std::string escape_json(const std::string& value) {
    std::ostringstream out;
    for (unsigned char c : value) {
        switch (c) {
        case '"': out << "\\\""; break;
        case '\\': out << "\\\\"; break;
        case '\n': out << "\\n"; break;
        case '\r': out << "\\r"; break;
        case '\t': out << "\\t"; break;
        default:
            if (c < 0x20) out << "\\u" << std::hex << std::setw(4) << std::setfill('0') << int(c) << std::dec;
            else out << char(c);
        }
    }
    return out.str();
}
}
std::string summarize(const Snapshot& snapshot) {
    std::ostringstream out;
#ifdef ASSETLENS_USE_FMT
    out << fmt::format("files={} bytes={} skipped={}\n", snapshot.files.size(), snapshot.total_bytes, snapshot.skipped);
#else
    out << "files=" << snapshot.files.size() << " bytes=" << snapshot.total_bytes
        << " skipped=" << snapshot.skipped << '\n';
#endif
    for (const auto& item : snapshot.by_extension) out << item.first << ": " << item.second << '\n';
    return out.str();
}
std::string to_json(const Snapshot& snapshot) {
    std::ostringstream out;
    out << "{\"count\":" << snapshot.files.size() << ",\"bytes\":" << snapshot.total_bytes
        << ",\"skipped\":" << snapshot.skipped << ",\"files\":[";
    bool first = true;
    for (const auto& file : snapshot.files) {
        if (!first) out << ',';
        first = false;
        out << "{\"path\":\"" << escape_json(file.relative_path.generic_u8string()) << "\",\"bytes\":" << file.bytes << '}';
    }
    out << "]}\n";
    return out.str();
}
}
