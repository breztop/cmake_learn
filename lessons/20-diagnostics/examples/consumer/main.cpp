#include <assetlens/scanner.hpp>
#include <iostream>
int main(int argc, char** argv) {
  if (argc != 2) return 2;
  std::cout << assetlens::summarize(assetlens::scan(argv[1]));
}
