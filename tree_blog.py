"""
FILE:       tree_blog.py
AUTHOR:     Ben Simcox
PROJECT:    Tree Blog (github.com/bnsmcx/tree_blog)
PURPOSE:    This simple Flask app is a CMS that is organized logically around parsing
            a directory tree to get its shape and compiling markdown to HTML to get
            its content.
"""
import os
import markdown
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)
content_dir = app.root_path + "/static/content/"
blog_dir = app.root_path + "/static/content/blog/"


@app.route('/')
def landing_page():
    """landing page defaults to resume"""
    try:
        return blog()
    except FileNotFoundError:
        return redirect(url_for("not_found"))


def get_preview(post_markdown_file: str) -> str:
    """Extract the h1 and a preview of the first paragraph and return it"""
    html = get_html(post_markdown_file)
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


@app.route('/blog')
def blog():
    """render the blog landing page"""
    blog_posts = os.listdir(blog_dir)
    content = ""
    for post_date in blog_posts:
        post_markdown_file = get_content_path(blog_dir + post_date + "/")
        preview = get_preview(post_markdown_file)
        content += "<a class=\"text-center text-decoration-none text-dark\" href=\"/blog/" + post_date + \
                   "\"><div class=\"blog-preview shadow-lg p-4 mb-5 rounded mask\">\n" + \
                   preview + \
                   "<h4>" + post_date + "</h4>" + \
                   "</div></a>\n"
    return render_template('base.html', links=map_links(), content=content)


@app.route('/blog/<post>')
def blog_post(post: str):
    """Render the requested post"""
    path = get_content_path(blog_dir + post + "/")
    if path:
        content = get_html(path)
        return render_template('base.html', links=map_links(), content=content)
    return redirect(url_for("not_found"))


@app.route('/not_found')
def not_found():
    """show the user a 404 message"""
    message = "<h1>404 - Page not found.</h1>"
    return render_template('base.html', links=map_links(), content=message), 404


def get_html(path: str) -> str:
    """access the provided markdown file, return its contents as html"""
    with open(path, "r") as file:
        md = file.read()
    html = markdown.markdown(md)
    return html


@app.route('/<path>')
def get_content(path: str):
    """if path exists give the user content, otherwise, a 404"""
    try:
        path = get_content_path(content_dir + path + "/")
        if path:
            content = get_html(path)
            return render_template('base.html', links=map_links(), content=content)
        return redirect(url_for("not_found"))
    except IsADirectoryError:
        return redirect(url_for("not_found"))


def get_content_path(path: str) -> str:
    """return the full path to a markdown content file"""
    markdown_file_path = ""
    if os.path.exists(path):
        markdown_file_path += path
        for file in os.listdir(path):
            if file[-3:].lower() == ".md":
                markdown_file_path += file
    return markdown_file_path


def map_links():
    """return a map of links based on the content directory"""
    try:
        links = os.listdir(content_dir)
        return links
    except FileNotFoundError:
        return []


if __name__ == '__main__':
    app.run(debug=True)
