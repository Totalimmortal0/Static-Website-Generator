import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    def test_tag_eq(self):
        node = HTMLNode("p")
        node2 = HTMLNode("p")
        self.assertEqual(node, node2)

    def test_value_eq(self):
        node = HTMLNode(None, "text in paragraph")
        node2 = HTMLNode(None, "text in paragraph")
        self.assertEqual(node, node2)

    def test_props_to_html_eq(self):
        node = HTMLNode("tag", "value", "children", {"href": "https://www.google.com", "target": "_blank",})
        result = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), result)

    # Testing LeafNode
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "This is the <p> Tag")
        result = "<p>This is the <p> Tag</p>"
        self.assertEqual(node.to_html(), result)

    def test_leaf_to_html_b_not_eq(self):
        node = LeafNode("p", "This is the <p> Tag")
        result = "<p>This is *not* the <p> Tag</p>"
        self.assertNotEqual(node.to_html(), result)

    def test_leaf_to_html_value(self):
        node = LeafNode(None, "This is the <b> Tag")
        result = "This is the <b> Tag"
        self.assertEqual(node.to_html(), result)

    # Testing ParentNode
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )