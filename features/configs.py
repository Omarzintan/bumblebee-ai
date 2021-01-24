from features.keywords import Keywords
from features.contacts import *
from features.google import *
from features.research import *
from features.myemail import *

keywords = Keywords()

getEmail = getemail.GetEmail(['get email'])
google_search = google_search.GoogleSearch(keywords.get('search_google'))
start_research_server = start_server.StartServer(keywords.get('start_research'))
stop_research_server = stop_server.StopServer(keywords.get('stop_research'))
store_research_data = store_data.StoreData(keywords.get('store_research_data'))
send_email = send_email.SendEmail(keywords.get('send_email'))

config_actions = [
    #getEmail,
    #google_search,
    #start_research_server,
    #store_research_data,
    #stop_research_server,
    #send_email
    ]

 #print(config_actions)
