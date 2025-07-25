from enum import Enum
from src.htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    PLAIN = "plain"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return NotImplemented
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)
    
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.PLAIN:
        return LeafNode(value=text_node.text, tag=None)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(value=text_node.text, tag="b")
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(value=text_node.text, tag="i")
    elif text_node.text_type == TextType.CODE:
        return LeafNode(value=text_node.text, tag="code")
    elif text_node.text_type == TextType.LINK:
        return LeafNode(value=text_node.text, tag="a", props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(value="", tag="img", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unknown text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # Only split nodes of type TEXT
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        # If delimiter not found, just add the node
        if len(parts) == 1:
            new_nodes.append(node)
            continue

        # If odd number of delimiters, raise an error
        if len(parts) % 2 == 0:
            raise Exception(f"Invalid Markdown syntax: unmatched delimiter '{delimiter}' in text '{node.text}'")

        # Alternate between TEXT and the given text_type
        for i, part in enumerate(parts):
            if part == "":
                continue  # skip empty segments
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes