import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

from control.AgendamentoController import AgendamentoController
from control.ClienteController import ClienteController
from control.ProfissionalController import ProfissionalController
from control.ServicoController import ServicoController


class JanelaCadastroAgendamento(tk.Toplevel):
    def __init__(self, master=None, agendamento=None):
        super().__init__(master)
        self.agendamento = agendamento
        self.title("Editar Agendamento" if agendamento else "Novo Agendamento")
        self.geometry("460x420")
        self.resizable(False, False)

        self.controller      = AgendamentoController()
        self.cli_controller  = ClienteController()
        self.pro_controller  = ProfissionalController()
        self.ser_controller  = ServicoController()

        self._clientes      = []
        self._profissionais = []
        self._servicos      = []

        tk.Label(self, text="Editar Agendamento" if agendamento else "Novo Agendamento",
                 font=("Helvetica", 15, "bold")).pack(pady=10)

        self.criar_widgets()
        self._carregar_combos()

        if self.agendamento:
            self.preencher_campos()

    def criar_widgets(self):
        frame = tk.Frame(self, padx=20)
        frame.pack(fill="x")

        # Cliente
        tk.Label(frame, text="Cliente:").grid(row=0, column=0, sticky="w", pady=5)
        self.cb_cliente = ttk.Combobox(frame, state="readonly", width=30)
        self.cb_cliente.grid(row=0, column=1, pady=5, sticky="ew")

        # Profissional
        tk.Label(frame, text="Profissional:").grid(row=1, column=0, sticky="w", pady=5)
        self.cb_profissional = ttk.Combobox(frame, state="readonly", width=30)
        self.cb_profissional.grid(row=1, column=1, pady=5, sticky="ew")

        # Servico
        tk.Label(frame, text="Servico:").grid(row=2, column=0, sticky="w", pady=5)
        self.cb_servico = ttk.Combobox(frame, state="readonly", width=30)
        self.cb_servico.grid(row=2, column=1, pady=5, sticky="ew")

        # Data
        tk.Label(frame, text="Data:").grid(row=3, column=0, sticky="w", pady=5)
        self.cal_data = DateEntry(frame, width=20, date_pattern="dd/mm/yyyy")
        self.cal_data.grid(row=3, column=1, pady=5, sticky="w")

        # Hora
        tk.Label(frame, text="Hora (HH:MM):").grid(row=4, column=0, sticky="w", pady=5)
        self.txt_hora = tk.Entry(frame, width=10)
        self.txt_hora.insert(0, "09:00")
        self.txt_hora.grid(row=4, column=1, pady=5, sticky="w")

        # Estrategia
        tk.Label(frame, text="Estrategia:").grid(row=5, column=0, sticky="w", pady=5)
        self.cb_estrategia = ttk.Combobox(
            frame, values=["normal", "promocional", "fidelidade"],
            state="readonly", width=20
        )
        self.cb_estrategia.current(0)
        self.cb_estrategia.grid(row=5, column=1, pady=5, sticky="w")

        # Status (somente para edicao)
        tk.Label(frame, text="Status:").grid(row=6, column=0, sticky="w", pady=5)
        self.cb_status = ttk.Combobox(
            frame, values=["agendado", "concluido", "cancelado"],
            state="readonly", width=20
        )
        self.cb_status.current(0)
        self.cb_status.grid(row=6, column=1, pady=5, sticky="w")

        frame.columnconfigure(1, weight=1)

        # Botoes
        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=20, pady=12)

        btn_text   = "Atualizar" if self.agendamento else "Salvar"
        btn_action = self.solicitar_atualizacao if self.agendamento else self.solicitar_cadastro
        tk.Button(frame_botoes, text=btn_text, width=12,
                  command=btn_action).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Fechar", width=10,
                  command=self.destroy).pack(side="right", padx=5)

    def _carregar_combos(self):
        self._clientes = self.cli_controller.listar_clientes()
        self.cb_cliente["values"] = [f"{c.id} - {c.nome}" for c in self._clientes]

        self._profissionais = self.pro_controller.listar_profissionais()
        self.cb_profissional["values"] = [f"{p.id} - {p.nome}" for p in self._profissionais]

        self._servicos = self.ser_controller.listar_servicos()
        self.cb_servico["values"] = [f"{s.id} - {s.nome}" for s in self._servicos]

    def _data_hora_str(self):
        data = self.cal_data.get_date().strftime("%d/%m/%Y")
        hora = self.txt_hora.get().strip()
        return f"{data} {hora}"

    def preencher_campos(self):
        a = self.agendamento
        # Seleciona cliente
        for i, c in enumerate(self._clientes):
            if c.id == a.cliente.id:
                self.cb_cliente.current(i)
                break
        # Seleciona profissional
        for i, p in enumerate(self._profissionais):
            if p.id == a.profissional.id:
                self.cb_profissional.current(i)
                break
        # Seleciona servico
        for i, s in enumerate(self._servicos):
            if s.id == a.servico.id:
                self.cb_servico.current(i)
                break
        self.cal_data.set_date(a.data_hora.date())
        self.txt_hora.delete(0, tk.END)
        self.txt_hora.insert(0, a.data_hora.strftime("%H:%M"))
        estrategia_str = type(a.estrategia).__name__.lower().replace("preco", "")
        self.cb_estrategia.set(estrategia_str)
        self.cb_status.set(a.status.value)

    def solicitar_cadastro(self):
        if self.cb_cliente.current() == -1:
            messagebox.showwarning("Aviso", "Selecione um cliente.", parent=self)
            return
        if self.cb_profissional.current() == -1:
            messagebox.showwarning("Aviso", "Selecione um profissional.", parent=self)
            return
        if self.cb_servico.current() == -1:
            messagebox.showwarning("Aviso", "Selecione um servico.", parent=self)
            return

        cliente      = self._clientes[self.cb_cliente.current()]
        profissional = self._profissionais[self.cb_profissional.current()]
        servico      = self._servicos[self.cb_servico.current()]

        sucesso, msg = self.controller.criar_agendamento(
            id_cliente      = cliente.id,
            id_profissional = profissional.id,
            id_servico      = servico.id,
            data_hora_str   = self._data_hora_str(),
            estrategia_str  = self.cb_estrategia.get()
        )
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)

    def solicitar_atualizacao(self):
        if self.cb_cliente.current() == -1 or self.cb_profissional.current() == -1 \
                or self.cb_servico.current() == -1:
            messagebox.showwarning("Aviso", "Preencha todos os campos.", parent=self)
            return

        cliente      = self._clientes[self.cb_cliente.current()]
        profissional = self._profissionais[self.cb_profissional.current()]
        servico      = self._servicos[self.cb_servico.current()]

        sucesso, msg = self.controller.atualizar_agendamento(
            id_agendamento  = self.agendamento.id,
            id_cliente      = cliente.id,
            id_profissional = profissional.id,
            id_servico      = servico.id,
            data_hora_str   = self._data_hora_str(),
            estrategia_str  = self.cb_estrategia.get(),
            status_str      = self.cb_status.get()
        )
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)