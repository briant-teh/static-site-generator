import unittest

from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode,
)


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "link", None, {
                        "href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(),
                         'href="https://www.google.com" target="_blank"')

    def test_props_to_html_none(self):
        node = HTMLNode("a", "link", None, None)
        self.assertEqual(node.props_to_html(), '')

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), '<p>This is a paragraph of text.</p>')

    def test_leaf_no_value_no_value(self):
        node = LeafNode("a", None)
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "This is a paragraph of text.")

    def test_parent_to_html_p(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(
        ), "<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p>")

    def test_parent_to_html_nested_two_layers(self):
        parent_node1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        leaf_node1 = LeafNode(
            "a", "Click me!", {"href": "https://www.google.com", "target": "_blank"})

        parent_node2 = ParentNode(
            "p",
            [
                parent_node1,
                leaf_node1
            ]
        )
        self.assertEqual(parent_node2.to_html(
        ), '<p><p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p>' +
            '<a href="https://www.google.com" target="_blank">Click me!</a></p>')

    def test_parent_to_html_nested_three_layers(self):
        parent_node1 = ParentNode("p", [LeafNode("b", "Bold text")])
        parent_node2 = ParentNode("p", [parent_node1])
        parent_node3 = ParentNode(
            "p", [parent_node2], {"class": "nested-paragraphs"})

        self.assertEqual(parent_node3.to_html(
        ), '<p class="nested-paragraphs"><p><p><b>Bold text</b></p></p></p>')

    def test_parent_to_html_no_tag(self):
        node = ParentNode(None)
        self.assertRaises(ValueError, node.to_html)

    def test_parent_to_html_no_children(self):
        node = ParentNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_eq(self):
        node1 = HTMLNode("a", "This is a link", None, {
                         "href": "https://www.google.com"})
        node2 = HTMLNode("a", "This is a link", None, {
                         "href": "https://www.google.com"})
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = HTMLNode("a", "This is a link", None, {
                         "href": "https://www.google.com"})
        node2 = HTMLNode("a", "Click me!", None, {
                         "href": "https://www.google.com"})
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node = HTMLNode("p", "This is a paragraph", None, None)
        self.assertEqual(
            str(node), "HTMLNode(p, This is a paragraph, None, None)")
