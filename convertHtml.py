
import os
import random
import string
import shutil
import re
import colorsys

import lxml.html
from docx import Document, opc, oxml
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH 


from helper_functions import *

#helper class for collecting styles for text
class DocText:
    def __init__(self):
        self.text = ""
        self.font = 'Arial' 
        self.font_size = 13 
        self.alignment = "left" #0 for left, 1 for right, 2 center, 3 justify
        self.bold = False 
        self.italic = False 
        self.underline = False
        self.strikethrough = False
        self.subscript = False
        self.superscript = False
        self.color = None
        self.highlight = None
        self.link = ""
        self.bullet = False
        self.number_list = False
        

    #writes text in given paragraph p in document
    def write(self, p, document):
        
        #add text
        run = p.add_run(self.text)       

        #add font and font size:
        run.font.name = self.font
        run.font.size = Pt(self.font_size)
        run.font.bold = self.bold
        run.font.italic = self.italic
        run.font.underline = self.underline
        run.font.strike = self.strikethrough
        run.font.subscript = self.subscript
        run.font.superscript = self.superscript
        if(self.color):
            run.font.color.rgb = self.color
        if(self.highlight):
            pass
            #run.font.highlight_color = self.highlight
            #not able to set custom color, only preset values.
        if(self.link):            
            add_hyperlink(p, self.link, self.text)


#reads the text of element and all its children recursively, and creates a list of DocText objects from them
def get_text(html_element, text_list = []):

    #create new style collector
    t = DocText()
 
    #get style
    style = get_style(html_element)
    
    #get text
    try:
        t.text = html_element.text.replace("\xa0", "")
    except:
        pass
    
    if(style):
        #get font
        font = get_value_from_string(style, "font-family")
        if(font):
            t.font = font
   
        #get font size
        font_size = get_value_from_string(style, "font-size")
        if(font_size):
            t.font_size = int(font_size[:-2]) #remove Pt
                      

        #get alignment
        alignment = get_value_from_string(style, "text-align")
        if(alignment):
            t.alignment = alignment

        #get text color
        hsl_color = get_value_from_string(style, "color")
        if(hsl_color):
            color = re.findall(r'\d+', hsl_color) #get all numbers https://stackoverflow.com/questions/4289331/how-to-extract-numbers-from-a-string-in-python
            rgb_color = colorsys.hls_to_rgb(float(color[0])/255.0, float(color[2])/100.0, float(color[1])/100.0) #colorsys expects values in 0-1 range
            t.color = RGBColor(int(rgb_color[0]*255.0), int(rgb_color[1]*255.0), int(rgb_color[2]*255.0))

        #get text highlight color (not able to set custom color, ignored)
        #hls_color = get_value_from_string(style, "background-color")
        #if(hls_color):
            #color = re.findall(r'\d+', hls_color) #get all numbers https://stackoverflow.com/questions/4289331/how-to-extract-numbers-from-a-string-in-python
            #rgb_color = colorsys.hls_to_rgb(float(color[0])/100.0, float(color[1])/100.0, float(color[2])/100.0) #colorsys expects values in 0-1 range
            #t.highlight = RGBColor(int(rgb_color[0]*100), int(rgb_color[1]*100), int(rgb_color[2]*100))

              
    #get link ()
    #if(html_element.tag == "a"):
    #    t.link = decoration.attrib['href']
    
    if(html_element.tag == "strong"):
        t.bold = True

    elif(html_element.tag == "i"):
        t.italic = True

    elif(html_element.tag == "u"):
        t.underline = True

    elif(html_element.tag == "s"):
        t.strikethrough = True

    elif(html_element.tag == "sub"):
        t.subscript = True

    elif(html_element.tag == "sup"):
        t.superscript = True

    text_list.append(t)

    #recursively add styles
    for element in html_element:
        text_list = get_text(element, text_list)

    return text_list


    
def iterate_html(html, document, story_folder):
    for element in html:
        
        #handle figure blocks                    
        if element.tag == "figure":  
            #get width of figure in percentage and adjust in cm (a4 has width of 20.1 cm)
            width = Cm(15.0)
            style = get_style(element)
            if style:
                p_width = get_value_from_string(style, "width")
                width = float(p_width) / 100.0 * width                  
                if(width > Cm(15.0)):
                    width = Cm(15.0)

            for figure in element:
                
                #handle tables
                if figure.tag == "table":
                    pass
                
                #handle images
                elif figure.tag == "img":                   
                    add_image(figure, width, document, story_folder)

        #handle text
        elif element.tag in ["p", "h2","h3","h4"]:            
            text_list = get_text(element, [])
            #add main paragraph
            if element.tag == "p":
                p = document.add_paragraph()
            elif element.tag == "h2":
                p = document.add_heading('', level=1)
            elif element.tag == "h3":
                p = document.add_heading('', level=2)
            elif element.tag == "h4":
                p = document.add_heading('', level=3)

            #add alignment
            if(text_list):
                if(text_list[0].alignment == "justify"):
                    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                elif(text_list[0].alignment == "right"):
                    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                elif(text_list[0].alignment == "center"):
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            
            for text in text_list:
                text.write(p,document)

        elif element.tag in ["ul","ol"]:
            for list_element in element:
                text_list = get_text(list_element, [])
                if(element.tag == "ul"):
                    p = document.add_paragraph(style='List Bullet')
                elif(element.tag == "ol"):
                    p = document.add_paragraph(style='List Number')           
            
                for text in text_list:
                    text.write(p,document)

