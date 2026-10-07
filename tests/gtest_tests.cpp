#include "assetlens/scanner.hpp"
#include <gtest/gtest.h>
TEST(Scanner, CountsFixture) {
  auto result = assetlens::scan(ASSETLENS_FIXTURE);
  EXPECT_EQ(result.files.size(), 3u);
  EXPECT_EQ(result.total_bytes, 22u);
}
TEST(Scanner, FiltersExtension) {
  EXPECT_EQ(assetlens::scan(ASSETLENS_FIXTURE, ".txt").files.size(), 2u);
}
TEST(Scanner, RejectsMissingDirectory) {
  EXPECT_THROW(assetlens::scan(std::filesystem::path(ASSETLENS_FIXTURE) / "missing"), std::runtime_error);
}
