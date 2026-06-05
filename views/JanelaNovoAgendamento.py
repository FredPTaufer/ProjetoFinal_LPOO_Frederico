import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

from control.AgendamentoController import AgendamentoController
from control.ProfissionalController import ProfissionalController
from control.ServicoController import ServicoController
from control.ClienteController import ClienteController


class JanelaNovoAgendamento(tk.Toplevel):
    def __init__(self, master=None, id_cliente: int = None):
        super().__init__(master)
        self.id_cliente = id_cliente
        self.title("Novo Agendamento")
        self.geometry("440x360")
        self.resizable(False, False)

        self.controller     = AgendamentoController()
        self.pro_controller = ProfissionalController()
        self.ser_controller = ServicoController()
        self.cli_controller = ClienteController()

        self._profissionais = []
        self._servicos      = []
        self._clientes      = []

        tk.Label(self, text="Novo Agendamento", font=("Helvetica", 15, "bold")).pack(pady=10)

        self.criar_widgets()
        self._carregar_combos()

    def criar_widgets(self):
        frame = tk.Frame(self, padx=20)
        frame.pack(fill="x")

        tk.Label(frame, text="Cliente:").grid(row=0, column=0, sticky="w", pady=5)
        self.cb_cliente = ttk.Combobox(frame, state="readonly", width=30)
        self.cb_cliente.grid(row=0, column=1, pady=5, sticky="ew")

        tk.Label(frame, text="Serviço:").grid(row=1, column=0, sticky="w", pady=5)
        self.cb_servico = ttk.Combobox(frame, state="readonly", width=30)
        self.cb_servico.grid(row=1, column=1, pady=5, sticky="ew")

        tk.Label(frame, text="Profissional:").grid(row=2, column=0, sticky="w", pady=5)
        self.cb_profissional = ttk.Combobox(frame, state="readonly", width=30)
        self.cb_profissional.grid(row=2, column=1, pady=5, sticky="ew")

        tk.Label(frame, text="Data:").grid(row=3, column=0, sticky="w", pady=5)
        self.cal_data = DateEntry(frame, width=20, date_pattern="dd/mm/yyyy")
        self.cal_data.grid(row=3, column=1, pady=5, sticky="w")

        tk.Label(frame, text="Hora (HH:MM):").grid(row=4, column=0, sticky="w", pady=5)
        self.txt_hora = tk.Entry(frame, width=10)
        self.txt_hora.insert(0, "09:00")
        self.txt_hora.grid(row=4, column=1, pady=5, sticky="w")

        frame.columnconfigure(1, weight=1)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=20, pady=15)
        tk.Button(frame_botoes, text="Confirmar", width=12, command=self.solicitar_agendamento).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Fechar", width=10, command=self.destroy).pack(side="right", padx=5)

    def _carregar_combos(self):
        self._clientes = self.cli_controller.listar_clientes()
        self.cb_cliente["values"] = [f"{c.id} - {c.nome}" for c in self._clientes]
        if self.id_cliente:
            for i, c in enumerate(self._clientes):
                if c.id == self.id_cliente:
                    self.cb_cliente.current(i)
                    self.cb_cliente.configure(state="disabled")
                    break

        self._profissionais = self.pro_controller.buscar_disponiveis()
        self.cb_profissional["values"] = [f"{p.id} - {p.nome}" for p in self._profissionais]

        self._servicos = self.ser_controller.listar_servicos()
        self.cb_servico["values"] = [f"{s.id} - {s.nome}" for s in self._servicos]

    def solicitar_agendamento(self):
        if self.cb_cliente.current() == -1:
            messagebox.showwarning("Aviso", "Selecione um cliente.", parent=self)
            return
        if self.cb_profissional.current() == -1:
            messagebox.showwarning("Aviso", "Selecione um profissional.", parent=self)
            return
        if self.cb_servico.current() == -1:
            messagebox.showwarning("Aviso", "Selecione um serviço.", parent=self)
            return

        cliente = self._clientes[self.cb_cliente.current()]
        profissional = self._profissionais[self.cb_profissional.current()]
        servico = self._servicos[self.cb_servico.current()]
        data = self.cal_data.get_date().strftime("%d/%m/%Y")
        hora = self.txt_hora.get().strip()

        sucesso, msg = self.controller.criar_agendamento(
            id_cliente      = cliente.id,
            id_profissional = profissional.id,
            id_servico      = servico.id,
            data_hora_str   = f"{data} {hora}"
        )
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)