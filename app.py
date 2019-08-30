"""
This script runs the application using a development server.
"""

import bottle
import os
import sys
import webbrowser

# routes contains the HTTP handlers for our server and must be imported.
import routes

if __name__ == '__main__':

    print("\n\n\n\n\n\n\n\n\nWelcome to using Tarina\nThe app should open in your default broswer. Otherwise you can find it at http://localhost:8181\n\n\n\n")
    print("Please make sure not to close this window before all editors have saved their contents.\n\n\n\n\n\n\n\n\n\n")

    webbrowser.open('http://localhost:8181')
    bottle.run(host='localhost', port=8181)
    
