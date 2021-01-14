from flask import Flask, jsonify, request
import time
import os, sys
import textwrap

'''
This file contains server code to be used by bumblebee.py research mode.
The server works hand in hand with a chrome extension to implement research mode. (Found in the extension folder)
'''

app = Flask(__name__)
url_timestamp = {}
url_viewtime = {}
parent_url_viewtime = {}
parent_url_timestamp = {}
prev_url = ""
prev_parent_url = ""
num_lines = 0


'''
Strips long url into a shorter url that only consists of the parent url.
e.g. long url = https://abcdefg.com/search?q=mysearch
     parent url = abcdefg.com
'''
def url_strip(url):
    if "http://" in url or "https://" in url:
        url = url.replace("https://", '').replace("http://", '').replace('\"', '')
    if "/" in url:
        url = url.split('/', 1)[0]
    return url

'''
Receives browser tab data from sender (in my case it is 
the Chrome extension.) 
Uses time module to calculate how long the tab has been 
active.
Also calculates final timestamp when tab is closed.
Send success message on success.
'''
@app.route('/send_url', methods=['POST'])
def send_url():
    resp_json = request.get_data()
    params = resp_json.decode()
    url = params.replace("url=", "")
    parent_url = url_strip(url)
    sys.stdout.write("currently viewing: %s\n" % parent_url)

    global parent_url_timestamp
    global parent_url_viewstamp
    global prev_url
    global prev_parent_url
 
    # If this is a new parent url. i.e. we have never
    # visited this url since the server started running.
    # Note: If the parent_url is not in the keys in the
    # parent_url_timestamp dictionary, it could be a new
    # tab or not.
    if parent_url not in parent_url_timestamp.keys():
        url_viewtime = {}
        # Set the viewtime of the specific url to 0.
        url_viewtime[url] = 0
        parent_url_viewtime[parent_url] = url_viewtime
        url_timestamp = {}
    else:
        # If we have seen this parent url before. Here, we
        # are either viewing a new specific url within the parent
        # url or we are viewing a specific url that we have seen before.
        
        # Access the url_viewtime dictionary for this parent_url.
        url_viewtime = parent_url_viewtime[parent_url]
        
        # If this specific url doesn't exist in the url_viewtime dictionary
        # (accessed in previous line), set the url_viewtime for this url to 0
        # and update the url_viewtime dictionary for the parent_url to include
        # this value.
        # Note: If it does exist, we do not need to do anything to it.
        if url not in url_viewtime.keys():
            url_viewtime[url] = 0
            parent_url_viewtime[parent_url] = url_viewtime
            
        # Access the specific url timestamp dictionary for this parent url.
        url_timestamp = parent_url_timestamp[parent_url]
   
    # If this is not the first tab/url opened on the browser.
    # We caculate the time spent on the previous tab/url by subtracting the
    # timestamp of that tab/url from the current time.
    if prev_url != '' and prev_parent_url != '':
        # Time spent is the current time - the timestamp of the previous url
        time_spent = int(time.time() - parent_url_timestamp[prev_parent_url][prev_url])
        
        # The url_viewtime of the previous url is then updated with time_spent
        parent_url_viewtime[prev_parent_url][prev_url] += time_spent
        
    x = int(time.time())
    
    # set the timestamp of the current url to x.
    url_timestamp[url] = x
    
    # Update the parent url_timestamp dictionary
    parent_url_timestamp[parent_url] = url_timestamp

    # Update the parent url_viewtime dictionary
    parent_url_viewtime[parent_url] = url_viewtime
    
    prev_url = url
    prev_parent_url = parent_url

    return jsonify({'message': 'success!'}), 200

'''
Does nothing but sends success message when a tab is closed. The 
collation of final timestamp data is done in the send_url function.
Sends success message on success
'''
@app.route('/quit_url', methods=['POST'])
def quit_url():
    resp_json = request.get_data()
    sys.stdout.write("Url closed: %" % resp_json.decode())
    return jsonify({'message': 'quit success!'}), 200

'''
Responsible for storing all the tab information into a .txt file for future use.
Sends success message on success.
'''
@app.route('/store_data', methods=['POST'])
def store_data():
    global parent_url_timestamp
    global parent_url_viewtime
    
    resp_json = request.get_data()
    # Get the file name
    params = resp_json.decode()
    filename = request.args.get('filename')
    
    # Store files in ./research-files
    os.makedirs(os.environ.get('BUMBLEBEE_PATH')+'research-files', exist_ok=True)
    
    # Open the file
    file = open(os.environ.get('BUMBLEBEE_PATH')+os.path.join('research-files', filename+'.txt'), 'a+')

    # Write data to the file
    for key in parent_url_timestamp.keys():
        total_viewtime = 0
        file.write('{}:\n'.format(key))
        wrapper = textwrap.TextWrapper(initial_indent='\t', subsequent_indent='\t') # Makes formating text easier
        for url in parent_url_viewtime[key].keys():
            wrapped = wrapper.fill('{}: viewtime = {}'.format(url, parent_url_viewtime[key][url]))
            file.write(wrapped+'\n')
            total_viewtime+=parent_url_viewtime[key][url]
        file.write('total_viewtime for {} = {}\n'.format(key, total_viewtime))        
    file.close()

    return jsonify({'message':'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
