class HTMLNode:
    def __init__(self,tag= None,value= None,children= None,props= None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        # print("it reached the to_html method")
        if self.tag is None:
            raise NotImplementedError("Subclasses should implement this method")

    def props_to_html(self):
        if not self.props:
            return ""
        return " ".join(f'{key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children},props= {self.props})"
    
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.props == other.props and
            self.children == other.children
        )

class ParentNode(HTMLNode):
    def __init__(self,tag,children,props= None):
        super().__init__(tag,None,children,props)

    def to_html(self):
        # print(f"\nit reached parentnode to_html: {self.tag}")
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        if not self.children:
            raise ValueError("All parent nodes must have children")
        return f"<{self.tag}>{to_html_with_recursion(self.children)}</{self.tag}>"
            
class LeafNode(HTMLNode):
    def __init__(self,tag= None,value= None,props= None):
        super().__init__(tag,value,None,props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        attrite = ""
        if self.props:
            attrite = " "+self.props_to_html()
        return f'<{self.tag}{attrite}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={repr(self.value)}, props={self.props})"
    
    
# Recursive function to convert children to HTML
def to_html_with_recursion(children):
    if not children:
        return ""
    return children[0].to_html() + to_html_with_recursion(children[1:])
    
    