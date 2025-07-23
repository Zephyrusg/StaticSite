from textnode import TextNode, TextType

def main():
    node1 = TextNode("Hello", TextType.PLAIN, "http://example.com")
    print(node1)

main()