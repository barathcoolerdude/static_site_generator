import re
from textnode import TextNode , TextType

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
    #loop through all the nodes
    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            raise Exception("Invalid type")
        
        text = old_node.text
        #rejecting non text nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue 

        #extracting the image url and alt text
        text_urls = extract_markdown_images(text)

        #loop through the tuples of alt text and image url
        for alt_text, image_url in text_urls:

            #exit if there are no text
            if not text_urls:
                break

            #if the alt text or image url is empty, append the old node
            if not alt_text or not image_url:
                new_nodes.append(old_node)
                continue

            #splitting the text into sections
            sections = text.split(f"![{alt_text}]({image_url})",1)

            #case if image is at the start
            if sections[0] == "":
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))
                text = sections[1]
            
            #case if text is at the start
            else:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))
                text = sections[1]
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    #loop through all the nodes
    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            raise Exception("Invalid type")
        text = old_node.text

        #rejecting non text nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue 

        #extracting the image url and alt text
        text_urls = extract_markdown_links(text)

        #loop through the tuples of alt text and image url
        for anker_text, url in text_urls:

            #exit if there are no text
            if not text_urls:
                break

            #if the alt text or image url is empty, append the old node
            if not anker_text or not url:
                new_nodes.append(old_node)
                continue

            #splitting the text into sections
            sections = text.split(f"[{anker_text}]({url})",1)

            #case if image is at the start
            if sections[0] == "":
                new_nodes.append(TextNode(anker_text, TextType.LINK, url))
                text = sections[1]
            
            #case if text is at the start
            else:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(anker_text, TextType.LINK, url))
                text = sections[1]
    return new_nodes

