from flask import Flask, jsonify, request
import time
import sys
from utils.helpers import bumblebee_root
from logging.config import fileConfig

'''
This file contains server code to be used for researching.
The server works hand in hand with a chrome extension to implement
research mode. (Found in the chrome extension folder)
'''

app = Flask(__name__)
fileConfig(bumblebee_root+'logging.cfg')

url_timestamp = {}
url_viewtime = {}
parent_url_viewtimes = {}
parent_url_timestamp = {}
prev_url = ""
prev_parent_url = ""
num_lines = 0


def url_strip(url):
    '''
    Strips long url into a shorter url that only consists of the parent url.
    e.g. long url = https://abcdefg.com/search?q=mysearch
    parent url = abcdefg.com
    '''
    if "http://" in url or "https://" in url:
        url = url.replace("https://", '')
        url = url.replace("http://", '')
        url = url.replace('\"', '')
    if "/" in url:
        url = url.split('/', 1)[0]
    return url


@app.route('/send_url', methods=['POST'])
def send_url():
    '''
    Receives browser tab data from sender (in my case it is
    the Chrome extension.)
    Uses time module to calculate how long the tab has been
    active.
    Also calculates final timestamp when tab is closed.
    Send success message on success.
    '''
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
        parent_url_viewtimes[parent_url] = url_viewtime
        url_timestamp = {}
    else:
        # If we have seen this parent url before. Here, we
        # are either viewing a new specific url within the parent
        # url or we are viewing a specific url that we have seen before.

        # Access the url_viewtime dictionary for this parent_url.
        url_viewtime = parent_url_viewtimes[parent_url]

        # If this specific url doesn't exist in the url_viewtime dictionary
        # (accessed in previous line), set the url_viewtime for this url to 0
        # and update the url_viewtime dictionary for the parent_url to include
        # this value.
        # Note: If it does exist, we do not need to do anything to it.
        if url not in url_viewtime.keys():
            url_viewtime[url] = 0
            parent_url_viewtimes[parent_url] = url_viewtime

        # Access the specific url timestamp dictionary for this parent url.
        url_timestamp = parent_url_timestamp[parent_url]

    # If this is not the first tab/url opened on the browser.
    # We caculate the time spent on the previous tab/url by subtracting the
    # timestamp of that tab/url from the current time.
    if prev_url != '' and prev_parent_url != '':
        # Time spent is the current time - the timestamp of the previous url
        time_spent = int(
            time.time() - parent_url_timestamp[prev_parent_url][prev_url]
        )

        # The url_viewtime of the previous url is then updated with time_spent
        parent_url_viewtimes[prev_parent_url][prev_url] += time_spent

    x = int(time.time())

    # set the timestamp of the current url to x.
    url_timestamp[url] = x

    # Update the parent url_timestamp dictionary
    parent_url_timestamp[parent_url] = url_timestamp

    # Update the parent url_viewtime dictionary
    parent_url_viewtimes[parent_url] = url_viewtime

    prev_url = url
    prev_parent_url = parent_url

    return jsonify({'message': 'success!'}), 200


@app.route('/quit_url', methods=['POST'])
def quit_url():
    '''
    Does nothing but sends success message when a tab is closed. The
    collation of final timestamp data is done in the send_url function.
    Sends success message on success
    '''
    resp_json = request.get_data()
    sys.stdout.write("Url closed: %s \n" % resp_json.decode())
    return jsonify({'message': 'quit success!'}), 200


@app.route('/store_data', methods=['GET'])
def store_data():
    '''
    Returns all tab info collected so far.
    To be called by helper function in research feature.
    '''
    return jsonify(
        {
            'message': 'success',
            'parent_urls': list(parent_url_timestamp.keys()),
            'url_viewtimes': parent_url_viewtimes
        }
    ), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
