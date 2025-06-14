from textnode import TextNode, TextType

def main():
    example1 = TextNode("example", TextType.PLAIN, None)
    print(example1)
    transfer_files()

def transfer_files():
    import shutil
    import os

    src = "/home/coolerdude/workspace/static_site_generator/static"
    dis = "/home/coolerdude/workspace/static_site_generator/public"

    if os.path.exists(dis):
        shutil.rmtree(dis)
    os.makedirs(dis)

    print(os.path.exists(dis))
    def copy_content(src, dis):
        for item in os.listdir(src):
            s_item = os.path.join(src, item)
            d_item = os.path.join(dis, item)

            if os.path.isdir(s_item):
                os.makedirs(d_item, exist_ok=True)
                print(f"copying directory {s_item} to {d_item}")
                copy_content(s_item, d_item)

            else:
                shutil.copy2(s_item, d_item)
                print(f"\ncopied content from {s_item} to {d_item}")
    copy_content(src, dis)
    
    


if __name__ == "__main__":
    main()



