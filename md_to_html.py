"""
FILE:       md_to_html.py
AUTHOR:     Ben Simcox
PROJECT:    probable-guacamole
PURPOSE:    Recursively compile markdown to html
"""
import re


def _parse_bold_italic(token: str) -> str:
    """Handle bold and italic"""
    if re.search("^\\*{3}.+\\*{3}$", token):
        return "<bold><em>" + token[3:-3] + "</em></bold>"
    if re.search("^\\*{3}", token):
        return "<bold><em>" + token[3:]
    if re.search("\\*{3}$", token):
        return token[:-3] + "</em></bold>"
    return token


def _parse_bold(token: str) -> str:
    """Handle bold"""
    if re.search("^\\*{2}.+\\*{2}$", token):
        return "<bold>" + token[2:-2] + "</bold>"
    if re.search("^\\*{2}", token):
        return "<bold>" + token[2:]
    if re.search("\\*{2}$", token):
        return token[:-2] + "</bold>"
    return token


def _parse_italic(token: str) -> str:
    """Handle Italics"""
    if re.search("^\\*.+\\*$", token):
        return "<em>" + token[1:-1] + "</em>"
    if re.search("^\\*", token):
        return "<em>" + token[1:]
    if re.search("\\*$", token):
        return token[:-1] + "</em>"
    return token


def _read_markdown(markdown_file_location: str) -> list:
    """Reads a markdown file and returns a list of lines"""
    with open(markdown_file_location) as file:
        return file.readlines()


def _parse_code_snippet(token: str) -> str:
    """Handle inline code snippets"""
    if re.search("^`.+`$", token):
        return "<code>" + token[1:-1] + "</code>"
    if re.search("^`", token):
        return "<code>" + token[1:]
    if re.search("`$", token):
        return token[:-1] + "</code>"
    return token


def _parse_link(token: str) -> str:
    """parse and return a link"""
    text = re.search(r"\[(.+)\]", token).group(1)
    url = re.search(r"\((.+)\)", token).group(1)
    return "<a href=\"" + url + "\">" + text + "</a>"


def _parse_image(token: str) -> str:
    """parse and return an html image"""
    text = re.search(r"\[(.+)\]", token).group(1)
    path = re.search(r"\((.+)\)", token).group(1)
    return "<img src=\"" + path + "\" alt=\"" + text + "\"" + " />"


def _parse_inline_syntax(token: str) -> str:
    """check for and handle inline syntax, statement order is meaningful"""
    punctuation = ""
    if re.search(r"!\[(.+)\]\((.+)\)", token):
        return _parse_image(token)
    if re.search(r"\[((.+)(\s*)(.*))\]\((.+)\)", token):
        return _parse_link(token)
    # This line handles punctuation adjacent to significant asterix
    if re.match("[^a-zA-Z0-9_\\*`]", token[-1]):
        punctuation = token[-1]
        token = token[:-1]
    if re.search("^\\*{3}", token) or re.search("\\*{3}$", token):
        return _parse_bold_italic(token) + punctuation
    if re.search("^\\*{2}", token) or re.search("\\*{2}$", token):
        return _parse_bold(token) + punctuation
    if re.search("^\\*", token) or re.search("\\*$", token):
        return _parse_italic(token) + punctuation
    if re.search("^`", token) or re.search("`$", token):
        return _parse_code_snippet(token) + punctuation
    return token + punctuation


def _parse_paragraph(line: list) -> str:
    """Parse markdown return html paragraph"""
    paragraph_text = ""
    if len(line) == 1 and line[0] == '\n':
        return paragraph_text
    for word in line:
        paragraph_text += _parse_inline_syntax(word)
    return "<p>" + paragraph_text.strip() + "</p>\n"


def _parse_heading(line: list, level: int) -> str:
    """process an html heading"""
    heading = "<h" + str(level) + ">"
    line = line[1:]
    while line:
        token = line.pop(0)
        heading += _parse_inline_syntax(token)
    return heading.strip() + "</h" + str(level) + ">\n"


def _parse_block_quote(line: list) -> str:
    """return a block quote"""
    quote = "\n<blockquote>"
    for word in line:
        quote += _parse_inline_syntax(word)
    return quote + "</blockquote>\n"


def _get_list_type(line: list) -> str:
    """determine if a list item is ordered or unorderd"""
    for item in line:
        if item == '\t':
            continue
        if item in ["*", "-"]:
            return "<ul>"
        if re.fullmatch("[0-9]+\\.", item):
            return "<ol>"
        return ""


