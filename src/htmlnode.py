class HTMLNode:
    def __init__(self, value = None, tag = None, children = None, props = None):
        self.value = value
        self.tag = tag
        self.children = children 
        if props is None:
            props = {}
        self.props = props
    
    def __repr__(self):
        return f"HTMLNode(value={self.value}, tag={self.tag}, children={self.children}, props={self.props})"

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method")
    
    def props_to_html(self):
        if not self.props:
            return ""
        
        return " ".join(f'{key}="{value}"' for key, value in self.props.items())

class LeafNode(HTMLNode):
    def __init__(self, value, tag, props = None):
        super().__init__(value, tag, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("Leaf node must have a value")
        if not self.tag:
            return self.value
        attribute_string = self.props_to_html()
        space_or_empty = f" {attribute_string}" if attribute_string else ""
        return f"<{self.tag}{space_or_empty}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(None, tag, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node must have a tag")
        if not self.children:
            raise ValueError("Parent node must have children")
        attribute_string = self.props_to_html()
        space_or_empty = f" {attribute_string}" if attribute_string else ""
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{space_or_empty}>{children_html}</{self.tag}>"