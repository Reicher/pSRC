# importer.py
from pathlib import Path
import PySimpleGUI as Gui
import importer
import storage
from gui import data_viewer

Gui.ChangeLookAndFeel('Dark')
example_file = "../tmp/PXL_20211112_111050667.jpg"

if __name__ == "__main__":
    settings = storage.init()

    path_layout = [Gui.Text('Path'),
                   Gui.Input(key="-FILE-", default_text=example_file),
                   Gui.FilesBrowse(button_text='File(s)'),
                   Gui.FolderBrowse(button_text='Folder')]
    analysis_layout = [Gui.Checkbox('Run all analysis', default=True)]
    confirm_layout = [Gui.Push(), Gui.Button("Import")]
    layout = [path_layout, analysis_layout, confirm_layout]

    window = Gui.Window("Import file or folder to storage", layout)
    while True:
        event, values = window.read()

        if event == "Exit" or event == Gui.WIN_CLOSED:
            break
        elif event == "Import":
            path = Path(values["-FILE-"])
            if path.is_file():
                importer.single_file(path, settings, True)
                data_viewer.make_window(path)
            elif path.is_dir():
                importer.all_in_folder(path, settings)
                Gui.popup("Imported all files in folder", keep_on_top=True)
            else:
                Gui.popup("Path is not a valid file or folder", keep_on_top=True)

    window.close()
