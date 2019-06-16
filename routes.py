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
from bottle import HTTPResponse, static_file

@route('/')
@route('/home')
def home():
    #story_map = get_file_map(default_path + stories_file)
    #duplicate all \ characters so that javascripts considers \n two characters instead of a new line etc
    #names = list(map(lambda s: s.replace('\\', '\\\\'), get_keys(story_map)))
    #return dict(
    #    title="writing app", titles=names
    #)
    return static_file('index.html', root='static/frontend/dist/')

@route('/get_stories')
def get_stories():
    try:
        story_map = get_file_map(default_path + stories_file)
        resp = json.dumps(get_keys(story_map))
        return HTTPResponse(status=200, body=resp)
    except:
        resp = json.dumps(['errors: could not load titles'])
        return HTTPResponse(status=500, body=resp)
    

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

        content = get_all_content_names(story_name)

        resp = json.dumps(content)
        return HTTPResponse(status=200, body=resp)
    except:
        resp = json.dumps(['errors: invalid input'])
        return HTTPResponse(status=422, body=resp)

@route('/new_item', method='POST')
def new_item():
    try:
        story_name = request.json["story_name"]
        category = request.json["item_category"]
        item_name = request.json["item_name"]

        resp = validate_name(item_name)
        if resp != None:
            return resp

        if category == "Categories":
            #add to categories mapping
            story_folder = get_story_folder(story_name)
            category_map = get_file_map(default_path + story_folder + '/' + categories_file)
            #check that item does not exist
            if item_name in category_map:
                resp = json.dumps(['error: name exists'])
                return HTTPResponse(status=422, body=resp)
            #add item
            random_name = get_new_name(get_values(category_map), 10)
            with open(default_path + story_folder + '/' + categories_file, 'a') as file:
                file.write("{} {}\n".format(random_name, item_name))
            #create folder
            os.mkdir(default_path + story_folder + '/' + random_name)
        else:
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

@route('/delete_item', method='POST')
def delete_item():
    try:
        story_name = request.json["story_name"]
        category = request.json["item_category"]
        item_name = request.json["item_name"]     

        if category == "Categories":
            story_folder = get_story_folder(story_name)
            category_map = get_file_map(default_path + story_folder + '/' + categories_file)           
            category_folder = category_map[item_name]                       

            #just in case check that folder does not have ..
            if category_folder.isalnum() == False:
                resp = json.dumps(['error: unksnown character in folder name'])
                return HTTPResponse(status=422, body=resp)

            #update mappings file
            with open(default_path + story_folder + '/' + categories_file, 'w') as file:
                for name, folder in category_map.items():
                    if name != item_name:
                        file.write("{} {}\n".format(folder, name))
           
            #remove category folder
            shutil.rmtree(default_path + story_folder + '/' + category_folder)

        else:
            category_path = get_path_to_items(story_name, category)
            item_map = get_file_map(category_path + item_names_file)
            item_file = item_map[item_name]

            #just in case check that file does not have ..
            if item_file.isalnum() == False:
                resp = json.dumps(['error: unksnown character in file name'])
                return HTTPResponse(status=422, body=resp)

            #delete item
            with open(category_path + item_names_file, 'w') as file:
                for name, folder in item_map.items():
                    if name != item_name:
                        file.write("{} {}\n".format(folder, name))     

            #delete file if exists
            try:
                os.remove(category_path + '/' + item_file)
            except:
                pass

        resp = json.dumps(['errors: '''])
        return HTTPResponse(status=200, body=resp)
    except:
        resp = json.dumps(['error: unexpected error deleting item'])
        return HTTPResponse(status=500, body=resp)

@route('/get_items', method='POST')
def get_items():
    try:
        story_name = request.json["story_name"]

        content = get_all_content_names(story_name)

        theBody = json.dumps(content)
        return HTTPResponse(status=200, body=theBody)
    except:
        resp = json.dumps(['error: failed to get story'])
        return HTTPResponse(status=500, body=resp)

#returns content of item
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

