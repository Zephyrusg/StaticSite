from textnode import TextNode, TextType
from osfunctions import clear_directory, copy_directory, copy_static_to_public
from functions import generate_page
def main():
    node1 = TextNode("Hello", TextType.PLAIN, "http://example.com")
    print(node1)
    copy_static_to_public("static", "public", verbose=True)
    generate_page("content/index.md", "template.html", "public/index.html")

main()
