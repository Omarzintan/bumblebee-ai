# bumblebee-ai
Voice Assistant in Python

## About
This is Bumblebee, a voice assistant made with Python. Bumblebee was made with the intention of automating certain boring or otherwise tedious tasks that I perform on a daily basis. Bumblebee was also made with the goal of being easily extendible. I also took the opportunity to learn about Neural Networks. Bumblebee works with a Deep Neural Network that is trained based on intents data and is able to find out the intent of a sentece spoken to it. Upon finding the intent of the input, Bumblebee run the action of the corresponding feature.
So far, Bumblebee works well with:
   - Python3.7 on MacOS Big Sur
(More platforms to be tested soon)

## Quickstart (How to add a basic feature)
1) In the `/features` folder, create a new file called `hello_world.py`
2) Import the BaseFeature class by typing `from features.default import BaseFeature`
3) Create your feature class as seen below:

```python
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
            # infinite_speaking_chances is a function that keeps asking for input if your speech is not recognized
            # correctly. To break out of this loop, that is if you don't want to proceed, just say 'cancel' or 'stop'.
            name = ''
            name = self.bs.infinite_speaking_chances(name)
            
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
                                                                
## Features
1) tells the time and date
2) Opens up browser with Google search on any query specified
3) Opens up browser with Youtube search on any query specified
4) Search for information on Wikipedia as well as Wolframalpha
5) Do math using Wolframalpha
6) Can send emails to any contact specified in a contacts.json file
7) Can clock me in and out of work (tracking how many hours I work my various work-study jobs)
8) Research mode *

### Starred Features
1) Research mode: Research mode is a feature that I find super useful with my regular work flow. It is basically a mode that Bumblebee goes into where she tracks all the tabs I open in a google chrome 
browser and stores how long I spend on each tab. The information is then stored in a file whose name Bumblebee requests before starting research mode. The information is stored in a format that is easily
readable. This feature makes conducting research easier since I will not have to worry about bookmarking certain pages or having to go through my whole history in order to find a site I visited weeks ago.
Research mode can be turned on/off on demand and so it doesn't store all the sites I visit all of the time.
(More information about how research mode works will be provided soon)



## Troubleshooting
1. Bumblebee says "Listening..." but does not respond to wake-word? 
  - If on MacOS Terminal, you will have to make sure audio permissions are enabled through System Preferences and try again.
  - For VSCode, make sure that audio permissions are enabled for MacOS terminal through System Preferences, and then launch Bumblebee through MacOS Terminal app. See [here](https://github.com/microsoft/vscode/issues/95062#issuecomment-625553211) for detailed steps.
