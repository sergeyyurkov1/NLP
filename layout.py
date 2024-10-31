import os

import PySimpleGUI as sg

import functions

folder_icon = b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABnUlEQVQ4y8WSv2rUQRSFv7vZgJFFsQg2EkWb4AvEJ8hqKVilSmFn3iNvIAp21oIW9haihBRKiqwElMVsIJjNrprsOr/5dyzml3UhEQIWHhjmcpn7zblw4B9lJ8Xag9mlmQb3AJzX3tOX8Tngzg349q7t5xcfzpKGhOFHnjx+9qLTzW8wsmFTL2Gzk7Y2O/k9kCbtwUZbV+Zvo8Md3PALrjoiqsKSR9ljpAJpwOsNtlfXfRvoNU8Arr/NsVo0ry5z4dZN5hoGqEzYDChBOoKwS/vSq0XW3y5NAI/uN1cvLqzQur4MCpBGEEd1PQDfQ74HYR+LfeQOAOYAmgAmbly+dgfid5CHPIKqC74L8RDyGPIYy7+QQjFWa7ICsQ8SpB/IfcJSDVMAJUwJkYDMNOEPIBxA/gnuMyYPijXAI3lMse7FGnIKsIuqrxgRSeXOoYZUCI8pIKW/OHA7kD2YYcpAKgM5ABXk4qSsdJaDOMCsgTIYAlL5TQFTyUIZDmev0N/bnwqnylEBQS45UKnHx/lUlFvA3fo+jwR8ALb47/oNma38cuqiJ9AAAAAASUVORK5CYII="
file_icon = b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABU0lEQVQ4y52TzStEURiHn/ecc6XG54JSdlMkNhYWsiILS0lsJaUsLW2Mv8CfIDtr2VtbY4GUEvmIZnKbZsY977Uwt2HcyW1+dTZvt6fn9557BGB+aaNQKBR2ifkbgWR+cX13ubO1svz++niVTA1ArDHDg91UahHFsMxbKWycYsjze4muTsP64vT43v7hSf/A0FgdjQPQWAmco68nB+T+SFSqNUQgcIbN1bn8Z3RwvL22MAvcu8TACFgrpMVZ4aUYcn77BMDkxGgemAGOHIBXxRjBWZMKoCPA2h6qEUSRR2MF6GxUUMUaIUgBCNTnAcm3H2G5YQfgvccYIXAtDH7FoKq/AaqKlbrBj2trFVXfBPAea4SOIIsBeN9kkCwxsNkAqRWy7+B7Z00G3xVc2wZeMSI4S7sVYkSk5Z/4PyBWROqvox3A28PN2cjUwinQC9QyckKALxj4kv2auK0xAAAAAElFTkSuQmCC"

sg.theme("LightGrey1")

models = functions.get_models()

default_model = functions.read_yaml("config.yaml").get("model", None)
path = functions.read_yaml("config.yaml").get("path", "")


def get_treedata(path: str) -> sg.TreeData:
    treedata = sg.TreeData()

    def add_files_in_folder(parent: str, dirname: str):
        try:
            files = os.listdir(dirname)
        except FileNotFoundError:  # first run - no folder
            return

        for f in files:
            fullname = os.path.join(dirname, f)

            if os.path.isdir(fullname):
                treedata.Insert(parent, fullname, f, values=[], icon=folder_icon)

                add_files_in_folder(fullname, fullname)
            else:
                treedata.Insert(
                    parent,
                    fullname,
                    f,
                    values=[os.stat(fullname).st_size],
                    icon=file_icon,
                )

    add_files_in_folder("", path)

    return treedata


col1 = sg.Column(
    [
        [
            sg.Tree(
                data=get_treedata(path),
                headings=[
                    "Size",
                ],
                auto_size_columns=True,
                select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
                num_rows=20,
                col0_width=40,
                key="-TREE-",
                show_expanded=False,
                enable_events=True,
                expand_x=True,
                expand_y=True,
            ),
        ],
    ]
)

menu = sg.Menu(
    [
        ["File", ["Open file", "Open folder", "---", "Quit"]],
        ["Settings"],
    ]
)

col2 = sg.Column(
    [
        [sg.Multiline(size=(40, 21), key="-ML-")],
    ]
)

layout = [
    [
        [
            sg.Text("Select folder"),
            sg.InputText(key="-SF-", enable_events=True, default_text=path),
            sg.FolderBrowse(target="-SF-", key="-FB-"),
            sg.Push(),
            sg.Text("Select model"),
            sg.Combo(
                models, default_value=default_model, key="-MODEL-", enable_events=True
            ),
        ],
    ],
    [
        # menu,
        col1,
        col2,
    ],
    [
        [
            sg.Input(key="-RI-"),
            sg.Button("Summarize"),
            sg.Button("Rename"),
            sg.Push(),
            sg.Button("Summarize & Rename All"),
            sg.Button("Cancel"),
        ],
    ],
    [sg.StatusBar("...", key="-SB-")],
    [sg.ProgressBar(100, orientation="h", expand_x=True, size=(20, 20), key="-PROG-")],
]
