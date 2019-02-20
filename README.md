# Stock-Notifications Webapp
This Web-app provides an interface for users to subscribe for notifications via Mail about stock price changes. Specifically, they can subscribe for notifications when the stock prices go above or below the specified price.  

This App is developed using Python and Flask. The UI is purposefuly made simple and the focus is more on the python processing at backend code and not on the front end HTML/CSS pages.

Live App run
==
This App is currently running on https://stock-notify-app.herokuapp.com/   

Frameworks used:
===
Flask, HTML/CSS.

Files are used instead of SQL DBs for simplicity

Instructions to run the App:
===
Download all files to local directory.
Get the App-key from Alpha Vantage website (Key is provided for FREE. Need to register in website and get the key).
Replace the key in stock.py file, line number - 93.
Start the project - "python stock.py".

NOTE for Pythonanywhere users:
=====
Since pythonanywhere website doesnot allow threading, separate files are developed for front-end UI manipulation(stock_pythonanywhere.py) and background NSE stock value checks(mail_script_pythonanywhere.py).

Basic Guidelines for working on Flask:
====
I) Always use virtualenv/virtualenv wrapper packages for the Flask projects. This is basically to create an isolated environment for the project and the packages downloaded will not affect rest of the libraries in system.

Steps for creating Virtualenv:
----
pip install virtualenv.

pip install virtualenvwrapper.

In Bash file ==> "export WORKON_HOME=~/.virtualenvs; source /usr/local/bin/virtualenvwrapper.sh".

Create a directory for project and goto directory.

Create the virtual env ==> "mkvirtualenv -a $(pwd) name-of-env" (This will help to map the virtual enviromnment to the path location).

To start wroking on virtual env ==> workon name-of-env.

For deleting the virtualenv, "rmvirtualenv name-of-env".

For viewing the list of packages in virtual env, "pip list".


