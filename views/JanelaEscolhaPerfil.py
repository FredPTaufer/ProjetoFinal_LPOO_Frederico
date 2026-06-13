import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk


class JanelaEscolhaPerfil(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Salão de Beleza")
        self.geometry("360x280")
        self.resizable(False, False)

        self._criar_widgets()

    def _criar_widgets(self):
        tk.Label(self, text="Salão de Beleza", font=("Arial", 20, "bold")).pack(pady=(30, 5))
        tk.Label(self, text="Selecione seu perfil para continuar", font=("Arial", 10), fg="gray").pack(pady=(0, 20))

        tk.Frame(self, height=1, bg="lightgray").pack(fill="x", padx=30, pady=5)

        tk.Button(self, text="Entrar como Administrador", font=("Arial", 11), width=26, height=2, bg="#4a90d9", fg="white", relief="flat", command=self._abrir_admin).pack(pady=10)
        tk.Button(self, text="Entrar como Cliente", font=("Arial", 11), width=26, height=2, bg="#5cb85c", fg="white", relief="flat", command=self._abrir_cliente).pack(pady=5)


    def _abrir_admin(self):
        from views.JanelaPrincipalAdmin import JanelaPrincipalAdmin
        self.destroy()
        app = JanelaPrincipalAdmin()
        app.mainloop()

    def _abrir_cliente(self):
        from views.JanelaLoginCliente import JanelaLoginCliente
        self.destroy()
        app = JanelaLoginCliente()
        app.mainloop()