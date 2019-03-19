from tkinter import *


def addFlat():
    kom_kv.grid(row=1, column=0, sticky=W)
    kom_kv1.grid(row=1, column=1, sticky=W)

    sobs.grid(row=2, column=0, sticky=W)
    sobs1.grid(row=2, column=1, sticky=W)


def deleteFlat():
    kom_kv.grid_remove()
    kom_kv1.grid_remove()
    sobs.grid_remove()
    sobs1.grid_remove()


root = Tk()
root.title("Нумерация")

fr = Frame(root)
fr.grid()
kom_kv = Label(fr, text='Введите номер квартиры с несколькими собственниками:')
kom_kv.grid(row=1, column=0, sticky=W)
kom_kv1 = Entry(fr)
kom_kv1.grid(row=1, column=1, sticky=W)

sobs = Label(fr, text='Введите колличество собственников:')
sobs.grid(row=2, column=0, sticky=W)
sobs1 = Entry(fr)
sobs1.grid(row=2, column=1, sticky=W)

plus = Button(root, text='Добавить квартиру', command=addFlat)
plus.grid(row=10, column=1, sticky=W)

plus = Button(root, text='Удалить квартиру', command=deleteFlat)
plus.grid(row=10, column=2, sticky=W)

root.mainloop()
