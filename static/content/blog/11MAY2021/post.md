# Hello World!!

I started down this path with innocent enough intentions, to write stuff the hard way so that maybe I could learn.  I originally did things like writing my own registration/authentication/session-tracking tools and play around with basic Jinja functionality.  

Almost separately I ended up toying with the idea of writing a markdown to HTML compiler.  Again, the motiviation was just to get some reps solving a problem.  Of course there are many libraries that already exist that will parse markdown into HTML, heck, that's the whole point of the language.  But I wanted to see if I could do it myself without consulting any of the existing solutions.  It may not be pretty but I wrote it all and this blog post is rendered using my compiler.  It just supports basic syntax but I'm proud of it.

## Yeah, but what's the deal with the rest of this site?

Well, as I was laying awake in bed one night, unable to sleep with code challenges tugging at my conciousness, I kind of had an epiphany.  I'm in love with Linux, the Unix Philosophy, and having simple apps that do one thing well.  I've never been a blogger but I realized that I'd accidentally stumbled upon an idea for a really simple Content Management System built around markdown, the filesystem, and my compiler.

## My guiding design philosophy:

1. Have all the links you see anywhere on the site be populated by the app parsing the content directory.
2. Have all content written in markdown and simply dropped in the appropriate folder.
3. Have the blog landing page populate with blog post previews in real time.

## Stretch goals

* Get the CSS dialed
* Polish the compiler and add extended markdown syntax support
* Get the project to a releaseable state.
