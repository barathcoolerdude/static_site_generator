from textnode import TextNode, TextType
from markdownnode import *
from transfer_file import transfer_files
from generate_page_recursive import generate_page_recursive
import sys

def main():
    example1 = TextNode("example", TextType.PLAIN, None) #test line
    print(example1)

    if len(sys.argv) > 1:
        print(f"sys.argc[1]: {sys.argv[1]}")
        basepath = sys.argv[1]
    else:
        basepath = "/"

    source_path = "./content"
    template_path = "./template.html"
    dest_path = "./docs"

    # transfer files from static t public directory
    transfer_files()
    
    generate_page_recursive(source_path, template_path, dest_path, basepath)


if __name__ == "__main__":
    main()
