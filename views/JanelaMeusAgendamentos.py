import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox

from control.AgendamentoController import AgendamentoController
from control.ClienteController import ClienteController
from model.StatusAgendamento import StatusAgendamento


class JanelaMeusAgendamentos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Meus Agendamentos")
        self.geometry("780x430")

        self.controller     = AgendamentoController()
        self.cli_controller = ClienteController()
        self._id_cliente    = None

        self.criar_widgets()

    def criar_widgets(self):
        tk.Label(self, text="Meus Agendamentos",
                 font=("Helvetica", 16, "bold")).pack(pady=10)

        # Busca por CPF
        frame_busca = tk.Frame(self)
        frame_busca.pack(fill="x", padx=20, pady=4)
        tk.Label(frame_busca, text="Seu CPF:").pack(side="left")
        self.txt_cpf = tk.Entry(frame_busca, width=16)
        self.txt_cpf.pack(side="left", padx=8)
        tk.Button(frame_busca, text="Buscar",
                  command=self.buscar_por_cpf).pack(side="left")

        # Treeview
        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=20, pady=5)

        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side="right", fill="y")

        colunas = ("ID", "Profissional", "Servico", "Data/Hora", "Status", "Valor")
        self.tree = ttk.Treeview(frame_tree, columns=colunas,
                                  show="headings", yscrollcommand=scrollbar.set)
        larguras = {"ID": 40, "Profissional": 160, "Servico": 130,
                    "Data/Hora": 130, "Status": 90, "Valor": 90}
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=larguras[col])

        self.tree.pack(expand=True, fill="both")
        scrollbar.config(command=self.tree.yview)

        # Botoes
        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=20, pady=5)

        tk.Button(frame_botoes, text="Cancelar Reserva", width=16,
                  command=self.cancelar_agendamento).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Fechar", width=10,
                  command=self.destroy).pack(side="right", padx=5)

    def buscar_por_cpf(self):
        cpf = self.txt_cpf.get().strip()
        if not cpf:
            messagebox.showwarning("Aviso", "Informe seu CPF.", parent=self)
            return

        cliente = self.cli_controller.buscar_por_cpf(cpf)
        if not cliente:
            messagebox.showwarning("Aviso", "Cliente nao encontrado.", parent=self)
            return

        self._id_cliente = cliente.id
        agendamentos = self.controller.buscar_por_cliente(cliente.id)

        for row in self.tree.get_children():
            self.tree.delete(row)

        for a in agendamentos:
            self.tree.insert("", "end", iid=str(a.id), values=(
                a.id,
                a.profissional.nome,
                a.servico.nome,
                a.data_hora.strftime("%d/%m/%Y %H:%M"),
                a.status.value.capitalize(),
                f"R$ {a.calcularValor():.2f}".replace(".", ",")
            ))

    def cancelar_agendamento(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um agendamento.", parent=self)
            return

        id_age = int(self.tree.item(selecionado[0])["values"][0])
        status = self.tree.item(selecionado[0])["values"][4].lower()

        if status != StatusAgendamento.AGENDADO.value:
            messagebox.showerror("Erro",
                "Somente agendamentos com status 'agendado' podem ser cancelados.",
                parent=self)
            return

        if messagebox.askyesno("Confirmar", "Deseja cancelar este agendamento?", parent=self):
            sucesso, msg = self.controller.cancelar(id_age)
            if sucesso:
                self.buscar_por_cpf()
                messagebox.showinfo("Sucesso", msg, parent=self)
            else:
                messagebox.showerror("Erro", msg, parent=self)