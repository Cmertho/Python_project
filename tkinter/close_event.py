import tkinter as tk
import os
import random
import string


class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.close_event)
        self.anytime = "".join([random.choice(string.ascii_letters) for _ in range(4)]) + ".txt"
        self.watchdog()

    def watchdog(self):
        tmpfile = open(self.anytime, 'w')
        tmpfile.write(str(random.randint(1, 1000)))
        tmpfile.close()
        self.after(1000, self.watchdog)

    def close_event(self):
        try:
            os.remove(self.anytime)
        except FileNotFoundError:
            pass
        with open("config.txt", "w") as text:
            text.write(self.anytime)
        self.destroy()


if __name__ == "__main__":
    Main().mainloop()
