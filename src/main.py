from textnode import TextNode, TextType
from osfunctions import clear_directory, copy_directory, copy_static_to_public
from functions import generate_pages_recursive
import sys

def main(args):
    if(args and len(args) > 1):
        basepath = args[1]
    else:
        basepath = "/"

    copy_static_to_public("static", "docs", verbose=True)
    generate_pages_recursive("content", "template.html", "docs", basepath)
    #generate_page("content/index.md", "template.html", "public/index.html")
    #generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")
    #generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")
    #generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")
    #generate_page("content/contact/index.md", "template.html", "public/contact/index.html")

main(sys.argv)
