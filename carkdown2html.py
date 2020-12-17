#!/usr/bin/python3
from sys import argv, exit, stderr
import re


class MarkdownToHTML:
    """Documentation"""
    def __init__(self, mdfile):
        """Documentation"""
        self.content = self.openmdfile(mdfile)
        self.html_content = ''

    def openmdfile(self, mdfile):
        """Documentation"""
        try:
            with open(mdfile, encoding="utf-8") as file:
                return [line.strip('\n') for line in file]
        except IOError:
            print(f"Missing {mdfile}", file=stderr)
            exit(1)

    def savetoHTMLfile(self, htmlfile):
        """Documentation"""
        with open(htmlfile, 'w', encoding='utf-8') as file:
            file.write(self.html_content)

    def parser(self):
        """Documentation"""
        if not self.content:
            print('File is empty')
            exit(0)
        lines = self.content
        print(lines)
        HTML = self.html_content
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

        self.html_content = HTML
        return self.html_content


if __name__ == '__main__':
    if len(argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=stderr)
        exit(1)
    f = argv[1]
    h = argv[2]
    x = MarkdownToHTML(f)
    x.parser()
    print(x.html_content)
    x.savetoHTMLfile(h)
