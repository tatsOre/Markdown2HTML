#!/usr/bin/python3
"""
Module for markdown2html: It is time to code a Markdown to HTML!
Usage: ./markdown2html.py SAMPLE.md SAMPLE.html
Class Version
"""
from sys import argv, exit, stderr
import re
import hashlib


class MarkdownToHTML:
    """Interprets/converts Markdown to HTML code:
       Headings, Unordered Lists, Ordered Lists, and paragraphs.
       Text Styles: Bold, Emphasis
       Text Convertions: Encode to MD5, Remove 'c' and 'C' chars.
       Reads .md file and save output to .html file
    """
    def __init__(self, mdfile):
        """Initializes a instance"""
        self.content = self.openmdfile(mdfile)
        self.html_content = ''
        self.__list_items = []

    def openmdfile(self, mdfile):
        """Opens the input markdown file"""
        try:
            with open(mdfile, encoding="utf-8") as file:
                return [line.strip('\n') for line in file]
        except IOError:
            print(f"Missing {mdfile}", file=stderr)
            exit(1)

    def savetoHTMLfile(self, htmlfile):
        """Creates if not exists and saves output to HTML file"""
        with open(htmlfile, 'w', encoding='utf-8') as file:
            file.write(self.html_content)

    def parser(self):
        """Documentation"""
        if not self.content:
            print('File is empty')
            exit(0)

        HTML = self.html_content
        paragraph = []

        for nline, line in enumerate(self.content):
            HEADING = re.search(r"^#{1,6} ", line)
            ULIST = re.search(r"^- ", line)
            OLIST = re.search(r"^\* ", line)

            if HEADING:
                level = len(HEADING.group(0).replace(' ', ''))
                content = line.replace(HEADING.group(0), '')
                HTML += f"<h{level}>{content}</h{level}>\n"

            elif ULIST or OLIST:
                LIST = OLIST if OLIST else ULIST
                pattern = r"^- " if ULIST else r"^\* "
                tags = ['<ul>', '</ul>'] if ULIST else ['<ol>', '</ol>']
                content = self.ziptolist(LIST, line, pattern, tags)
                if content:
                    HTML += content
                    self.__list_items = []

            elif line:
                line = self.styletext(line)  # Looks for bold, emphasis style
                try:
                    if self.content[nline + 1] == '':
                        paragraph.append(f"{line}")
                        HTML += f"<p>\n{''.join(paragraph)}\n</p>\n"
                        paragraph = []
                    else:
                        paragraph.append(f"{line}\n<br/>\n")
                except IndexError:
                    HTML += f"<p>\n{''.join(paragraph)}\n</p>\n"

        self.html_content = HTML
        return self.html_content

    def ziptolist(self, LIST, line, pattern, tags):
        """Method that wraps list items in urordered or ordered list"""
        LINES = self.content
        content = line.replace(LIST.group(0), '')
        content = self.styletext(content)  # Looks for bold, emphasis style
        self.__list_items.append(f"<li>{content}</li>\n")
        try:
            if not re.search(pattern, LINES[LINES.index(line) + 1]):
                return f"{tags[0]}\n{''.join(self.__list_items)}{tags[1]}\n"
        except IndexError:
            return f"{tags[0]}\n'{''.join(self.__list_items)}{tags[1]}\n"

    def styletext(self, line):
        """Method that redirects for possible text styles"""
        line = self.bold(line)
        line = self.emphasis(line)
        line = self.md5(line)
        line = self.goodbyeC(line)
        return line

    def bold(self, line):
        """
        Method that parses input and styles a text if the pattern is matched
        """
        match = re.findall(r"\*{2}(.+?)\*{2}", line)
        if not match:
            return line
        for item in match:
            line = line.replace(f"**{item}**", f"<b>{item}</b>")
        return line

    def emphasis(self, line):
        """
        Method that parses input and styles a text if the pattern is matched
        """
        match = re.findall(r"__(.+?)__", line)
        if not match:
            return line
        for item in match:
            line = line.replace(f"__{item}__", f"<em>{item}</em>")
        return line

    def md5(self, line):
        """
        Method that parses input and styles a text if the pattern is matched
        """
        match = re.findall(r"\[{2}(.+?)\]{2}", line)
        if not match:
            return line
        content = line.replace('[[', '').replace(']]', '')
        for item in match:
            encoded = hashlib.md5(item.lower().encode()).hexdigest()
            content = content.replace(item, encoded)
        return content

    def goodbyeC(self, line):
        """
        Method that parses input and styles a text if the pattern is matched
        """
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

    code = MarkdownToHTML(argv[1])
    code.parser()
    code.savetoHTMLfile(argv[2])
