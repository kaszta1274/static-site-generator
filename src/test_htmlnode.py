import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_no_values(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_init(self):
        node = HTMLNode("p", "Test")
        self.assertEqual(node.tag, "p")

    def test_props_to_html(self):
        node = HTMLNode("p", "Test", None, { "href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    

if __name__ == "__main__":
    unittest.main()