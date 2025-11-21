"""Interfaz Home de la app"""

import tkinter as tk
from interfaces.ventana_cifrado import VentanaCifrado
from interfaces.ventana_keys import VentanaKeys


class VentanaHome:
    """
    Clase de la interfaz del home
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Seguridad Informática -Home")
        self.root.geometry("400x300")

        # Titulo
        titulo = tk.Label(root, text="Menú Principal", font=("Arial", 16))
        titulo.pack(pady=20)
        # Botón: Cifrado de documentos
        btn_cifrado = tk.Button(
            root, text="Cifrado Simétrico", width=20, command=self.abrir_cifrado
        )
        btn_cifrado.pack(pady=10)
        # Botón: Cifrado asimétrico (generar keys)
        btn_cifrado = tk.Button(
            root, text="Generar Keys", width=20, command=self.abrir_keys
        )
        btn_cifrado.pack(pady=10)


    # Metodos:
    def abrir_cifrado(self):
        """
        Metodo para abrir la ventana de cifrar archivos
        """
        VentanaCifrado()

    def abrir_keys(self):
        """
        Metodo para abrir la ventana keys
        """
        VentanaKeys()
 
