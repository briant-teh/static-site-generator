import unittest

from gen_content import (
    extract_title
)


class TestGenContent(unittest.TestCase):
    def test_extract_title(self):
        markdown = "Some generic plaintext\n- list item 1\n- list item 2\n# My Title\n1. Cat\n2. Dog"
        self.assertEqual(extract_title(markdown), "My Title")
