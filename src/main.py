from gen_content import (
    generate_page,
    generate_pages_recursive,
)
from copy_static import copy_directory
import os
import shutil


def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    copy_directory("static", "public")

    generate_pages_recursive(
        "content/index.md", "template.html", "public/index.html")


main()
