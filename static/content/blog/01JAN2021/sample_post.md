# Sample Post

The name of the markdown file doesn't matter, but the extension does.  The folder name gives the blog post it's URL and is featured in the 'preview' rendered on the /blog page.

## Adding a blog post

Simply drop a folder with the date into the `/content/blog/` directory and then drop your post's markdown file into that folder.  Remember, each post's directory should contain one-and-only-one file.

## Why I did it this way

Because you can deploy a completely empty site and then populate the whole thing by SCP'ing your content directory onto the server.  I also whipped up a simple 'publish' script that accepts a markdown file as an argument, parses today's date, and SCP's the folder and markdown file to the server.  With like four lines of code.
