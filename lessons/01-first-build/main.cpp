#include <filesystem>
#include <iostream>
int main(int argc, char** argv) {
  if (argc != 2) return 2;
  if (!std::filesystem::is_directory(argv[1])) return 1;
  std::size_t count = 0;
  for (const auto& entry : std::filesystem::recursive_directory_iterator(argv[1]))
    if (entry.is_regular_file()) ++count;
  std::cout << "files=" << count << '\n';
}
