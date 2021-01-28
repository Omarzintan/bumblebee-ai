class Keywords:
    """Dictionary containing all keywords to corresponding functions in bumblebee.py
    """
    def __init__(self):
        self.keywords = {
            "sleep": ['i\'m done', 'all done', 'exit', 'bye', 'go to sleep'],
            "search_wikipedia": ['wikipedia'],
            "search_wolframalpha": ['calculate', 'what is'],
            "search_google": ['google'],
            "search_youtube": ['youtube'],
            "time": ['time'],
            "greet": ['hello', 'what\'s up', 'hey'],
            "help": ['about yourself', 'help me', 'who are you', 'what are you'],
            "open_notepad": ['open notepad'],
            "send_email": ['send email'],
            "add_contact": ['add email contact', 'add contact'],
            "stop_research": ['stop research', 'exit research mode', 'done researching'],
            "start_research": ['start research', 'research mode' 'let\'s do research'],
            "store_research_data": ['store data', 'save research', 'save tabs'],
            "open_shell": ['open shell'],
            "clock_in": ['clock in', 'let\'s work', 'start work'],
            "clock_out": ['clock out', 'done working', 'stop work'],
            "stop_listening": ['stop listening', 'shutdown', 'shut down'],
        }

    def get(self, key_name):
        if key_name == 'all':
            return self.keywords
        return self.keywords[key_name]
