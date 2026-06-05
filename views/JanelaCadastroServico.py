import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox

from control.ServicoController import ServicoController


class JanelaCadastroServico(tk.Toplevel):
    def __init__(self, master=None, servico=None):
        super().__init__(master)
        self.servico = servico
        self.title("Editar Servico" if servico else "Novo Servico")
        self.geometry("380x240")
        self.resizable(False, False)

        self.controller = ServicoController()

        tk.Label(self, text="Editar Servico" if servico else "Novo Servico",
                 font=("Helvetica", 15, "bold")).pack(pady=10)

        self.criar_widgets()

        if self.servico:
            self.preencher_campos()

    def criar_widgets(self):
        frame = tk.Frame(self, padx=20)
        frame.pack(fill="x")

        # Tipo
        tk.Label(frame, text="Tipo:").grid(row=0, column=0, sticky="w", pady=5)
        tipos = self.controller.tipos_disponiveis()
        self.cb_tipo = ttk.Combobox(frame, values=tipos, state="readonly", width=28)
        self.cb_tipo.current(0)
        self.cb_tipo.grid(row=0, column=1, pady=5, sticky="ew")

        # Preco
        tk.Label(frame, text="Preco (R$):").grid(row=1, column=0, sticky="w", pady=5)
        self.txt_preco = tk.Entry(frame, width=30)
        self.txt_preco.grid(row=1, column=1, pady=5, sticky="ew")

        frame.columnconfigure(1, weight=1)

        # Botoes
        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=20, pady=15)

        btn_text   = "Atualizar" if self.servico else "Salvar"
        btn_action = self.solicitar_atualizacao if self.servico else self.solicitar_cadastro
        tk.Button(frame_botoes, text=btn_text, width=12,
                  command=btn_action).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Fechar", width=10,
                  command=self.destroy).pack(side="right", padx=5)

    def preencher_campos(self):
        self.cb_tipo.set(type(self.servico).__name__.lower())
        self.cb_tipo.configure(state="disabled")  # tipo nao pode mudar na edicao
        self.txt_preco.insert(0, f"{self.servico.preco:.2f}".replace(".", ","))

    def solicitar_cadastro(self):
        sucesso, msg = self.controller.salvar_servico(
            tipo      = self.cb_tipo.get(),
            preco_str = self.txt_preco.get()
        )
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)

    def solicitar_atualizacao(self):
        sucesso, msg = self.controller.atualizar_servico(
            id_servico = self.servico.id,
            preco_str  = self.txt_preco.get()
        )
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)