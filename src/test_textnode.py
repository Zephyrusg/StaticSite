import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_urlNone(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        self.assertIsNone(node.url)
    def test_urlNotNone(self):
        node = TextNode("This is a text node", TextType.LINK, "http://example.com")
        self.assertEqual(node.url, "http://example.com")

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
if __name__ == "__main__":
    unittest.main()