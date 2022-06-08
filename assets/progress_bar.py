from tkinter import *
from tkinter.ttk import Progressbar
import time

ws = Tk()
ws.title('PythonGuides')
ws.geometry('450x350')
ws.config(bg='#345')

pb3 = Progressbar(
    ws,
    orient = HORIZONTAL,
    length = 300,
    mode = 'determinate'
    )

pb3.place(x=80, y=140)
pb3.start()

ws.after(5000, lambda: ws.destroy())
ws.mainloop()