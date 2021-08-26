'''Runs a routine of features.'''
from features.default import BaseFeature
from features.feature_helpers import get_search_query
from tinydb import TinyDB, Query


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "run_routine"
        self.patterns = [
            "run routine for", "start routine",
            "start routine for"
        ]
        self.api = bumblebee_api
        self.bs = bumblebee_api.get_speech()
        self.config = bumblebee_api.get_config()

        routines_db_path = self.config['Database']['routines']
        self.routines_db = TinyDB(routines_db_path)

    def action(self, spoken_text, arguments_list: list = []):
        name = self.get_search_query(spoken_text)
        tags_list, arguments = self.process_routine_file(
            self.get_routine_filepath(name))
        if not tags_list:
            self.bs.respond(f"Could not run '{name}' routine.")
            return
        self.bs.respond(f"Running '{name}' routine.")
        self.api.run_by_tags(tags_list, arguments)
        return

    def get_routine_filepath(self, name):
        '''Searches for specific routine based on its name and returns the
        routine's filename.
        Arguments: <string> name - the name of the routine.
        Return type: <string> filename - the filename of the routine.
        '''
        Item = Query()
        results_list = self.routines_db.search(Item.name == name)
        if not results_list:
            self.bs.respond(f"Could not find routine called {name}.")
            return ""
        # get the first search result
        result = results_list[0]
        return result["filepath"]

    def process_routine_file(self, filepath):
        '''Processes the routine file to retrieve the tag names and their
        respective arguments.
        Arguments: <string> filepath - the path to the routine file.
        Return type: <list> tags_list - the list of feature tags retrieved
        from the file, <list> arguments_list - the list of arguments for each
        feature tag retrieved from the file.
        '''
        tag_list = []
        arguments_list = []
        if not filepath:
            return tag_list, arguments_list
        # open file
        with open(filepath, "r") as routine_file:
            # read first line - name of routine
            routine_file.readline()
            # read second line - blank line
            routine_file.readline()
            # read rest of lines until EOF.
            for line in routine_file.read().splitlines():
                split_line = line.split("->")
                # get the tag name.
                tag_name = split_line[0]
                tag_list.append(tag_name)
                # append empty list of arguments if no arguments are given for
                # a tag and move to next line.
                if (len(split_line) == 1):
                    arguments_list.append([])
                    continue
                # get arguments if they exist.
                arguments = list(split_line[1].split(";"))
                arguments_list.append(arguments)
        return tag_list, arguments_list

    def get_search_query(self, spoken_text):
        '''
        Parse spoken text to retrieve a the name of the routine.
        '''
        search_terms = ['to', 'for']
        search_query = get_search_query(
            spoken_text,
            self.patterns,
            search_terms
        )
        return search_query
