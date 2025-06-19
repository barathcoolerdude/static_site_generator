import re
from textnode import TextNode , TextType, text_node_to_html_node
import enum
from htmlnode import HTMLNode , ParentNode, LeafNode



class BlockType(enum.Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"

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
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
            
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
    split_markdowns = markdown.split("\n\n")
    striped_markdowns = [split_markdown.strip() for split_markdown in split_markdowns if split_markdown.strip()]
    cleaned_markdown = [re.sub(r"\n[ \t]+", "\n", striped_markdown) for striped_markdown in striped_markdowns]
    return cleaned_markdown

def block_to_block_type(markdown):
    if re.match(r"^(#{1,6})\s", markdown):
        return  BlockType.HEADING
    elif re.match(r"^```[\s\S]*?```$", markdown):
        return BlockType.CODE
    elif re.match(r"^\s*>", markdown):
        return BlockType.QUOTE
    elif re.match(r"^(?:- .*\n?)*$", markdown):
        return BlockType.UNORDERED
    elif re.match(r"^\d+\. ", markdown):
        return BlockType.ORDERED
    else:
        return BlockType.PARAGRAPH

def get_tag_from_block_type(block_type, markdown):
    if block_type == BlockType.HEADING:
        matches = re.match(r"^(#{1,6})*", markdown)
        if matches:
            level = len(matches.group(1))
        else:
            None
        return "h", level
    elif block_type == BlockType.CODE:
        return "code", None
    elif block_type == BlockType.QUOTE:
        return "blockquote", None
    elif block_type == BlockType.UNORDERED:
        return "ul", None
    elif block_type == BlockType.ORDERED:
        return "ol", None
    else:
        return "p", None  # default for paragraphs

def text_to_children(text):
    if not text:
        return []
    htmlnodes = []
    textnodes = text_to_textnodes(text)
    for textnode in textnodes:
        htmlnodes.append(text_node_to_html_node(textnode))
    return htmlnodes

def markdown_to_html_node(markdown):
    parent = ParentNode("div", [])
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block = block.strip()
        block_type = block_to_block_type(block)
        tag, matches = get_tag_from_block_type(block_type, block)

        if tag == "p":
            node = ParentNode(tag,text_to_children(block))
            parent.children.append(node)

        elif tag == "h":
            cleaned_heading = block.lstrip("#").strip()
            node = ParentNode(f"{tag}{matches}", text_to_children(cleaned_heading))
            parent.children.append(node)

        elif tag == "code":
            cleaned_block = block.strip().strip("`")
            text_node = TextNode(cleaned_block, TextType.CODE)
            children_node = text_node_to_html_node(text_node)
            node = ParentNode("pre", children = [children_node])
            parent.children.append(node)
    
        elif tag == "blockquote":
            cleaned_block = block.lstrip(">").strip()
            node = ParentNode(tag, text_to_children(cleaned_block))
            parent.children.append(node)

        elif tag == "ul":
            item_list = block.split("\n")
            cleaned_item = list(map(lambda x: x.lstrip("-").strip(), item_list))
            children_node = [
                ParentNode("li", text_to_children(item))
                for item in cleaned_item
            ]
            parent.children.append(ParentNode(tag, children_node))
    
        elif tag == "ol":
            item_list = block.split("\n")
            cleaned_item = [re.sub(r"^\d+\.\s*", "", item) for item in item_list]
            children_node = [
                ParentNode("li", text_to_children(item))
                for item in cleaned_item
            ]
            parent.children.append(ParentNode(tag, children_node))

        else:
            raise ValueError(f"Unknown block type: {block_type}")
        
    return parent

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        line = line.strip()
        if re.match(r'^#(?!#)\s*\S', line):
            return line.lstrip("#").strip()
    raise Exception("No title found in the markdown")


        
        
    
