from features.default import BaseFeature
from features.global_vars import bumble_speech as bs
from features.research import glocal_vars, helpers
import os, sys

class StoreData(BaseFeature):
    def __init__(self, keywords):
        self.tag_name = 'store_research_data'
        self.patterns = ["store data", "save my research", "save tabs", "save my data"]
        self.index

    def action(self, spoken_text):
        try:
            filename = self.store_data()
            bs.respond('Research data stored successfully at {}.md'.format(filename))
            return
        except:
            print("Unexpected error:", sys.exc_info())
            bs.respond('Failed to store research data.')
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
                record["page_title"] = self.get_title(url)
                record["url"] = url
                record["viewtime"] = url_viewtimes[parent_url][url]
                record["date_created"] = today
                record["last_updated"] = today

                # Updates record if url already exists, otherwise insert as new record.
                research_db.upsert(record, Record.url == url)
            
        md_file_create(glocal_vars.research_topic, bumblebee_root+'research-files/'+filename)
        return filename

    '''
    Gets title of a url given the url.
    Arguments: <string> url
    Returns the title of the url
    '''
    def get_title(self, url):
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
    def md_file_create(self, research_topic, filename, ordered_by='time'):
        Record = Query()
        records = research_db.search(Record.research_topic == research_topic)
        mdfile = MdUtils(file_name=filename,title=research_topic)
        for record in records:
            mdfile.new_line('- '+ mdfile.new_inline_link(link=record["url"], text=record["page_title"]))
        mdfile.create_md_file()
        return

