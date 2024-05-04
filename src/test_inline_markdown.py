import unittest
from textnode import (
    TextNode,
    TextType
)

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links
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

    def test_extract_markdown_images(self):
        text = "This is text with an " + \
            "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) " + \
            "and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        list_of_extracted_images = [
            ("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png"),
        ]
        self.assertEqual(extract_markdown_images(
            text), list_of_extracted_images)
        
    def test_extract_markdown_images_empty_alt(self):
        text = "This is text with an " + \
            "!(https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) " + \
            "and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        list_of_extracted_images = [
            ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png"),
        ]
        self.assertEqual(extract_markdown_images(
            text), list_of_extracted_images)
        
    def test_extract_markdown_images_empty_no_image(self):
        text = "This is text with no image"
        list_of_extracted_images = []
        self.assertEqual(extract_markdown_images(
            text), list_of_extracted_images)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) " + \
            "and [another](https://www.example.com/another)"
        list_of_extracted_links = [
            ("link", "https://www.example.com"),
            ("another", "https://www.example.com/another"),
        ]
        self.assertEqual(extract_markdown_links(text), list_of_extracted_links)
        
    def test_extract_markdown_links_empty_anchor_text(self):
        text = "This is text with a (https://www.example.com) " + \
            "and [another](https://www.example.com/another)"
        list_of_extracted_links = [
            ("another", "https://www.example.com/another"),
        ]
        self.assertEqual(extract_markdown_links(text), list_of_extracted_links)
        
    def test_extract_markdown_links_no_links(self):
        text = "This is text with no links"
        list_of_extracted_links = []
        self.assertEqual(extract_markdown_links(
            text), list_of_extracted_links)
