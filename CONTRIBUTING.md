# CONTRIBUTING
Contributions are welcome, no matter how small or large. Please read this file to help you contribute to this project. All contributed code should follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) standards.

## Some example contributions.
1) Adding more features (also called skills) to bumblebee-ai.
2) Spelling mistakes in the documentation.
3) Really anything that you think will be helpful.

## Recommended Communication style
1) Please leave a detailed description in the Pull Request.
2) Always review your code first. Leaving comments in your code, noting questions or interesting things for the reviewer.
3) Always communicate as this helps everyone around you.

## Pull Requests
1) Fork the repo and create your branch from ```main```.
2) Your branch name should be descriptive of the work you are doing. i.e. fixes-something, adds-something
3) If you have added code that should be tested, please add tests.
4) Ensure that your tests pass.

## Quickstart (How to add a basic feature)
1) In the `/features` folder, create a new file called `hello_world.py`
2) Create your feature class as seen below:

```python
   from features.default import BaseFeature
   
   class Feature(BaseFeature):
         def __init__(self, bumblebee_api):
             # The tag_name will automatically be used as an intent
             # identifier in the Neural Network.
             # While your tag_name can be anything you want it to be,
             # it must be the same name as your .py file             
             self.tag_name = "hello_world"

             # Define what patterns of sentences you want this feature to correspond with.
             # You can modify these patterns as desired.
             self.patterns = ["say hello world", "repeat hello world!", "my first contribution to Bumblebee!"]

             # Access the the speech instance from the bumblebee_api
             self.speech = bumblebee_api.get_speech()

        # We define our action function where all the action happens :).
        # This function has to be called action.
        def action(self, spoken_text):
            # this is how Bumblebee would ask the user a question to the user.
            name = self.speech.ask_question("What is your name?")

            # the speech.ask_question() function returns 0 if the user expresses the 
            # desire to abort the feature by saying "cancel" or "stop".
            if not name:
              return
               
            # We use the respond function from the bs (bumble speech) class to let Bumblebee say "Hello, world".
            self.speech.respond(f"Hey {name}")
            self.speech.respond("Hello, world!")
            
            return
```
4) Now that you have created your feature file, open the `__init__.py` file in the `/features` folder and add the name of your file to the `__all__` list like so:
   ```python
   __all__ = [
        'hello_world'
    ]
   ``` 
5) If you are using the neural-network-based approach as the decision strategy, when you run `python main.py` from the bumblebee folder, you should see that the `intents.json` file is regenerated and the model is retrained. Now when you say "Bumblebee" and Bumblebee asks "how may I help you?" you can say any sentence similar to the sentence `patterns` you defined in your `hello_world.py` file and the action for your feature should be executed! Note: If you are using the rule-based approach as the decision strategy, make sure what you say to Bumblebee contains at least one of the phrases you listed in the `self.patterns`.

## Useful information for creating new features.
### Using the bumblebee_api to store global variables across features.
If you need to store global variables that can be accessed by other features in bumblebee, use the bumblebee_api. The bumblebee_api is passed into every feature through the `__init__` function of the Feature class. Here is how you would store a global variable using the bumblebee_api:
```python
# feature1.py

from features.default import BaseFeature 

class StoreKeys():
      MYGLOBAL_VAR = 'myvariable'

class Feature(BaseFeature):
      def __init__(self, bumblebee_api):

          ...

        # Store the bumblebee_api as api
        self.api = bumblebee_api

      
      def action(self):
        # storing a global variable
        myvariable = "hey"
        self.api.store_var(StoreKeys.MYGLOBAL_VAR, myvariable)

      ...
```
Now if you want to retrieve this same global variable from another feature, you would use the bumblebee_api like so:
```python
# feature2.py

from features.default import BaseFeature
from features.feature1 import StoreKeys as feature1_store

class Feature(BaseFeature):
      def __init__(self, bumblebee_api):

          ...

        # Store the bumblebee_api as api
        self.api = bumblebee_api

      def action(self):
        # retrieving a global variable from feature1
        myvariable = self.api.get_var(
          feature1_store.MYGLOBAL_VAR
          )

        ...

```

