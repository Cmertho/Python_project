try:
    import Tkinter as tk
except ModuleNotFoundError:
    import tkinter as tk


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.hours, self.minutes, self.second = 2, 0, 0
        self.label = tk.Label(text="Прошло времени: %02d : %02d : %02d" % (self.hours, self.minutes, self.second))
        self.label.pack()

        button_start = tk.Button(text="Нажать чтобы начать отсчет", command=self.start).pack()
        button_stop = tk.Button(text="Остановить отсчет", command=self.stop).pack()

    def start(self):
        if self.second == 0:
            if self.minutes == 0:
                if self.hours == 0:
                    self.label.config(text='СТОП!')
                    self.stop()
                else:
                    self.hours -= 1
                    self.minutes = 59
                    self.second = 59
            else:
                self.minutes -= 1
                self.second = 59
        else:
            self.second -= 1
        if self.label["text"] == "СТОП!":
            self.stop()
        else:
            self.label.config(text="Прошло времени: %02d : %02d : %02d" % (self.hours, self.minutes, self.second))
            self.time = self.after(1000, self.start)

    def stop(self):
        if self.time is not None:
            self.after_cancel(self.time)
            self.time = None


if __name__ == "__main__":
    main = Main()
    main.mainloop()
