import os
import shutil
from markdownnode import markdown_to_html_node, extract_title

def generate_page_recursive(source_path, template_path, dest_path,basepath):
    if os.path.isdir(source_path):

        for item in os.listdir(source_path):
            item_path = os.path.join(source_path, item)

            if os.path.isdir(item_path):
                sub_source_path = os.path.join(source_path, item)
                sub_dest_path = os.path.join(dest_path, item)
                if os.path.exists(sub_dest_path):
                    shutil.rmtree(sub_dest_path)
                os.makedirs(sub_dest_path, exist_ok=True)
                generate_page_recursive(sub_source_path, template_path, sub_dest_path, basepath)

            elif item.endswith(".md"):
                file_from_path = os.path.join(source_path, item)
                file_dest_file = os.path.join(dest_path, item.replace(".md", ".html"))
                generate_page(file_from_path, template_path, file_dest_file, basepath)


def generate_page(from_path, template_path, dest_file, basepath):

    with open(from_path, "r") as file:
        source_content = file.read()
    
    with open(template_path, "r") as file:
        template_content = file.read()

    title = extract_title(source_content)
    content = markdown_to_html_node(source_content)
    html = content.to_html()
    htmloutput = template_content.replace("{{ Content }}", html).replace("{{ Title }}", title)
    basepath = "helloworld"
    htmloutput = htmloutput.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    with open(dest_file, "w") as file:
        file.write(htmloutput)


    