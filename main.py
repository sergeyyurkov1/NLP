import PySimpleGUI as sg

import handlers
import layout


def main():
    window = sg.Window(
        "PDF Renamer", layout.layout, resizable=False, finalize=False
    )  # finalize=True

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Quit"):
            break

        try:
            handlers.event_handlers[event](event=event, values=values, window=window)
        except KeyError:
            print(f"Cannot read '{event}'")

    window.close()


if __name__ == "__main__":
    main()
