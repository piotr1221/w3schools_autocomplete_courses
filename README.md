# w3schools_autocomplete_courses
Selenium script in Python to automatically complete lessons and excercises from W3Schools tutorials

# Requirements
## Python 3.8+ required
Otherwise, argparse library won't work. Compatibility for older versions in the making.
## Firefox (geckodriver)
Currently the script only works with Firefox through geckodriver. Chrome compatibility incoming.
## Install the dependencies
pip install -r requirements.txt

# How to use
Execute script on console as:\
python main.py --email your-email --password your-password --course coursename --tutorial --exercise --path path-to-geckodriver

Currently accepted values for argument --course:
- HTML
- CSS
- JavaScript
- Node.js
- React
- PHP
- jQuery
- AngularJS
- XML
- SQL
- MySQL

--tutorial and --exercise are boolean arguments. Type the argument without any value (as in example above) for True or --no-tutorial and --no-exercise for False.

--path argument is optional if geckodriver is in the same folder of the script or if it is added to path variables; otherwise, enter the full path to geckodriver.exe.

.env contains a series of xpath references, html id's and text that the script uses to find elements in the website.