import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, markdown_to_html_node, BlockType

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
    

class TestBlocksToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """
# Heading 1

###### Heading 6

## **Bold heading**
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h6>Heading 6</h6><h2><b>Bold heading</b></h2></div>",
        )

    def test_lists(self):
        md = """
- 1
- **2**
- 3

1. 1
2. _second_
3. 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>1</li><li><b>2</b></li><li>3</li></ul><ol><li>1</li><li><i>second</i></li><li>3</li></ol></div>",
        )

    def test_quote(self):
        md = """
> The time you enjoy wasting is not wasted time.

> Believe you can
> and you're halfway there.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>The time you enjoy wasting is not wasted time.</blockquote><blockquote>Believe you can and you're halfway there.</blockquote></div>",
        )


if __name__ == "__main__":
    unittest.main()