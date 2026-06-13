import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox

from control.ClienteController import ClienteController


class JanelaCadastroCliente(tk.Toplevel):
    def __init__(self, master=None, cliente=None):
        super().__init__(master)
        self.cliente = cliente
        self.title("Editar Cliente" if cliente else "Novo Cliente")
        self.geometry("400x320")
        self.resizable(False, False)

        self.controller = ClienteController()

        tk.Label(self, text="Editar Cliente" if cliente else "Novo Cliente", font=("Arial", 15, "bold")).pack(pady=10)

        self.criar_widgets()

        if self.cliente:
            self.preencher_campos()

    def criar_widgets(self):
        frame = tk.Frame(self, padx=20)
        frame.pack(fill="x")

        tk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="w", pady=5)
        self.txt_nome = tk.Entry(frame, width=30)
        self.txt_nome.grid(row=0, column=1, pady=5, sticky="ew")

        tk.Label(frame, text="CPF (somente números):").grid(row=1, column=0, sticky="w", pady=5)
        self.txt_cpf = tk.Entry(frame, width=30)
        self.txt_cpf.grid(row=1, column=1, pady=5, sticky="ew")

        tk.Label(frame, text="Telefone:").grid(row=2, column=0, sticky="w", pady=5)
        self.txt_telefone = tk.Entry(frame, width=30)
        self.txt_telefone.grid(row=2, column=1, pady=5, sticky="ew")

        tk.Label(frame, text="Email:").grid(row=3, column=0, sticky="w", pady=5)
        self.txt_email = tk.Entry(frame, width=30)
        self.txt_email.grid(row=3, column=1, pady=5, sticky="ew")

        frame.columnconfigure(1, weight=1)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=20, pady=15)

        btn_text = "Atualizar" if self.cliente else "Salvar"
        btn_action = self.solicitar_atualizacao if self.cliente else self.solicitar_cadastro
        tk.Button(frame_botoes, text=btn_text, width=12, command=btn_action).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Fechar", width=10, command=self.destroy).pack(side="right", padx=5)

    def preencher_campos(self):
        self.txt_nome.insert(0, self.cliente.nome)
        self.txt_cpf.insert(0, self.cliente.cpf)
        self.txt_cpf.configure(state="disabled")
        self.txt_telefone.insert(0, self.cliente.telefone)
        self.txt_email.insert(0, self.cliente.email)

    def solicitar_cadastro(self):
        sucesso, msg = self.controller.salvar_cliente(
            nome = self.txt_nome.get(),
            cpf = self.txt_cpf.get(),
            telefone = self.txt_telefone.get(),
            email = self.txt_email.get()
        )
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)

    def solicitar_atualizacao(self):
        sucesso, msg = self.controller.atualizar_cliente(
            id_cliente = self.cliente.id,
            nome = self.txt_nome.get(),
            telefone = self.txt_telefone.get(),
            email = self.txt_email.get()
        )
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)