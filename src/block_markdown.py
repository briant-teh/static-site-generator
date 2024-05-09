import re
import os

from enum import Enum
from htmlnode import (
    LeafNode,
    ParentNode,
)

from textnode import text_node_to_html_node

from inline_markdown import text_to_text_nodes


class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = list(filter(lambda x: x != "", blocks))
    blocks = list(map(lambda x: x.strip(), blocks))
    return blocks


def markdown_to_lines(markdown):
    blocks = markdown_to_blocks(markdown)
    lines = []
    for block in blocks:
        lines.extend(block.split("\n"))
    return lines


def block_to_block_type(block):
    if len(block) > 6 and block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE

    lines = block.split("\n")

    is_block_type = {
        BlockType.HEADING: True,
        BlockType.QUOTE: True,
        BlockType.UNORDERED_LIST: True,
        BlockType.ORDERED_LIST: True,
    }

    ordered_list_counter = 1

    for line in lines:
        if len(line) < 2:
            continue

        if not re.search(r"^(#{1,6} (.+?))", line):
            is_block_type[BlockType.HEADING] = False

        if line[0] != ">":
            is_block_type[BlockType.QUOTE] = False

        if not (line[:2] == "* " or line[:2] == "- "):
            is_block_type[BlockType.UNORDERED_LIST] = False

        if not (line[:2] == str(ordered_list_counter) + "."):
            is_block_type[BlockType.ORDERED_LIST] = False

        ordered_list_counter += 1

    for type in is_block_type:
        if is_block_type[type]:
            return type

    return BlockType.PARAGRAPH


def block_to_paragraph(block):
    text_nodes = text_to_text_nodes(block)
    html_nodes = list(map(text_node_to_html_node, text_nodes))

    if len(html_nodes) == 1:
        if html_nodes[0].tag == None:
            return LeafNode("p", html_nodes[0].value)
        return html_nodes[0]
    return ParentNode("p", html_nodes)


def block_to_heading(block):
    sub_str = block.split(" ", 1)
    hashes = sub_str[0]
    if hashes == "#":
        tag = "h1"
    elif hashes == "##":
        tag = "h2"
    elif hashes == "###":
        tag = "h3"
    elif hashes == "####":
        tag = "h4"
    elif hashes == "#####":
        tag = "h5"
    else:
        tag = "h6"

    text_nodes = text_to_text_nodes(sub_str[1])
    if len(text_nodes) <= 1:
        return LeafNode(tag, sub_str[1])

    html_nodes = list(map(text_node_to_html_node, text_nodes))
    return ParentNode(tag, html_nodes)


def block_to_code(block):
    text_nodes = text_to_text_nodes(block[3:-3])
    if len(text_nodes) <= 1:
        return ParentNode("pre", [
            LeafNode("code", block[3:-3])
        ])

    html_nodes = list(map(text_node_to_html_node, text_nodes))
    return ParentNode("pre", [
        ParentNode("code", html_nodes)
    ])


def block_to_quote(block):
    lines = block.split("\n")
    value = "\n".join(list(map(lambda x: x[1:].strip(), lines)))

    text_nodes = text_to_text_nodes(value)
    if len(text_nodes) <= 1:
        return LeafNode("blockquote", value)

    html_nodes = list(map(text_node_to_html_node, text_nodes))
    return ParentNode("blockquote", html_nodes)


def block_to_unordered_list(block):
    lines = block.split("\n")
    nodes = []
    for line in lines:
        value = line[2:]
        text_nodes = text_to_text_nodes(value)
        if len(text_nodes) <= 1:
            nodes.append(LeafNode("li", value))
            continue

        html_nodes = list(map(text_node_to_html_node, text_nodes))
        nodes.append(ParentNode("li", html_nodes))

    return ParentNode("ul", nodes)


def block_to_ordered_list(block):
    lines = block.split("\n")

    def get_list_value(line):
        value = line.split(".", 1)[1]
        return value.strip()

    nodes = []
    for line in lines:
        value = get_list_value(line)
        text_nodes = text_to_text_nodes(value)
        if len(text_nodes) <= 1:
            nodes.append(LeafNode("li", value))
            continue

        html_nodes = list(map(text_node_to_html_node, text_nodes))
        nodes.append(ParentNode("li", html_nodes))

    return ParentNode("ol", nodes)


def block_to_html_node(block, type):
    if type == BlockType.PARAGRAPH:
        return block_to_paragraph(block)
    if type == BlockType.HEADING:
        return block_to_heading(block)
    if type == BlockType.CODE:
        return block_to_code(block)
    if type == BlockType.QUOTE:
        return block_to_quote(block)
    if type == BlockType.UNORDERED_LIST:
        return block_to_unordered_list(block)
    if type == BlockType.ORDERED_LIST:
        return block_to_ordered_list(block)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        nodes.append(block_to_html_node(block, block_to_block_type(block)))

    return ParentNode("div", nodes)
