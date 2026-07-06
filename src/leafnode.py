from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}" + self.props_to_html() + f">{self.value}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"{self.tag} {self.value} {self.props}"