import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    result = []
    for block in blocks:
        block = block.strip()
        if block != "":
            result.append(block)
    return result

def block_to_block_type(block: str) -> BlockType:
    heading_matches = re.findall(r"^#{1,6} .+", block)
    if heading_matches:
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split("\n")

    quote = True
    for line in lines:
        if not line.startswith(">"):
            quote = False
            break
    if quote:
        return BlockType.QUOTE
    
    unordered = True
    for line in lines:
        if not line.startswith("- "):
            unordered = False
            break
    if unordered:
        return BlockType.UNORDERED_LIST
    
    ordered = True
    i = 1
    for line in lines:
        if not line.startswith(f"{i}. "):
            ordered = False
            break
        i += 1
    if ordered:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH