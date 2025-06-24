import unittest
import re
from splitdelimiter import *
from textnode import TextNode, TextType

class TestSplitDelimiter(unittest.TestCase):
    def test_no_delimiters(self):
        with self.assertRaises(Exception):
            node = TextNode("This is a **bold** text node", TextType.NORMAL_TEXT)
            new_nodes = split_nodes_delimiter([node], None, TextType.BOLD)

    def test_whitespace_delimiters(self):
        with self.assertRaises(Exception):
            node = TextNode("This is a **bold** test node", TextType.NORMAL_TEXT)
            new_nodes = split_nodes_delimiter([node], " ", TextType.NORMAL_TEXT)

    def test_whitespace_textnode(self):
            node = TextNode("      ", TextType.NORMAL_TEXT)
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
            self.assertEqual([node], new_nodes)

    def test_beginningend_delimiters(self):
        node = TextNode("**This is a bold test node**", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual([TextNode("", TextType.NORMAL_TEXT), TextNode("This is a bold test node", TextType.BOLD), TextNode("", TextType.NORMAL_TEXT)], new_nodes)

    def test_consec_delimters(self):
        node = TextNode("**This is a** **bold test node**", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual([TextNode("", TextType.NORMAL_TEXT), TextNode("This is a", TextType.BOLD), TextNode(" ", TextType.NORMAL_TEXT), TextNode("bold test node", TextType.BOLD), TextNode("", TextType.NORMAL_TEXT)], new_nodes)

    def test_notNormalTest(self):
        node = TextNode("This is an **italic** test node", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual([node], new_nodes)

    def test_emptynode(self):
        with self.assertRaises(Exception):
            node = TextNode(None, TextType.NORMAL_TEXT)
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)


    def test_unmatched_delimiters(self):
        with self.assertRaises(Exception):
            node = TextNode("This is a **bold text node", TextType.NORMAL_TEXT)
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_empty_old_nodes(self):
        node = TextNode("", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual([node], new_nodes)

    def test_no_markdown(self):
        node = TextNode("This is text with no markdowns)",TextType.NORMAL_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual([node], new_nodes)

    def test_markdown_beginning(self):
        node = TextNode("[to boot dev](https://www.boot.dev) This is text so markdown is at the beginning", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual([
            TextNode("to boot dev", TextType.LINK, url="https://www.boot.dev"),
            TextNode(" This is text so markdown is at the beginning", TextType.NORMAL_TEXT)
        ], new_nodes)

    def test_multiple_markdown(self):
        node = TextNode("[to boot dev](https://www.boot.dev) This is text with multiple markdowns [to boot dev](https://www.boot.dev)",TextType.NORMAL_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual([
            TextNode("to boot dev", TextType.LINK, url="https://www.boot.dev"),
            TextNode(" This is text with multiple markdowns ", TextType.NORMAL_TEXT),
            TextNode("to boot dev", TextType.LINK, url="https://www.boot.dev")
        ], new_nodes)

    def test_mixed_markdowns(self):
        node = TextNode("This is text with an image ![image](https://i.imgur.com/zjjcJKZ.png) and a link [to boot dev](https://www.boot.dev)",TextType.NORMAL_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual([
            TextNode("This is text with an image ", TextType.NORMAL_TEXT),
            TextNode("image", TextType.IMAGE, url="https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a link [to boot dev](https://www.boot.dev)", TextType.NORMAL_TEXT)
        ], new_nodes)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        output = text_to_textnodes(text)
        self.assertEqual(output, [
            TextNode("This is ", TextType.NORMAL_TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL_TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL_TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL_TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL_TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])
