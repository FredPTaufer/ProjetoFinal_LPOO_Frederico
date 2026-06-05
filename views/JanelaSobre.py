import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk


class JanelaSobre(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Sobre o Sistema")
        self.geometry("380x250")
        self.resizable(False, False)

        self._criar_widgets()

    def _criar_widgets(self):
        tk.Label(self, text="Salao de Beleza",
                 font=("Helvetica", 16, "bold")).pack(pady=(20, 4))
        tk.Label(self, text="Sistema de Gerenciamento",
                 font=("Helvetica", 10, "italic"), fg="gray").pack()

        tk.Frame(self, height=1, bg="lightgray").pack(fill="x", padx=20, pady=12)

        tk.Label(self,
                 text="Disciplina: Linguagem de Programacao Orientada a Objetos\n"
                      "Professora: Vanessa Lago Machado\n"
                      "Autor: Frederico Parise Taufer\n"
                      "Curso: Bacharelado em Ciencia da Computacao",
                 font=("Helvetica", 9), fg="#555555", justify="center").pack(pady=4)

        tk.Frame(self, height=1, bg="lightgray").pack(fill="x", padx=20, pady=8)

        tk.Label(self,
                 text="Padroes utilizados: MVC, DAO, Factory, Strategy",
                 font=("Helvetica", 9), fg="gray").pack()

        tk.Button(self, text="Fechar", width=12,
                  command=self.destroy).pack(pady=12)