#converts story and writes docx document in downloads folder
def create_docx(story_name):
    try:
        #get current path  
        story_folder = get_story_folder(story_name)
        path = default_path + story_folder + '/'

        #get gategory map
        categories = get_file_map(path + categories_file)  

        #create empty document
        document = Document()

        #write title
        document.add_heading(story_name, 0)

        #write all categories
        for category, category_folder in categories.items():
           
            #add subheader
            document.add_heading(category, 1)

            #get chapters        
            category_path = path + category_folder + '/'
            item_map = get_file_map(category_path + item_names_file)
      
            #append all chapters together
            for name, folder in item_map.items():
                with open(category_path + '/' + folder, encoding='utf-8', mode='r') as file:

                    #write chapter title
                    document.add_heading(name, 2)

                    #travel through html
                    iterate_html(lxml.html.fromstring(file.read()), document, story_folder)                                  
           
        document.save(default_path + 'story.docx')
        return True

    except:
        print("error making html file")
        return False
                

                                  

#return the inline style for element
def get_style(element):
    try:
        for attrib, value in element.items():
            if(attrib == "style"):
                return value
    except:
        return ""


#return value for attrib:value pair in string str
def get_value_from_string(str, attrib):
    tmp = str.split(";")
    for s in tmp:
        if s.startswith(attrib):
            result = s.split(":")
            return result[1].replace("%","")
    return ""



#A function that places a hyperlink within a paragraph object. https://github.com/python-openxml/python-docx/issues/384
#
#param paragraph: The paragraph we are adding the hyperlink to.
#param url: A string containing the required url
#param text: The text displayed for the url
#return: The hyperlink object

def add_hyperlink(paragraph, url, text):

    # This gets access to the document.xml.rels file and gets a new relation id value
    part = paragraph.part
    r_id = part.relate_to(url, opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    # Create the w:hyperlink tag and add needed values
    hyperlink = oxml.shared.OxmlElement('w:hyperlink')
    hyperlink.set(oxml.shared.qn('r:id'), r_id, )

    # Create a w:r element
    new_run = oxml.shared.OxmlElement('w:r')

    # Create a new w:rPr element
    rPr = oxml.shared.OxmlElement('w:rPr')

    # Join all the xml elements together add add the required text to the w:r element
    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)

    paragraph._p.append(hyperlink)

    return hyperlink

def add_image(img_element, width, document, story_folder):
    bofero, delime, image_name = img_element.attrib['src'].rpartition('/')
    for filename in os.listdir(default_path + story_folder):                                     
        if filename.startswith(image_name):            
            document.add_picture(default_path + story_folder + "/" + filename, width=width)


#create html that includes all folders and files from the story. The result expexts that images are located in assets folder
def create_html(story_name):
    try:
        #get current path  
        story_folder = get_story_folder(story_name)
        path = default_path + story_folder + '/'

        #get gategory map
        categories = get_file_map(path + categories_file)             

        #overwrite previous file
        #head
        html_string = '''   <!DOCTYPE html>
                            <head>
                            <meta charset="utf-8">
                            <meta http-equiv="X-UA-Compatible" content="IE=edge">
                            <meta name="viewport" content="width=device-width,initial-scale=1.0">

                            <style>
                            body {
                                background: rgb(204,204,204); 
                            }
                            page {
                                background: white;
                                display: block;
                                margin: 0 auto;
                                margin-bottom: 0.5cm;
                                box-shadow: 0 0 0.5cm rgba(0,0,0,0.5);
                                padding: 1.0cm;
                            }
                            page[size="A4"] {  
                                width: 21cm;
                            }
                            @media print {
                            body, page {
                                margin: 0;
                                box-shadow: 0;
                                }
                            }
                            img {
                                max-width: 100%;
                                height: auto;
                            }
                            </style>

                            </head> 
                      '''
        #start body
        html_string += '''  <body>
                            <page size="A4">

                       '''
        
        #write title
        html_string += '<h1>' + story_name + '</h1>'
        with open(download_path + 'story.html', encoding='utf-8', mode='w') as output:
            output.write(html_string)

        #write all categories
        for category, category_folder in categories.items():
           
            html_string = '<h2>' + category + '</h2>'

            #get chapters        
            category_path = path + category_folder + '/'
            item_map = get_file_map(category_path + item_names_file)
      
            #append all chapters together
            for name, folder in item_map.items():
                with open(category_path + '/' + folder, encoding='utf-8', mode='r') as file:

                    #write chapter title
                    html_string += '<h3>' + name + '</h3>'

                    #write chapter contents
                    html_string += file.read()

            #fix links https://stackoverflow.com/questions/19357506/python-find-html-tags-and-replace-their-attributes
            root = lxml.html.fromstring(html_string)
            for el in root.iter('img'):
                bofero, delime, image_name = el.attrib['src'].rpartition('/')
                for filename in os.listdir(default_path + story_folder):                                     
                    if filename.startswith(image_name):
                        el.attrib['src'] = 'assets/' + filename            
            html_string = lxml.html.tostring(root, pretty_print=True).decode('utf-8')

            #write the category to html
            with open(download_path + 'story.html', encoding='utf-8', mode='a') as output:
                output.write(html_string)
        

        #end body
        html_string = '''  
                            </page>
                            </body>
                       '''      
        with open(download_path + 'story.html', encoding='utf-8', mode='a') as output:
            output.write(html_string)

        return True

    except:
        print("error making html file")
        return False