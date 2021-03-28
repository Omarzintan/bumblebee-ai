'''Helper Functions for research features.'''

from tkinter import *
import json
import os, sys
from features.research import glocal_vars
from tinydb import TinyDB, Query
import subprocess
import signal
import datetime
from helpers import bumblebee_root
import requests
from mdutils import MdUtils
from bs4 import BeautifulSoup
import validators

research_db = TinyDB(os.getenv('BUMBLEBEE_PATH')+'database/research_db.json')

'''
Opens a Tkinter window to allow the user to edit the research topic as heard.
Argument: <string> topic
Return type: <JSON> topic_details_json
'''
def topic_edit(topic):
    root = Tk()
    root.geometry("320x100")
    root.title("Edit research topic")
    content = Frame(root)
    content.pack()
    topic_details = {}

    # creating topic field
    Label(content, text="Topic").grid(row=0, column=0, padx=5, sticky='sw')

    topic_entry = Entry(content, width=24)
    topic_entry.grid(row=0, column=1, padx=5)

    # inserting previous topic
    topic_entry.insert(END, topic)

    # retrieve edited topic from window
    def saveInput():
        topic_details["topic"] = str(topic_entry.get())
        root.destroy()

    def clear():
        topic_entry.delet(0, "end")

    # Buttons for saving and clearing
    saveButton = Button(content, text="Save", command=saveInput)
    clearButton = Button(content, text="Clear", command=clear)
    saveButton.grid(row=1, column=1, padx=5, sticky='e')
    clearButton.grid(row=1, column=1, padx=5, sticky='w')

    root.mainloop()

    topic_details_json = json.dumps(topic_details)
    return topic_details_json

'''Stops the flask server for research mode.'''
def stop_server():
    print(glocal_vars.server_proc)
    print(glocal_vars.server_proc.pid)
    try:
        glocal_vars.server_proc.kill()
        glocal_vars.server_proc = ''
        print('Server stopped')
    except:
        print("Unexpected error:", sys.exc_info())
        bs.respond('The server does not seem to be running')

'''Starts the flask server for research mode.'''
def start_server():
    # Create the subprocess for the flask server.
    glocal_vars.server_proc = subprocess.Popen([os.environ.get('PYTHON3_ENV'), bumblebee_root+'server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid())
    return

'''
Gets title of a url given the url.
Arguments: <string> url
Returns the title of the url
'''
def get_title(url):
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    url_title = ''
    for title in soup.find_all('title'):
        url_title+=title.get_text()
    return url_title

'''
Creates a markdown file of data in the research database given 
a research topic.
Returns the file name
'''
def md_file_create(research_topic, filename, ordered_by='time'):
    Record = Query()
    records = research_db.search(Record.research_topic == research_topic)
    mdfile = MdUtils(file_name=filename,title=research_topic)
    for record in records:
       mdfile.new_line('- '+ mdfile.new_inline_link(link=record["url"], text=record["page_title"]))
    mdfile.create_md_file()
    return

'''
Retrieves research data from server and stores the data in 
the research database.
'''
def store_data():
    # Store files in ./research-files
    os.makedirs(bumblebee_root+'research-files', exist_ok=True)

    filename = glocal_vars.research_topic
    filename = filename.replace(' ', '-')
    today = datetime.datetime.now().strftime('%a %b, %Y')

    res = requests.get(os.getenv('SERVER_URL')+'/store_data')
    res.raise_for_status()
    json_response = res.json()
    parent_urls = json_response["parent_urls"]
    url_viewtimes = json_response["url_viewtimes"]
    Record = Query()

    #store data in tinydb
    for parent_url in parent_urls:
        record = {}
        for url in url_viewtimes[parent_url]:
            if not validators.url(url):
                continue
            record["research_topic"] = glocal_vars.research_topic
            record["parent_url"] = parent_url
            record["page_title"] = get_title(url)
            record["url"] = url
            record["viewtime"] = url_viewtimes[parent_url][url]
            record["last_updated"] = today

            # Updates record if url already exists, otherwise insert as new record.
            research_db.upsert(record, Record.url == url)
            
    md_file_create(glocal_vars.research_topic, bumblebee_root+'research-files/'+filename)
    return filename
