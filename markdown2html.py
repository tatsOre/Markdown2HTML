#!/usr/bin/python3
"""
Module for markdown2html: It is time to code a Markdown to HTML!
Usage: ./markdown2html.py SAMPLE.md SAMPLE.html
"""
from sys import argv, exit, stderr
import re
import hashlib


def markdown2html(mdfile, htmlfile):
    """Method that interprets/converts Markdown to HTML code:
       Headings, Unordered Lists, Ordered Lists, and paragraphs.
       Text Styles: Bold, Emphasis
       Text Convertions: Encode to MD5, Remove 'c' and 'C' chars.
       Arguments:
        - mdfile[str]: name of the Markdown file
        - htmlfile[str]: output file name
    """
    HTML = ''
    with open(mdfile, encoding="utf-8") as file:
        lines = [line.strip('\n') for line in file]
        list_items = []
        paragraph = []
        for nline, line in enumerate(lines):
            line = styletext(line)
            HEADING = re.search(r"^#{1,6} ", line)
            ULIST = re.search(r"^- ", line)
            OLIST = re.search(r"^\* ", line)

            if HEADING:
                level = len(HEADING.group(0).replace(' ', ''))
                content = line.replace(HEADING.group(0), '')
                HTML += f"<h{level}>{content}</h{level}>\n"

            elif ULIST:
                content = line.replace(ULIST.group(0), '')
                list_items.append(f"<li>{content}</li>\n")
                try:
                    if re.search(r"^- ", lines[nline + 1]) is None:
                        HTML += '<ul>\n' + ''.join(list_items) + '</ul>\n'
                        list_items = []
                except IndexError:
                    HTML += '<ul>\n' + ''.join(list_items) + '</ul>\n'
                    list_items = []

            elif OLIST:
                content = line.replace(OLIST.group(0), '')
                list_items.append(f"<li>{content}</li>\n")
                try:
                    if re.search(r"^\* ", lines[nline + 1]) is None:
                        HTML += '<ol>\n' + ''.join(list_items) + '</ol>\n'
                        list_items = []
                except IndexError:
                    HTML += '<ol>\n' + ''.join(list_items) + '</ol>\n'
                    list_items = []

            elif line:
                try:
                    if lines[nline + 1] == '':
                        paragraph.append(f"{line}")
                        HTML += f"<p>\n{''.join(paragraph)}\n</p>\n"
                        paragraph = []
                    else:
                        paragraph.append(f"{line}\n<br/>\n")
                except IndexError:
                    HTML += f"<p>\n{''.join(paragraph)}\n</p>\n"

    with open(htmlfile, 'w', encoding='utf-8') as file:
        file.write(HTML)
    return HTML


def styletext(line):
    """Method that redirects for possible text styles"""
    line = bold(line)
    line = emphasis(line)
    line = md5(line)
    line = goodbyeC(line)
    return line


def bold(line):
    """Method that parses input and styles a text if the pattern is matched"""
    match = re.findall(r"\*{2}(.+?)\*{2}", line)
    if not match:
        return line
    for item in match:
        line = line.replace(f"**{item}**", f"<b>{item}</b>")
    return line


def emphasis(line):
    """Method that parses input and styles a text if the pattern is matched"""
    match = re.findall(r"__(.+?)__", line)
    if not match:
        return line
    for item in match:
        line = line.replace(f"__{item}__", f"<em>{item}</em>")
    return line


def md5(line):
    """Method that parses input and styles a text if the pattern is matched"""
    match = re.findall(r"\[{2}(.+?)\]{2}", line)
    if not match:
        return line
    content = line.replace('[[', '').replace(']]', '')
    for item in match:
        encoded = hashlib.md5(item.lower().encode()).hexdigest()
        content = content.replace(item, encoded)
    return content


def goodbyeC(line):
    """Method that parses input and styles a text if the pattern is matched"""
    match = re.findall(r"\({2}(.+?)\){2}", line)
    if not match:
        return line
    content = line.replace('((', '').replace('))', '')
    content = content.replace('c', '').replace('C', '')
    return content


if __name__ == '__main__':
    if len(argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=stderr)
        exit(1)
    try:
        markdown2html(mdfile=argv[1], htmlfile=argv[2])
        exit(0)
    except IOError:
        print("Missing {}".format(argv[1]), file=stderr)
        exit(1)
