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
        self.geometry("460x560")
        self.resizable(False, False)

        self.controller = AgendamentoController()
        self.cli_controller = ClienteController()
        self.pro_controller = ProfissionalController()
        self.ser_controller = ServicoController()

        self._clientes = []
        self._profissionais = []
        self._servicos = []
        self._slots = []

        tk.Label(self, text="Editar Agendamento" if agendamento else "Novo Agendamento", font=("Arial", 15, "bold")).pack(pady=10)

        self.criar_widgets()
        self._carregar_clientes_servicos()

        if self.agendamento:
            self.preencher_campos()

    def criar_widgets(self):
        """Cria os widgets da janela de cadastro/edição de agendamento"""
        frame = tk.Frame(self, padx=20)
        frame.pack(fill="x")

        tk.Label(frame, text="Cliente:").grid(row=0, column=0, sticky="w", pady=4)
        self.cb_cliente = ttk.Combobox(frame, state="readonly", width=32)
        self.cb_cliente.grid(row=0, column=1, pady=4, sticky="ew")

        tk.Label(frame, text="Serviço:").grid(row=1, column=0, sticky="w", pady=4)
        self.cb_servico = ttk.Combobox(frame, state="readonly", width=32)
        self.cb_servico.grid(row=1, column=1, pady=4, sticky="ew")
        self.cb_servico.bind("<<ComboboxSelected>>", self._ao_selecionar_servico)

        tk.Label(frame, text="Profissional:").grid(row=2, column=0, sticky="w", pady=4)
        self.cb_profissional = ttk.Combobox(frame, state="readonly", width=32)
        self.cb_profissional.grid(row=2, column=1, pady=4, sticky="ew")
        self.cb_profissional.bind("<<ComboboxSelected>>", self._ao_selecionar_profissional)

        self.lbl_aviso_pro = tk.Label(frame, text="", fg="gray", font=("Arial", 8))
        self.lbl_aviso_pro.grid(row=3, column=1, sticky="w")

        tk.Label(frame, text="Data:").grid(row=4, column=0, sticky="w", pady=4)
        self.cal_data = DateEntry(frame, width=20, date_pattern="dd/mm/yyyy")
        self.cal_data.grid(row=4, column=1, pady=4, sticky="w")
        self.cal_data.bind("<<DateEntrySelected>>", self._ao_selecionar_data)

        tk.Label(frame, text="Horário:").grid(row=5, column=0, sticky="nw", pady=4)

        frame_slots = tk.Frame(frame)
        frame_slots.grid(row=5, column=1, pady=4, sticky="ew")
        scrollbar = ttk.Scrollbar(frame_slots, orient="vertical")
        self.lb_slots = tk.Listbox(frame_slots, height=5, width=32, yscrollcommand=scrollbar.set, selectmode="single", exportselection=False)
        scrollbar.config(command=self.lb_slots.yview)
        self.lb_slots.pack(side="left", fill="x", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.lbl_aviso_slot = tk.Label(frame, text="Selecione serviço e profissional.", fg="gray", font=("Arial", 8))
        self.lbl_aviso_slot.grid(row=6, column=1, sticky="w")

        tk.Label(frame, text="Estratégia:").grid(row=7, column=0, sticky="w", pady=4)
        self.cb_estrategia = ttk.Combobox(frame, values=["normal", "promocional", "fidelidade"], state="readonly", width=20)
        self.cb_estrategia.current(0)
        self.cb_estrategia.grid(row=7, column=1, pady=4, sticky="w")

        tk.Label(frame, text="Status:").grid(row=8, column=0, sticky="w", pady=4)
        self.cb_status = ttk.Combobox(frame, values=["agendado", "concluido", "cancelado"], state="readonly", width=20)
        self.cb_status.current(0)
        self.cb_status.grid(row=8, column=1, pady=4, sticky="w")

        frame.columnconfigure(1, weight=1)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=20, pady=10)
        btn_text = "Atualizar" if self.agendamento else "Salvar"
        btn_action = self.solicitar_atualizacao if self.agendamento else self.solicitar_cadastro
        tk.Button(frame_botoes, text=btn_text, width=12, command=btn_action).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Fechar", width=10, command=self.destroy).pack(side="right", padx=5)

    def _carregar_clientes_servicos(self):
        """Carrega clientes e serviços para os comboboxes"""
        self._clientes = self.cli_controller.listar_clientes()
        self.cb_cliente["values"] = [f"{c.nome} ({c.cpf})" for c in self._clientes]
        self._servicos = self.ser_controller.listar_servicos()
        self.cb_servico["values"] = [s.nome for s in self._servicos]

    def _ao_selecionar_servico(self, event=None):
        """Carrega os profissionais disponíveis para esse serviço"""
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
            self.lbl_aviso_pro.config(text="Nenhum profissional com esta especialidade.")
        else:
            self.cb_profissional["values"] = [
                f"{p.nome} ({p.cpf})" for p in self._profissionais
            ]
            self.lbl_aviso_pro.config(
                text=f"{len(self._profissionais)} profissional(is) encontrado(s).")
        self.lbl_aviso_slot.config(text="Selecione o profissional e a data.")

    def _ao_selecionar_profissional(self, event=None):
        self._carregar_horarios()

    def _ao_selecionar_data(self, event=None):
        self._carregar_horarios()

    def _carregar_horarios(self):
        """Carrega os horários disponíveis para o profissional, serviço e data selecionados"""
        idx_pro = self.cb_profissional.current()
        idx_ser = self.cb_servico.current()
        if idx_pro == -1 or idx_ser == -1:
            return

        profissional = self._profissionais[idx_pro]
        servico = self._servicos[idx_ser]
        data_str = self.cal_data.get_date().strftime("%d/%m/%Y")

        self.lb_slots.delete(0, tk.END)
        self._slots = self.controller.horarios_disponiveis(profissional.id, servico.id, data_str, id_agendamento=self.agendamento.id if self.agendamento else None)

        if not self._slots:
            self.lbl_aviso_slot.config(
                text="Nenhum horário disponível nesta data. Tente outro dia.")
        else:
            for slot in self._slots:
                self.lb_slots.insert(tk.END, slot.strftime("%H:%M"))
            self.lbl_aviso_slot.config(
                text=f"{len(self._slots)} horário(s) disponível(is).")

    def _slot_selecionado(self):
        sel = self.lb_slots.curselection()
        if not sel:
            return None
        return self._slots[sel[0]]

    def preencher_campos(self):
        """Preenche os campos com os dados do agendamento a ser editado"""
        a = self.agendamento
        for i, c in enumerate(self._clientes):
            if c.id == a.cliente.id:
                self.cb_cliente.current(i)
                break
        for i, s in enumerate(self._servicos):
            if s.id == a.servico.id:
                self.cb_servico.current(i)
                self._ao_selecionar_servico()
                break
        for i, p in enumerate(self._profissionais):
            if p.id == a.profissional.id:
                self.cb_profissional.current(i)
                break
        self.cal_data.set_date(a.data_hora.date())
        self._carregar_horarios()
        hora_atual = a.data_hora.strftime("%H:%M")
        for i in range(self.lb_slots.size()):
            if self.lb_slots.get(i) == hora_atual:
                self.lb_slots.selection_set(i)
                self.lb_slots.see(i)
                break
        estrategia_str = type(a.estrategia).__name__.lower().replace("preco", "")
        self.cb_estrategia.set(estrategia_str)
        self.cb_status.set(a.status.value)

    def solicitar_cadastro(self):
        """Solicita ao controller que crie um novo agendamento"""
        if self.cb_cliente.current() == -1 or self.cb_profissional.current() == -1 \
                or self.cb_servico.current() == -1:
            messagebox.showwarning("Aviso", "Preencha todos os campos.", parent=self)
            return
        slot = self._slot_selecionado()
        if not slot:
            messagebox.showwarning("Aviso", "Selecione um horário disponível.", parent=self)
            return

        cliente = self._clientes[self.cb_cliente.current()]
        profissional = self._profissionais[self.cb_profissional.current()]
        servico = self._servicos[self.cb_servico.current()]

        sucesso, msg = self.controller.criar_agendamento(
            id_cliente=cliente.id, 
            id_profissional=profissional.id,
            id_servico=servico.id,
            data_hora_str=slot.strftime("%d/%m/%Y %H:%M"),
            estrategia_str=self.cb_estrategia.get()
        )
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)

    def solicitar_atualizacao(self):
        """Solicita ao controller que atualize um agendamento"""
        if self.cb_cliente.current() == -1 or self.cb_profissional.current() == -1 \
                or self.cb_servico.current() == -1:
            messagebox.showwarning("Aviso", "Preencha todos os campos.", parent=self)
            return
        slot = self._slot_selecionado()
        if not slot:
            messagebox.showwarning("Aviso", "Selecione um horário disponível.", parent=self)
            return

        cliente = self._clientes[self.cb_cliente.current()]
        profissional = self._profissionais[self.cb_profissional.current()]
        servico = self._servicos[self.cb_servico.current()]

        sucesso, msg = self.controller.atualizar_agendamento(
            id_agendamento=self.agendamento.id, 
            id_cliente=cliente.id,
            id_profissional=profissional.id, 
            id_servico=servico.id,
            data_hora_str=slot.strftime("%d/%m/%Y %H:%M"),
            estrategia_str=self.cb_estrategia.get(),
            status_str=self.cb_status.get()
        )
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)