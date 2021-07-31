import PySimpleGUI as sg

MAIN_LAYOUT =   [
                    [
                        sg.Output(size=(110, 20), font=('Helvetica 10'), key="-OUTPUT-")
                    ],
                    [
                        sg.Text("Send:"),
                        sg.In(size=(98, 1), enable_events=True, key="-INPUT-", focus=True),
                        sg.Button("SEND")
                    ]
                ]
