"""INTERFAZ CIFRADO"""

import tkinter as tk
from tkinter import filedialog, messagebox
from functions.cifrado_simetrico import clave_desde_password, cifrar_archivo, descifrar_archivo


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
        # Entrada clave
        tk.Label(self.root, text="Ingrese su clave o contraseña:").pack()
        self.entry_clave = tk.Entry(self.root, width=40, show="*")
        self.entry_clave.pack(pady=5)
        # Mostrar salt generado
        tk.Label(self.root, text="Salt (automático):").pack()
        self.entry_salt = tk.Entry(self.root, width=40)
        self.entry_salt.pack(pady=5)

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

    def obtener_clave_derivada(self):
        """
        Metodo para generar clave del cifrado(se conecta con la funcion que hace el proceso)
        """
        password=self.entry_clave.get()
        
        if not password:
            messagebox.showerror("Error","Debe ingresar una clave primero.")
            return None
        #salt
        if not self.salt:
            self.salt= os.urandom(16)
            self.entry_salt.delete(0, tk.END)
            self.entry_salt.insert(0, self.salt.hex())
        return clave_desde_password(password,self.sal)


    def cifrar_ui(self):
        """
        Metodo para cifrar el archivo(se conecta con la funcion que hace el proceso)
        """
        if not self.archivo_seleccionado or not self.clave:
            messagebox.showerror("Error", "Selecciona archivo y genera clave primero.")
            return
        clave=self.obtener_clave_derivada()
        if not clave:
            return

        datos_cifrados = cifrar_archivo(self.archivo_seleccionado, self.clave)

        ruta_salida = filedialog.asksaveasfilename(
            title="Guardar archivo cifrado",
            defaultextension=".enc",
            filetypes=[("Encrypted", "*.enc"), ("Todos", "*.*")],
        )

        if ruta_salida:
            with open(ruta_salida, "wb") as f:
                f.write(self.salt + datos_cifrados) #guardaremos en salt el archivo
            messagebox.showinfo("Éxito", "Archivo cifrado guardado correctamente.")

    def descifrar_ui(self):
        """
        Metodo para descifrar el  archivo(se conecta con la funcion que hace el proceso)
        """
        if not self.archivo_seleccionado :
            messagebox.showerror("Error", "Selecciona archivo  primero.")
            return
        password=self.entry_clave.get()
        if not password:
            messagebox.showerror("Error","Ingrese la clave usada en el cifrado.")
            return
        #leer el salt desde el archivo cifrado
        with open(self.archivo_seleccionado,"rb") as f:
            contenido=f.read()
        salt=contenido[:16]
        datos=contenido[16:]
        try:
            clave_fernet = clave_desde_password(password, salt)
            datos_descifrados = Fernet(clave_fernet).decrypt(datos)
        except Exception:
            messagebox.showerror("Error", "Clave incorrecta o archivo corrupto.")
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
