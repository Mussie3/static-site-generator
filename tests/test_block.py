import unittest
from block import Block, BlockType

class TestBlock(unittest.TestCase):
        def test_markdown_to_blocks_eq(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = Block.markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

        def test_markdown_to_blocks_ineq(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list - with items
"""
            blocks = Block.markdown_to_blocks(md)
            self.assertNotEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )
        
        def test_block_to_code_type_eq(self):
            given = """```
def function():
    print("Hello")
```"""
            type = Block.block_to_block_type(given)
            self.assertEqual(type, BlockType.CODE)

        def test_block_to_heading_type_eq(self):
            given = "### Heading 3" 
            type = Block.block_to_block_type(given)
            self.assertEqual(type, BlockType.HEADING)

        def test_block_to_quote_type_eq(self):
            given = """> This is a quote
>This is a quote as well""" 
            type = Block.block_to_block_type(given)
            self.assertEqual(type, BlockType.QUOTE)

        def test_block_to_unordered_type_eq(self):
            given = """- First
- Second
- Third""" 
            type = Block.block_to_block_type(given)
            self.assertEqual(type, BlockType.UNORDERED_LIST)

        def test_block_to_ordered_type_eq(self):
            given = """1. First
2. Second
3. Third""" 
            type = Block.block_to_block_type(given)
            self.assertEqual(type, BlockType.ORDERED_LIST)

        def test_block_to_paragraph_type_eq(self):
            given = "This is paragraph" 
            type = Block.block_to_block_type(given)
            self.assertEqual(type, BlockType.PARAGRAPH)

        def test_block_to_code_type_ineq(self):
            given = """``
def function():
    print("Hello")
``""" 
            type = Block.block_to_block_type(given)
            self.assertNotEqual(type, BlockType.CODE)

        def test_block_to_heading_type_ineq(self):
            given = "######## Not Heading"
            type = Block.block_to_block_type(given)
            self.assertNotEqual(type, BlockType.HEADING)

        def test_block_to_quote_type_ineq(self):
            given = "This is not a quote as well"
            type = Block.block_to_block_type(given)
            self.assertNotEqual(type, BlockType.QUOTE)

        def test_block_to_unordered_type_ineq(self):
            given = "-This should not be correct"
            type = Block.block_to_block_type(given)
            self.assertNotEqual(type, BlockType.UNORDERED_LIST)
        
        def test_block_to_ordered_type_ineq(self):
            given = """1. This should be correct
4. This isn't correct""" 
            type = Block.block_to_block_type(given)
            self.assertNotEqual(type, BlockType.ORDERED_LIST)
        def test_paragraphs(self):
            md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

            node = Block.markdown_to_html_node(md)
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

            node = Block.markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            )

        def test_headings(self):
            md = """
# Heading 1

## Heading **bold** 2

###### Heading 6
"""
            node = Block.markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><h1>Heading 1</h1><h2>Heading <b>bold</b> 2</h2><h6>Heading 6</h6></div>",
            )

        def test_quote(self):
            md = """
> This is a quote
> with multiple lines
> and _italic_ text
"""
            node = Block.markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><blockquote>This is a quote with multiple lines and <i>italic</i> text</blockquote></div>",
            )

        def test_unordered_list(self):
            md = """
- first item
- second **bold** item
- third item
"""
            node = Block.markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><ul><li>first item</li><li>second <b>bold</b> item</li><li>third item</li></ul></div>",
            )

        def test_ordered_list(self):
            md = """
1. first
2. second `code`
3. third
"""
            node = Block.markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><ol><li>first</li><li>second <code>code</code></li><li>third</li></ol></div>",
            )

        def test_mixed_blocks(self):
            md = """
# Title

Some **paragraph**.

- item 1
- item 2
"""
            node = Block.markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><h1>Title</h1><p>Some <b>paragraph</b>.</p><ul><li>item 1</li><li>item 2</li></ul></div>",
            )