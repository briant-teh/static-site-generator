import unittest

from textnode import (
    TextNode,
    TextType
)

from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
    text_to_text_nodes
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

    def test_extract_markdown_images_no_image(self):
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

    def test_split_nodes_image(self):
        node = TextNode("This is text with an " +
                        "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)" +
                        " and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
                        TextType.TEXT)

        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE,
                     "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE,
                     "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
        ])

    def test_split_nodes_image_just_image(self):
        node = TextNode("![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
                        TextType.TEXT)

        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("image", TextType.IMAGE,
                     "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
        ])

    def test_split_nodes_image_no_alt(self):
        node = TextNode("This is text with an " +
                        "(https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)" +
                        " and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
                        TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with an (https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE,
                     "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
        ])

    def test_split_nodes_image_no_image(self):
        node = TextNode("This is text with no image", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with no image", TextType.TEXT),
        ])

    def test_split_nodes_image_multiple_nodes(self):
        node1 = TextNode("This is just text", TextType.TEXT)
        node2 = TextNode(
            "This is text with an ![image](https://www.example.com/images/cat.png) of a cat", TextType.TEXT)
        new_nodes = split_nodes_image([node1, node2])
        self.assertEqual(
            new_nodes, [
                TextNode("This is just text", TextType.TEXT),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://www.example.com/images/cat.png"),
                TextNode(" of a cat", TextType.TEXT),
            ]
        )

    def test_split_nodes_link(self):
        node = TextNode("This is text with a [link](https://www.example.com)" +
                        " and another [second link](https://www.example.com/other)",
                        TextType.TEXT)

        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.example.com"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second link", TextType.LINK,
                     "https://www.example.com/other"),
        ])

    def test_split_nodes_link_just_link(self):
        node = TextNode("[link](https://www.catcatcat.com)",
                        TextType.TEXT)

        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("link", TextType.LINK,
                     "https://www.catcatcat.com"),
        ])

    def test_split_nodes_link_no_anchor(self):
        node = TextNode("This is text with a (https://www.example.com)" +
                        " and another [second link](https://www.example.com/other)",
                        TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode(
                "This is text with a (https://www.example.com) and another ", TextType.TEXT),
            TextNode("second link", TextType.LINK,
                     "https://www.example.com/other"),
        ])

    def test_split_nodes_link_no_link(self):
        node = TextNode("This is text with no link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with no link", TextType.TEXT),
        ])

    def test_split_nodes_link_multiple_nodes(self):
        node1 = TextNode("This is just text", TextType.TEXT)
        node2 = TextNode(
            "This is text with a [link](https://www.example.com) to a website", TextType.TEXT)
        new_nodes = split_nodes_link([node1, node2])
        self.assertEqual(
            new_nodes, [
                TextNode("This is just text", TextType.TEXT),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK,
                         "https://www.example.com"),
                TextNode(" to a website", TextType.TEXT),
            ]
        )

    def test_text_to_text_node(self):
        text = "This is **text** with an *italic* word and a `code block` and an " + \
            "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/" + \
            "course_assets/zjjcJKZ.png) and a [link](https://www.google.com)"
        self.assertEqual(text_to_text_nodes(text), [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE,
                     "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.google.com"),
        ])


print(f"__name__: {__name__}")
if __name__ == "__main__":
    unittest.main()
