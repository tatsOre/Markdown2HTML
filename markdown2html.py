#!/usr/bin/python3
"""Module for markdown2html"""
from sys import argv, exit, stderr
import re


def markdown2html(mdfile, htmlfile):
    """It is time to code a Markdown to HTML!"""
    HTML = ''
    with open(mdfile, encoding="utf-8") as file:
        lines = [line.strip('\n') for line in file]
        list_items = []
        for nline, line in enumerate(lines):
            HEADING = re.search(r"^#{1,6} ", line)
            ULIST = re.search(r"^- ", line)
            OLIST = re.search(r"^\* ", line)
            BOLD = re.findall(r"\*{2}(.+?)\*{2}", line)
            EMPHASIS = re.findall(r"_{2}(.+?)_{2}", line)

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

            elif BOLD:
                content = line.replace('**', '')
                for item in BOLD:
                    content = content.replace(item, f"<b>{item}</b>")
                HTML += f"{content}\n"

            elif EMPHASIS:
                content = line.replace('__', '')
                for item in EMPHASIS:
                    content = content.replace(item, f"<em>{item}</em>")
                HTML += f"{content}\n"

    with open(htmlfile, 'w', encoding='utf-8') as file:
        file.write(HTML)
    return HTML


if __name__ == '__main__':
    if len(argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=stderr)
        exit(1)
    try:
        RET = markdown2html(mdfile=argv[1], htmlfile=argv[2])
        exit(0)
    except IOError:
        print("Missing {}".format(argv[1]), file=stderr)
        exit(1)
