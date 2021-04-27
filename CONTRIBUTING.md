# CONTRIBUTING
Contributions are welcome, no matter how small or large. Please read this file to help you contribute to this project.

## Some example contributions.
1) Adding more features (also called skills) to bumblebee-ai.
2) Spelling mistakes in the documentation.
3) Really anything that you think will be helpful.

## Recommended Communication style
1) Please leave a detailed description in the Pull Request.
2) Always review your code first. Leaving comments in you code, noting questions or interesting things for the reviewer.
3) Always communicate as this helps everyone around you.

## Pull Requests
1) Fork the repo and create your branch from ```main```.
2) Your branch name should be descriptive of the work you are doing. i.e. fixes-something, adds-something
3) If you have added code that should be tested, please add tests.
4) Ensure that your tests pass.

## Quickstart (How to add a basic feature)
1) In the `/features` folder, create a new file called `hello_world.py`
2) Import the BaseFeature class by typing `from features.default import BaseFeature`
3) Create your feature class as seen below:

```python
   from features.default import BaseFeature
   
   class Feature(BaseFeature):
         def __init__(self):
             # The tag_name will automatically be used as an intent
             # identifier in the Neural Network.
             # While your tag_name can be anything you want it to be,
             # it must be the same name as your .py file             
             self.tag_name = "hello_world"

             # Define what patterns of sentences you want this feature to correspond with.
             # You can modify these patterns as desired.
             self.patterns = ["say hello world", "repeat hello world!", "my first contribution to Bumblebee!"]

             # Initialize some important variables from the BaseFeature class in default.py
             # Such important variables include Bumblebee's speech function (which we call bs)
             # i.e. short for bumble speech, as well as Bumblebee's config variable which we use
             # to read values from the config.ini file. (Not relevant here)
             super().__init__()

        # We define our action function where all the action happens.
        # This function has to be called action.
        def action(self, spoken_text):
            # use the respond function from the bs (bumble speech) class to let Bumblebee ask for your name.
            self.bs.respond("What is your name?")
            
            # this is how Bumblebee would receive a response from the user
            # hear is a function that keeps asking for input if your speech is not recognized
            # correctly. 
            name = self.bs.hear()
            
            # stops running feature if 'cancel' or 'stop' is in input
            if self.bs.interrupt_check(name):
               return
               
            # We use the respond function from the bs (bumble speech) class to let Bumblebee say "Hello, world".
            self.bs.respond(f"Hey {name}")
            self.bs.respond("Hello, world!")
            
            return
```
4) Now that you have created your feature file, open the `__init__.py` file in the `/features` folder and add the name of your file to the `__all__` list like so:
   ```python
   __all__ = [
        'hello_world'
    ]
   ``` 
5) When you run `python main.py` from the bumblebee folder, you should see that the `intents.json` file is regenerated and the model is retrained. Now when you say "Bumblebee" and Bumblebee asks "how may I help you?" you can say any sentence similar to the sentence `patterns` you defined in your `hello_world.py` file and the action for your feature should be executed!

## Useful information for creating new features.
### Using the globals_api
If you need to store global variables that can be accessed by other features in bumblebee, use the globals_api. Since every feature you create inherits from the BaseFeature class, you should have access to the ```globals_api``` from within your feature. Here is how you would store a global variable:
```python
# feature1.py

from features.default import BaseFeature 

class Feature(BaseFeature):
      ...

      # storing a global variable
      myvariable = "hey"
      self.globals_api.store('myvariable', myvariable)

      ...
```
Now if you want to retrieve this same global variable from another feature, you would use the globals_api like so:
```python
# feature2.py

from features.default import BaseFeature

class Feature(BaseFeature):
      ...

      # retrieving a global variable
      myvariable = self.globals_api.retrieve('myvariable')

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

      ...
      
      # Accessing the bumblebee_dir variable.
      bumblebee_dir = self.config['Common']['bumblebee_dir']
      
```

#### Modifying the config file
If you are simply changing values of existing variables in the config file, you should change them manually.

If you are adding a new variable that you want to be added by default whenever bumblebee is freshly installed by someone, you can go ahead and add it to the `utils/config_builder.py` file.

### Dealing with thread-based feature actions
#### Adding thread_failsafe
If you write a feature that performs an action within a thread. You need to use our ```add_thread_failsafe``` function in the ```globals_api``` to ensure that bumblebee terminates the thread before shutting down if the thread is not terminated manually.

For instance, I have a feature that starts a server in a separate thread which runs in the background while bumblebee is running. This is how I would add a thread failsafe.
```python
# run_server.py

import threading
import subprocess
from features.default import BaseFeature

class Feature(BaseFeature):

      ...

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
          self.globals_api.store('server_proc_id', proc_id)
          
          # Adding the thread failsafe.
          # The add_thread_failsafe function takes the process id,
          # and a list of tags of features you want to run when this
          # thread is being terminated.

          # In this example, I have two other features whose tag_names 
          # are save_server_data and stop_server. I want bumblebee to
          # run these features before terminating this thread. The order
          # in which you put the tags is the same order in which the
          # features related to these tags are run.
          
          self.globals_api.add_thread_failsafe(
                proc_id, [save_server_data, stop_server]
                )
```

#### Removing thread_failsafe
If you write a feature that runs in a thread, it is advisable to also create another feature responsible for terminating this thread. Using the above example of our ```run_server.py``` feature, we would also create a ```stop_server.py``` feature. In this feature, we will use ```self.globals_api.remove_thread_failsafe()``` to remove the failsafe after we have terminated the thread.
```python
# stop_server.py

import os
import signal
from features.default import BaseFeature

class Feature(BaseFeature):

      ...

      def action(self, spoken_text):
          '''Calls the stop server function.'''
          self.stop_server()

      def stop_server(self):
          '''Stops my running server.'''
          # Retrieve the proc_id of the server stored globally.
          server_proc_id = self.globals_api.retrieve('server_proc_od')

          # Kill the server process
          os.kill(server_proc_id, signal.SIGTERM)

          # Remove the thread_failsafe that we added for the server process
          # Pass in the process id as the argument.
          self.globals_api.remove_thread_failsafe(server_proc_id)
```

## Community
If you have questions. Join the conversation in our Discord[PUT LINK HERE]
