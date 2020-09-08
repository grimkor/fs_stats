# import tkinter
# import threading
#
# class MyTkApp(threading.Thread):
#     def __init__(self):
#         self.root=tkinter.Tk()
#         self.s = tkinter.StringVar()
#         self.s.set('Foo')
#         l = tkinter.Label(self.root,textvariable=self.s)
#         l.pack()
#         threading.Thread.__init__(self)
#
#     def run(self):
#         self.root.mainloop()

import tkinter as tk

from fs_stats import StateMachine


class Application(tk.Frame):
    def __init__(self):
        self.master = tk.Tk()
        super().__init__(self.master)
        self.create_widgets()
        self.backend = StateMachine(self)
        self.backend.start()
        self.grid_columnconfigure(2, pad=2)
        self.grid_rowconfigure(2, pad=2)
        self.pack()

    def create_widgets(self):
        self.status_title = tk.Label(self)
        self.status_title["text"] = "Status:"
        self.status_title.grid(row=0)
        # self.status_title.pack()

        self.status_message = tk.Entry(self, width=20, justify="center")
        self.status_message.insert(0, 'Pending')
        self.status_message.grid(row=0, column=1)
        # self.hi_there.pack()

        self.opponent_title = tk.Label(self, justify="center")
        self.opponent_title["text"] = "Opponent"
        self.opponent_title.grid(row=2, column=0)
        # self.opponent_title.pack()

        self.opponent_name = tk.Entry(self, width=20, justify="center")
        self.opponent_name.insert(1, 'Pending')
        self.opponent_name["state"] = "disabled"
        self.opponent_name.grid(row=2, column=1)

        self.opponent_rank = tk.Entry(self, width=10, justify="center")
        self.opponent_rank.insert(1, -1)
        self.opponent_rank["state"] = "disabled"
        self.opponent_rank.grid(row=2, column=2)

        # self.message = tk.Label(self)
        # self.message["text"] = 'Initial message'
        # self.message.grid(row=1)
        # self.message.pack()

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row=3, column=2)

    def update_status(self, text):
        self.status_message["state"] = "normal"
        self.status_message.delete(0, "end")
        self.status_message.insert(0, text)
        self.status_message["state"] = "disabled"

    def update_opponent_name(self, text):
        self.opponent_name["state"] = "normal"
        self.opponent_name.delete(0, "end")
        self.opponent_name.insert(0, text)
        self.opponent_name["state"] = "disabled"


app = Application()
app.mainloop()
