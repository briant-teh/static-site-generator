import unittest

from block_markdown import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
    block_to_html_node,
    block_to_paragraph,
    block_to_heading,
    block_to_code,
    block_to_quote,
    block_to_unordered_list,
    block_to_ordered_list,
    markdown_to_html_node,
)

from htmlnode import (
    ParentNode,
    LeafNode,
)


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = "This is **bolded** paragraph\n\n" + \
            "This is another paragraph with *italic* text and `code` here\n" + \
            "This is the same paragraph on a new line\n\n* This is a list\n* with items"

        self.assertEqual(markdown_to_blocks(markdown), [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\n" +
            "This is the same paragraph on a new line",
            "* This is a list\n* with items"
        ])

    def test_markdown_to_blocks_excessive_newlines(self):
        markdown = "This is **bolded** paragraph\n\n\n\n" + \
            "This is another paragraph with *italic* text and `code` here\n" + \
            "This is the same paragraph on a new line\n\n\n\n\n* This is a list\n* with items"

        self.assertEqual(markdown_to_blocks(markdown), [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\n" +
            "This is the same paragraph on a new line",
            "* This is a list\n* with items"
        ])

    def test_block_to_block_type(self):
        block = "paragraph 1\nparagraph 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "### Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```Lines of code```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote 1\n> quote 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "* unordered list item 1\n- unordered list item 2"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. ordered list item 1\n2.ordered list item 2"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_paragraph(self):
        block = "paragraph 1\nparagraph 2"
        self.assertEqual(block_to_paragraph(block),
                         LeafNode("p", "paragraph 1\nparagraph 2"))

    def test_block_to_paragraph_with_inline(self):
        block = "paragraph 1 contains *italic* text"
        self.assertEqual(block_to_paragraph(block),
                         ParentNode("p", [
                             LeafNode(None, "paragraph 1 contains "),
                             LeafNode("i", "italic"),
                             LeafNode(None, " text"),
                         ]))

    def test_block_to_heading(self):
        block = "### Heading"
        self.assertEqual(block_to_heading(block),
                         LeafNode("h3", "Heading"))

    def test_block_to_code(self):
        block = "```Lines of code```"
        self.assertEqual(block_to_code(block),
                         ParentNode("pre", [
                             LeafNode("code", "Lines of code")
                         ]))

    def test_block_to_quote(self):
        block = "> quote 1\n>quote 2"
        self.assertEqual(block_to_quote(block),
                         LeafNode("blockquote", "quote 1\nquote 2"))

    def test_block_to_unordered_list(self):
        block = "* unordered list item 1\n- unordered list item 2"
        self.assertEqual(block_to_unordered_list(block),
                         ParentNode("ul", [
                             LeafNode("li", "unordered list item 1"),
                             LeafNode("li", "unordered list item 2"),
                         ]))

    def test_block_to_ordered_list(self):
        block = "1. ordered list item 1\n2.ordered list item 2"
        self.assertEqual(block_to_ordered_list(block),
                         ParentNode("ol", [
                             LeafNode("li", "ordered list item 1"),
                             LeafNode("li", "ordered list item 2"),
                         ]))

    def test_block_to_html_node(self):
        block = "paragraph 1\nparagraph 2"
        self.assertEqual(block_to_html_node(block, BlockType.PARAGRAPH),
                         LeafNode("p", "paragraph 1\nparagraph 2"))

        block = "### Heading"
        self.assertEqual(block_to_html_node(block, BlockType.HEADING),
                         LeafNode("h3", "Heading"))

        block = "```Lines of code```"
        self.assertEqual(block_to_html_node(block, BlockType.CODE),
                         ParentNode("pre", [
                             LeafNode("code", "Lines of code")
                         ]))
        block = "> quote 1\n>quote 2"
        self.assertEqual(block_to_html_node(block, BlockType.QUOTE),
                         LeafNode("blockquote", "quote 1\nquote 2"))

        block = "* unordered list item 1\n- unordered list item 2"
        self.assertEqual(block_to_html_node(block, BlockType.UNORDERED_LIST),
                         ParentNode("ul", [
                             LeafNode("li", "unordered list item 1"),
                             LeafNode("li", "unordered list item 2"),
                         ]))

        block = "1. ordered list item 1\n2.ordered list item 2"
        self.assertEqual(block_to_html_node(block, BlockType.ORDERED_LIST),
                         ParentNode("ol", [
                             LeafNode("li", "ordered list item 1"),
                             LeafNode("li", "ordered list item 2"),
                         ]))

    def test_markdown_to_html_node(self):
        md = "## Header\n\n- This is an unordered list\n- with *italic* items" + \
            "\n- and **bold** items too\n\n1. This is an ordered list\n2. with `some code` items" + \
            "\n3. and some plain text"

        node = markdown_to_html_node(md)
        self.assertEqual(node,
                         ParentNode("div", [
                             LeafNode("h2", "Header"),
                             ParentNode("ul", [
                                 LeafNode("li", "This is an unordered list"),
                                 ParentNode("li", [
                                     LeafNode(None, "with "),
                                     LeafNode("i", "italic"),
                                     LeafNode(None, " items"),
                                 ]),
                                 ParentNode("li", [
                                     LeafNode(None, "and "),
                                     LeafNode("b", "bold"),
                                     LeafNode(None, " items too"),
                                 ]),
                             ]),
                             ParentNode("ol", [
                                 LeafNode("li", "This is an ordered list"),
                                 ParentNode("li", [
                                     LeafNode(None, "with "),
                                     LeafNode("code", "some code"),
                                     LeafNode(None, " items"),
                                 ]),
                                 LeafNode("li", "and some plain text"),
                             ])
                         ]))

        self.assertEqual(node.to_html(),
                         "<div><h2>Header</h2><ul><li>This is an unordered list</li>" +
                         "<li>with <i>italic</i> items</li><li>and <b>bold</b> items too</li></ul>" +
                         "<ol><li>This is an ordered list</li><li>with <code>some code</code> items</li>" +
                         "<li>and some plain text</li></ol></div>")
