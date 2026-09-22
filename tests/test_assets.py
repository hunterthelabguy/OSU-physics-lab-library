"""Committed brand assets are the official files, byte for byte (D-0014, D-0020)."""

import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRAND = ROOT / "site" / "brand"

# SHA-256 of the files in OSU-branding/, hashed 2026-09-21.
LOGOS = {
    "OSU_horizontal_2C_W_over_B.png": "29b50744b39b1dadfbe55a5517c0b55da3d9d2e7ef2be7ad25a0b68cb12e50f1",
    "OSU_horizontal_2C_O_over_W.png": "8721817d9c9ca785fd3611b2f498b43f3ea21c762de95e45ea77efacb0a73c06",
    "OSU_horizontal_2C_O_over_B.png": "b6e0ba835619a2023b1403e40c7e7dda52c0ef7019411c31eddd23d421297fc8",
}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


class LogoFiles(unittest.TestCase):

    def test_logos_are_byte_for_byte(self):
        for name, digest in LOGOS.items():
            with self.subTest(name=name):
                self.assertEqual(sha256((BRAND / name).read_bytes()), digest)

    def test_trademark_notice(self):
        text = (BRAND / "README.md").read_text(encoding="utf-8")
        self.assertIn("registered trademark", text)
        self.assertIn("excluded from any license", text)


if __name__ == "__main__":
    unittest.main()
