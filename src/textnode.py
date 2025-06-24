from enum import Enum
from htmlnode import *

def text_node_to_htmlnode(text_node):
    if text_node.text_type == TextType.NORMAL_TEXT:
        return LeafNode(tag=None, value=f"{text_node.text}")
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag='b', value=f"{text_node.text}")
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag='i', value=f"{text_node.text}")
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag='code', value=f"{text_node.text}")
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag='a', value=f"{text_node.text}", props={'href':text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag='img', value="", props={"src":text_node.url, "alt":text_node.text})
    else:
        raise ValueError("Not a valid text type")

class TextType(Enum):
    NORMAL_TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return(
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def to_html(self):
        if self.text_type == TextType.BOLD:
            return f"<b>{self.text}</b>"
        elif self.text_type == TextType.ITALIC:
            return f"<i>{self.text}</i>"
        elif self.text_type == TextType.CODE:
            return f"<code>{self.text}</code>"
        elif self.text_type == TextType.LINK:
            return f'<a href="{self.url}">{self.text}</a>'
        elif self.text_type == TextType.IMAGE:
            return f'<img src="{self.url}" alt="{self.text}"/>'
        else:  # plain text
            return self.text
