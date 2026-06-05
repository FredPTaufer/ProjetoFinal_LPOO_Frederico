import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox

from control.ServicoController import ServicoController
from views.JanelaCadastroServico import JanelaCadastroServico


class JanelaListagemServicos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Servicos")
        self.geometry("620x380")

        self.controller = ServicoController()

        self.criar_widgets()
        self.carregar_dados()

    def criar_widgets(self):
        tk.Label(self, text="Gerenciamento de Servicos",
                 font=("Helvetica", 16, "bold")).pack(pady=10)

        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=20, pady=5)

        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side="right", fill="y")

        colunas = ("ID", "Nome", "Tipo", "Duracao (min)", "Preco (R$)")
        self.tree = ttk.Treeview(frame_tree, columns=colunas,
                                  show="headings", yscrollcommand=scrollbar.set)
        larguras = {"ID": 40, "Nome": 150, "Tipo": 130,
                    "Duracao (min)": 100, "Preco (R$)": 100}
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=larguras[col])

        self.tree.pack(expand=True, fill="both")
        scrollbar.config(command=self.tree.yview)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=20, pady=5)

        tk.Button(frame_botoes, text="Novo",    width=10,
                  command=self.abrir_novo).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Editar",  width=10,
                  command=self.abrir_editar).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Remover", width=10,
                  command=self.remover).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Fechar",  width=10,
                  command=self.destroy).pack(side="right", padx=5)

    def carregar_dados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for s in self.controller.listar_servicos():
            self.tree.insert("", "end", iid=str(s.id), values=(
                s.id, s.nome, type(s).__name__,
                s.duracao,
                f"R$ {s.preco:.2f}".replace(".", ",")
            ))

    def abrir_novo(self):
        janela = JanelaCadastroServico(self)
        self.wait_window(janela)
        self.carregar_dados()

    def abrir_editar(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um servico para editar.", parent=self)
            return
        id_ser = int(self.tree.item(selecionado[0])["values"][0])
        servico = self.controller.buscar_por_id(id_ser)
        if not servico:
            messagebox.showerror("Erro", "Servico nao encontrado.", parent=self)
            return

        janela = JanelaCadastroServico(self, servico=servico)
        self.wait_window(janela)
        self.carregar_dados()

    def remover(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um servico para remover.", parent=self)
            return
        id_ser = int(self.tree.item(selecionado[0])["values"][0])
        nome   = self.tree.item(selecionado[0])["values"][1]
        if messagebox.askyesno("Confirmar", f"Remover servico '{nome}'?", parent=self):
            sucesso, msg = self.controller.remover_servico(id_ser)
            if sucesso:
                self.carregar_dados()
                messagebox.showinfo("Sucesso", msg, parent=self)
            else:
                messagebox.showerror("Erro", msg, parent=self)