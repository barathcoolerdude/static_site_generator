from textnode import TextNode, TextType
import shutil
import os
from markdownnode import *
from transfer_file import transfer_files
from generate_page_recursive import generate_page_recursive
import sys

def main():
    example1 = TextNode("example", TextType.PLAIN, None) #test line
    print(example1)

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
        print(f"basepath: {basepath}")
    else:
        basepath = "/"
        print(f"basepath: {basepath}")

    public_dir = "./public"
    index_html_file = "./public/index.html"
    source_path = "./content"
    template_path = "./template.html"
    dest_path = "./docs"

    # create empty public directory
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.makedirs(public_dir, exist_ok=True)

    # transfer files from static t public directory
    transfer_files()
    
    #generate index.html file
    if os.path.isfile(index_html_file):
        os.remove(index_html_file)
    generate_page_recursive(source_path, template_path, dest_path, basepath)


if __name__ == "__main__":
    main()



