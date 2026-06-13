import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk


class JanelaSobre(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Sobre o Sistema")
        self.geometry("380x300")
        self.resizable(False, False)

        self._criar_widgets()

    def _criar_widgets(self):
        tk.Label(self, text="Salão de Beleza", font=("Arial", 16, "bold")).pack(pady=(20, 4))
        tk.Label(self, text="Sistema de Gerenciamento", font=("Arial", 10, "italic"), fg="gray").pack()

        tk.Frame(self, height=1, bg="lightgray").pack(fill="x", padx=20, pady=12)

        tk.Label(self,
                 text="Disciplina: Linguagem de Programação Orientada a Objetos\n"
                      "Professora: Vanessa Lago Machado\n"
                      "Autor: Frederico Parise Taufer\n"
                      "Curso: Bacharelado em Ciência da Computação",
                 font=("Arial", 9), fg="#555555", justify="center").pack(pady=4)

        tk.Frame(self, height=1, bg="lightgray").pack(fill="x", padx=20, pady=8)

        tk.Label(self, text="Padrões utilizados: MVC, DAO, Factory, Strategy", font=("Arial", 9), fg="gray").pack()

        tk.Button(self, text="Fechar", width=12, command=self.destroy).pack(pady=12)