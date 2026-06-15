import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from views.JanelaListagemClientes import JanelaListagemClientes
from views.JanelaListagemProfissionais import JanelaListagemProfissionais
from views.JanelaListagemServicos import JanelaListagemServicos
from views.JanelaListagemAgendamentos import JanelaListagemAgendamentos
from views.JanelaSobre import JanelaSobre


class JanelaPrincipalAdmin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Salão de Beleza - Administrador")
        self.geometry("420x240")
        self.resizable(False, False)

        self._criar_menu()
        self._criar_tela_inicial()

    def _criar_menu(self):
        barra_menu = tk.Menu(self)
        self.config(menu=barra_menu)

        # Menu Cadastro
        menu_cadastro = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Cadastro", menu=menu_cadastro)
        menu_cadastro.add_command(label="Clientes", command=self._abrir_clientes)
        menu_cadastro.add_command(label="Profissionais", command=self._abrir_profissionais)
        menu_cadastro.add_command(label="Serviços", command=self._abrir_servicos)

        # Menu Agendamentos
        menu_agenda = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Agendamentos", menu=menu_agenda)
        menu_agenda.add_command(label="Gerenciar Agendamentos", command=self._abrir_agendamentos)

        # Menu Sistema
        menu_sistema = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Sistema", menu=menu_sistema)
        menu_sistema.add_command(label="Sobre", command=self._abrir_sobre)
        menu_sistema.add_separator()
        menu_sistema.add_command(label="Sair", command=self._sair)

    def _criar_tela_inicial(self):
        """Exibe uma tela inicial com informações básicas sobre o sistema e opções de navegação"""
        tk.Label(self, text="Painel do Administrador", font=("Arial", 16, "bold")).pack(pady=(30, 5))
        tk.Label(self, text="Perfil: Administrador", font=("Arial", 10), fg="#4a90d9").pack(pady=2)
        tk.Frame(self, height=1, bg="lightgray").pack(fill="x", padx=20, pady=12)
        tk.Label(self, text="Cadastro: Clientes / Profissionais / Serviços\n"
                      "Agendamentos: Gerenciar Agendamentos\n"
                      "Sistema: Sobre | Sair", font=("Arial", 9), fg="gray", justify="center").pack()

    def _abrir_clientes(self):
        """Abre a janela de listagem de clientes"""
        janela = JanelaListagemClientes(self)
        self.wait_window(janela)

    def _abrir_profissionais(self):
        """Abre a janela de listagem de profissionais"""
        janela = JanelaListagemProfissionais(self)
        self.wait_window(janela)

    def _abrir_servicos(self):
        """Abre a janela de listagem de serviços"""
        janela = JanelaListagemServicos(self)
        self.wait_window(janela)

    def _abrir_agendamentos(self):
        """Abre a janela de listagem de agendamentos"""
        janela = JanelaListagemAgendamentos(self)
        self.wait_window(janela)

    def _abrir_sobre(self):
        """Abre a janela sobre o sistema"""
        janela = JanelaSobre(self)
        self.wait_window(janela)

    def _sair(self):
        """Confirmação para sair do sistema e volta para a escolha de perfil"""
        from views.JanelaEscolhaPerfil import JanelaEscolhaPerfil
        self.destroy()
        app = JanelaEscolhaPerfil()
        app.mainloop()