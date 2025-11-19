"""INTERFAZ CIFRADO"""

import tkinter as tk
from tkinter import filedialog, messagebox
from functions.cifrado_simetrico import generar_clave, cifrar_archivo, descifrar_archivo


class VentanaCifrado:
    """
    Ventana para realizar cifrado y descifrado simétrico
    """

    def __init__(self):
        # Crear nueva ventana
        self.root = tk.Toplevel()
        self.root.title("Cifrado Simétrico")
        self.root.geometry("400x400")

        self.archivo_seleccionado = None
        self.clave = None

        titulo = tk.Label(self.root, text="Cifrado Simétrico", font=("Arial", 16))
        titulo.pack(pady=20)

        # BTN seleccionar archivo
        btn_sel = tk.Button(
            self.root, text="Seleccionar Archivo", command=self.seleccionar_archivo
        )
        btn_sel.pack(pady=10)
        # Botón generar clave
        btn_clave = tk.Button(
            self.root, text="Generar Clave", command=self.generar_clave_ui
        )
        btn_clave.pack(pady=10)

        # Botón cifrar
        btn_cifrar = tk.Button(self.root, text="Cifrar Archivo", command=self.cifrar_ui)
        btn_cifrar.pack(pady=10)

        # Botón descifrar
        btn_descifrar = tk.Button(
            self.root, text="Descifrar Archivo", command=self.descifrar_ui
        )
        btn_descifrar.pack(pady=10)

        # Botón para cerrar
        btn = tk.Button(self.root, text="Cerrar", command=self.root.destroy)
        btn.pack(pady=20)

    # metodos UI
    def seleccionar_archivo(self):
        """
        Metodo para abrir archivo(se conecta con la funcion que hace el proceso)
        """
        ruta = filedialog.askopenfilename()
        if ruta:
            self.archivo_seleccionado = ruta
            messagebox.showinfo("Archivo", f"Archivo seleccionado:\n{ruta}")

    def generar_clave_ui(self):
        """
        Metodo para generar clave del cifrado(se conecta con la funcion que hace el proceso)
        """
        self.clave = generar_clave()
        messagebox.showinfo("Clave generada", "Se generó una nueva clave Fernet.")

    def cifrar_ui(self):
        """
        Metodo para cifrar el archivo(se conecta con la funcion que hace el proceso)
        """
        if not self.archivo_seleccionado or not self.clave:
            messagebox.showerror("Error", "Selecciona archivo y genera clave primero.")
            return

        datos_cifrados = cifrar_archivo(self.archivo_seleccionado, self.clave)

        ruta_salida = filedialog.asksaveasfilename(
            title="Guardar archivo cifrado",
            defaultextension=".enc",
            filetypes=[("Encrypted", "*.enc"), ("Todos", "*.*")],
        )

        if ruta_salida:
            with open(ruta_salida, "wb") as f:
                f.write(datos_cifrados)
            messagebox.showinfo("Éxito", "Archivo cifrado guardado correctamente.")

    def descifrar_ui(self):
        """
        Metodo para descifrar el  archivo(se conecta con la funcion que hace el proceso)
        """
        if not self.archivo_seleccionado or not self.clave:
            messagebox.showerror("Error", "Selecciona archivo y genera clave primero.")
            return

        try:
            datos_descifrados = descifrar_archivo(self.archivo_seleccionado, self.clave)
        except Exception:
            messagebox.showerror("Error", "No se pudo descifrar. ¿Clave incorrecta?")
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
