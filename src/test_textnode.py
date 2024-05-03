import unittest

from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
)
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node",
                         TextType.BOLD, "http://www.google.com")
        node2 = TextNode("This is a text node",
                         TextType.BOLD, "http://www.google.com")
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = TextNode("This is a text node",
                         TextType.BOLD, "http://www.google.com")
        node2 = TextNode("This is a text node",
                         TextType.ITALIC, "http://www.google.com")
        self.assertNotEqual(node1, node2)

    def test_text_node_to_html_node_text(self):
        text_node = TextNode(
            "This is a text node of type - text", TextType.TEXT)
        leaf_node = LeafNode(
            None, "This is a text node of type - text", None)
        converted_node = text_node_to_html_node(text_node)
        self.assertEqual(converted_node, leaf_node)

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode(
            "This is a text node of type - bold", TextType.BOLD)
        leaf_node = LeafNode(
            "b", "This is a text node of type - bold", None)
        converted_node = text_node_to_html_node(text_node)
        self.assertEqual(converted_node, leaf_node)

    def test_text_node_to_html_node_italic(self):
        text_node = TextNode(
            "This is a text node of type - italic", TextType.ITALIC)
        leaf_node = LeafNode(
            "i", "This is a text node of type - italic", None)
        converted_node = text_node_to_html_node(text_node)
        self.assertEqual(converted_node, leaf_node)

    def test_text_node_to_html_node_code(self):
        text_node = TextNode(
            "This is a text node of type - code", TextType.CODE)
        leaf_node = LeafNode(
            "code", "This is a text node of type - code", None)
        converted_node = text_node_to_html_node(text_node)
        self.assertEqual(converted_node, leaf_node)

    def test_text_node_to_html_node_link(self):
        text_node = TextNode(
            "This is a text node of type - link", TextType.LINK, "https://www.google.com")
        leaf_node = LeafNode(
            "a", "This is a text node of type - link", {"href": "https://www.google.com"})
        converted_node = text_node_to_html_node(text_node)
        self.assertEqual(converted_node, leaf_node)

    def test_text_node_to_html_node_image(self):
        text_node = TextNode(
            "This is a text node of type - image", TextType.IMAGE, "images/cat.png")
        leaf_node = LeafNode(
            "img", "", {"src": "images/cat.png", "alt": "This is a text node of type - image"})
        converted_node = text_node_to_html_node(text_node)
        self.assertEqual(converted_node, leaf_node)

    def test_text_node_to_html_node_invalid_text_type(self):
        text_node = TextNode(
            "This is a text node of type - invalid", "invalid")
        self.assertRaises(ValueError, text_node_to_html_node, text_node)

    def test_repr(self):
        node = TextNode("This is a text node", "bold", "http://test.com")
        self.assertAlmostEqual(
            str(node), "TextNode(This is a text node, bold, http://test.com)")


print(f"__name__: {__name__}")
if __name__ == "__main__":
    unittest.main()
