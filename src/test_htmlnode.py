from htmlnode import HTMLNode, LeafNode, ParentNode
import unittest as unittest


if __name__ == "__main__":
    props = {"href": "https://example.com", "target": "_blank"}
    node = HTMLNode("a", "click here",None, props)

    print("props to HTML:")
    print(node.props_to_html())

    print("\nOject representation:")
    print(repr(node))
    
class TestHTMLNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, World!")
        self.assertEqual(node.to_html(),"<p>Hello, World!</p>")

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

if __name__== "__main__":
    unittest.main()