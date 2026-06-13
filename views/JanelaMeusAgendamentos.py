import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox

from control.AgendamentoController import AgendamentoController
from model.StatusAgendamento import StatusAgendamento


class JanelaMeusAgendamentos(tk.Toplevel):
    def __init__(self, master=None, cliente=None):
        super().__init__(master)
        self.cliente = cliente
        self.title("Meus Agendamentos")
        self.geometry("740x400")

        self.controller = AgendamentoController()

        self.criar_widgets()
        if self.cliente:
            self.carregar_dados()

    def criar_widgets(self):
        tk.Label(self, text="Meus Agendamentos", font=("Arial", 16, "bold")).pack(pady=10)

        if self.cliente:
            tk.Label(self, text=f"Cliente: {self.cliente.nome} ({self.cliente.cpf})", font=("Arial", 9), fg="gray").pack()

        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=20, pady=5)

        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side="right", fill="y")

        colunas = ("Profissional", "Serviço", "Data/Hora", "Status", "Valor")
        self.tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", yscrollcommand=scrollbar.set)
        larguras = {"Profissional": 170, "Serviço": 140, "Data/Hora": 130, "Status": 90, "Valor": 100}
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=larguras[col])

        self.tree.pack(expand=True, fill="both")
        scrollbar.config(command=self.tree.yview)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=20, pady=5)

        tk.Button(frame_botoes, text="Cancelar Reserva", width=16, command=self.cancelar_agendamento).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Fechar", width=10, command=self.destroy).pack(side="right", padx=5)

    def carregar_dados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for a in self.controller.buscar_por_cliente(self.cliente.id):
            self.tree.insert("", "end", iid=str(a.id), values=(
                a.profissional.nome,
                a.servico.nome,
                a.data_hora.strftime("%d/%m/%Y %H:%M"),
                a.status.value.capitalize(),
                f"R$ {a.calcularValor():.2f}".replace(".", ",")
            ))

    def cancelar_agendamento(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um agendamento.", parent=self)
            return

        id_age = int(sel[0])
        status = self.tree.item(sel[0])["values"][3].lower()

        if status != StatusAgendamento.AGENDADO.value:
            messagebox.showerror("Erro",
                "Somente agendamentos com status 'Agendado' podem ser cancelados.",
                parent=self)
            return

        if messagebox.askyesno("Confirmar", "Deseja cancelar este agendamento?", parent=self):
            sucesso, msg = self.controller.cancelar(id_age)
            if sucesso:
                self.carregar_dados()
                messagebox.showinfo("Sucesso", msg, parent=self)
            else:
                messagebox.showerror("Erro", msg, parent=self)