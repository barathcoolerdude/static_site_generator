import re
from textnode import TextNode , TextType
print()
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        text = old_node.text
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_string = []
        sections = text.split(delimiter)
        if len(sections)%2 == 0:
            raise Exception("Invalid number of delimiter")
        
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i%2 == 0:
                split_string.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_string.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_string)
    return new_nodes

    #extract images url and alt text 
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches

    #extract anker text and url
def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            raise Exception("invalid type")

        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        matches = extract_markdown_images(text)
        if not matches:
            new_nodes.append(old_node)
            continue

        for alt_text, image_url in matches:
            split_text = text.split(f"![{alt_text}]({image_url})", 1)
            
            if len(split_text) != 2:
                continue

            if not split_text[0]:
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))
                text = split_text[1]

            else:
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))
                text = split_text[1]
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
            
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    #loop through all the nodes
    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            raise Exception("Invalid type")

        #rejecting non text nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue 

        text = old_node.text
        matches = extract_markdown_links(text)

        for alt_text, url in matches:
            if not matches:
                new_nodes.append(old_node)
                break
            
            split_text = text.split(f"[{alt_text}]({url})",1)

            if len(split_text) != 2:
                continue

            #case if text is at the start
            if not split_text[0]:
                new_nodes.append(TextNode(alt_text, TextType.LINK, url))
                text = split_text[1]
            
            #case if image is at the start
            else:
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                new_nodes.append(TextNode(alt_text, TextType.LINK, url))
                text = split_text[1]
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
        
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes

def markdown_to_blocks(markdown):
    print(markdown)
    split_markdowns = markdown.split("\n\n")
    striped_markdowns = [split_markdown.strip() for split_markdown in split_markdowns if split_markdown.strip()]
    cleaned = [re.sub(r"\n[ \t]+", "\n", striped_markdown) for striped_markdown in striped_markdowns]
    return cleaned

