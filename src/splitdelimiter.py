import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if delimiter == None or delimiter == "":
        raise Exception("No delimiter found")
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(node)
        elif node.text_type == TextType.NORMAL_TEXT:
                new_node = node.text.split(delimiter)
                if len(new_node)%2 == 0:
                    raise Exception("No closing delimiter")
                for index, element in enumerate(new_node):
                    if index%2 == 0:
                        new_nodes.append(TextNode(element, TextType.NORMAL_TEXT))
                    else:
                        new_nodes.append(TextNode(element.strip(), text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.NORMAL_TEXT)

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(node)
        elif node.text_type == TextType.NORMAL_TEXT:
            n = node.text
            links = extract_markdown_links(n)
            if links == []:
                new_nodes.append(node)
            else:
                for delimiter in links:
                    split_list = n.split(f"[{delimiter[0]}]({delimiter[1]})", 1)
                    if split_list[0] != "":
                        new_nodes.append(TextNode(split_list[0], TextType.NORMAL_TEXT))
                    new_nodes.append(TextNode(f"{delimiter[0]}", TextType.LINK, url=f"{delimiter[1]}"))
                    n = split_list[1]
                if n != "":
                    new_nodes.append(TextNode(n, TextType.NORMAL_TEXT))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(node)
        elif node.text_type == TextType.NORMAL_TEXT:
            n = node.text
            images = extract_markdown_images(n)
            if images == []:
                new_nodes.append(node)
            else:
                for delimiter in images:
                    split_list = n.split(f"![{delimiter[0]}]({delimiter[1]})", 1)
                    new_nodes.append(TextNode(split_list[0], TextType.NORMAL_TEXT))
                    new_nodes.append(TextNode(f"{delimiter[0]}", TextType.IMAGE, url=f"{delimiter[1]}"))
                    n = split_list[1]
                if n != "":
                    new_nodes.append(TextNode(n, TextType.NORMAL_TEXT))
    return new_nodes

def text_to_textnodes(text):
    node = [TextNode(text, TextType.NORMAL_TEXT)]
    nodes = split_nodes_delimiter(node, "**", TextType.BOLD)
    nodes1 = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes2 = split_nodes_delimiter(nodes1, "`", TextType.CODE)
    nodes3 = split_nodes_link(nodes2)
    nodes4 = split_nodes_image(nodes3)
    return nodes4

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return ParentNode(
            tag="a",
            children=[LeafNode(tag=None, value=text_node.text)],
            props={"href": text_node.url}
        )
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(
            tag="img",
            value="",
            props={"src": text_node.url, "alt": text_node.text}
        )
    else:
        return LeafNode(tag=None, value=text_node.text)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(n) for n in text_nodes]