def _strip_list_item(line: list) -> list:
    """strip leading white space and list number or bullet"""
    stripped_list = []
    for item in line:
        if item in ['\t', '\n', '*', '-'] or re.fullmatch("[0-9]+\\.", item):
            continue
        stripped_list.append(item)
    return stripped_list[1:]


class Compiler:
    """Compiler class manages markdown to html compiling"""

    def __init__(self, markdown_file_location: str):
        """Initialize attributes"""
        self.md_tokens = _read_markdown(markdown_file_location)  # list
        self.html = self._compile()  # str
        self.preview = self.get_preview()  # str

    def get_html(self) -> str:
        """return the html"""
        return self.html

    def get_preview(self) -> str:
        """return the preview"""
        html = self.html
        title = html[html.find("<h1>"):html.find("</h1>") + 5]
        para_start = html.find("<p>")
        para_end = html.find("</p>")
        if para_end - para_start > 100:
            preview_length = 100
            while html[para_start + preview_length] != " ":
                preview_length += 1
            para_end = para_start + preview_length
            para_preview = html[para_start:para_end] + "..."
        else:
            para_preview = html[para_start:para_end]
        para_preview += "</p>"
        preview = title + "\n" + para_preview
        return preview

    def _compile(self):
        """Entry point where the parsing of markdown begins"""
        html = ""
        while self.md_tokens:
            html += self._parse_line(self._get_next_line())
        return html

    def _parse_line(self, line: list) -> str:
        """Process a line"""
        if len(line) == 0:
            return ""
        if line[0] == "<!--":
            return "\n<!--" +\
                   self._recursive_descent_parser(line[1:], True, "-->") +\
                   "-->\n"
        if line[0] in ['#', '##', '###', '####', '#####']:
            return _parse_heading(line, len(line[0]))
        if line[0] == "```":
            return "\n<pre><code>\n" +\
                   self._recursive_descent_parser(line[1:], False, "```") +\
                   "\n</code></pre>\n"
        if line[0] == '>':
            return _parse_block_quote(line[1:])
        if line[0] in ['---', '===']:
            return "<hr />\n"
        if line[0] in ['*', '-'] or re.fullmatch("[0-9]+\\.", line[0]):
            return self._parse_list(line, 0)
        return _parse_paragraph(line)

    def _parse_comment(self, line: list) -> str:
        """process an html comment"""
        comment = ""
        if len(line) == 0:
            line = self._get_next_line()
        token = line.pop(0)
        if token != "-->":
            if token == "<!--":
                comment += token
            else:
                comment += " " + token
            comment += self._parse_comment(line)
        elif token == "-->":
            comment += " " + token + "\n"
        return comment

    def _get_next_line(self) -> list:
        """Get the next line of markdown, return it as a list"""
        stripped_line = []
        if self.md_tokens:
            line = re.split("([\\t\\s])", self.md_tokens.pop(0))
            for item in line:
                if item == "":
                    continue
                stripped_line.append(item)
        return stripped_line

    def _recursive_descent_parser(self, line: list, parse_inline: bool, final_token: str) -> str:
        """Recursively descend into and parse nested structures"""
        result = ""
        if len(line) == 0:
            result += "\n"
            line = self._get_next_line()
        while line:
            token = line.pop(0)
            if token == final_token:
                return result
            if token == "\t":
                result += "    "
                continue
            result += _parse_inline_syntax(token) if parse_inline else token
        result += self._recursive_descent_parser(self._get_next_line(), parse_inline, final_token)
        return result

    def _parse_list(self, line: list, depth: int) -> str:
        """Recursively handle ordered and unordered lists"""
        opening_tag = _get_list_type(line)
        closing_tag = re.sub("<", "</", opening_tag) + "\n"
        list_text = opening_tag
        while True:
            item = "<li>"
            line = _strip_list_item(line)
            for word in line:
                item += _parse_inline_syntax(word)
            if _get_list_type(self._peek_next_line()) not in ["<ol>", "<ul>"]:
                list_text += _parse_inline_syntax(item) + "</li>\n"
                break
            list_text += item + "</li>\n"
            line = self._get_next_line()
        return list_text + closing_tag

    def _peek_next_line(self) -> list:
        """return the next line without popping it"""
        stripped_line = []
        if self.md_tokens:
            line = re.split("([\\t\\s])", self.md_tokens[0])
            for item in line:
                if item == "":
                    continue
                stripped_line.append(item)
        return stripped_line
        return line
