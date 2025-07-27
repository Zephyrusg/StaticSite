from htmlnode import LeafNode
from textnode import TextNode, TextType

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

def extract_markdown_images(text):
    import re
    pattern = r'!\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    import re
    pattern = r'(?<!!)\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return matches

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # Only split nodes of type TEXT
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = extract_markdown_links(node.text)
        if not parts:
            new_nodes.append(node)
            continue

        # Split the text into segments based on links
        segments = []
        last_index = 0
        for text, url in parts:
            start_index = node.text.find(f"[{text}]({url})", last_index)
            if start_index == -1:
                raise ValueError(f"Link '{text}' not found in text '{node.text}'")
            if last_index < start_index:
                segments.append(TextNode(node.text[last_index:start_index], TextType.TEXT))
            segments.append(TextNode(text, TextType.LINK, url))
            last_index = start_index + len(f"[{text}]({url})")

        if last_index < len(node.text):
            segments.append(TextNode(node.text[last_index:], TextType.TEXT))

        new_nodes.extend(segments)

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # Only split nodes of type TEXT
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = extract_markdown_images(node.text)
        if not parts:
            new_nodes.append(node)
            continue

        # Split the text into segments based on images
        segments = []
        last_index = 0
        for alt_text, url in parts:
            start_index = node.text.find(f"![{alt_text}]({url})", last_index)
            if start_index == -1:
                raise ValueError(f"Image '{alt_text}' not found in text '{node.text}'")
            if last_index < start_index:
                segments.append(TextNode(node.text[last_index:start_index], TextType.TEXT))
            segments.append(TextNode(alt_text, TextType.IMAGE, url))
            last_index = start_index + len(f"![{alt_text}]({url})")

        if last_index < len(node.text):
            segments.append(TextNode(node.text[last_index:], TextType.TEXT))

        new_nodes.extend(segments)

    return new_nodes

text= "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

def text_to_textnodes(text):
    if not text:
        return []

    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)


    return nodes

def markdown_to_blocks(text):
    if not text:
        return []
    # Split on two or more newlines, strip whitespace from each block, and filter out empty blocks
    blocks = [block.strip() for block in text.split("\n\n") if block.strip()]
    return blocks
