import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        else:
            split = old_node.text.split(delimiter)
            if len(split) % 2 != 1:
                raise Exception("Invalid Markdown syntax")
            for i in range(len(split)):
                if split[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(split[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split[i], text_type))

    return new_nodes
    
def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)