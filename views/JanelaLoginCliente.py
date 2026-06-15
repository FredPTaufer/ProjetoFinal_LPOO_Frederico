import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox

from control.ClienteController import ClienteController


class JanelaLoginCliente(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Salão de Beleza - Acesso do Cliente")
        self.geometry("380x280")
        self.resizable(False, False)

        self.controller = ClienteController()
        self._criar_widgets()

    def _criar_widgets(self):
        tk.Label(self, text="Salão de Beleza", font=("Arial", 18, "bold")).pack(pady=(25, 4))
        tk.Label(self, text="Informe seu CPF para continuar", font=("Arial", 10), fg="gray").pack(pady=(0, 20))

        tk.Frame(self, height=1, bg="lightgray").pack(fill="x", padx=30, pady=5)

        frame = tk.Frame(self, padx=30)
        frame.pack(fill="x", pady=10)
        tk.Label(frame, text="CPF (somente números):").pack(anchor="w")
        self.txt_cpf = tk.Entry(frame, width=30, font=("Arial", 11))
        self.txt_cpf.pack(fill="x", pady=4)
        self.txt_cpf.bind("<Return>", lambda e: self._entrar())

        tk.Button(self, text="Entrar", font=("Arial", 11), width=20, height=1, bg="#5cb85c", fg="white", relief="flat", command=self._entrar).pack(pady=8)
        tk.Button(self, text="Não tenho cadastro — Registrar-me", font=("Arial", 9), fg="#4a90d9", relief="flat", cursor="hand2", command=self._registrar).pack()
        tk.Button(self, text="Voltar", font=("Arial", 9), fg="gray", relief="flat", cursor="hand2", command=self._voltar).pack(pady=4)

    def _entrar(self):
        """Tenta autenticar o cliente pelo CPF e abrir a janela principal do cliente"""
        cpf = self.txt_cpf.get().strip()
        if not cpf:
            messagebox.showwarning("Aviso", "Informe seu CPF.", parent=self)
            return

        cliente = self.controller.buscar_por_cpf(cpf)
        if not cliente:
            resposta = messagebox.askyesno(
                "CPF não encontrado",
                "Nenhum cliente encontrado com este CPF.\n\n"
                "Deseja se cadastrar agora?",
                parent=self
            )
            if resposta:
                self._registrar()
            return

        
        from views.JanelaPrincipalCliente import JanelaPrincipalCliente 
        self.destroy()
        app = JanelaPrincipalCliente(cliente=cliente)
        app.mainloop()

    def _registrar(self):
        """Abre uma janela para novo cadastro de cliente"""
        janela_cad = tk.Toplevel(self)
        janela_cad.title("Novo Cadastro")
        janela_cad.geometry("400x320")
        janela_cad.resizable(False, False)
        janela_cad.grab_set()

        tk.Label(janela_cad, text="Criar Conta", font=("Arial", 15, "bold")).pack(pady=10)

        frame = tk.Frame(janela_cad, padx=20)
        frame.pack(fill="x")

        tk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="w", pady=5)
        txt_nome = tk.Entry(frame, width=28)
        txt_nome.grid(row=0, column=1, pady=5, sticky="ew")

        tk.Label(frame, text="CPF (somente números):").grid(row=1, column=0, sticky="w", pady=5)
        txt_cpf = tk.Entry(frame, width=28)
        txt_cpf.insert(0, self.txt_cpf.get().strip())
        txt_cpf.grid(row=1, column=1, pady=5, sticky="ew")

        tk.Label(frame, text="Telefone:").grid(row=2, column=0, sticky="w", pady=5)
        txt_tel = tk.Entry(frame, width=28)
        txt_tel.grid(row=2, column=1, pady=5, sticky="ew")

        tk.Label(frame, text="Email:").grid(row=3, column=0, sticky="w", pady=5)
        txt_email = tk.Entry(frame, width=28)
        txt_email.grid(row=3, column=1, pady=5, sticky="ew")

        frame.columnconfigure(1, weight=1)

        def confirmar_cadastro():
            """Tenta cadastrar o cliente com os dados informados"""
            sucesso, msg = self.controller.salvar_cliente(
                nome = txt_nome.get(),
                cpf = txt_cpf.get(),
                telefone = txt_tel.get(),
                email = txt_email.get()
            )
            if sucesso:
                messagebox.showinfo("Sucesso", "Cadastro realizado! Faça o login.", parent=janela_cad)
                self.txt_cpf.delete(0, tk.END)
                self.txt_cpf.insert(0, txt_cpf.get().strip())
                janela_cad.destroy()
            else:
                messagebox.showerror("Erro", msg, parent=janela_cad)

        frame_btn = tk.Frame(janela_cad)
        frame_btn.pack(pady=12)
        tk.Button(frame_btn, text="Cadastrar", width=12, command=confirmar_cadastro).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Cancelar", width=10, command=janela_cad.destroy).pack(side="left", padx=5)

    def _voltar(self):
        from views.JanelaEscolhaPerfil import JanelaEscolhaPerfil
        self.destroy()
        app = JanelaEscolhaPerfil()
        app.mainloop()