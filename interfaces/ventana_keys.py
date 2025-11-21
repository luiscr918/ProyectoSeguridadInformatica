import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

from functions.cifrado_asimetrico import (
    generar_claves_pgp,
    guardar_clave_publica,
    guardar_clave_privada,
)

class VentanaKeys:

    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Cifrado Asimétrico RSA")
        self.root.geometry("400x300")

        self.private_key = None
        self.public_key = None
        self.archivo = None

        tk.Label(self.root, text="Cifrado Asimétrico RSA", font=("Arial", 16)).pack(pady=10) 
        tk.Button(self.root, text="Generar Claves RSA desde frase", command=self.generar_claves).pack(pady=10)

        # NUEVOS BOTONES QUE FALTABAN
        tk.Button(self.root, text="Guardar Clave Privada", command=self.guardar_privada).pack(pady=10)
        tk.Button(self.root, text="Guardar Clave Pública", command=self.guardar_publica).pack(pady=10)

       
        tk.Button(self.root, text="Cerrar", command=self.root.destroy).pack(pady=20)

    def seleccionar_archivo(self):
        ruta = filedialog.askopenfilename()
        if ruta:
            self.archivo = ruta
            messagebox.showinfo("Archivo", f"Archivo seleccionado:\n{ruta}")

    def generar_claves(self):
        nombre = simpledialog.askstring("Nombre", "Ingresa tu nombre:")
        correo = simpledialog.askstring("Correo", "Ingresa tu correo:")
        passphrase = simpledialog.askstring("Passphrase", "Crea una passphrase:", show="*")

        if not nombre or not correo or not passphrase:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            self.fingerprint = generar_claves_pgp(nombre, correo, passphrase)
            self.passphrase = passphrase
            messagebox.showinfo("Éxito", "Claves PGP generadas correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # NUEVOS MÉTODOS: GUARDAR CLAVES
    def guardar_privada(self):
        if not hasattr(self, "fingerprint"):
            messagebox.showerror("Error", "Primero genera las claves.")
            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".asc",
            filetypes=[("PGP Private Key", "*.asc"), ("Todos", "*.*")]
        )
        if ruta:
            guardar_clave_privada(self.fingerprint, ruta, self.passphrase)
            messagebox.showinfo("Éxito", f"Clave privada guardada en:\n{ruta}")

    def guardar_publica(self):
        if not hasattr(self, "fingerprint"):
            messagebox.showerror("Error", "Primero genera las claves.")
            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".asc",
            filetypes=[("PGP Public Key", "*.asc"), ("Todos", "*.*")]
        )
        if ruta:
            guardar_clave_publica(self.fingerprint, ruta)
            messagebox.showinfo("Éxito", f"Clave pública guardada en:\n{ruta}")


