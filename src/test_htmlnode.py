import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode(value="Hello", tag="p", children=None, props={"class": "text"})
        self.assertTrue(node.value == "Hello")
        self.assertTrue(node.tag == "p")
        self.assertTrue(node.children is None)
        self.assertTrue(node.props == {"class": "text"})

    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_non_empty(self):
        node = HTMLNode(props={"class": "text", "id": "main"})
        self.assertEqual(node.props_to_html(), 'class="text" id="main"')
    
    def test_leafnode_to_html(self):
        node = LeafNode(value="Hello", tag="p", props={"class": "text"})
        self.assertEqual(node.to_html(), '<p class="text">Hello</p>')

    def test_leafnode_to_html_no_props(self):
        node = LeafNode(value="Hello", tag="p")
        self.assertEqual(node.to_html(), '<p>Hello</p>')

    def test_leafnode_to_html_no_value(self):
        node = LeafNode(value=None, tag="p")
        with self.assertRaises(ValueError):
            node.to_html()  

    def test_leafnode_to_html_no_tag(self):
        node = LeafNode(value="Hello", tag=None)
        self.assertEqual(node.to_html(), "Hello")

    def test_parentnode_to_html(self):
        child1 = LeafNode(value="Child 1", tag="span")
        child2 = LeafNode(value="Child 2", tag="span")
        node = ParentNode(tag="div", children=[child1, child2], props={"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container"><span>Child 1</span><span>Child 2</span></div>')

    def test_parentnode_to_html_no_props(self):
        child1 = LeafNode(value="Child 1", tag="span")
        child2 = LeafNode(value="Child 2", tag="span")
        node = ParentNode(tag="div", children=[child1, child2])
        self.assertEqual(node.to_html(), '<div><span>Child 1</span><span>Child 2</span></div>')

    def test_parentnode_to_html_no_tag(self):
        child1 = LeafNode(value="Child 1", tag="span")
        child2 = LeafNode(value="Child 2", tag="span")
        node = ParentNode(tag=None, children=[child1, child2])
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_parentnode_to_html_no_children(self):
        node = ParentNode(tag="div", children=None)
        with self.assertRaises(ValueError):
            node.to_html()