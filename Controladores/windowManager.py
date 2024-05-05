from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from Controladores.twitch import *
import asyncio

entry = False


def conectar_Twitch():
    
    Canal = entry.get()
    if (len(Canal) == 0):
        return messagebox.showinfo(message="Papi pero ponga su canal :v", title="Jaja pero que pendejou")
    asyncio.run(twitch_init("ne5hqtrbra01hx63nwexir2xsgtd9d","6a40qxlat8jdzumc4rw63b5gvsjhfg",Canal))


root = False
def window_Init():
    global root
    global entry
    root = Tk()
    root.title("Utilidades de twitch de ASH")
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm,text="Nombre de tu canal: ").grid(column=0, row=0)
    entry = ttk.Entry(frm)
    entry.grid(column=1, row=0)
    
    ttk.Button(frm, text="Conectar", command=conectar_Twitch).grid(column=2, row=0)
    twitchCheckSong(root)
    root.mainloop()

