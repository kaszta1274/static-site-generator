import re
from textnode import TextNode, TextType

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


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


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            remaining_text = old_node.text
            image_matches = extract_markdown_images(remaining_text)
            if image_matches:
                for alt, url in image_matches:
                    before_text, after_text = remaining_text.split(f"![{alt}]({url})", 1)
                    remaining_text = after_text
                    if before_text != "":
                        new_nodes.append(TextNode(before_text, TextType.TEXT))
                    new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                if remaining_text != "":
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            else:
                new_nodes.append(old_node)
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            remaining_text = old_node.text
            link_matches = extract_markdown_links(remaining_text)
            if link_matches:
                for text, url in link_matches:
                    before_text, after_text = remaining_text.split(f"[{text}]({url})", 1)
                    remaining_text = after_text
                    if before_text != "":
                        new_nodes.append(TextNode(before_text, TextType.TEXT))
                    new_nodes.append(TextNode(text, TextType.LINK, url))
                if remaining_text != "":
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            else:
                new_nodes.append(old_node)
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes