from bee_creator import Bumblebee
import PySimpleGUI as sg

if __name__ == "__main__":

    print(sg.version)
    sg.theme('DarkAmber')
    layout = [[sg.Text("Pick a Wake Phrase")],
              [sg.Combo(['porcupine', 'grasshopper', 'jarvis', 'terminator',
                         'americano', 'alexa', 'blueberry', 'hey siri',
                        'hey google', 'computer', 'grapefruit', 'pico clock',
                         'bumblebee', 'picovoice', 'ok google'],
                        default_value='bumblebee',
                        key='wake_phrase')],
              [sg.Text("Pick your desired list of features")],
              [sg.Combo(['all', 'test', 'cybersecurity', 'geo'],
                        default_value='all',
                        key='feature_list_name')],
              [sg.Text(
                  "Enter the config file name (recommended to leave as is):"),
               sg.InputText(default_text="config", key="config_file")],
              [sg.Button("Run"), sg.Button("Cancel")]

              ]

    # Create the Window
    window = sg.Window("Bumblebee Main Menu", layout)
    # Event Loop to process "events" and get the "values of the inputs"
    ready_to_run = False
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        if event == "Run":
            ready_to_run = True
            wake_phrase = values['wake_phrase']
            feature_list_name = values['feature_list_name']
            config_file = values['config_file']
            window.close()
            break

    if ready_to_run:
        bee_runner = Bumblebee(
            name=wake_phrase, feature_list_name=feature_list_name,
            config_yaml_name=config_file)
        bee_runner.run_bee()
