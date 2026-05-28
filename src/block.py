import re
from enum import Enum
from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType
from inline import Inline

class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6



class Block():

    def markdown_to_blocks(markdown: str):
        new_clean_list = []
        markdown_list = markdown.split("\n\n")
        for each in markdown_list:
            clean_text = each.strip()
            new_clean_list.append(clean_text)

        return new_clean_list
    
    def block_to_block_type(markdown: str):
        lines = markdown.split("\n")

        if markdown.startswith("#"):
            if re.match(r"^#{1,6} \w+", markdown):
                return BlockType.HEADING
            
        elif markdown.startswith("```"):
            if markdown.startswith("```\n") and markdown.endswith("```") and len(markdown) >= 7:
                return BlockType.CODE
            
        elif markdown.startswith(">"):
            is_valid_quote = True
            for line in lines:
                if not re.match(r"^>( ?)(.*)$", line):
                    is_valid_quote = False
                    break
            if is_valid_quote:
                return BlockType.QUOTE
            
        elif markdown.startswith("- "):
            is_valif_ul = True
            for line in lines:
                if not line.startswith("- "):
                    is_valif_ul = False
                    break
            if is_valif_ul:
                return BlockType.UNORDERED_LIST
            
        elif markdown.startswith("1. "):
            is_valid_ol = True
            expected_number = 1
            for line in lines:
                match = re.match(r"^(\d+)\. (.*)$", line)
                if not match:
                    is_valid_ol = False
                    break

                current_number = int(match.group(1))
                if current_number != expected_number:
                    is_valid_ol = False
                    break

                expected_number += 1

            if is_valid_ol:
                return BlockType.ORDERED_LIST
        else:
            return BlockType.PARAGRAPH
    
    def text_to_children(text):
        children_node = []
        children_text_nodes = Inline.text_to_textnodes(text)
        for child in children_text_nodes:
            children_node.append(Block.text_node_to_html_node(child))
        return children_node

    def markdown_to_html_node(markdown):
        block_nodes = []
        blocks = Block.markdown_to_blocks(markdown)
        for block in blocks:
            if len(block) == 0:
                continue
            type = Block.block_to_block_type(block)
            match type:
                case BlockType.HEADING:
                    level = len(block) - len(block.lstrip("#"))
                    text = block[level + 1:]
                    node = ParentNode(f"h{level}", Block.text_to_children(text))
                case BlockType.CODE:
                    code_text = block.removeprefix("```\n").removesuffix("```")
                    node = ParentNode("code", code_text)
                case BlockType.QUOTE:
                    lines = [re.sub(r"^>\s?", "", line) for line in block.split("\n")]
                    text = " ".join(lines)
                    node = ParentNode("blockquote", Block.text_to_children(text))
                case BlockType.UNORDERED_LIST:
                    items = [
                        ParentNode("li", Block.text_to_children(line.removeprefix("- ")))
                        for line in block.split("\n")
                    ]
                    node = ParentNode("ul", items)
                case BlockType.ORDERED_LIST:
                    items = [
                        ParentNode("li", Block.text_to_children(re.sub(r"^\d+\. ", "", line)))
                        for line in block.split("\n")
                    ]
                    node = ParentNode("ol", items)
                case _:
                    text = " ".join(block.split("\n"))
                    node = ParentNode("p", Block.text_to_children(text))
            block_nodes.append(node)

        return ParentNode("div", block_nodes)

    def text_node_to_html_node(text_node: TextNode):
        match text_node.text_type:
            case TextType.TEXT:
                return LeafNode(None, text_node.text, None)
            case TextType.BOLD:
                return LeafNode("b", text_node.text, None)
            case TextType.ITALIC:
                return LeafNode("i", text_node.text, None)
            case TextType.CODE:
                return LeafNode("code", text_node.text, None)
            case TextType.LINK:
                return LeafNode("a", text_node.text, { "href": text_node.url })
            case TextType.IMAGE:
                return LeafNode("img", "", { "src": text_node.url, "alt": text_node.text })
            case _:
                raise Exception("Not Valid type!")
            

md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
node = Block.markdown_to_html_node(md)
html = node.to_html()
print(html)