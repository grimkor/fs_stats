import tkinter as tk
from fs_stats import StateMachine


class Application(tk.Frame):
    def __init__(self):
        self.master = tk.Tk()
        super().__init__(self.master)
        self.backend = StateMachine(self)
        self.grid_columnconfigure(0, pad=5, minsize=70)
        self.create_widgets()
        self.backend.start()
        self.pack()

    def create_widgets(self):
        class RowCounter:
            def __init__(self):
                self.count = 0

            def __call__(self, *args, **kwargs):
                self.count += 1
                return self.count

        def make_row(label, val, row):
            self.__setattr__(f"{val}_label", tk.Label(self, justify="center"))
            self.__getattribute__(f"{val}_label")["text"] = label
            self.__getattribute__(f"{val}_label").grid(row=row, column=0)

            self.__setattr__(f"{val}_value", tk.Entry(self, justify="center"))
            self.__getattribute__(f"{val}_value").insert(1, '-')
            self.__getattribute__(f"{val}_value")["state"] = "disabled"
            self.__getattribute__(f"{val}_value").grid(row=row, column=1)

        next_row = RowCounter()

        self.status_title = tk.Label(self)
        self.status_title["text"] = "Status:"
        self.status_title.grid(row=0)

        self.status_message = tk.Entry(self, width=20, justify="center")
        self.status_message.insert(0, 'Pending')
        self.status_message.grid(row=0, column=1)

        self.status_title = tk.Label(self, font=("Helvetica", 14), text="My Stats", justify="center")
        self.status_title.grid(row=next_row(), padx=0, pady=5, column=0, columnspan=3)

        make_row("Rank", "my_rank", next_row())

        self.status_title = tk.Label(self, font=("Helvetica", 14), text="Last Match", justify="center")
        self.status_title.grid(row=next_row(), padx=0, pady=5, column=0, columnspan=3)

        for datapoint in ["name", "rank"]:
            make_row(datapoint.capitalize(), f"opp_{datapoint}", next_row())

        make_row("Score", "score", next_row())

        self.quit = tk.Button(self, text="HELLO", fg="green",
                              command=self.backend.hello_there)
        self.quit.grid(row=10, column=1)
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row=10, column=2)

    def update_status(self, text):
        self.status_message["state"] = "normal"
        self.status_message.delete(0, "end")
        self.status_message.insert(0, text)
        self.status_message["state"] = "disabled"

    def set_values(self, obj: dict):
        for key, value in obj.items():
            field = self.__getattribute__(f"{key}_value")
            field["state"] = "normal"
            field.delete(0, "end")
            field.insert(0, value)
            field["state"] = "disabled"


app = Application()
app.mainloop()
