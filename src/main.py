from textnode import TextNode, TextType
from osfunctions import clear_directory, copy_directory, copy_static_to_public
def main():
    node1 = TextNode("Hello", TextType.PLAIN, "http://example.com")
    print(node1)
    copy_static_to_public("static", "public", verbose=True)
main()
