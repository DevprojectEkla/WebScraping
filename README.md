# WebScraping
My first steps in web scraping using bs4 (BeautifulSoup) library on python. This one only allows you to scrap wallpapers from an hardcoded website.
It allows you to download every wallpaper providing a keyword like 'landscape' or 'star wars' (or iterates on a list of keywords written in a .txt file).
It iterates over all pages of the given keyword.

There is two branches: 
'main' is the CLI version with a simple user input to type one keyword (ex:'landscape', 'airplane', 'stars') and the number of pages you want to scrap.
'GTK' is the GUI version of the same app but it allows you to 'stop' scraping as you wish and restart with other keywords. You can also open a list of keyword or dynamically create a list, whereas the CLI version only load the default 'list.txt' if you just press enter instead of typing a keyword.

USAGE:

main branch: (make sure to create an environment with all requirements) just run  'python WebSiteScraping.py'
GTK branch: (it gives you a very basic User Interface): run the command 'python _GTK_MainWindow.py'
