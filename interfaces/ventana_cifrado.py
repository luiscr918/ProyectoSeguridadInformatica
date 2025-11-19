"""interfaces/ventana_cifrado.py"""

import tkinter as tk
import os
from tkinter import filedialog, messagebox
from cryptography.fernet import InvalidToken
from functions.cifrado_simetrico import (
    clave_desde_password,
    cifrar_archivo,
    descifrar_archivo_bytes,
)


class VentanaCifrado:
    """
    Ventana para realizar cifrado y descifrado simétrico
    """

    def __init__(self):
        # Crear nueva ventana
        self.root = tk.Toplevel()
        self.root.title("Cifrado Simétrico")
        self.root.geometry("450x420")

        self.archivo_seleccionado = None

        titulo = tk.Label(self.root, text="Cifrado Simétrico", font=("Arial", 16))
        titulo.pack(pady=12)

        # BTN seleccionar archivo
        btn_sel = tk.Button(
            self.root, text="Seleccionar Archivo", command=self.seleccionar_archivo
        )
        btn_sel.pack(pady=8)

        # Entrada clave (contraseña que el usuario escribe)
        tk.Label(self.root, text="Ingrese su clave o contraseña:").pack()
        self.entry_clave = tk.Entry(self.root, width=40, show="*")
        self.entry_clave.pack(pady=5)

        # Botones
        btn_cifrar = tk.Button(self.root, text="Cifrar Archivo", command=self.cifrar_ui)
        btn_cifrar.pack(pady=10)

        btn_descifrar = tk.Button(
            self.root, text="Descifrar Archivo", command=self.descifrar_ui
        )
        btn_descifrar.pack(pady=6)

        # Botón para cerrar
        btn = tk.Button(self.root, text="Cerrar", command=self.root.destroy)
        btn.pack(pady=18)

    # metodos UI
    def seleccionar_archivo(self):
        """
        metodo para seleccionar archivos
        """
        ruta = filedialog.askopenfilename()
        if ruta:
            self.archivo_seleccionado = ruta
            messagebox.showinfo("Archivo", f"Archivo seleccionado:\n{ruta}")

    def cifrar_ui(self):
        """
        Método para cifrar archivos
        """
        if not self.archivo_seleccionado:
            messagebox.showerror("Error", "Seleccione un archivo primero.")
            return

        password = self.entry_clave.get()
        if not password:
            messagebox.showerror("Error", "Ingrese una contraseña.")
            return
        # Generar salt automáticamente
        salt = os.urandom(16)

        # Derivar clave Fernet desde password + salt
        clave_fernet = clave_desde_password(password, salt)
        try:
            datos_cifrados = cifrar_archivo(self.archivo_seleccionado, clave_fernet)
        except (OSError, ValueError) as e:
            messagebox.showerror("Error", f"Error cifrando archivo: {e}")
            return

        ruta_salida = filedialog.asksaveasfilename(
            title="Guardar archivo cifrado",
            defaultextension=".enc",
            filetypes=[("Encrypted", "*.enc"), ("Todos", "*.*")],
        )
        if ruta_salida:
            with open(ruta_salida, "wb") as f:
                f.write(salt + datos_cifrados)
            messagebox.showinfo(
                "Éxito",
                "Archivo cifrado correctamente.\n"
                "Recuerde su contraseña, la necesitará para descifrar.",
            )

    def descifrar_ui(self):
        """
        Método para descifrar archivos
        """
        if not self.archivo_seleccionado:
            messagebox.showerror("Error", "Seleccione un archivo cifrado primero.")
            return

        password = self.entry_clave.get()
        if not password:
            messagebox.showerror("Error", "Ingrese la clave usada en el cifrado.")
            return

        # Leer salt desde el archivo cifrado (primeros 16 bytes)
        try:
            with open(self.archivo_seleccionado, "rb") as f:
                contenido = f.read()
            if len(contenido) <= 16:
                raise ValueError("Archivo demasiado corto o no contiene salt/payload.")
            salt = contenido[:16]
            datos = contenido[16:]
        except (OSError, ValueError) as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")
            return

        # derivar clave y descifrar
        clave_fernet = clave_desde_password(password, salt)
        if not clave_fernet:
            return
        try:
            datos_descifrados = descifrar_archivo_bytes(datos, clave_fernet)
        except (InvalidToken, ValueError):
            messagebox.showerror(
                "Error",
                "No se pudo descifrar.\nContraseña incorrecta o archivo dañado.",
            )
            return

        ruta_salida = filedialog.asksaveasfilename(
            title="Guardar archivo descifrado",
            defaultextension=".dec",
            filetypes=[("Decrypted", "*.dec"), ("Todos", "*.*")],
        )
        if ruta_salida:
            with open(ruta_salida, "wb") as f:
                f.write(datos_descifrados)
            messagebox.showinfo("Éxito", "Archivo descifrado guardado correctamente.")
