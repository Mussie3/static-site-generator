from typing import List

class HTMLNode():

    def __init__(self, tag: str = None, value: str = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None:
            return
        text = ""
        for key in self.props:
            text += f'{key}="{self.props[key]}" '
        
        return text

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

    def __repr__(self):
        return f"""
            tags: {self.tag},\n
            value: {self.value},\n
            children: {self.children},\n
            props: {self.props}
        """

class LeafNode(HTMLNode):
    def __init__(self, tag: str = None, value: str = None, props = None):
        self.tag = tag
        self.value = value
        self.props = props
        super()
    
    def to_html(self):
        if self.value == None:
            raise ValueError()
        elif self.tag == None:
            return self.value
        else:
            props = ""
            if self.props != None:
                for key in self.props:
                    props += f' {key}="{self.props[key]}"' 
            return f"<{self.tag}{props}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"""
            tags: {self.tag},\n
            value: {self.value},\n
            props: {self.props}
        """

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: List[LeafNode], props=None):
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag == None:
            raise ValueError("A node can't be a parent with no tag")
        elif self.children == None:
            raise ValueError("A parent node can't be a parent node with no child")
        else:
            props = ""
            if self.props != None:
                for key in self.props:
                    props += f' {key}="{self.props[key]}"'
            for leafNode in self.children:
                child = leafNode.to_html()
                return f"<{self.tag}{props}>{child}</{self.tag}>"