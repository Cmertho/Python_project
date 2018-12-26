import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd


class Main(tk.Tk):
	def __init__(self, parent=None, text: pd.DataFrame = None):
		super().__init__(parent)
		self.text = text.columns.values
		self.parent = parent
		self.tree = ttk.Treeview(self.parent, columns=self.text[1:])
		self.vsb = tk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
		self.tree.configure(yscrollcommand=self.vsb.set)

		self.vsb.pack(side="right", fill="y")
		for i, j in enumerate(self.text):
			self.tree.heading(f"#{i}", text=j)
		for i in range(len(text[self.text[0]])):
			self.tree.insert('', 'end', text=text[self.text[0]][i], values=list(map(lambda x: text[x][i], self.text[1:])))

		self.tree.pack()


if __name__ == "__main__":
	data = pd.read_csv('1.csv')
	main = Main(text=data)
	main.mainloop()
