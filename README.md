# Tarina

Tarina is a novel writing tool that runs on the browser. Unlike many other programs, Tarina allows you to open the story in multiple windows. This way editing and referencing becomes easier and the whole writing experience is more fluid. The editor utilizes CKeditor5 which includes wide variety of formatting options as well as adding tables and images. The novels can be exported in either docx or html format.

## Installation
Install the required python packages and npm modules. Note that backend requires python 3.6 or newer
```
git clone https://github.com/mattocksw/Tarina.git
cd Tarina
pip install -r requirements.txt
npm install
python app.py
```

The backend logic is handled by python bottle server and the frontend by vue CLI. The editor instances use ckeditor5.
