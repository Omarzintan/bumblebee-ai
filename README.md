# bumblebee-ai
Virtual Assistant in Python

## About
This is Bumblebee, a voice assistant made with Python. Bumblebee was made with the intention of automating certain boring or otherwise tedious tasks that I perform on a daily basis. Bumblebee was also made with the goal of being easily extendible. I also used this as an opportunity to learn about Neural Networks. Bumblebee works with a Deep Neural Network that is trained based on intent data and is able to find out the intent of a sentence spoken to it. Upon finding the intent of the input, Bumblebee runs the action of the corresponding feature.

*So far, Bumblebee works well with:*
   - MacOS Big Sur
   - MacOS Catalina
   *(More platforms to be tested soon)*

## Try Bumblebee out (Mac users)
### Requirements
1) Ensure that you have miniconda/anaconda installed. (miniconda is recommended because it is more lightweight.) [Install miniconda/anaconda](https://docs.conda.io/projects/continuumio-conda/en/latest/user-guide/install/macos.html)
 *If you are not sure whether you have miniconda/anaconda, check by opening a fresh terminal and running ```conda -V``` to ensure that conda is ready to use.
2) You will need ```portaudio``` for bumblebee to work. Ensure that you have portaudio installed. Otherwise, install it here: [install portaudio](https://formulae.brew.sh/formula/portaudio)

### If all requirements are met:
1) Clone this repo. 
   ```bash
   git clone GITHUBURL YOUR_FOLDER_NAME
   ```
2) Get into the bumblebee folder. 
   ```bash
   cd YOUR_FOLDER_NAME/bumblebee
   ```
3) Run this command to install bumblebee's environment and run it!
   ```bash
   source setup.sh
   ```

NOTE: After initial installation, bumblebee will run automatically. If you close bumblebee and you want to run it again, go into the bumblebee folder and ensure that the bumblebee environment is activated. Otherwise, activate it by typing ```conda activate bumblebee-ai``` then type ```python main.py```. If the environment is already activated, you can type ```python main.py``` to run bumblebee.

## Features
- Stores and open zoom links on demand
- Opens up browser with Google search on any query specified
- Opens up browser with Youtube search on any query specified
- Searches for information on Wikipedia as well as Wolframalpha
- Does math using Wolframalpha
- Can send emails to any contact specified in a contacts database
- Works both in voice mode and silent mode(text only)
- Has a chatbot for generic conversations (uses chatterbot for this)
- Can clock me in and out of work (tracking how many hours I work my various work-study jobs)
- Research mode *
- TinyDB is the database used to store information such as contacts, zoom links, research data.

### Starred Features
1) Research mode: Research mode is a feature that I find super useful with my regular work flow. It is basically a mode that Bumblebee goes into where all the tabs I open in a google chrome 
browser and how long I spend on each tab are stored. The information is then stored in a file whose name Bumblebee requests before starting research mode. The file is stored in markdown. This feature makes conducting research easier since I will not have to worry about bookmarking certain pages or having to go through my whole history in order to find a site I visited weeks ago.
Research mode can be turned on/off on demand and so it doesn't store all the sites I visit all of the time.

## Contributing
Contributions are welcome, no matter how small or large. Please read this file to help you contribute to this project. Please see our [CONTRIBUTE.md](/CONTRIBUTING.md) to learn more about how to contribute.

## Troubleshooting
1. Bumblebee says "Listening..." but does not respond to wake-word? 
  - If on MacOS Terminal, you will have to make sure audio permissions are enabled through System Preferences and try again.
  - For VSCode, make sure that audio permissions are enabled for MacOS terminal through System Preferences, and then launch Bumblebee through MacOS Terminal app. See [here](https://github.com/microsoft/vscode/issues/95062#issuecomment-625553211) for detailed steps.
