import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk

from views.JanelaNovoAgendamento import JanelaNovoAgendamento
from views.JanelaMeusAgendamentos import JanelaMeusAgendamentos
from views.JanelaHistoricoCliente import JanelaHistoricoCliente
from views.JanelaSobre import JanelaSobre
from views.JanelaLoginCliente import JanelaLoginCliente


class JanelaPrincipalCliente(tk.Tk):
    def __init__(self, cliente=None):
        super().__init__()
        self.cliente = cliente
        self.title("Salão de Beleza - Cliente")
        self.geometry("420x250")
        self.resizable(False, False)

        self._criar_menu()
        self._criar_tela_inicial()

    def _criar_menu(self):
        barra_menu = tk.Menu(self)
        self.config(menu=barra_menu)

        # Menu Agendamento
        menu_agenda = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Agendamento", menu=menu_agenda)
        menu_agenda.add_command(label="Novo Agendamento",  command=self._abrir_novo_agendamento)
        menu_agenda.add_command(label="Meus Agendamentos", command=self._abrir_meus_agendamentos)
        menu_agenda.add_command(label="Meu Histórico",     command=self._abrir_historico)

        # Menu Sistema
        menu_sistema = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Sistema", menu=menu_sistema)
        menu_sistema.add_command(label="Sobre", command=self._abrir_sobre)
        menu_sistema.add_separator()
        menu_sistema.add_command(label="Sair",  command=self._sair)

    def _criar_tela_inicial(self):
        """Exibe uma tela inicial com informações básicas sobre o sistema e opções de navegação"""
        nome = self.cliente.nome if self.cliente else "Cliente"
        tk.Label(self, text=f"Bem-vindo, {nome}!", font=("Arial", 16, "bold")).pack(pady=(30, 5))
        tk.Label(self, text="Perfil: Cliente", font=("Arial", 10), fg="#5cb85c").pack(pady=2)
        tk.Frame(self, height=1, bg="lightgray").pack(fill="x", padx=20, pady=12)
        tk.Label(self,text="Agendamento: Novo / Meus Agendamentos / Histórico\n"
                      "Sistema: Sobre | Sair", font=("Arial", 9), fg="gray", justify="center").pack()

    def _abrir_novo_agendamento(self):
        """Abre a janela para agendamento de novos serviços"""
        janela = JanelaNovoAgendamento(self, id_cliente=self.cliente.id if self.cliente else None)
        self.wait_window(janela)

    def _abrir_meus_agendamentos(self):
        """Abre a janela com os agendamentos do cliente logado"""
        janela = JanelaMeusAgendamentos(self, cliente=self.cliente)
        self.wait_window(janela)

    def _abrir_historico(self):
        """Abre a janela com o histórico de agendamentos do cliente logado"""
        janela = JanelaHistoricoCliente(self, cliente=self.cliente)
        self.wait_window(janela)

    def _abrir_sobre(self):
        """Abre a janela sobre o sistema"""
        janela = JanelaSobre(self)
        self.wait_window(janela)

    def _sair(self):
        """Confirmação para sair do sistema e volta para a tela de login do cliente"""
        self.destroy()
        app = JanelaLoginCliente()
        app.mainloop()