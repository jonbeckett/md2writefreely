# md2write.as

## Markdown files to Write.As upload tool for Python 3.x

This python 3.x script will upload a collection of markdown files prepared by [wp2md](https://github.com/jonbeckett/wp2md) into a write.as blog.

Usage:

`python md2write.as.py`

(you will need to change the parameters within the script file)


### Notes

The script presumes the markdown files will be formatted as per those output by [wp2md](https://github.com/jonbeckett/wp2md) - where the top four lines of each markdown file are the title, a blank line, the date, another blank line, and then the content of the post. The script also presumes that the filenames start with the date in `yyyy-mm-dd` format, and uses it to pass the original post date to the write.as API in order to back-date posts.

It's worth noting that this script was written really for my own purposes (and curiosity) - there are probably lots of ways it can go wrong.