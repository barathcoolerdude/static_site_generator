import os
import shutil


#tranfers file from static to public directory
def transfer_files():
    print(f"process entered transfer_files")
    src = "./static"
    dis = "./docs"

    if os.path.exists(dis):
        shutil.rmtree(dis)
    os.makedirs(dis)
    #recursive function to copy content from source to destination
    def copy_content(src, dis):
            for item in os.listdir(src):
                s_item = os.path.join(src, item)
                d_item = os.path.join(dis, item)

                if os.path.isdir(s_item):
                    os.makedirs(d_item, exist_ok=True)
                    copy_content(s_item, d_item)

                else:
                    shutil.copy2(s_item, d_item)
    copy_content(src, dis)