import unittest
from functions import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images
from textnode import TextNode, TextType

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

    
if __name__ == "__main__":
    unittest.main()