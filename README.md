This simple Flask app is a CMS that is organized logically around parsing a directory tree to get its shape and compiling markdown to HTML to get its content.

For example, given the following tree:

```
/Content
|___/Resume
    |___resume.md
|___/Blog
    |___/20DEC2021
	|___post.MD
    |___/23DEC2021
	|___post.MD
```

The web page navigation bar will have two links, 'Resume' and 'Blog'.  Note that only the folder name will be parsed to generate links but the content must come from the markdown file within the folder.  Each and every folder must have one and only one markdown file.  The name of the markdown file does not matter as long as it has the markdown extension.

Navigating to 'Blog' on the webpage will show the user a summary of all posts.  Changes made to the content directory will take effect upon page reload.

Things you'll need to change:

* The 'title' and 'navbar-brand' components of the `/static/templates/base.html` template are currently set to "Tree Blog."  Put your site name here.
* Whatever style changes you want.  There is a simple and functional theme.  All style editing is done within the `base.html` template using bootstrap with the exception of the 'hover' effect over the blog post preview.  That is done in `/static/style.css` and is the only custom css.