### Dealing with the config file.
#### Sample config file
This is what the config file (automatically generated on install) looks like:
```yaml
Api_keys:
  gmail: YOUR_PATH_TO_GMAIL_CREDENTIALS_FILE
  wolframalpha: YOUR_API_KEY_HERE
Common:
  bumblebee_dir: /Users/user/Desktop/bumblebee/
  python3_env: /Users/user/opt/anaconda3/envs/bumblebee/bin/python3.7
Databases:
  contacts: /Users/user/Desktop/bumblebee/databases/contacts_db.json
  employers: /Users/user/Desktop/bumblebee/databases/employers_db.json
  research: /Users/user/Desktop/bumblebee/databases/research_db.json
  zoom: /Users/user/Desktop/bumblebee/databases/zoom_db.json
Folders:
  research_files: /Users/user/Desktop/bumblebee/research_files/
  work_study: /Users/user/Desktop/bumblebee/work_study
  models: /Users/zintan/fun-projects/bumblebee/models
Utilities:
  research_server_url: http://127.0.0.1:8000
```

#### Accessing variables from the config file
This how you can access variables in the config file from your feature file.

```python
# feature.py

from features.default import BaseFeature

class Feature(BaseFeature):
      
      def __init__(self, bumblebee_api):

        ...

        # get config file through the bumblebee_api
        self.config = bumblebee_api.get_config()

        # Accessing the bumblebee_dir variable.
        bumblebee_dir = self.config['Common']['bumblebee_dir']

        ...


      
```

#### Modifying the config file
If you are simply changing values of existing variables in the config file, you should change them manually.

If you are adding a new variable that you want to be added by default whenever bumblebee is freshly installed by someone, you can go ahead and add it to the `utils/config_builder.py` file.

### Dealing with thread-based feature actions
#### Adding thread_failsafe
If you write a feature that performs an action within a thread. You need to use our ```add_thread_failsafe``` function in the ```bumblebee_api``` to ensure that bumblebee terminates the thread before shutting down if the thread is not terminated manually.

For instance, I have a feature that starts a server in a separate thread which runs in the background while bumblebee is running. This is how I would add a thread failsafe.
```python
# run_server.py

import threading
import subprocess
from features.default import BaseFeature

class StoreKeys():
      SERVER_PROC_ID = 'server_proc_id'

class Feature(BaseFeature):

      def __init__(self,  bumblebee_api):

        ...

        self.api = bumblebee_api
        self.config = bumbleee_api.get_config

      def action(self, spoken_text):
          '''Calls my run_server function in a separate thread.'''
          threading.Thread(target=self.run_server).start()

      def run_server(self):
          '''Runs a server using subprocess.'''
          # Access important file paths from self.config
          python3_path = self.config['Common']['python3_path']
          bumblebee_dir = self.config['Common']['bumblebee_dir']

          # Creating the subprocess that calls my server
          process = subprocess.Popen(
                     [python3_path, bumblebee_dir+'server.py']
                     )
          
          # Get the process id and store it globally.
          proc_id = process.pid
          self.api.store_var(
            StoreKeys.SERVER_PROC_ID, proc_id
            )
          
          # Adding the thread failsafe.
          # The add_thread_failsafe function takes the process id,
          # and a list of tags of features you want to run when this
          # thread is being terminated.

          # In this example, I have two other features whose tag_names 
          # are save_server_data and stop_server. I want bumblebee to
          # run these features before terminating this thread. The order
          # in which you put the tags is the same order in which the
          # features related to these tags are run.
          
          self.api.add_thread_failsafe(
                proc_id, [save_server_data, stop_server]
                )
```

#### Removing thread_failsafe
If you write a feature that runs in a thread, it is advisable to also create another feature responsible for terminating this thread. Using the above example of our ```run_server.py``` feature, we would also create a ```stop_server.py``` feature. In this feature, we will use ```self.api.remove_thread_failsafe()``` to remove the failsafe after we have terminated the thread.
```python
# stop_server.py

import os
import signal
from features.default import BaseFeature
from features.run_server import StoreKeys as run_server_store

class Feature(BaseFeature):

      def __init__(self, bumblebee_api):

        ...

        self.api = bumblebee_api

      def action(self, spoken_text):
          '''Calls the stop server function.'''
          self.stop_server()

      def stop_server(self):
          '''Stops my running server.'''
          # Retrieve the proc_id of the server stored globally.
          server_proc_id = self.api.pop_var(
            run_server_store.SERVER_PROC_ID
            )

          # Kill the server process
          os.kill(server_proc_id, signal.SIGTERM)

          # Remove the thread_failsafe that we added for the server process
          # Pass in the process id as the argument.
          self.api.remove_thread_failsafe(server_proc_id)
```

