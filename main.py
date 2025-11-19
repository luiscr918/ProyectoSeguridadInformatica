"""Este es el archivo main de la aplicacion"""

import tkinter as tk
from interfaces.ventana_home import VentanaHome

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaHome(root)
    root.mainloop()
