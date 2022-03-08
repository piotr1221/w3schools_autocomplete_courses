# w3schools_autocomplete_courses
Selenium script in Python to automatically complete lessons and excercises from W3Schools tutorials

# Install the dependencies
pip install -r requirements.txt

# How to use
Execute script on console as:\
python script.py --email your-email --password your-password --course coursename --tutorial --exercise

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

--tutorial and --exercise are boolean arguments. Type the argument without any value (as in example above) for True or --no-tutorial and --no-exercise for False.