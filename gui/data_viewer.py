# importer.py
from pathlib import Path
import PySimpleGUI as Gui

Gui.ChangeLookAndFeel('Dark')
example_file = "/home/regen/psrc/tmp/1636715450000000000.png"


def make_window(p):
    image_layout = [[Gui.Image(p, expand_x=True, expand_y=True)]]
    info_layout = [[Gui.Text("Loads of coool info about the image")]]
    layout = [[Gui.TabGroup([[Gui.Tab('Preview', image_layout),
                              Gui.Tab('Info', info_layout)]],
                            key='-TAB GROUP-', expand_x=True, expand_y=True)]]

    window = Gui.Window("Image Viewer", layout, size=(600, 500))
    while True:
        event, values = window.read()

        if event == "Exit" or event == Gui.WIN_CLOSED:
            break

    window.close()


if __name__ == "__main__":
    make_window(example_file)
