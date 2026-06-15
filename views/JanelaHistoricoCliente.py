import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox

from control.AgendamentoController import AgendamentoController
from control.ClienteController import ClienteController
from model.StatusAgendamento import StatusAgendamento


class JanelaHistoricoCliente(tk.Toplevel):
    def __init__(self, master=None, cliente=None):
        super().__init__(master)
        self.cliente    = cliente
        self.title("Meu Histórico")
        self.geometry("740x400")

        self.controller = AgendamentoController()

        self.criar_widgets()
        if self.cliente:
            self.carregar_historico()

    def criar_widgets(self):
        tk.Label(self, text="Histórico de Atendimentos", font=("Arial", 16, "bold")).pack(pady=10)

        if self.cliente:
            tk.Label(self, text=f"Cliente: {self.cliente.nome} ({self.cliente.cpf})", font=("Arial", 9), fg="gray").pack()

        self.lbl_total = tk.Label(self, text="", fg="#2e7d32", font=("Arial", 10, "bold"))
        self.lbl_total.pack(anchor="e", padx=25)

        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=20, pady=5)

        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side="right", fill="y")

        colunas = ("Profissional", "Serviço", "Data/Hora", "Valor")
        self.tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", yscrollcommand=scrollbar.set)
        larguras = {"Profissional": 190, "Serviço": 160, "Data/Hora": 140, "Valor": 110}
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=larguras[col])

        self.tree.pack(expand=True, fill="both")
        scrollbar.config(command=self.tree.yview)

        tk.Button(self, text="Fechar", width=10, command=self.destroy).pack(pady=8)

    def carregar_historico(self):
        """Carrega o histórico de atendimentos do cliente e exibe na tabela"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        todos = self.controller.buscar_por_cliente(self.cliente.id)
        historico = [a for a in todos if a.status == StatusAgendamento.CONCLUIDO]

        total = 0.0
        for a in historico:
            valor  = a.calcularValor()
            total += valor
            self.tree.insert("", "end", iid=str(a.id), values=(
                a.profissional.nome,
                a.servico.nome,
                a.data_hora.strftime("%d/%m/%Y %H:%M"),
                f"R$ {valor:.2f}".replace(".", ",")
            ))

        self.lbl_total.config(text=f"Total gasto: R$ {total:.2f}".replace(".", ","))