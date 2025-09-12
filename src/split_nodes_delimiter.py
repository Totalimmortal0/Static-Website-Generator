from textnode import *
from regex_matching import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        if delimiter not in node.text:
            result.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("Invalid Markdown syntax: Delimiter not found in node")
        
        for i, chunk in enumerate(parts):
            if not chunk:
                continue
            if i % 2 == 0:
                result.append(TextNode(chunk, TextType.TEXT))
            elif i % 2 != 0:
                result.append(TextNode(chunk, text_type))
    return result


def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        text = node.text
        while True:
            images = extract_markdown_images(text)
            if not images:
                break

            alt, url = images[0]
            match = f"![{alt}]({url})"
            if match not in text:
                break

            before, after = text.split(match, 1)
            if before:
                result.append(TextNode(before, TextType.TEXT))
            result.append(TextNode(alt, TextType.IMAGE, url))
            text = after
        
        if text:
            result.append(TextNode(text, TextType.TEXT))

    return result


def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        text = node.text
        while True:
            links = extract_markdown_links(text)
            if not links:
                break

            label, url = links[0]
            match = f"[{label}]({url})"
            if match not in text:
                break
            
            before, after = text.split(match, 1)
            if before:
                result.append(TextNode(before, TextType.TEXT))
            result.append(TextNode(label, TextType.LINK, url))
            text = after
        
        if text:
            result.append(TextNode(text, TextType.TEXT))

    return result
