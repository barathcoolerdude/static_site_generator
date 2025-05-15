import unittest

from textnode import TextNode, TextType,text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.PLAIN)
        node2 = TextNode("This is a text node", TextType.PLAIN)
        self.assertEqual(node1, node2)

    def test_is_eq(self):
        node1 = TextNode("this is a line", TextType.PLAIN,None)
        node2 = TextNode("this is a line", TextType.PLAIN,None)
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = TextNode("this is same line",TextType.IMAGE)
        node2 = TextNode("this is not same line",TextType.IMAGE)
        self.assertNotEqual(node1, node2)

    def test_type_not_eq(self):
        node1 = TextNode("this is equal",TextType.LINK,"example.com")
        node2 = TextNode("this is equal",TextType.PLAIN,"example.com")
        self.assertNotEqual(node1, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()