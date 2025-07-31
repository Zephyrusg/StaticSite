from textnode import TextNode, TextType
from osfunctions import clear_directory, copy_directory, copy_static_to_public
from functions import generate_pages_recursive
def main():
    node1 = TextNode("Hello", TextType.PLAIN, "http://example.com")
    print(node1)
    copy_static_to_public("static", "public", verbose=True)
    generate_pages_recursive("content", "template.html", "public")
    #generate_page("content/index.md", "template.html", "public/index.html")
    #generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")
    #generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")
    #generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")
    #generate_page("content/contact/index.md", "template.html", "public/contact/index.html")

main()
