import unittest
from block_to_block_type import (
    markdown_to_html_node,
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
)

class TestTextNode(unittest.TestCase):
    def test_heading_simple(self):
        b = "# Title"
        assert block_to_block_type(b) == BlockType.HEADING

    def test_heading_no_space(self):
        b = "###Title"
        assert block_to_block_type(b) == BlockType.PARAGRAPH

    def test_code_block_fenced(self):
        b = "```\nprint('hi')\n```"
        assert block_to_block_type(b) == BlockType.CODE

    def test_quote_all_lines(self):
        b = "> a\n> b\n> c"
        assert block_to_block_type(b) == BlockType.QUOTE

    def test_unordered_list_valid(self):
        b = "- a\n- b"
        assert block_to_block_type(b) == BlockType.UNORDERED_LIST

    def test_unordered_list_missing_space(self):
        b = "-a\n- b"
        assert block_to_block_type(b) == BlockType.PARAGRAPH

    def test_ordered_list_valid(self):
        b = "1. a\n2. b\n3. c"
        assert block_to_block_type(b) == BlockType.ORDERED_LIST

    def test_ordered_list_bad_increment(self):
        b = "1. a\n3. b"
        assert block_to_block_type(b) == BlockType.PARAGRAPH

    def test_paragraph_fallback(self):
        b = "Just a simple line."
        assert block_to_block_type(b) == BlockType.PARAGRAPH
    
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )