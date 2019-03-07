

import os
import random
import string
import shutil

import json
from bottle import HTTPResponse

default_path = "files/default/"
users_file = "users.txt"
stories_file = "story_names.txt"
categories_file = "category_names.txt"
item_names_file = "item_names.txt"

default_categories = ["Chapters", "Characters", "Locations"]

#return dictionary with name as key and file/folder as value
def get_file_map(path_to_file):
    file_map = {}
    try:
        with open(path_to_file, 'r') as file:
            lines = file.readlines()
            for line in lines:  
                file, name = line.split(' ', 1)
                file_map[name.rstrip('\n')] = file
    except:
        pass
    return file_map

def get_keys(d):
    return list(d.keys())

def get_values(d):
    return list(d.values())

# Creates a random string of length N consisting of letters and digits that doesn't match any string in folders
def get_new_name(folders, N):
    filename_exists = True
    while filename_exists:
        # https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
        filename = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(N))
        if filename not in folders:
            return filename

def create_default_categories(story_folder):
    os.mkdir(default_path + story_folder)

    #create directories for default categories and write them in mapping file
    with open(default_path + story_folder + '/' + categories_file, 'a') as file:
        for category in default_categories:
            os.mkdir('files/default/' + story_folder + '/' + category)
            file.write("{} {}\n".format(category, category))

def get_all_content_names(story_name):
    content = {}

    stories = get_file_map(default_path + stories_file)
    story_folder = stories[story_name]

    categories = get_file_map(default_path + story_folder + '/' + categories_file)
    for category, category_folder in categories.items():
        #get item names from each category and put them in dictionary under category name
        try:
            items = get_file_map(default_path + story_folder + '/' + category_folder + '/' + item_names_file)
            content[category] = get_keys(items)
        except:
            pass
    return content

def get_story_folder(story_name):
    story_map = get_file_map(default_path + stories_file)
    return story_map[story_name]

def get_path_to_items(story_name, category):
    #get story folder
    story_map = get_file_map(default_path + stories_file)
    story_folder = story_map[story_name]

    #get category folder
    category_map = get_file_map(default_path + story_folder + '/' + categories_file)
    category_folder = category_map[category]

    #path to items
    return default_path + story_folder + '/' + category_folder + '/'

def validate_name(name):
    if(name == None or name == ""):
        resp = json.dumps(['error: empty name'])
        return HTTPResponse(status=422, body=resp)
    
    #check that name does not have new line or null terminating character that would break file format
    if '\n' in name:
        resp = json.dumps(['error: new line not allowed in name'])
        return HTTPResponse(status=422, body=resp)
    if '\x00' in name:
        resp = json.dumps(['error: null terminating character not allowed in name'])
        return HTTPResponse(status=422, body=resp)