from textnode import TextNode, TextType
from copystatic import copy_contents

def main() -> None:
    copy_contents("static", "public")

if __name__ == "__main__":
    main()
