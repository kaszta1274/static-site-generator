import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType

class TestBlocks(unittest.TestCase):
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

    def test_markdown_to_blocks_empty_space(self):
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
    
    def test_block_to_block_type_heading(self):
        heading_block = "### Heading"
        self.assertEqual(
            block_to_block_type(heading_block),
            BlockType.HEADING
        )
        heading_block = "###### Heading"
        self.assertEqual(
            block_to_block_type(heading_block),
            BlockType.HEADING
        )
        not_heading_block = "####### not a heading"
        self.assertEqual(
            block_to_block_type(not_heading_block),
            BlockType.PARAGRAPH
        )
        not_heading_block = "##"
        self.assertEqual(
            block_to_block_type(not_heading_block),
            BlockType.PARAGRAPH
        )
        not_heading_block = "#Hello"
        self.assertEqual(
            block_to_block_type(not_heading_block),
            BlockType.PARAGRAPH
        )
        not_heading_block = "Hello"
        self.assertEqual(
            block_to_block_type(not_heading_block),
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_code(self):
        code_block = "```\ncode```"
        self.assertEqual(
            block_to_block_type(code_block),
            BlockType.CODE
        )
        not_code_block = "```code```"
        self.assertEqual(
            block_to_block_type(not_code_block),
            BlockType.PARAGRAPH
        )
        not_code_block = "```\ncode"
        self.assertEqual(
            block_to_block_type(not_code_block),
            BlockType.PARAGRAPH
        )
        not_code_block = "code```"
        self.assertEqual(
            block_to_block_type(not_code_block),
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_quote(self):
        quote_block = "> Hello\n>Hello"
        self.assertEqual(
            block_to_block_type(quote_block),
            BlockType.QUOTE
        )
        not_quote_block = "> Hello\nHello"
        self.assertEqual(
            block_to_block_type(not_quote_block),
            BlockType.PARAGRAPH
        )
        not_quote_block = " Hello\n>Hello"
        self.assertEqual(
            block_to_block_type(not_quote_block),
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_unordered(self):
        unordered_block = "- Hello\n- Hello"
        self.assertEqual(
            block_to_block_type(unordered_block),
            BlockType.UNORDERED_LIST
        )
        not_unordered_block = "- Hello\n-Hello"
        self.assertEqual(
            block_to_block_type(not_unordered_block),
            BlockType.PARAGRAPH
        )
        not_unordered_block = "Hello\n- Hello"
        self.assertEqual(
            block_to_block_type(not_unordered_block),
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_ordered(self):
        unordered_block = "1. first\n2. second"
        self.assertEqual(
            block_to_block_type(unordered_block),
            BlockType.ORDERED_LIST
        )
        unordered_block = "2. first\n3. second"
        self.assertEqual(
            block_to_block_type(unordered_block),
            BlockType.PARAGRAPH
        )
        unordered_block = "1.first"
        self.assertEqual(
            block_to_block_type(unordered_block),
            BlockType.PARAGRAPH
        )
        unordered_block = "1. first\n3. second"
        self.assertEqual(
            block_to_block_type(unordered_block),
            BlockType.PARAGRAPH
        )
        

if __name__ == "__main__":
    unittest.main()