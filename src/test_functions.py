from textnode import TextNode, TextType  
from functions import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links

def test_text_node_to_html_node(self):
    text_node = TextNode("Hello", TextType.PLAIN)
    html_node = text_node_to_html_node(text_node)
    self.assertEqual(html_node.value, "Hello")
    self.assertIsNone(html_node.tag)

    text_node = TextNode("Bold Text", TextType.BOLD)
    html_node = text_node_to_html_node(text_node)
    self.assertEqual(html_node.value, "Bold Text")
    self.assertEqual(html_node.tag, "b")

    text_node = TextNode("Italic Text", TextType.ITALIC)
    html_node = text_node_to_html_node(text_node)
    self.assertEqual(html_node.value, "Italic Text")
    self.assertEqual(html_node.tag, "i")

    text_node = TextNode("Code Snippet", TextType.CODE)
    html_node = text_node_to_html_node(text_node)
    self.assertEqual(html_node.value, "Code Snippet")
    self.assertEqual(html_node.tag, "code")

    text_node = TextNode("Link", TextType.LINK, "http://example.com")
    html_node = text_node_to_html_node(text_node)
    self.assertEqual(html_node.value, "Link")
    self.assertEqual(html_node.tag, "a")
    self.assertEqual(html_node.props["href"], "http://example.com")

    text_node = TextNode("Image", TextType.IMAGE, "http://example.com/image.png")
    html_node = text_node_to_html_node(text_node)
    self.assertEqual(html_node.value, "")
    self.assertEqual(html_node.tag, "img")
    self.assertEqual(html_node.props["src"], "http://example.com/image.png")
    self.assertEqual(html_node.props["alt"], "Image")

def test_split_nodes_delimiter(self):
    nodes = [TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)]
    delimiter = "**"
    text_type = TextType.BOLD
    new_nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    self.assertEqual(len(new_nodes), 3)
    self.assertEqual(new_nodes[0].text, "This is text with a ")
    self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    self.assertEqual(new_nodes[1].text, "bolded phrase")
    self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
    self.assertEqual(new_nodes[2].text, " in the middle")
    self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    # Test with no delimiter
    nodes = [TextNode("Hello world", TextType.TEXT)]
    new_nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    self.assertEqual(len(new_nodes), 1)
    self.assertEqual(new_nodes[0].text, "Hello world")

    # Test unmatched delimiter raises Exception
    nodes = [TextNode("Hello **bla world", TextType.TEXT)]
    with self.assertRaises(Exception) as context:
        split_nodes_delimiter(nodes, delimiter, TextType.BOLD)
    self.assertEqual(
        str(context.exception),
        "Invalid Markdown syntax: unmatched delimiter '**' in text 'Hello **bla world'"
    )

def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

def test_extract_markdown_links(self):
    matches = extract_markdown_links(
        "This is text with a [link](https://example.com)"
    )
    self.assertListEqual([("link", "https://example.com")], matches)

def test_extract_markdown_links_exclamationmark(self):
    matches = extract_markdown_links(
        "This is text with a [link](https://example.com) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("link", "https://example.com")], matches)
    