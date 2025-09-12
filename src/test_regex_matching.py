import unittest
from regex_matching import *

class TestTextNode(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            'This is text with an [link](https://youtu.be/fDzPL9hNpUA)'
        )
        self.assertListEqual([("link", "https://youtu.be/fDzPL9hNpUA")], matches)