### More about bumblebee_api
#### Here are all functions that the bumblebee_api can perform
```python
'''
Internal API for Bumblebee. Functions include:
    Handling global variables that need to be shared
between features.
    Modifying characteristics of the bee instance running
the features.
    Exposes certain function of the bee instance to features.
    Utility functions for tracking and safely removing threaded
feature actions.
'''
def store_var(self, name: str, value):
    """
    Stores variable in global store of bee instance.
    Arguments: <string> name, value
    Returns: None
    Example: bumblebee_api.store_var("my_variable", variable value)
    """

def get_var(self, name: str):
    """
    Retrieves a variable from global store of the bee instance.
    Arguments: <string> name
    Returns if found: value of variable name stored in global_store
    Returns if not found: None
    Example: bumblebee_api.get_var("my_variable")
    """

def remove_var(self, name: str):
    """
    Removes a variable from the global store of the bee instance.
    Arguments: <string> name
    Returns if successful: None
    Returns if unsuccessful: None (prints error)
    Example: bumblebee_api.remove_var("my_variable")
    """

def pop_var(self, name: str):
    """
    Removes a variable from the global store of the bee instance and
    returns it.
    Arguments: <string> name
    Returns if found: value of variable
    Returns if not found: None (prints error)
    Example: bumblebee_api.pop_var("my_variable")
    """

def add_thread_failsafe(self, proc_id: int,
                        termination_features=[]):
    """
    Inserts a record of a running thread into the threads
    list in Bee.
    Arguments: <int> proc_id (process id of the thread),
                <list> termination_features (list of feature tags,
                indicating features to run in order to terminate thread.
                These features are run when exiting gracefully)
    Returns: None
    Example: bumblebee_api.add_thread_failsafe(myproc_id, [feature_1_tag, feature_2_tag])
    """

def remove_thread_failsafe(self, proc_id: int):
    """
    Removes record of running thread from threads list
    in Bee.
    Arguments: <int> proc_id (process id of the thread)
    Returns if successful: None
    Returns if unsuccessful: None (prints error)
    Example: bumblebee_api.remove_thread_failsafe(myproc_id)
    """

def get_config(self):
    """
    Get the config file for the bee instance.
    Arguments: None
    Returns: config yaml file of bee instance
    Example: bumblebee_api.get_config()
    """

def get_speech(self):
    """
    Get the BumbleSpeech instance of the bee instance.
    Arguments: None
    Returns: speech instance of bee instance
    Example: bumblebee_api.get_speech()
    """
    
def get_name(self):
    """
    Gets the name of the bee_instance
    Arguments: None
    Returns: name of bee instance
    Example: bumblebee_api.get_name()
    """

def run_by_tags(self, feature_tags: list, argmuments_list: list = []):
    """
    Run a list of feature actions given their tags and arguments lists.
    Arguments: <list> feature_tags, <list<list>> arguments_list
    Returns: whatever the feature ran will return
    Example: 
    feature_tags = [feature_1_tag, feature_2_tag, feature_3_tag, feature_4_tag]
    arguments_list = [[arg1_for_feature1, arg2_for_feature1], [arg1_for_feature2, arg2_for_feature2, arg_3_for_feature2], [arg1_for_feature3], []]
    bumblebee_api.run_by_tags(feature_tags, arguments_list)
    """

def run_by_input_list(self, input_list: list):
    """
    Run features based on a list of inputs.
    Arguments: <list> input_list
    Returns: whatever the features chosen do with the input given to them.
    Example: bumblebee_api.run_by_input_list(["say hello world", "what is the time?"])
    """

def sleep_on(self):
    """
    Puts bee instance to sleep
    Arguments: None
    Returns: None
    Example: bumblebee_api.sleep_on()
    """
```
## Community
If you have questions, feel free to join the conversation in the discussions tab.
