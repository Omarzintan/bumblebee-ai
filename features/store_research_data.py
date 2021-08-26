from features.default import BaseFeature
import datetime
import requests
from tinydb import TinyDB, Query
from mdutils import MdUtils
from features.start_research_server import StoreKeys as research_store
from bs4 import BeautifulSoup
import validators


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = 'store_research_data'
        self.patterns = [
            "store data",
            "save my research",
            "save tabs",
            "save my data"
        ]
        self.api = bumblebee_api
        self.bs = self.api.get_speech()
        self.config = self.api.get_config()

        research_db_path = self.config['Database']['research']
        self.research_db = TinyDB(research_db_path)

    def action(self, spoken_text: str = "", arguments_list: list = []):
        try:
            filename = self.store_data()
            self.bs.respond(
                f'Research data stored successfully at {filename}.md'
            )
            return
        except Exception as exception:
            print(exception)
            self.bs.respond('Failed to store research data.')
            return

    '''
    Retrieves research data from server and stores the data in
    the research database.
    '''

    def store_data(self):
        # The research files folder is gauranteed to exist.
        research_files_path = self.config['Folders']['research_files']
        server_url = self.config['Utilities']['research_server_url']

        research_topic = self.api.get_var(
            research_store.RESEARCH_TOPIC
        )
        filename = research_topic.replace(' ', '-')
        today = datetime.datetime.now().strftime('%a %b, %Y')

        res = requests.get(server_url+'/store_data')
        res.raise_for_status()
        json_response = res.json()
        parent_urls = json_response["parent_urls"]
        url_viewtimes = json_response["url_viewtimes"]
        Record = Query()

        # store data in tinydb
        for parent_url in parent_urls:
            record = {}
            for url in url_viewtimes[parent_url]:
                if not validators.url(url):
                    continue
                record["research_topic"] = research_topic
                record["parent_url"] = parent_url
                record["page_title"] = self.get_title(url)
                record["url"] = url
                record["viewtime"] = url_viewtimes[parent_url][url]
                record["date_created"] = today
                record["last_updated"] = today

                # Updates record if url already exists, otherwise insert
                # as new record.
                self.research_db.upsert(record, Record.url == url)

        self.md_file_create(research_topic, research_files_path + filename)
        return filename

    def get_title(self, url):
        '''
        Gets title of a url given the url.
        Arguments: <string> url
        Returns the title of the url
        '''
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        url_title = ''
        for title in soup.find_all('title'):
            url_title += title.get_text()
        return url_title

    def md_file_create(self, research_topic, filename, ordered_by='time'):
        '''
        Creates a markdown file of data in the research database given
        a research topic.
        Returns the file name
        '''
        Record = Query()
        records = self.research_db.search(
            Record.research_topic == research_topic
        )
        mdfile = MdUtils(file_name=filename, title=research_topic)
        for record in records:
            mdfile.new_line('- ' +
                            mdfile.new_inline_link(
                                link=record["url"],
                                text=record["page_title"]
                            )
                            )
        mdfile.create_md_file()
        return
