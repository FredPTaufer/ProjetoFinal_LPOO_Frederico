import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox

from control.AgendamentoController import AgendamentoController
from control.ClienteController import ClienteController
from model.StatusAgendamento import StatusAgendamento


class JanelaHistoricoCliente(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Meu Historico")
        self.geometry("780x420")

        self.controller     = AgendamentoController()
        self.cli_controller = ClienteController()

        self.criar_widgets()

    def criar_widgets(self):
        tk.Label(self, text="Historico de Atendimentos",
                 font=("Helvetica", 16, "bold")).pack(pady=10)

        # Busca por CPF
        frame_busca = tk.Frame(self)
        frame_busca.pack(fill="x", padx=20, pady=4)
        tk.Label(frame_busca, text="Seu CPF:").pack(side="left")
        self.txt_cpf = tk.Entry(frame_busca, width=16)
        self.txt_cpf.pack(side="left", padx=8)
        tk.Button(frame_busca, text="Buscar",
                  command=self.carregar_historico).pack(side="left")

        # Label de total gasto
        self.lbl_total = tk.Label(self, text="", fg="#2e7d32",
                                   font=("Helvetica", 10, "bold"))
        self.lbl_total.pack(anchor="e", padx=25)

        # Treeview — apenas concluidos
        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=20, pady=5)

        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side="right", fill="y")

        colunas = ("ID", "Profissional", "Servico", "Data/Hora", "Valor")
        self.tree = ttk.Treeview(frame_tree, columns=colunas,
                                  show="headings", yscrollcommand=scrollbar.set)
        larguras = {"ID": 40, "Profissional": 180, "Servico": 150,
                    "Data/Hora": 140, "Valor": 100}
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=larguras[col])

        self.tree.pack(expand=True, fill="both")
        scrollbar.config(command=self.tree.yview)

        tk.Button(self, text="Fechar", width=10,
                  command=self.destroy).pack(pady=8)

    def carregar_historico(self):
        cpf = self.txt_cpf.get().strip()
        if not cpf:
            messagebox.showwarning("Aviso", "Informe seu CPF.", parent=self)
            return

        cliente = self.cli_controller.buscar_por_cpf(cpf)
        if not cliente:
            messagebox.showwarning("Aviso", "Cliente nao encontrado.", parent=self)
            return

        todos = self.controller.buscar_por_cliente(cliente.id)
        # Historico = apenas concluidos
        historico = [a for a in todos if a.status == StatusAgendamento.CONCLUIDO]

        for row in self.tree.get_children():
            self.tree.delete(row)

        total = 0.0
        for a in historico:
            valor = a.calcularValor()
            total += valor
            self.tree.insert("", "end", iid=str(a.id), values=(
                a.id,
                a.profissional.nome,
                a.servico.nome,
                a.data_hora.strftime("%d/%m/%Y %H:%M"),
                f"R$ {valor:.2f}".replace(".", ",")
            ))

        self.lbl_total.config(
            text=f"Total gasto: R$ {total:.2f}".replace(".", ",")
        )