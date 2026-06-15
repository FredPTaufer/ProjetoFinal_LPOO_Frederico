import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox
from views.JanelaCadastroCliente import JanelaCadastroCliente
from control.ClienteController import ClienteController


class JanelaListagemClientes(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Clientes")
        self.geometry("680x430")

        self.controller = ClienteController()

        self.criar_widgets()
        self.carregar_dados()

    def criar_widgets(self):
        tk.Label(self, text="Gerenciamento de Clientes", font=("Arial", 16, "bold")).pack(pady=10)

        frame_busca = tk.Frame(self)
        frame_busca.pack(fill="x", padx=20, pady=4)
        tk.Label(frame_busca, text="Buscar por nome:").pack(side="left")
        self.txt_busca = tk.Entry(frame_busca, width=30)
        self.txt_busca.pack(side="left", padx=8)
        tk.Button(frame_busca, text="Buscar", command=self.filtrar_dados).pack(side="left")
        tk.Button(frame_busca, text="Limpar", command=self.carregar_dados).pack(side="left", padx=4)

        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=20, pady=5)

        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side="right", fill="y")

        colunas = ("Nome", "CPF", "Telefone", "Email")
        self.tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", yscrollcommand=scrollbar.set)
        larguras = {"Nome": 200, "CPF": 110, "Telefone": 120, "Email": 200}
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
        self.txt_busca.delete(0, tk.END)
        self._preencher_tree(self.controller.listar_clientes())

    def filtrar_dados(self):
        """Busca clientes por nome"""
        termo = self.txt_busca.get().strip().lower()
        todos = self.controller.listar_clientes()
        self._preencher_tree([c for c in todos if termo in c.nome.lower()] if termo else todos)

    def _preencher_tree(self, clientes):
        """Atualiza a treeview com a lista de clientes"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for c in clientes:
            self.tree.insert("", "end", iid=str(c.id), values=(
                c.nome, c.cpf, c.telefone, c.email
            ))

    def _id_selecionado(self):
        """Retorna o ID do cliente selecionado ou None se nada estiver selecionado"""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um cliente.", parent=self)
            return None
        return int(sel[0])

    def abrir_novo(self):
        janela = JanelaCadastroCliente(self)
        self.wait_window(janela)
        self.carregar_dados()

    def abrir_editar(self):
        id_cli = self._id_selecionado()
        if id_cli is None:
            return
        cliente = self.controller.buscar_por_id(id_cli)
        if not cliente:
            messagebox.showerror("Erro", "Cliente não encontrado.", parent=self)
            return
        
        janela = JanelaCadastroCliente(self, cliente=cliente)
        self.wait_window(janela)
        self.carregar_dados()

    def remover(self):
        id_cli = self._id_selecionado()
        if id_cli is None:
            return
        nome = self.tree.item(str(id_cli))["values"][0]
        if messagebox.askyesno("Confirmar", f"Remover cliente '{nome}'?", parent=self):
            sucesso, msg = self.controller.remover_cliente(id_cli)
            if sucesso:
                self.carregar_dados()
                messagebox.showinfo("Sucesso", msg, parent=self)
            else:
                messagebox.showerror("Erro", msg, parent=self)