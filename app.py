"""
FILE:       app.py
AUTHOR:     Ben Simcox
PROJECT:    bnsmcx.com
PURPOSE:    Flask entry point.
"""
import os
import md_to_html as m2h

from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)
content_dir = app.root_path + "/static/content/"
blog_dir = app.root_path + "/static/content/blog/"


@app.route('/')
def landing_page():
    """landing page defaults to resume"""
    return blog()


@app.route('/blog')
def blog():
    """render the blog landing page"""
    blog_posts = os.listdir(blog_dir)
    content = ""
    for post_date in blog_posts:
        post_markdown_file = get_content_path(blog_dir + post_date + "/")
        preview = m2h.Compiler(post_markdown_file).get_preview()
        # The first line of 'content' makes the entire content division a link to the post
        content += "<a style=\"display:block\" href=\"/blog/" + post_date + "\"><div>\n" + \
                   post_date + \
                   preview + \
                   "</div></a>\n"
    return render_template('base.html', links=map_links(), content=content)


@app.route('/blog/<post>')
def blog_post(post: str):
    """Render the requested post"""
    path = get_content_path(blog_dir + post + "/")
    if path:
        content = m2h.Compiler(path).get_html()
        return render_template('base.html', links=map_links(), content=content)
    return redirect(url_for("not_found"))


@app.route('/not_found')
def not_found():
    """show the user a 404 message"""
    message = "<h1>404 - Page not found.</h1>"
    return render_template('base.html', links=map_links(), content=message)


@app.route('/<path>')
def get_content(path: str):
    """if path exists give the user content, otherwise, a 404"""
    path = get_content_path(content_dir + path + "/")
    if path:
        content = m2h.Compiler(path).get_html()
        return render_template('base.html', links=map_links(), content=content)
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
    links = os.listdir(content_dir)
    return links


if __name__ == '__main__':
    app.run()
