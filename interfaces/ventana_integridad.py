import tkinter as tk
from tkinter import filedialog, messagebox

from functions.hash_integridad import hash_sha256, hash_md5, comparar_hashes

class VentanaIntegridad:

    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Verificación de Integridad")
        self.root.geometry("400x380")

        self.original = None
        self.copia = None

        tk.Label(self.root, text="Verificación de Integridad", font=("Arial", 16)).pack(pady=20)

        tk.Button(self.root, text="Seleccionar Archivo Original", command=self.sel_original).pack(pady=10)
        tk.Button(self.root, text="Seleccionar Archivo Copia", command=self.sel_copia).pack(pady=10)
        tk.Button(self.root, text="Verificar", command=self.verificar).pack(pady=20)

    def sel_original(self):
        ruta = filedialog.askopenfilename()
        if ruta:
            self.original = ruta
            messagebox.showinfo("Archivo", f"Original:\n{ruta}")

    def sel_copia(self):
        ruta = filedialog.askopenfilename()
        if ruta:
            self.copia = ruta
            messagebox.showinfo("Archivo", f"Copia:\n{ruta}")

    def verificar(self):
        if not self.original or not self.copia:
            messagebox.showerror("Error", "Selecciona ambos archivos.")
            return

        sha_orig = hash_sha256(self.original)
        sha_copia = hash_sha256(self.copia)
        md5_orig = hash_md5(self.original)
        md5_copia = hash_md5(self.copia)

        resultado = comparar_hashes(self.original, self.copia)

        mensaje = (
            f"SHA-256 Original: {sha_orig}\n"
            f"SHA-256 Copia:    {sha_copia}\n\n"
            f"MD5 Original:     {md5_orig}\n"
            f"MD5 Copia:        {md5_copia}\n\n"
            f"Resultado: {'SIN ALTERACIONES' if resultado else 'ALTERADO'}"
        )

        messagebox.showinfo("Resultado Integridad", mensaje)
