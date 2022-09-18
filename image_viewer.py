# image_viewer.py
import io
import os
import random
import string

import PySimpleGUI as sg
from PIL import Image

import importer
import storage

example_file = "/home/regen/psrc/tmp/PXL_20211112_220502078.jpg"

file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]

sg.ChangeLookAndFeel('Dark')


def main():
    settings = storage.init()
    layout = [
        [sg.Image(key="-IMAGE-"),
         sg.Text('', size=(20, None), k='-C1-'),
         sg.Text('', k='-C2-')],
        [
            # sg.Radio('Permission Granted', "RADIO1", default=False)
            sg.Text("Image File To Import"),
            sg.Input(size=(24, 1), key="-FILE-", default_text=example_file), # FolderBrowse i framtiden
            sg.FileBrowse(file_types=file_types),
            sg.Button("Show Image"),
            sg.Button("Analyse Image"),
            sg.Button("Import Image"),
        ],
    ]
    window = sg.Window("Image Viewer", layout)
    while True:
        event, values = window.read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "Show Image":
            filename = values["-FILE-"]
            if os.path.exists(filename):
                image = Image.open(values["-FILE-"])
                image.thumbnail((400, 400))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-IMAGE-"].update(data=bio.getvalue())
        elif event == "Analyse Image":
            window['-C1-'].update('')
            window['-C2-'].update('')
            info_dict = storage.analysis(values["-FILE-"])
            l1 = ''
            l2 = ''
            for key, value in info_dict.items():
                if type(value) is dict and value is not {}:
                    l1 += key + '\n'
                    l2 += '\n'
                    for deeper_key, deeper_value in value.items():
                        l1 += '   ' + deeper_key + '\n'
                        l2 += '   ' + str(deeper_value) + '\n'
                else:
                    l1 += key + '\n'
                    l2 += str(value) + '\n'
            window['-C1-'].update(l1)
            window['-C2-'].update(l2)
        elif event == "Import Image":
            filename = values["-FILE-"]
            importer.single_file(filename, settings, True)

    window.close()


if __name__ == "__main__":
    main()
