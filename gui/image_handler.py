# image_handler.py
import io
import os
import PySimpleGUI as Gui
from PIL import Image

import importer
import storage

example_file = "/tmp/PXL_20211112_111050667.jpg"

file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]

Gui.ChangeLookAndFeel('Dark')


def main():
    settings = storage.init()
    layout = [
        [Gui.Image(key="-IMAGE-"),
         Gui.Text('', size=(20, None), k='-C1-'),
         Gui.Text('', k='-C2-')],
        [
            # Gui.Radio('Permission Granted', "RADIO1", default=False)
            Gui.Text("Image File To Import"),
            Gui.Input(size=(24, 1), key="-FILE-", default_text=example_file),
            Gui.FileBrowse(file_types=file_types, button_text='WHAAAT'),
            Gui.Button("Show Image"),
            Gui.Button("Analyse Image"),
            Gui.Button("Import Image"),
        ],
    ]
    window = Gui.Window("Image Viewer", layout)
    while True:
        event, values = window.read()

        if event == "Exit" or event == Gui.WIN_CLOSED:
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
