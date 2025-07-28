from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

class BlockNode:
    def __init__(self, content: str, block_type: BlockType):
        self.content = content
        self.block_type = block_type

    def __repr__(self):
        block_type_str = self.block_type.value if hasattr(self.block_type, "value") else str(self.block_type)
        return f"BlockNode({self.content}, {block_type_str})"

    def __eq__(self, other):
        if not isinstance(other, BlockNode):
            return NotImplemented
        return (self.content == other.content and
                self.block_type == other.block_type)

