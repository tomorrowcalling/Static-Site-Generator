import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag=None, value=None, children=None, props ={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        test = node.props_to_html()
        self.assertEqual(test, ' href="https://www.google.com" target="_blank"')

    def test_props_to_None(self):
        node = HTMLNode(tag=None, value=None, children=None, props=None)
        test = node.props_to_html()
        self.assertEqual(test, "")

    def test_props_to_empty(self):
        node = HTMLNode(tag=None, value=None, children=None, props={})
        test = node.props_to_html()
        self.assertEqual(test, "")

    def test_leaf_init(self):
        node = LeafNode(tag="a", value="b", props=None)
        node2 = LeafNode(tag="a", value="b", props=None)
        self.assertEqual(node, node2)

    def test_leaf_no_value(self):
        node = LeafNode(tag="a", value=None, props=None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_no_tag(self):
        node = LeafNode(tag=None, value="b", props=None)
        self.assertEqual(node.to_html(), "b")

    def test_recursion(self):
        with self.assertRaises(RecursionError):
            node = ParentNode(tag='a', children=[], props=None)
            node2 = ParentNode(tag='b', children=[node], props = None)
            node.children = [node2]
            node2.to_html()

    def test_empty_child(self):
        node = ParentNode(tag='div', children=[], props=None)
        result = node.to_html()
        self.assertEqual(result, "<div></div>")

    def test_empty_tag(self):
        with self.assertRaises(ValueError):
            child = LeafNode("b", "test")
            node = ParentNode("", [child])
            result = node.to_html()

    def test_mixed_child_types(self):
        leaf_child = LeafNode("b", "bold text")
        parent_child = ParentNode("i", [LeafNode("span", "nested")])
        mixed_parent = ParentNode("div", [leaf_child, parent_child])
        result = mixed_parent.to_html()
        self.assertEqual(result, "<div><b>bold text</b><i><span>nested</span></i></div>")

    def test_deepnest(self):
        leaf = LeafNode("b", "bold text")
        parent1 = ParentNode("i", [leaf])
        parent2 = ParentNode("u", [parent1])
        parent3 = ParentNode("div", [parent2])
        result = parent3.to_html()
        self.assertEqual(result, "<div><u><i><b>bold text</b></i></u></div>")

    def test_widelevel(self):
        leaf1 = LeafNode("b", "bold text")
        leaf2 = LeafNode("i", "italic text")
        leaf3 = LeafNode("u", "underlined text")
        parent = ParentNode("div", [leaf1,leaf2,leaf3])
        result = parent.to_html()
        self.assertEqual(result,"<div><b>bold text</b><i>italic text</i><u>underlined text</u></div>")

    def test_props(self):
        child = LeafNode("b", "bold text")
        parent = ParentNode("div", [child], {"class": "container", "id": "main"})
        result = parent.to_html()
        self.assertEqual(result,'<div class="container" id="main"><b>bold text</b></div>')

    def test_props_none(self):
        child = LeafNode("span", "text")
        parent = ParentNode("div", [child], None)  # props explicitly set to None
        result = parent.to_html()
        self.assertEqual(result, "<div><span>text</span></div>")

if __name__ == "__main__":
    unittest.main()