@route('/reorder_items', method='POST')
def reorder_items():
    try:
        #get value from post
        story_name = request.json["story_name"]
        category = request.json["item_category"]
        item_names = request.json["item_names"]

        #get item names
        category_path = get_path_to_items(story_name, category)
        item_map = get_file_map(category_path + item_names_file)

        #check that item names are equal
        if len(item_map) != len(item_names) or set(get_keys(item_map)) != set(item_names):
            resp = json.dumps(['error : unexpected item names'])
            return HTTPResponse(status=422, body=resp)

        #write items in new order, dict in python 3.6 should be ordered in insert order
        with open(category_path + item_names_file, 'w') as file:
            for item in item_names:
                file.write("{} {}\n".format(item_map[item], item)) 

        resp = json.dumps(['errors '''])
        return HTTPResponse(status=200, body=resp)

    except:
        resp = json.dumps(['error : failed to save item order'])
        return HTTPResponse(status=500, body=resp)

#return image
@route('/<story_folder>/<filename>', method='GET')
def get_image(story_folder, filename):
    try: 
        #validate storyname
        story_map = get_file_map(default_path + stories_file)
        if story_folder not in get_values(story_map):
            resp = json.dumps({'error': "story not found"})
            return HTTPResponse(status=404, body=resp)

        #get extension for filename
        for file in os.listdir(default_path + story_folder):
            if file.startswith(filename):
                valid_path = default_path + story_folder + '/' + file
                with open(valid_path, "rb") as f:
                    name, ext = os.path.splitext(file)
                    return HTTPResponse(f.read(), content_type="image/" + ext[1:])
        resp = json.dumps({'error': "image not found"})
        return HTTPResponse(status=404, body=resp)
    except:
        resp = json.dumps({'error': "image not found"})
        return HTTPResponse(status=404, body=resp)

@route('/save_image', method='POST')
def save_image():
    try: 
        #get image
        file = request.files.get('image')
        story_name = request.forms.get("story_name")        
        name, ext = os.path.splitext(file.filename)
        if ext not in ('.png', '.jpg', '.jpeg'):
            resp = json.dumps({'story_folder': 'filename', 'file_name': 'filename'})
            return HTTPResponse(status=500, body=resp)

        #get save path
        story_folder = get_story_folder(story_name)
        
        random_name = get_new_name(os.listdir(default_path + story_folder), 11)
        save_path = default_path + story_folder + '/' + random_name + ext

        #save file
        file.save(save_path)

        resp = json.dumps({'story_folder': story_folder, 'file_name': random_name})
        return HTTPResponse(status=200, body=resp)
    except:
        resp = json.dumps({'story_folder': 'name', 'file_name': 'filename'})
        return HTTPResponse(status=500, body=resp)

@route('/save', method='POST')
def save_item():
    try:
        print("here")
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

        #just in case check that file does not have ..
        if item.isalnum() == False:
            resp = json.dumps(['error: unksnown character in file name'])
            return HTTPResponse(status=422, body=resp)

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

        #just in case check that folder does not have ..
        if story_folder.isalnum() == False:
            resp = json.dumps(['error: unksnown character in folder name'])
            return HTTPResponse(status=422, body=resp)

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


@route('/rename_item', method='POST')
def rename_item():
    try:
        story_name = request.json["story_name"]
        category = request.json["item_category"]
        item_name = request.json["item_name"]
        new_name = request.json["new_name"]
        target =  request.json["target"]

        resp = validate_name(new_name)
        if resp != None:
            return resp

        #if folder
        if target != 'file':
            #rename in categories mapping
            story_folder = get_story_folder(story_name)
            category_map = get_file_map(default_path + story_folder + '/' + categories_file)
            category_folder = category_map[category] 
            
            #update mappings file
            with open(default_path + story_folder + '/' + categories_file, 'w') as file:
                for name, folder in category_map.items():
                    if folder != category_folder:
                        file.write("{} {}\n".format(folder, name))
                    else:
                        file.write("{} {}\n".format(folder, new_name))
            
            resp = json.dumps({'target': 'folder'})
            return HTTPResponse(status=200, body=resp)

        else:
            #get item names
            category_path = get_path_to_items(story_name, category)
            item_map = get_file_map(category_path + item_names_file)
            item_file = item_map[item_name]

            #update mapping
            with open(category_path + item_names_file, 'w') as file:
                for name, folder in item_map.items():
                    if folder != item_file:
                        file.write("{} {}\n".format(folder, name))
                    else:
                        file.write("{} {}\n".format(folder, new_name))        

            resp = json.dumps({'target': 'file'})
            return HTTPResponse(status=200, body=resp)


        resp = json.dumps(['errors: '''])
        return HTTPResponse(status=200, body=resp)
    except:
        resp = json.dumps(['error: unexpected error creating item'])
        return HTTPResponse(status=500, body=resp)
