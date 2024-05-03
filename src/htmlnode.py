class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None:
            return ""

        def convert(x):
            return f'{x}="{self.props[x]}"'
        html_string = " ".join(map(convert, self.props))
        return html_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None or self.value == "":
            raise ValueError(
                "value cannot be empty for LeafNode")
        if self.tag == None or self.tag == "":
            return self.value
        html_string = wrap_text_with_tags(
            self.tag, self.value, self.props_to_html())
        return html_string


class ParentNode(HTMLNode):
    def __init__(self, tag="", children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("tag cannot be empty")
        if self.children == None or self.children == "":
            raise ValueError("children cannot be empty")

        child_html_string = ""
        for child in self.children:
            child_html_string += child.to_html()

        html_string = wrap_text_with_tags(
            self.tag, child_html_string, self.props_to_html())
        # html_string = f"<{self.tag}>{child_html_string}</{self.tag}>"
        return html_string


def wrap_text_with_tags(tag, value, props):
    if props == None or props == "":
        return f"<{tag}>{value}</{tag}>"
    return f"<{tag} {props}>{value}</{tag}>"
