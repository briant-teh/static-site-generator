import unittest

from textnode import TextNode, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", "bold", "http://test.com")
        node2 = TextNode("This is a text node", "bold", "http://test.com")
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = TextNode("This is a text node", "bold", "http://test.com")
        node2 = TextNode("This is a text node", "italic", "http://test.com")
        self.assertNotEqual(node1, node2)

    def test_text_node_to_html_node_text(self):
        text_node = TextNode("This is a text node of type - text", "text")
        leaf_node = LeafNode(
            None, "This is a text node of type - text", None, None)
        converted_node = text_node_to_html_node(text_node)
        self.assertEqual(converted_node, leaf_node)

    def test_text_node_to_html_node_text(self):
        text_node = TextNode("This is a text node of type - bold", "bold")
        leaf_node = LeafNode(
            "b", "This is a text node of type - bold", None, None)
        converted_node = text_node_to_html_node(text_node)
        self.assertEqual(converted_node, leaf_node)

    def test_text_node_to_html_node_text(self):
        text_node = TextNode("This is a text node of type - text", "text")
        leaf_node = LeafNode(
            None, "This is a text node of type - text", None, None)
        converted_node = text_node_to_html_node(text_node)
        self.assertEqual(converted_node, leaf_node)

    def test_text_node_to_html_node_text(self):
        text_node = TextNode("This is a text node of type - text", "text")
        leaf_node = LeafNode(
            None, "This is a text node of type - text", None, None)
        converted_node = text_node_to_html_node(text_node)
        self.assertEqual(converted_node, leaf_node)

    def test_text_node_to_html_node_text(self):
        text_node = TextNode("This is a text node of type - text", "text")
        leaf_node = LeafNode(
            None, "This is a text node of type - text", None, None)
        converted_node = text_node_to_html_node(text_node)
        self.assertEqual(converted_node, leaf_node)

    def test_text_node_to_html_node_text(self):
        text_node = TextNode("This is a text node of type - text", "text")
        leaf_node = LeafNode(
            None, "This is a text node of type - text", None, None)
        converted_node = text_node_to_html_node(text_node)
        self.assertEqual(converted_node, leaf_node)

    def test_repr(self):
        node = TextNode("This is a text node", "bold", "http://test.com")
        self.assertAlmostEqual(
            str(node), "TextNode(This is a text node, bold, http://test.com)")


print(f"__name__: {__name__}")
if __name__ == "__main__":
    unittest.main()
