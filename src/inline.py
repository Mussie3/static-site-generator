import re
from textnode import TextNode, TextType
from typing import List

class Inline():

    def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
        new_nodes = []
        for node in old_nodes:
            splited_text = node.text.split(delimiter)
            for i, text in enumerate(splited_text):
                if len(text) == 0:
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(text, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(text, text_type))

        return new_nodes

    def extract_markdown_images(text: str) -> List[(str, str)]:
        image_info = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
        return image_info

    def split_at_markdown_images(text: str) -> List[str]:
        text_info = re.split(r"(!\[[^\[\]]*\]\([^\(\)]*\))", text)
        return text_info

    def extract_markdown_links(text: str) -> List[(str, str)]:
        link_info = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
        return link_info

    def split_at_markdown_links(text: str) -> List[str]:
        text_info = re.split(r"(!\[[^\[\]]*\]\([^\(\)]*\))|((?<!\!)\[[^\[\]]*\]\([^\(\)]*\))", text)
        return text_info

    def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
        new_nodes = []
        for node in old_nodes:
            segments = Inline.split_at_markdown_images(node.text)
            for segment in segments:
                if not segment:
                    continue
                match = re.match(r"!\[(.*?)\]\((.*?)\)", segment)
                if match:
                    new_nodes.append(TextNode(match.group(1), TextType.IMAGE, match.group(2)))
                else:
                    new_nodes.append(TextNode(segment, TextType.TEXT))

        return new_nodes

    def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
        new_nodes = []
        for node in old_nodes:
            segments = Inline.split_at_markdown_links(node.text)
            for segment in segments:
                if not segment:
                    continue
                match = re.match(r"(?<!\!)\[(.*?)\]\((.*?)\)", segment)
                if match:
                    new_nodes.append(TextNode(match.group(1), TextType.LINK, match.group(2)))
                else:
                    new_nodes.append(TextNode(segment, TextType.TEXT))

        return new_nodes