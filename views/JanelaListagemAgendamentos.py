import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox

from control.AgendamentoController import AgendamentoController
from views.JanelaCadastroAgendamento import JanelaCadastroAgendamento


class JanelaListagemAgendamentos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Agendamentos - Admin")
        self.geometry("820x420")

        self.controller = AgendamentoController()

        self.criar_widgets()
        self.carregar_dados()

    def criar_widgets(self):
        """Cria os widgets da janela de listagem de agendamentos"""
        tk.Label(self, text="Gerenciamento de Agendamentos", font=("Arial", 16, "bold")).pack(pady=10)

        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=20, pady=5)

        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side="right", fill="y")

        colunas = ("Cliente", "Profissional", "Serviço", "Data/Hora", "Status", "Valor")
        self.tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", yscrollcommand=scrollbar.set)
        larguras = {"Cliente": 140, "Profissional": 140, "Serviço": 120, "Data/Hora": 120, "Status": 80, "Valor": 90}
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=larguras[col])

        self.tree.pack(expand=True, fill="both")
        scrollbar.config(command=self.tree.yview)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=20, pady=5)
        tk.Button(frame_botoes, text="Novo", width=10, command=self.abrir_novo).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Editar", width=10, command=self.abrir_editar).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Ver Detalhes", width=12, command=self.ver_detalhes).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Concluir", width=10, command=self.concluir).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Cancelar", width=10, command=self.cancelar).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Remover", width=10, command=self.remover).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Fechar", width=10, command=self.destroy).pack(side="right", padx=5)

    def carregar_dados(self):
        """Carrega os dados dos agendamentos no treeview"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for a in self.controller.listar_agendamentos():
            self.tree.insert("", "end", iid=str(a.id), values=(
                a.cliente.nome,
                a.profissional.nome,
                a.servico.nome,
                a.data_hora.strftime("%d/%m/%Y %H:%M"),
                a.status.value.capitalize(),
                f"R$ {a.calcularValor():.2f}".replace(".", ",")
            ))

    def _id_selecionado(self):
        """Retorna o id do agendamento selecionado"""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um agendamento.", parent=self)
            return None
        return int(sel[0])

    def abrir_novo(self):
        """Abre a janela de cadastro de agendamento"""
        janela = JanelaCadastroAgendamento(self)
        self.wait_window(janela)
        self.carregar_dados()

    def abrir_editar(self):
        """Abre a janela de edição de agendamento"""
        id_age = self._id_selecionado()
        if id_age is None:
            return
        agendamento = self.controller.buscar_por_id(id_age)
        if not agendamento:
            messagebox.showerror("Erro", "Agendamento não encontrado.", parent=self)
            return
        
        janela = JanelaCadastroAgendamento(self, agendamento=agendamento)
        self.wait_window(janela)
        self.carregar_dados()

    def ver_detalhes(self):
        """Exibe uma janela com os detalhes do agendamento selecionado"""
        id_age = self._id_selecionado()
        if id_age is None:
            return
        a = self.controller.buscar_por_id(id_age)
        if not a:
            messagebox.showerror("Erro", "Agendamento não encontrado.", parent=self)
            return
        msg = (
            f"Cliente:       {a.cliente.nome}\n"
            f"Profissional:  {a.profissional.nome}\n"
            f"Serviço:       {a.servico.nome}\n"
            f"Duração:       {a.servico.duracao} minutos\n"
            f"Data/Hora:     {a.data_hora.strftime('%d/%m/%Y %H:%M')}\n"
            f"Status:        {a.status.value.capitalize()}\n"
            f"Estratégia:    {type(a.estrategia).__name__}\n"
            f"Valor:         R$ {a.calcularValor():.2f}"
        )
        messagebox.showinfo("Detalhes do Agendamento", msg, parent=self)

    def concluir(self):
        """Conclui o agendamento selecionado"""
        id_age = self._id_selecionado()
        if id_age is None:
            return
        sucesso, msg = self.controller.concluir(id_age)
        if sucesso:
            self.carregar_dados()
            messagebox.showinfo("Sucesso", msg, parent=self)
        else:
            messagebox.showerror("Erro", msg, parent=self)

    def cancelar(self):
        """Cancela o agendamento selecionado"""
        id_age = self._id_selecionado()
        if id_age is None:
            return
        if messagebox.askyesno("Confirmar", "Deseja cancelar este agendamento?", parent=self):
            sucesso, msg = self.controller.cancelar(id_age)
            if sucesso:
                self.carregar_dados()
                messagebox.showinfo("Sucesso", msg, parent=self)
            else:
                messagebox.showerror("Erro", msg, parent=self)

    def remover(self):
        id_age = self._id_selecionado()
        if id_age is None:
            return
        if messagebox.askyesno("Confirmar", "Remover agendamento permanentemente?", parent=self):
            sucesso, msg = self.controller.remover_agendamento(id_age)
            if sucesso:
                self.carregar_dados()
                messagebox.showinfo("Sucesso", msg, parent=self)
            else:
                messagebox.showerror("Erro", msg, parent=self)