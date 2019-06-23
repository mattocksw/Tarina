"""
This script runs the application using a development server.
"""

import bottle
import os
import sys

# routes contains the HTTP handlers for our server and must be imported.
import routes

if __name__ == '__main__':
    bottle.run(host='localhost', port=8181)
