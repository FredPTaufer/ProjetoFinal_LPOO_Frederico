import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox

from control.ServicoController import ServicoController


class JanelaListagemServicos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Serviços")
        self.geometry("700x400")

        self.controller = ServicoController()

        self.criar_widgets()
        self.carregar_dados()

    def criar_widgets(self):
        tk.Label(self, text="Serviços Oferecidos", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self, text="Selecione um serviço e clique em Editar Preço para atualizar o valor.", font=("Arial", 9), fg="gray").pack()

        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=20, pady=8)

        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side="right", fill="y")

        colunas = ("Nome", "Duração (min)", "Preço (R$)")
        self.tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", yscrollcommand=scrollbar.set)
        larguras = {"Nome": 200, "Duração (min)": 120, "Preço (R$)": 120}
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=larguras[col])

        self.tree.pack(expand=True, fill="both")
        scrollbar.config(command=self.tree.yview)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=20, pady=8)
        tk.Button(frame_botoes, text="Editar Preço", width=14, command=self.editar_preco).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Fechar", width=10, command=self.destroy).pack(side="right", padx=5)

    def carregar_dados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for s in self.controller.listar_servicos():
            self.tree.insert("", "end", iid=str(s.id), values=(
                s.nome,
                f"{s.duracao} min",
                f"R$ {s.preco:.2f}".replace(".", ",")
            ))

    def editar_preco(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um serviço.", parent=self)
            return

        id_ser  = int(sel[0])
        servico = self.controller.buscar_por_id(id_ser)
        if not servico:
            messagebox.showerror("Erro", "Servico não encontrado.", parent=self)
            return

        janela = tk.Toplevel(self)
        janela.title(f"Editar Preço — {servico.nome}")
        janela.geometry("320x150")
        janela.resizable(False, False)

        tk.Label(janela, text=f"Servico: {servico.nome}", font=("Arial", 11, "bold")).pack(pady=(15, 5))

        frame = tk.Frame(janela, padx=20)
        frame.pack(fill="x")
        tk.Label(frame, text="Novo preço (R$):").pack(side="left")
        txt_preco = tk.Entry(frame, width=12)
        txt_preco.insert(0, f"{servico.preco:.2f}".replace(".", ","))
        txt_preco.pack(side="left", padx=8)

        def confirmar():
            sucesso, msg = self.controller.atualizar_servico(
                id_servico = id_ser,
                preco_str = txt_preco.get()
            )
            if sucesso:
                janela.destroy()
                self.carregar_dados()
                messagebox.showinfo("Sucesso", msg, parent=self)
            else:
                messagebox.showerror("Erro", msg, parent=janela)

        frame_btn = tk.Frame(janela)
        frame_btn.pack(pady=12)
        tk.Button(frame_btn, text="Salvar",  width=10, command=confirmar).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Cancelar",width=10, command=janela.destroy).pack(side="left", padx=5)