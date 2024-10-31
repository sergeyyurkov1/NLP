import importlib
import os

import fitz
import PySimpleGUI as sg

import functions
import layout
from preprocessor import Preprocessor

path = functions.read_yaml("config.yaml").get("path", "")

pp = Preprocessor()


def _summarize(model: str, text: str) -> str:
    try:
        model = importlib.import_module(f"models.{model}.main")

        result = getattr(model, "default")(text)

        if len(result) > 0:
            r = result[0][0]

            r = pp.remove_punctuation(r)
            r = pp.remove_digits(r)
            r = r.replace(" ", "_").lower()
            r = r.replace("__", "_")

            return r
    except Exception as e:
        sg.Print(e)


def summarize_all(event, values, window):
    paths = [i for i in window["-TREE-"].TreeData.tree_dict if i != ""]

    window["-PROG-"].update(current_count=0, max=len(paths))

    for e, path in enumerate(paths):
        event, values = window.read(timeout=10)
        if event == "Cancel":
            window["-PROG-"].update(current_count=0, max=len(paths))
            window["-SB-"].update("Cancelled")

            break

        ext = path.split(".")[-1]
        text = ext_handler[ext](path)

        model_value = values["-MODEL-"]

        summary = _summarize(model_value, text)

        name = f"{summary}.{ext}"

        src = path
        src_dir = src.split("\\")[0]
        dst = os.path.join(src_dir, name)

        try:
            os.rename(src=src, dst=dst)
        except FileNotFoundError:  # no double renaming
            return
        except FileExistsError:
            pass

        folder_browse_handler(event, values, window)

        window["-PROG-"].update(current_count=e + 1, max=len(paths))

    window["-SB-"].update("Done")


def summarize(event, values, window):
    value = values["-ML-"]

    if value == "":
        return

    window["-SB-"].update("Summarizing...")  # ???

    model_value = values["-MODEL-"]

    summary = _summarize(model_value, value)

    ext = values["-RI-"].split(".")[-1]
    name = f"{summary}.{ext}"

    window["-RI-"].update(name)

    window["-SB-"].update("Done")


def read_pdf(path):
    doc = fitz.open(path)

    text = ""
    for page in doc:
        text += page.get_text()

    return text


def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def tree_handler(event, values, window):
    try:
        path: str = values[event][0]
    except IndexError:  # if nothing is selected
        return

    if not os.path.isfile(path):  # if folder
        return

    filename = path.split("\\")[-1]
    ext = path.split(".")[-1]

    res = ext_handler[ext](path)

    window["-ML-"].update(res)
    window["-RI-"].update(filename)


def folder_browse_handler(event, values, window):
    value = values["-SF-"]

    window["-TREE-"].update(layout.get_treedata(value))


def rename_handler(event, values, window):
    value = values["-RI-"]
    if value == "":
        return

    src = values["-TREE-"][0]
    src_dir = src.split("\\")[0]
    dst = os.path.join(src_dir, value)

    try:
        os.rename(src=src, dst=dst)
    except FileNotFoundError:  # no double renaming
        return

    window["-RI-"].update("")
    window["-TREE-"].update(layout.get_treedata(path))
    window["-SB-"].update("Done")


def model_handler(event, values, window):
    config = functions.read_yaml("config.yaml")

    model = values["-MODEL-"]

    config["model"] = model

    functions.write_yaml("config.yaml", config)


# Registering handlers
event_handlers = {
    "-SF-": folder_browse_handler,
    "-TREE-": tree_handler,
    "-MODEL-": model_handler,
    #
    "Rename": rename_handler,
    "Summarize": summarize,
    "Summarize & Rename All": summarize_all,
}
ext_handler = {
    "pdf": read_pdf,
    "txt": read_txt,
}
