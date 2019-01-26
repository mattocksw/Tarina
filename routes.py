"""
Routes and views for the bottle application.
"""

import os
import random
import string
import shutil

from bottle import route, view, request
from datetime import datetime

from helper_functions import *

import json
from bottle import HTTPResponse

@route('/')
@route('/home')
@view('layout')
def home():
    story_map = get_file_map(default_path + stories_file)
    #duplicate all \ characters so that javascripts considers \n two characters instead of a new line etc
    names = list(map(lambda s: s.replace('\\', '\\\\'), get_keys(story_map)))
    return dict(
        title="writing app", titles=names
    )

@route('/new_story', method='POST')
def add_story():
    try:
        # get story name from post
        story_name = request.json["story_name"]
        
        #check for non allowed characters
        resp = validate_name(story_name)
        if resp != None:
            return resp

        #check that story does not exist
        story_map = get_file_map(default_path + stories_file)
        if story_name in story_map:
            resp = json.dumps(['error: title exists'])
            return HTTPResponse(status=422, body=resp)

        #create folder for the story
        story_folder = get_new_name(get_values(story_map), 10)
        create_default_categories(story_folder)

        #write the story to the story name folder name mapping file
        with open(default_path + stories_file, 'a') as file:
            file.write("{} {}\n".format(story_folder, story_name))

        resp = json.dumps(['errors: '''])
        return HTTPResponse(status=200, body=resp)
    except:
        resp = json.dumps(['errors: invalid input'])
        return HTTPResponse(status=422, body=resp)

@route('/new_item', method='POST')
def new_item():
    try:
        story_name = request.json["story_name"]
        category = request.json["category"]
        item_name = request.json["item_name"]

        resp = validate_name(item_name)
        if resp != None:
            return resp

        #get item names
        category_path = get_path_to_items(story_name, category)
        item_map = get_file_map(category_path + item_names_file)

        #check that item does not exist
        if item_name in item_map:
            resp = json.dumps(['error: name exists'])
            return HTTPResponse(status=422, body=resp)

        #add item
        random_name = get_new_name(get_values(item_map), 10)
        with open(category_path + item_names_file, 'a') as file:
            file.write("{} {}\n".format(random_name, item_name))     

        resp = json.dumps(['errors: '''])
        return HTTPResponse(status=200, body=resp)
    except:
        resp = json.dumps(['error: unexpected error creating item'])
        return HTTPResponse(status=500, body=resp)

@route('/get_items', method='POST')
def get_items():
    try:
        story_name = request.json["story_name"]
        category = request.json["category"]

        #get item names
        category_path = get_path_to_items(story_name, category)
        item_map = get_file_map(category_path + item_names_file)

        theBody = json.dumps(get_keys(item_map))
        return HTTPResponse(status=200, body=theBody)
    except:
        resp = json.dumps(['error: failed to get story'])
        return HTTPResponse(status=500, body=resp)

@route('/get_item', method='POST')
def get_item():
    try:
        #get value from post
        story_name = request.json["story_name"]
        category = request.json["category"]
        item_name = request.json["item_name"]
       
        #get item names
        category_path = get_path_to_items(story_name, category)
        item_map = get_file_map(category_path + item_names_file)

        #get item folder
        item = item_map[item_name]
        content = ''
        try:
            with open(category_path + '/' + item, 'r') as file:
                content = file.read()
        except:
            pass
        theBody = json.dumps(content)
        return HTTPResponse(status=200, body=theBody)
    except:
        resp = json.dumps(['error : failed to get story'])
        return HTTPResponse(status=500, body=resp)

@route('/save', method='POST')
def save_item():
    try:
        #get value from post
        story_name = request.json["story_name"]
        category = request.json["category"]
        item_name = request.json["item_name"]
        content = request.json["content"]
       
        #get item names
        category_path = get_path_to_items(story_name, category)
        item_map = get_file_map(category_path + item_names_file)

        #get item file
        item = item_map[item_name]

        try:
            with open(category_path + '/' + item, 'w') as file:
                file.write(content)
        except:
            resp = json.dumps(['error : failed to save'])
            return HTTPResponse(status=500, body=resp)

        theBody = json.dumps(content)
        return HTTPResponse(status=200, body=theBody)
    except:
        resp = json.dumps(['error : failed to get story'])
        return HTTPResponse(status=500, body=resp)

@route('/delete', method='POST')
def delete_story():
    try:
        story_name = request.json["story_name"]

        #get story folder
        story_map = get_file_map(default_path + stories_file)
        story_folder = story_map[story_name]

        #remove folder
        shutil.rmtree(default_path + story_folder)

        #update story mapping file
        with open(default_path + stories_file, 'w') as file:
            for name, folder in story_map.items():
                if name != story_name:
                    file.write("{} {}\n".format(folder, name))

        resp = json.dumps(['errors '''])
        return HTTPResponse(status=200, body=resp)
    except:
        resp = json.dumps(['error : failed to delete story'])
        return HTTPResponse(status=500, body=resp)



