import unittest
from textnode import *
from split_nodes_delimiter import *

class TestTextNode(unittest.TestCase):
    def test_code_split_simple(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        got = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

        self.assertEqual(len(got), 3)
        self.assertEqual(got[0].text, "This is text with a ")
        self.assertEqual(got[0].text_type, TextType.TEXT)
        self.assertEqual(got[1].text, "code block")
        self.assertEqual(got[1].text_type, TextType.CODE_TEXT)
        self.assertEqual(got[2].text, " word")
        self.assertEqual(got[2].text_type, TextType.TEXT)

    def test_non_text_unchanged(self):
        node = TextNode("already code", TextType.CODE_TEXT)
        got = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(got, [node])

    def test_raises_on_unmatched(self):
        node = TextNode("bad `code start", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://youtu.be/fDzPL9hNpUA) and another [second link](https://youtu.be/9utPhVRESYY)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://youtu.be/fDzPL9hNpUA"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://youtu.be/9utPhVRESYY"
                ),
            ],
            new_nodes,
        )