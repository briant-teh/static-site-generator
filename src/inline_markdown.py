import re

from textnode import (
    TextNode,
    TextType
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        sub_str = node.text.split(delimiter)

        if len(sub_str) <= 1:
            new_nodes.append(TextNode(node.text, TextType.TEXT, node.url))
            continue

        if len(sub_str) % 2 == 0:
            raise ValueError(
                "invalid syntax: opening delimiter was found without closing delimiter")

        for i in range(0, len(sub_str)):
            if i % 2 == 0:
                new_nodes.append(TextNode(sub_str[i], TextType.TEXT))
                continue
            new_nodes.append(TextNode(sub_str[i], text_type))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)
