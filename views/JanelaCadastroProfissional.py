import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox

from control.ProfissionalController import ProfissionalController


ESPECIALIDADES = [
    "Corte Masculino",
    "Corte Feminino",
    "Barba",
    "Pintar Cabelo",
    "Sobrancelha"
]


class JanelaCadastroProfissional(tk.Toplevel):
    def __init__(self, master=None, profissional=None):
        super().__init__(master)
        self.profissional = profissional
        self.title("Editar Profissional" if profissional else "Novo Profissional")
        self.geometry("420x360")
        self.resizable(False, False)

        self.controller = ProfissionalController()

        tk.Label(self, text="Editar Profissional" if profissional else "Novo Profissional",
                 font=("Helvetica", 15, "bold")).pack(pady=10)

        self.criar_widgets()

        if self.profissional:
            self.preencher_campos()

    def criar_widgets(self):
        frame = tk.Frame(self, padx=20)
        frame.pack(fill="x")

        # Nome
        tk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="w", pady=5)
        self.txt_nome = tk.Entry(frame, width=30)
        self.txt_nome.grid(row=0, column=1, pady=5, sticky="ew")

        # CPF
        tk.Label(frame, text="CPF (somente numeros):").grid(row=1, column=0, sticky="w", pady=5)
        self.txt_cpf = tk.Entry(frame, width=30)
        self.txt_cpf.grid(row=1, column=1, pady=5, sticky="ew")

        # Especialidades — checkboxes
        tk.Label(frame, text="Especialidades:").grid(row=2, column=0, sticky="nw", pady=5)

        frame_checks = tk.Frame(frame)
        frame_checks.grid(row=2, column=1, sticky="w", pady=5)

        self.vars_especialidades = {}
        for esp in ESPECIALIDADES:
            var = tk.BooleanVar(value=False)
            self.vars_especialidades[esp] = var
            tk.Checkbutton(frame_checks, text=esp, variable=var).pack(anchor="w")

        frame.columnconfigure(1, weight=1)

        # Botoes
        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=20, pady=12)

        btn_text   = "Atualizar" if self.profissional else "Salvar"
        btn_action = self.solicitar_atualizacao if self.profissional else self.solicitar_cadastro
        tk.Button(frame_botoes, text=btn_text, width=12,
                  command=btn_action).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Fechar", width=10,
                  command=self.destroy).pack(side="right", padx=5)

    def _especialidades_selecionadas(self):
        return ", ".join(esp for esp, var in self.vars_especialidades.items() if var.get())

    def preencher_campos(self):
        self.txt_nome.insert(0, self.profissional.nome)
        self.txt_cpf.insert(0, self.profissional.cpf)
        self.txt_cpf.configure(state="disabled")

        # Marca os checkboxes correspondentes às especialidades salvas
        especialidades_salvas = [e.strip() for e in self.profissional.especialidade.split(",")]
        for esp, var in self.vars_especialidades.items():
            var.set(esp in especialidades_salvas)

    def solicitar_cadastro(self):
        especialidades = self._especialidades_selecionadas()
        if not especialidades:
            messagebox.showwarning("Aviso", "Selecione ao menos uma especialidade.", parent=self)
            return

        sucesso, msg = self.controller.salvar_profissional(
            nome          = self.txt_nome.get(),
            cpf           = self.txt_cpf.get(),
            especialidade = especialidades
        )
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)

    def solicitar_atualizacao(self):
        especialidades = self._especialidades_selecionadas()
        if not especialidades:
            messagebox.showwarning("Aviso", "Selecione ao menos uma especialidade.", parent=self)
            return

        sucesso, msg = self.controller.atualizar_profissional(
            id_profissional = self.profissional.id,
            nome            = self.txt_nome.get(),
            especialidade   = especialidades,
            disponivel      = True
        )
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)