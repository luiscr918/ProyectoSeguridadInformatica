import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

from functions.cifrado_asimetrico import (
    generar_claves_rsa,
    guardar_clave_publica,
    guardar_clave_privada,
    cargar_clave_publica,
    cargar_clave_privada,
    cifrar_archivo_rsa,
    descifrar_archivo_rsa
)

class VentanaKeys:

    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Cifrado Asimétrico RSA")
        self.root.geometry("400x420")

        self.private_key = None
        self.public_key = None
        self.archivo = None

        tk.Label(self.root, text="Cifrado Asimétrico RSA", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Seleccionar Archivo", command=self.seleccionar_archivo).pack(pady=10)
        tk.Button(self.root, text="Generar Claves RSA desde frase", command=self.generar_claves).pack(pady=10)
        tk.Button(self.root, text="Cargar Clave Privada", command=self.cargar_privada).pack(pady=10)
        tk.Button(self.root, text="Cargar Clave Pública", command=self.cargar_publica).pack(pady=10)
        tk.Button(self.root, text="Cifrar Archivo", command=self.cifrar).pack(pady=10)
        tk.Button(self.root, text="Descifrar Archivo", command=self.descifrar).pack(pady=10)
        tk.Button(self.root, text="Cerrar", command=self.root.destroy).pack(pady=20)

    def seleccionar_archivo(self):
        ruta = filedialog.askopenfilename()
        if ruta:
            self.archivo = ruta
            messagebox.showinfo("Archivo", f"Archivo seleccionado:\n{ruta}")

    def generar_claves(self):
        frase = simpledialog.askstring("Clave", "Escribe una frase para generar las claves:")
        if not frase:
            messagebox.showerror("Error", "Debes escribir una frase.")
            return

        self.private_key, self.public_key = generar_claves_rsa(frase)
        messagebox.showinfo("Éxito", "Claves generadas correctamente.")

    def cargar_privada(self):
        ruta = filedialog.askopenfilename()
        if ruta:
            self.private_key = cargar_clave_privada(ruta)
            messagebox.showinfo("Clave", "Clave privada cargada.")

    def cargar_publica(self):
        ruta = filedialog.askopenfilename()
        if ruta:
            self.public_key = cargar_clave_publica(ruta)
            messagebox.showinfo("Clave", "Clave pública cargada.")

    def cifrar(self):
        if not self.archivo or not self.public_key:
            messagebox.showerror("Error", "Selecciona archivo y clave pública.")
            return

        datos = cifrar_archivo_rsa(self.archivo, self.public_key)

        salida = filedialog.asksaveasfilename(defaultextension=".rsa")
        if salida:
            with open(salida, "wb") as f:
                f.write(datos)
            messagebox.showinfo("Éxito", "Archivo cifrado.")

    def descifrar(self):
        if not self.archivo or not self.private_key:
            messagebox.showerror("Error", "Selecciona archivo y clave privada.")
            return

        try:
            datos = descifrar_archivo_rsa(self.archivo, self.private_key)
        except:
            messagebox.showerror("Error", "No se pudo descifrar.")
            return

        salida = filedialog.asksaveasfilename(defaultextension=".dec")
        if salida:
            with open(salida, "wb") as f:
                f.write(datos)
            messagebox.showinfo("Éxito", "Archivo descifrado.")
