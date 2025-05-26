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
            ],new_nodes
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
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and another one",
        TextType.TEXT,
    )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            TextNode(" and another one", TextType.TEXT),
        ],
        new_nodes
    )
    
    #testing the method's functionality
    def test_split_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and"
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
                TextNode(" and", TextType.TEXT),
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
        self.assertEqual(str(context.exception), "invalid type")

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

    def test_text_to_textnode(self):
        node = TextNode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.TEXT)
        new_nodes = text_to_textnodes(node.text)
        self.assertListEqual(
                [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ], new_nodes
        )

    def test_text_to_textnode_2(self):
        node = TextNode("the _italic_ word and **bold** with a `code` added ![dog](dog.png) and a [cat](cat.com) to one", TextType.TEXT)
        new_nodes = text_to_textnodes(node.text)
        self.assertListEqual(
            [
                TextNode("the ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" with a ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" added ", TextType.TEXT),
                TextNode("dog", TextType.IMAGE, "dog.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("cat", TextType.LINK, "cat.com"),
                TextNode(" to one", TextType.TEXT)
            ],new_nodes
        )

    def test_markdown_to_blocks(self):
            md = """
                This is **bolded** paragraph

                This is another paragraph with _italic_ text and `code` here
                This is the same paragraph on a new line

                - This is a list
                - with items
                """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                            blocks,
                            [
                                "This is **bolded** paragraph",
                                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                                "- This is a list\n- with items",
                            ],
                        )
    def test_markdown_to_blocks_with_images(self):
        md = """
            This is a paragraph with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)"
            ],
        )

    def test_block_to_heading_type(self):
        block = "### this is a heading block"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_code_type(self):
        block = "```print('hello')```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_paragraph_type(self):
        block = "this is paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_quote_type(self):
        block = "> this is a quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_unordered_list_type(self):
        block = "- this is an unordered list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED)

    def test_block_to_ordered_list_type(self):
        block = "1. this is an ordered list\n 3. with items"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED)

if __name__ == "__main__":
    unittest.main()


