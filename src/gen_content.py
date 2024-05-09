import os
import pathlib
from block_markdown import (
    markdown_to_lines,
    markdown_to_html_node,
)


def extract_title(markdown):
    lines = markdown_to_lines(markdown)

    for line in lines:
        if line.startswith("# "):
            return line[2:]

    return ""


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {
          dest_path} using {template_path}")
    with open(from_path) as f, open(template_path) as t:
        markdown = f.read()
        template = t.read()
        html = markdown_to_html_node(markdown).to_html()
        title = extract_title(markdown)
        template = template.replace("{{ Title }}", title)
        template = template.replace("{{ Content }}", html)
        dir_name = os.path.dirname(dest_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        new_file = open(dest_path, "w")
        new_file.write(template)
        new_file.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.isfile(dir_path_content):
        generate_page(dir_path_content, template_path, dest_dir_path)
    src_dirname = os.path.dirname(dir_path_content)
    src_basename = os.path.basename(dir_path_content)
    dest_dirname = os.path.dirname(dest_dir_path)
    dest_basename = os.path.basename(dest_dir_path)

    items = os.listdir(src_dirname)
    for item in items:
        src_path = os.path.join(src_dirname, item)
        if not os.path.isfile(src_path):
            generate_page(os.path.join(src_path, src_basename),
                          template_path, os.path.join(dest_dirname, item, dest_basename))

