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