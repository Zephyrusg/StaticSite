import unittest

from BlockNode import BlockNode
from BlockNode import BlockType

class TestBlockNode(unittest.TestCase):
    def test_eq(self):
        node = BlockNode("This is a block node", "paragraph")
        node2 = BlockNode("This is a block node", "paragraph")
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = BlockNode("This is a block node", "paragraph")
        node2 = BlockNode("This is a different block node", "paragraph")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = BlockNode("This is a block node", "paragraph")
        self.assertEqual(repr(node), "BlockNode(This is a block node, paragraph)")

    def test_block_to_block_type(self):
        self.assertEqual(BlockNode.block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(BlockNode.block_to_block_type("#### dsafvff"), BlockType.HEADING)
        self.assertEqual(BlockNode.block_to_block_type("```code```"), BlockType.CODE)
        self.assertEqual(BlockNode.block_to_block_type("> Quote"), BlockType.QUOTE)
        self.assertEqual(BlockNode.block_to_block_type("- Unordered list item"), BlockType.UNORDERED_LIST)
        self.assertEqual(BlockNode.block_to_block_type("1. Ordered list item"), BlockType.ORDERED_LIST)
        self.assertEqual(BlockNode.block_to_block_type("Just a paragraph"), BlockType.PARAGRAPH)
        self.assertEqual(BlockNode.block_to_block_type(""), BlockType.PARAGRAPH)  # Empty string should return PARAGRAPH
        self.assertEqual(BlockNode.block_to_block_type("   "), BlockType.PARAGRAPH)