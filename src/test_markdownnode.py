import unittest

from markdownnode import split_nodes_delimiter

from textnode import TextNode, TextType

class TestDinlinemarkdown(unittest.TestCase):
    def test_bold_delimiter(self):
        node = TextNode("this is a **bold** sentence",TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("this is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" sentence", TextType.TEXT)
            ]
        ,new_nodes
        )

    def test_double_bold_delimiter(self):
        node = TextNode("this is a **bold** and **bold** sentence",TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("this is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" sentence", TextType.TEXT)
            ],new_nodes
        )
        
    def test_invalid_delimiter(self):
        node = TextNode("this is a **bold** and **bold sentence",TextType.TEXT)
        with self.assertRaises(Exception) as context: 
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(context.exception), "Invalid number of delimiter")

    def test_italic_delimiter(self):
        node = TextNode("this is a __italic__ sentence", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "__", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("this is a ",TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" sentence",TextType.TEXT)
            ],new_nodes
        )

if __name__ == "__main__":
    unittest.main()