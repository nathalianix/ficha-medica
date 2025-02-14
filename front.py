import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def criar_banco():
    with sqlite3.connect("prontuario_clinica_medica.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                data_nascimento TEXT NOT NULL,
                sexo TEXT CHECK(sexo IN ('M', 'F', 'Outro')) NOT NULL,
                contato TEXT NOT NULL,
                queixa_principal TEXT NOT NULL,
                historico_clinico TEXT
            )
        ''')
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS prontuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                descricao TEXT NOT NULL,
                data TEXT NOT NULL,
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE
            )
        ''')
    print("Banco de dados criado!")

def excluir_paciente(paciente_id):
    with sqlite3.connect("prontuario_clinica_medica.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM pacientes WHERE id = ?", (paciente_id,))
        conexao.commit()

    messagebox.showinfo("Sucesso", "Paciente excluído com sucesso!")
    listar_pacientes()

def adicionar_paciente():
    nome = entry_nome.get().strip()
    data_nascimento = entry_data.get().strip()
    sexo = combo_sexo.get()
    contato = entry_contato.get().strip()
    queixa_principal = entry_queixa.get().strip()
    historico_clinico = entry_historico.get().strip()

    if not nome or not data_nascimento or not contato or not queixa_principal:
        messagebox.showwarning("Atenção", "Todos os campos obrigatórios devem ser preenchidos!")
        return

    with sqlite3.connect("prontuario_clinica_medica.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO pacientes (nome, data_nascimento, sexo, contato, queixa_principal, historico_clinico) VALUES (?, ?, ?, ?, ?, ?)",
            (nome, data_nascimento, sexo, contato, queixa_principal, historico_clinico))
        conexao.commit()

    messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")
    listar_pacientes()

def editar_paciente(paciente_id):
    with sqlite3.connect("prontuario_clinica_medica.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM pacientes WHERE id = ?", (paciente_id,))
        paciente = cursor.fetchone()

    entry_nome.delete(0, tk.END)
    entry_nome.insert(0, paciente[1])
    entry_data.delete(0, tk.END)
    entry_data.insert(0, paciente[2])
    combo_sexo.set(paciente[3])
    entry_contato.delete(0, tk.END)
    entry_contato.insert(0, paciente[4])
    entry_queixa.delete(0, tk.END)
    entry_queixa.insert(0, paciente[5])
    entry_historico.delete(0, tk.END)
    entry_historico.insert(0, paciente[6])

    btn_adicionar.config(text="Atualizar Paciente", command=lambda: atualizar_paciente(paciente_id))

def atualizar_paciente(paciente_id):
    nome = entry_nome.get().strip()
    data_nascimento = entry_data.get().strip()
    sexo = combo_sexo.get()
    contato = entry_contato.get().strip()
    queixa_principal = entry_queixa.get().strip()
    historico_clinico = entry_historico.get().strip()

    if not nome or not data_nascimento or not contato or not queixa_principal:
        messagebox.showwarning("Atenção", "Todos os campos obrigatórios devem ser preenchidos!")
        return

    with sqlite3.connect("prontuario_clinica_medica.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("""
            UPDATE pacientes 
            SET nome = ?, data_nascimento = ?, sexo = ?, contato = ?, queixa_principal = ?, historico_clinico = ? 
            WHERE id = ?""",
            (nome, data_nascimento, sexo, contato, queixa_principal, historico_clinico, paciente_id))
        conexao.commit()

    messagebox.showinfo("Sucesso", "Paciente atualizado com sucesso!")
    btn_adicionar.config(text="Cadastrar Paciente", command=adicionar_paciente)
    listar_pacientes()

def listar_pacientes():
    for row in tree.get_children():
        tree.delete(row)

    for btn in botao_exclusao:
        btn.grid_forget()

    botao_exclusao.clear()

    with sqlite3.connect("prontuario_clinica_medica.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, data_nascimento, sexo FROM pacientes")
        for paciente in cursor.fetchall():
            item_id = tree.insert("", "end", values=(paciente[0], paciente[1], paciente[2], paciente[3]))

            btn_delete = ttk.Button(frame, text="🗑️", bootstyle="danger",
                                    command=lambda paciente_id=paciente[0]: excluir_paciente(paciente_id))
            btn_delete.grid(row=len(botao_exclusao) + 8, column=1, padx=10, pady=5)
            botao_exclusao.append(btn_delete)

            btn_edit = ttk.Button(frame, text="✏️", bootstyle="primary",
                                  command=lambda paciente_id=paciente[0]: editar_paciente(paciente_id))
            btn_edit.grid(row=len(botao_exclusao) + 8, column=0, padx=10, pady=5)

def pesquisar_paciente():
    termo = entry_pesquisa.get().lower()
    for row in tree.get_children():
        tree.delete(row)

    with sqlite3.connect("prontuario_clinica_medica.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, data_nascimento, sexo FROM pacientes WHERE nome LIKE ?", ('%' + termo + '%',))
        for paciente in cursor.fetchall():
            tree.insert("", "end", values=(paciente[0], paciente[1], paciente[2], paciente[3]))

app = ttk.Window(title="Prontuário Médico", themename="morph")
app.geometry("600x600")

frame = ttk.Frame(app, padding=20)
frame.pack(expand=True)

tk.Label(frame, text="Nome:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_nome = ttk.Entry(frame, width=40)
entry_nome.grid(row=0, column=1, padx=10, pady=5, sticky="w")

tk.Label(frame, text="Data de Nascimento (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_data = ttk.Entry(frame, width=40)
entry_data.grid(row=1, column=1, padx=10, pady=5, sticky="w")

tk.Label(frame, text="Sexo:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
combo_sexo = ttk.Combobox(frame, values=["M", "F", "Outro"])
combo_sexo.grid(row=2, column=1, padx=10, pady=5, sticky="w")
combo_sexo.current(0)

tk.Label(frame, text="Contato:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_contato = ttk.Entry(frame, width=40)
entry_contato.grid(row=3, column=1, padx=10, pady=5, sticky="w")

tk.Label(frame, text="Queixa Principal:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
entry_queixa = ttk.Entry(frame, width=40)
entry_queixa.grid(row=4, column=1, padx=10, pady=5, sticky="w")

tk.Label(frame, text="Histórico Clínico:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
entry_historico = ttk.Entry(frame, width=40)
entry_historico.grid(row=5, column=1, padx=10, pady=5, sticky="w")

btn_adicionar = ttk.Button(frame, text="Cadastrar Paciente", bootstyle="success", command=adicionar_paciente)
btn_adicionar.grid(row=6, column=0, columnspan=2, pady=10)

tk.Label(frame, text="Pesquisar Paciente:").grid(row=7, column=0, padx=10, pady=5, sticky="w")
entry_pesquisa = ttk.Entry(frame, width=40)
entry_pesquisa.grid(row=7, column=1, padx=10, pady=5, sticky="w")
btn_pesquisar = ttk.Button(frame, text="Pesquisar", bootstyle="info", command=pesquisar_paciente)
btn_pesquisar.grid(row=7, column=2, padx=10, pady=5)

tree = ttk.Treeview(frame, columns=("ID", "Nome", "Nascimento", "Sexo"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nome", text="Nome")
tree.heading("Nascimento", text="Nascimento")
tree.heading("Sexo", text="Sexo")
tree.grid(row=8, column=0, columnspan=3, pady=10)

botao_exclusao = []

criar_banco()
listar_pacientes()

app.mainloop()
