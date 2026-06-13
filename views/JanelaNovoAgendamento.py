import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

from control.AgendamentoController import AgendamentoController
from control.ProfissionalController import ProfissionalController
from control.ServicoController import ServicoController


class JanelaNovoAgendamento(tk.Toplevel):
    def __init__(self, master=None, id_cliente: int = None):
        super().__init__(master)
        self.id_cliente = id_cliente
        self.title("Novo Agendamento")
        self.geometry("440x480")
        self.resizable(False, False)

        self.controller     = AgendamentoController()
        self.pro_controller = ProfissionalController()
        self.ser_controller = ServicoController()

        self._profissionais = []
        self._servicos      = []
        self._slots         = []

        tk.Label(self, text="Novo Agendamento", font=("Arial", 15, "bold")).pack(pady=10)

        self.criar_widgets()
        self._carregar_servicos()

    def criar_widgets(self):
        frame = tk.Frame(self, padx=20)
        frame.pack(fill="x")

        # Servico
        tk.Label(frame, text="1. Serviço:").grid(row=0, column=0, sticky="w", pady=5)
        self.cb_servico = ttk.Combobox(frame, state="readonly", width=32)
        self.cb_servico.grid(row=0, column=1, pady=5, sticky="ew")
        self.cb_servico.bind("<<ComboboxSelected>>", self._ao_selecionar_servico)

        # Profissional
        tk.Label(frame, text="2. Profissional:").grid(row=1, column=0, sticky="w", pady=5)
        self.cb_profissional = ttk.Combobox(frame, state="readonly", width=32)
        self.cb_profissional.grid(row=1, column=1, pady=5, sticky="ew")
        self.cb_profissional.bind("<<ComboboxSelected>>", self._ao_selecionar_profissional)

        self.lbl_aviso_pro = tk.Label(frame, text="", fg="gray", font=("Arial", 8))
        self.lbl_aviso_pro.grid(row=2, column=1, sticky="w")

        # Data
        tk.Label(frame, text="3. Data:").grid(row=3, column=0, sticky="w", pady=5)
        self.cal_data = DateEntry(frame, width=20, date_pattern="dd/mm/yyyy")
        self.cal_data.grid(row=3, column=1, pady=5, sticky="w")
        self.cal_data.bind("<<DateEntrySelected>>", self._ao_selecionar_data)

        # Horarios disponíveis
        tk.Label(frame, text="4. Horário:").grid(row=4, column=0, sticky="nw", pady=5)

        frame_slots = tk.Frame(frame)
        frame_slots.grid(row=4, column=1, pady=5, sticky="ew")

        scrollbar = ttk.Scrollbar(frame_slots, orient="vertical")
        self.lb_slots = tk.Listbox(frame_slots, height=6, width=32, yscrollcommand=scrollbar.set, selectmode="single", exportselection=False)
        scrollbar.config(command=self.lb_slots.yview)
        self.lb_slots.pack(side="left", fill="x", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.lbl_aviso_slot = tk.Label(frame, text="Selecione o serviço e profissional primeiro.", fg="gray", font=("Arial", 8))
        self.lbl_aviso_slot.grid(row=5, column=1, sticky="w")

        frame.columnconfigure(1, weight=1)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=20, pady=12)
        tk.Button(frame_botoes, text="Confirmar", width=12, command=self.solicitar_agendamento).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Fechar", width=10, command=self.destroy).pack(side="right", padx=5)

    def _carregar_servicos(self):
        self._servicos = self.ser_controller.listar_servicos()
        self.cb_servico["values"] = [s.nome for s in self._servicos]

    def _ao_selecionar_servico(self, event=None):
        idx = self.cb_servico.current()
        if idx == -1:
            return
        servico = self._servicos[idx]
        self._profissionais = self.pro_controller.buscar_por_servico(servico.nome)
        self.cb_profissional.set("")
        self.lb_slots.delete(0, tk.END)
        self._slots = []

        if not self._profissionais:
            self.cb_profissional["values"] = []
            self.lbl_aviso_pro.config(
                text="Nenhum profissional disponível para este serviço.")
        else:
            self.cb_profissional["values"] = [f"{p.nome} ({p.cpf})" for p in self._profissionais]
            self.lbl_aviso_pro.config(text=f"{len(self._profissionais)} profissional(is) encontrado(s).")
        self.lbl_aviso_slot.config(text="Selecione o profissional e a data.")

    def _ao_selecionar_profissional(self, event=None):
        self._carregar_horarios()

    def _ao_selecionar_data(self, event=None):
        self._carregar_horarios()

    def _carregar_horarios(self):
        idx_pro = self.cb_profissional.current()
        idx_ser = self.cb_servico.current()
        if idx_pro == -1 or idx_ser == -1:
            return

        profissional = self._profissionais[idx_pro]
        servico = self._servicos[idx_ser]
        data_str = self.cal_data.get_date().strftime("%d/%m/%Y")

        self.lb_slots.delete(0, tk.END)
        self._slots = self.controller.horarios_disponiveis(profissional.id, servico.id, data_str)

        if not self._slots:
            self.lbl_aviso_slot.config(
                text="Nenhum horário disponível nesta data. Tente outro dia.")
        else:
            for slot in self._slots:
                self.lb_slots.insert(tk.END, slot.strftime("%H:%M"))
            self.lbl_aviso_slot.config(text=f"{len(self._slots)} horário(s) disponível(is).")

    def solicitar_agendamento(self):
        if self.cb_servico.current() == -1:
            messagebox.showwarning("Aviso", "Selecione um serviço.", parent=self)
            return
        if self.cb_profissional.current() == -1:
            messagebox.showwarning("Aviso", "Selecione um profissional.", parent=self)
            return
        if not self.lb_slots.curselection():
            messagebox.showwarning("Aviso", "Selecione um horário disponível.", parent=self)
            return

        profissional = self._profissionais[self.cb_profissional.current()]
        servico = self._servicos[self.cb_servico.current()]
        slot = self._slots[self.lb_slots.curselection()[0]]
        data_hora_str = slot.strftime("%d/%m/%Y %H:%M")

        sucesso, msg = self.controller.criar_agendamento(
            id_cliente = self.id_cliente,
            id_profissional = profissional.id,
            id_servico = servico.id,
            data_hora_str = data_hora_str
        )
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)