import re
from enum import Enum
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes

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

def quote_to_text(block:str) -> str:
    result = ""
    lines = block.split("\n")
    for line in lines:
        result += line[1:].lstrip() + " "
    return result[:-1]

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    results: list[HTMLNode] = []
    for text_node in text_nodes:
        results.append(text_node_to_html_node(text_node))
    return results

def unordered_list_to_children(block: str) -> list[HTMLNode]:
    children: list[HTMLNode] = []
    lines = block.split("\n")
    for line in lines:
        value = line[2:]
        children.append(ParentNode(tag="li", children=text_to_children(value)))
    return children

def ordered_list_to_children(block: str) -> list[HTMLNode]:
    children: list[HTMLNode] = []
    lines = block.split("\n")
    for line in lines:
        _, value = line.split(". ", 1)
        children.append(ParentNode(tag="li", children=text_to_children(value)))
    return children

def markdown_to_html_node(markdown: str) -> HTMLNode:
    html_nodes: list[HTMLNode] = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                text = block.replace("\n", " ")
                children = text_to_children(text)
                block_node = ParentNode(tag="p", children=children)

            case BlockType.HEADING:
                i = block.count("#", 0, 7)
                text = block[i+1:]
                children = text_to_children(text)
                block_node = ParentNode(tag=f"h{i}", children=children)

            case BlockType.CODE:
                text = block[4:-3]
                block_node = ParentNode(tag="pre", children=[LeafNode(tag="code", value=text)])

            case BlockType.QUOTE:
                text = quote_to_text(block)
                children = text_to_children(text)
                block_node = ParentNode(tag="blockquote", children=children)

            case BlockType.UNORDERED_LIST:
                children = unordered_list_to_children(block)
                block_node = ParentNode(tag="ul", children=children)

            case BlockType.ORDERED_LIST:
                children = ordered_list_to_children(block)
                block_node = ParentNode(tag="ol", children=children)

        html_nodes.append(block_node)

    return ParentNode(tag="div", children=html_nodes)