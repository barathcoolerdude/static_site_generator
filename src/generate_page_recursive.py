import os
import shutil
from markdownnode import markdown_to_html_node, extract_title
def generate_page_recursive(from_path, template_path, dest_file):
    print(f"Generating page from {from_path} to {dest_file} using {template_path}")

    with open(from_path, "r") as file:
        source_content = file.read()
    
    with open(template_path, "r") as file:
        template_content = file.read()

    title = extract_title(source_content)
    content = markdown_to_html_node(source_content)
    html = content.to_html()
    htmloutput = template_content.replace("{{ Content }}", html).replace("{{ Title }}", title)

    if not os.path.exists(os.path.dirname(dest_file)):
        os.makedirs(os.path.dirname(dest_file), exist_ok= True)
    with open(dest_file, "w") as file:
        file.write(htmloutput)
    

    