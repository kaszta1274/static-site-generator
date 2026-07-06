from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("All parent nodes must have children")
        
        result = f"<{self.tag}" + self.props_to_html() + f">"
        for child in self.children:
            result += child.to_html()
        return result + f"</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"{self.tag} {self.children} {self.props}"