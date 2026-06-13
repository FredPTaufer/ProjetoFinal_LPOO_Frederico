import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox

from control.ProfissionalController import ProfissionalController
from views.JanelaCadastroProfissional import JanelaCadastroProfissional


class JanelaListagemProfissionais(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Profissionais")
        self.geometry("720x400")

        self.controller = ProfissionalController()

        self.criar_widgets()
        self.carregar_dados()

    def criar_widgets(self):
        tk.Label(self, text="Gerenciamento de Profissionais", font=("Arial", 16, "bold")).pack(pady=10)

        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=20, pady=5)

        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side="right", fill="y")

        colunas = ("Nome", "CPF", "Especialidades", "Disponível")
        self.tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", yscrollcommand=scrollbar.set)
        larguras = {"Nome": 180, "CPF": 110, "Especialidades": 260, "Disponível": 80}
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=larguras[col])

        self.tree.pack(expand=True, fill="both")
        scrollbar.config(command=self.tree.yview)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=20, pady=5)
        tk.Button(frame_botoes, text="Novo", width=10, command=self.abrir_novo).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Editar", width=10, command=self.abrir_editar).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Remover", width=10, command=self.remover).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Fechar", width=10, command=self.destroy).pack(side="right", padx=5)

    def carregar_dados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in self.controller.listar_profissionais():
            self.tree.insert("", "end", iid=str(p.id), values=(
                p.nome, p.cpf, p.especialidade,
                "Sim" if p.disponivel else "Nao"
            ))

    def _id_selecionado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um profissional.", parent=self)
            return None
        return int(sel[0])

    def abrir_novo(self):
        janela = JanelaCadastroProfissional(self)
        self.wait_window(janela)
        self.carregar_dados()

    def abrir_editar(self):
        id_pro = self._id_selecionado()
        if id_pro is None:
            return
        profissional = self.controller.buscar_por_id(id_pro)
        if not profissional:
            messagebox.showerror("Erro", "Profissional não encontrado.", parent=self)
            return
        
        janela = JanelaCadastroProfissional(self, profissional=profissional)
        self.wait_window(janela)
        self.carregar_dados()

    def remover(self):
        id_pro = self._id_selecionado()
        if id_pro is None:
            return
        nome = self.tree.item(str(id_pro))["values"][0]
        if messagebox.askyesno("Confirmar", f"Remover profissional '{nome}'?", parent=self):
            sucesso, msg = self.controller.remover_profissional(id_pro)
            if sucesso:
                self.carregar_dados()
                messagebox.showinfo("Sucesso", msg, parent=self)
            else:
                messagebox.showerror("Erro", msg, parent=self)