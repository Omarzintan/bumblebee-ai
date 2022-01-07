# bumblebee-ai
Virtual Assistant in Python

## About
Bumblebee is a voice assistant that was made with the intention of automating certain boring or otherwise tedious tasks on the computer. Bumblebee was also made with the goal of being easily extendible. Bumblebee has two approached to inferring the intent of commands, namely a neural-network-based approach and a rule-based approach. 
* The neural-network-based approach works with a Deep Neural Network that is trained on the input patterns of the all features (skills) that the assistant can perform. This trained Deep Neural Network is then used to infer which feature a user wants to run based on their input.
* The rule-based approach basically examines the input text from a user to see if the input matches any of the input patterns of the features (skills).

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

NOTE: After initial installation, bumblebee will run automatically. If you close bumblebee and you want to run it again, you should be able to run `bumblebee` from your terminal to start it up since the installation automatically adds this `bumblebee` command to your path. If this still does not work you can go into the bumblebee folder and ensure that the bumblebee environment is activated. Otherwise, activate it by typing ```conda activate bumblebee-ai``` then type ```python main.py```.

## Contributing
Contributions are welcome, no matter how small or large. Please read this file to help you contribute to this project. Please see our [CONTRIBUTE.md](/CONTRIBUTING.md) to learn more about how to contribute.

## Troubleshooting
1. Bumblebee says "Listening..." but does not respond to wake-word? 
  - If on MacOS Terminal, you will have to make sure audio permissions are enabled through System Preferences and try again.
  - For VSCode, make sure that audio permissions are enabled for MacOS terminal through System Preferences, and then launch Bumblebee through MacOS Terminal app. See [here](https://github.com/microsoft/vscode/issues/95062#issuecomment-625553211) for detailed steps.
