import unittest

from blocknode import BlockNode
from blocknode import BlockType


class TestBlockNode(unittest.TestCase):
    def test_eq(self):
        node = BlockNode("This is a block node", block_type=BlockType.PARAGRAPH)
        node2 = BlockNode("This is a block node", block_type=BlockType.PARAGRAPH)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = BlockNode("This is a block node", block_type=BlockType.PARAGRAPH)
        node2 = BlockNode("This is a different block node", block_type=BlockType.PARAGRAPH)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = BlockNode("This is a block node", block_type=BlockType.PARAGRAPH)
        self.assertEqual(repr(node), "BlockNode(This is a block node, paragraph)")

    