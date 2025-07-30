from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType
from blocknode import BlockNode,BlockType
import html
import os
import re



def text_node_to_html_node(text_node):
    if text_node.text_type in (TextType.PLAIN, TextType.TEXT):
        return LeafNode(value=text_node.text, tag=None)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(value=text_node.text, tag="b")
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(value=text_node.text, tag="i")
    elif text_node.text_type == TextType.CODE:
        print("Escaping:", repr(text_node.text))
        escaped = html.escape(text_node.text)
        return LeafNode(value=escaped, tag="code")
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

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(text):
    #heading need tommatch  (\#{1,6} .+)
    text = text.strip()
    if not text:
        return BlockType.PARAGRAPH

    # Check for headings
    if re.match(r"^#{1,6} .+", text):
        return BlockType.HEADING
    elif text.startswith("```"):
        return BlockType.CODE
    elif text.startswith("> "):
        return BlockType.QUOTE
    elif text.startswith("- ") or text.startswith("* "):
        return BlockType.UNORDERED_LIST
    elif text[0].isdigit() and text[1] == '.':
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    NodeChildren = []

    for block in blocks:
        if not block.strip():
            continue
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            # Convert to child nodes, e.g. via text_to_children, then wrap in ParentNode("p")
            lines = block.split("\n")
            paragraph = " ".join(lines)
            normalized_paragraph = " ".join(paragraph.split())
            children = text_to_children(normalized_paragraph)
            NodeChildren.append(ParentNode(tag="p", children=children))
        
        elif block_type == BlockType.HEADING:
            level = 0
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break
            if level + 1 >= len(block):
                raise ValueError(f"invalid heading level: {level}")
            text = block[level + 1 :]
            children = text_to_children(text)
            NodeChildren.append(ParentNode(tag=f"h{level}", children=children))


        elif block_type == BlockType.CODE:
            if not block.startswith("```") or not block.endswith("```"):
                raise ValueError("invalid code block")
            lines = block.split("\n")
            code_content = "\n".join(lines[1:-1])
            escaped = html.escape(code_content)
            code_leaf = LeafNode(value=escaped, tag="code")
            pre = ParentNode("pre", [code_leaf])
            NodeChildren.append(pre)

        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                if not line.strip():
                    continue
                if not line.startswith(">"):
                    raise ValueError("invalid quote block")
                content = (line.lstrip(">").strip())
                if content:
                    new_lines.append(content)
            content = "<br>".join(new_lines)
            children = text_to_children(content)
            NodeChildren.append(ParentNode("blockquote", children))

        elif block_type == BlockType.UNORDERED_LIST:
            items = block.split("\n")
            html_items = []
            for item in items:
                text = item[2:]
                children = text_to_children(text)
                html_items.append(ParentNode("li", children))
            NodeChildren.append(ParentNode("ul", html_items))   

        elif block_type == BlockType.ORDERED_LIST:
            items = block.split("\n")
            html_items = []
            for item in items:
                text = item[item.index(".") + 1:].strip()
                children = text_to_children(text)
                html_items.append(ParentNode("li", children))
            NodeChildren.append(ParentNode("ol", html_items))

        # ...any more block types...

    return ParentNode("div", NodeChildren, None)

def extract_title(markdown):
    """
    Extract the title from the markdown text.
    The title is assumed to be the first heading (h1) in the markdown.
    If no h1 is found, return None.
    """
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING and block.startswith("# "):
            return block[2:].strip()  # Return the text after the '# '
    raise Exception("No title found in the markdown text.")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} using template {template_path} to {dest_path}")
    with open(from_path, 'r') as f:
        content = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    # Replace placeholders in the template with actual content
    html_content = markdown_to_html_node(content).to_html()
    title = extract_title(content)
    template = template.replace("{{ Content }}", html_content)
    template = template.replace("{{ Title }}", title)
    #Write the new full HTML page to a file at dest_path. Be sure to create any necessary directories if they don't exist.
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(template)
        print(f"Page generated successfully at {dest_path}")