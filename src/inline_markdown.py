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

        sub_str = (list(filter(lambda x: x != "", sub_str)))

        if len(sub_str) % 2 == 0:
            raise ValueError(
                "invalid syntax: opening delimiter was found without closing delimiter")

        for i in range(0, len(sub_str)):
            if i % 2 == 0:
                new_nodes.append(TextNode(sub_str[i], TextType.TEXT))
                continue
            new_nodes.append(TextNode(sub_str[i], text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    def get_nodes_from_image_text(node):
        nodes_to_return = []
        extracted_images = extract_markdown_images(node.text)

        if len(extracted_images) < 1:
            return [node]

        sub_str_arr = node.text.split(f"![{extracted_images[0][0]}]({
            extracted_images[0][1]})", 1)

        if sub_str_arr[0] != "":
            nodes_to_return.append(TextNode(sub_str_arr[0], TextType.TEXT))

        nodes_to_return.append(
            TextNode(extracted_images[0][0],
                     TextType.IMAGE, extracted_images[0][1])
        )

        if sub_str_arr[1] != "":
            nodes_to_return.extend(
                get_nodes_from_image_text(TextNode(sub_str_arr[1], TextType.TEXT)))

        return nodes_to_return

    new_nodes = []
    for node in old_nodes:
        n = get_nodes_from_image_text(node)
        new_nodes.extend(n)

    return new_nodes


def split_nodes_link(old_nodes):
    def get_nodes_from_link_text(node):
        nodes_to_return = []
        extracted_links = extract_markdown_links(node.text)

        if len(extracted_links) < 1:
            return [node]

        sub_str_arr = node.text.split(f"[{extracted_links[0][0]}]({
            extracted_links[0][1]})", 1)

        if sub_str_arr[0] != "":
            nodes_to_return.append(TextNode(sub_str_arr[0], TextType.TEXT))

        nodes_to_return.append(
            TextNode(extracted_links[0][0],
                     TextType.LINK, extracted_links[0][1])
        )

        if sub_str_arr[1] != "":
            nodes_to_return.extend(
                get_nodes_from_link_text(TextNode(sub_str_arr[1], TextType.TEXT)))

        return nodes_to_return

    new_nodes = []
    for node in old_nodes:
        n = get_nodes_from_link_text(node)
        new_nodes.extend(n)

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def text_to_text_nodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
