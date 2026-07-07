import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

class TestSplitDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes, 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_multiple_code(self):
        node = TextNode("This `has` two `code` blocks", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes, 
            [
                TextNode("This ", TextType.TEXT),
                TextNode("has", TextType.CODE),
                TextNode(" two ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" blocks", TextType.TEXT),
            ]
        )
    
    def test_code_at_start(self):
        node = TextNode("`code block` text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes, 
            [
                TextNode("code block", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ]
        )

    def test_code_invalid(self):
        node = TextNode("`code block text", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    
    def test_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes, 
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ]
        )

    def test_italic(self):
        node = TextNode("This is _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes, 
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ]
        )
   

if __name__ == "__main__":
    unittest.main()