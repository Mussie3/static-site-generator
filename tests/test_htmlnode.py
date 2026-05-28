import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h1", "This is a header title")
        node2 = HTMLNode("h1", "This is a header title")
        self.assertEqual(node, node2)

    def test_value_ineq(self):
        node = HTMLNode("h1", "This is a header title")
        node2 = HTMLNode("h1", "This is a second header title")
        self.assertNotEqual(node, node2)

    def test_children_ineq(self):
        node = HTMLNode("div", None, "<p>Hi</p>")
        node2 = HTMLNode("div", None,"<span>Hi</span>" )
        self.assertNotEqual(node, node2)

    def test_props_ineq(self):
        node = HTMLNode("a", None, None, { "href": "https://www.google.com", "target": "_blank", })
        node2 = HTMLNode("a", None, None, { "href": "https://www.google.com" })
        self.assertNotEqual(node, node2)

    def test_prop_as_html(self):
        inputNode = HTMLNode("a", None, None, { "href": "https://www.google.com", "target": "_blank", })
        input = inputNode.props_to_html()
        result =  'href="https://www.google.com" target="_blank" '
        self.assertEqual(input, result)
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello World!")
        self.assertEqual(node.to_html(), "<p>Hello World!</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()