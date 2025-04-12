#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@project: PyCharm
@file: app.py
@author: Shengqiang Zhang
@time: 2019/8/6 02:53
@mail: sqzhang77@gmail.com
"""

# Import the Dash app instance from the configuration module
from app_configuration import app
# Import the layout of the web page
from app_layout import app_layout
# Import the callback function to update the web page data
from app_callback import app_callback_function

# Set the title of the web page
app.title = 'Browser History Analysis'

# Enable serving local CSS and JS files
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# Define the layout of the HTML elements
# The layout is fully embedded in the Python code
# This is suitable for quickly setting up simple web pages
# For complex pages, it is not recommended to use Dash
# If you are not familiar with the layout code below, do not modify it随意
app.layout = app_layout

# Define callbacks to update the web page data
# Dash is a framework where the front-end and back-end are not separated
# It is suitable for simple page deployments, but not recommended for complex pages
app_callback_function()

# Start running the web server
if __name__ == '__main__':
    # Determine if the app is running locally (for testing)
    app_local = False

    # '127.0.0.1' means the page can be viewed on the local machine
    # '0.0.0.0' means the page can be viewed by all users, generally used for deploying to a server
    # If deploying to a server, make sure to allow port 8090 in the firewall settings of the cloud control panel
    if app_local:
        app.run_server(host='127.0.0.1', debug=True, port='8090')
    else:
        app.run_server(host='0.0.0.0', debug=False, port='8090')
