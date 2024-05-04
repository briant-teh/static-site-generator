from textnode import TextNode, TextType
from inline_markdown import extract_markdown_links


def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
    print(node)

    node2 = TextNode("This is text with a [link](https://www.example.com) ", TextType.TEXT)
    print(extract_markdown_links(node2.text))


main()
