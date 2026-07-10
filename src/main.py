from textnode import TextNode, TextType
from copystatic import copy_contents
from generate_page import generate_page

def main() -> None:
    copy_contents("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()
