# wafflebot
Simple Reddit bot using PRAW/MariaDB/Python to automatically post the fabled waffle gif of Olli Jokinen.  This is a basic project for learning the PRAW API and handling submission and comment streams.  Feel free to customize it to your own purposes.

# Setup
This was programmed using Python 2.7 so in theory it should work with Python 3.x, but no promises are made.  For this particular project you also need a MariaDB database as well.  The schema is basic, but included. 

# Running
To make the bot run forever, you can setup a `screen` or `tmux` session and then simply run `python wafflebot.py`. 
