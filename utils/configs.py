from features.keywords import Keywords
from features.google import *
from features.research import *
from features.myemail import *
from features.employment import *
from features.mywolframalpha import *
from features.control import *
from features.greeting import *
from features.youtube import *
from features.mywikipedia import *
from features.bumblebee_help import *
from features.mynotepad import *
from features.time import *
from features.zoom import *
from features.silent_mode import *

keywords = Keywords()

google_search = google_search.GoogleSearch(keywords.get('search_google'))
start_research_server = start_server.StartServer(keywords.get('start_research'))
stop_research_server = stop_server.StopServer(keywords.get('stop_research'))
store_research_data = store_data.StoreData(keywords.get('store_research_data'))
send_email = send_email.SendEmail(keywords.get('send_email'))
clock_in = clock_in.ClockIn(keywords.get('clock_in'))
clock_out = clock_out.ClockOut(keywords.get('clock_out'))
wolfram_search = wolfram_search.WolframalphaSearch(keywords.get('search_wolframalpha'))
sleep = sleep.Sleep(keywords.get('sleep'))
stop_listening = stop_listening.StopListening(keywords.get('stop_listening'))
greet = greeting.Greeting(keywords.get('greet'))
youtube_search = youtube_search.YoutubeSearch(keywords.get('search_youtube'))
wiki_search = wiki_search.WikipediaSearch(keywords.get('search_wikipedia'))
bumble_help = bumble_help.BumbleHelp(keywords.get('help'))
open_notepad = open_notepad.OpenNotepad(keywords.get('open_notepad'))
get_time = get_time.GetTime(keywords.get('time'))
add_zoom = add_zoom.AddZoom(keywords.get('add_zoom'))
open_zoom = open_zoom.OpenZoom(keywords.get('open_zoom'))
silent_mode_on = silent_mode_on.SilentModeOn(keywords.get('silent_mode_on'))
silent_mode_off = silent_mode_off.SilentModeOff(keywords.get('silent_mode_off'))

config_actions = [
    google_search,
    start_research_server,
    store_research_data,
    stop_research_server,
    send_email,
    clock_in,
    clock_out,
    wolfram_search,
    sleep,
    stop_listening,
    greet,
    youtube_search,
    wiki_search,
    bumble_help,
    open_notepad,
    get_time,
    add_zoom,
    open_zoom,
    silent_mode_on,
    silent_mode_off
]