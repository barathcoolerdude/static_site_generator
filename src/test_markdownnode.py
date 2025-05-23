import unittest

from markdownnode import *

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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_mark_down_images(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev","https://www.boot.dev"),("to youtube","https://www.youtube.com/@bootdotdev")],matches)

    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ],
        new_nodes,
    )
    
    #testing the method's functionality
    def test_split_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
                        ,TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
             [
               TextNode("This is text with a link ", TextType.TEXT),
               TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
               TextNode(" and ", TextType.TEXT),
               TextNode(
                   "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
               ),
            ], new_nodes
        )

#a dummy for the test
class dummy(unittest.TestCase):
    pass

    #testing invalid text text
    def test_split_image_invalid_type(self):
        node= dummy()
        with self.assertRaises(Exception) as context:
            split_nodes_image([node])
        self.assertEqual(str(context.exception), "Invalid type")

    #if link is at the start
    def test_split_link_at_start(self):
        node= TextNode("[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],new_nodes
        )

    #if url is at the end
    def test_split_image_at_end(self):
        node = TextNode("this is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("this is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],new_nodes
        )

if __name__ == "__main__":
    unittest.main()