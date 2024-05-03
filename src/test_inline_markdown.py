import unittest
from textnode import (
    TextNode,
    TextType
)

from inline_markdown import (
    split_nodes_delimiter
)


class InlineMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_code_multiple_nodes(self):
        node1 = TextNode(
            "This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode(
            "This is text with a **bolded block** word", TextType.TEXT)
        node3 = TextNode(
            "This is text with a *italicized block* word", TextType.CODE)
        new_nodes = split_nodes_delimiter(
            [node1, node2, node3], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with a **bolded block** word", TextType.TEXT),
            TextNode("This is text with a *italicized block* word",
                     TextType.CODE),
        ])

    def test_split_nodes_delimiter_no_delimiters(self):
        node = TextNode("This is text with a code block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a code block word", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_not_text_type(self):
        node = TextNode("This is text with a `code block` word", TextType.LINK,
                        "https://www.google.com")
        new_nodes = split_nodes_delimiter([node], "`", TextType.LINK)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a `code block` word", TextType.LINK,
                     "https://www.google.com"),
        ])

    def test_split_nodes_delimiter_unclosed_delimiters(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        self.assertRaises(ValueError, split_nodes_delimiter,
                          [node], "`", TextType.CODE)
