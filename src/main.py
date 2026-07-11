from textnode import TextNode, TextType
from copystatic import copy_contents
from generate_page import generate_pages_recursive

def main() -> None:
    copy_contents("static", "public")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
