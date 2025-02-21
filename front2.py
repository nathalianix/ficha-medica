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
    print("Banco de dados criado!")

def excluir_paciente():
    selected_item = tree.selection()
    if selected_item:
        paciente_id = tree.item(selected_item)['values'][0]
        with sqlite3.connect("prontuario_clinica_medica.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM pacientes WHERE id = ?", (paciente_id,))
            conexao.commit()
        messagebox.showinfo("Sucesso", "Paciente excluído com sucesso!")
        listar_pacientes()
    else:
        messagebox.showwarning("Atenção", "Selecione um paciente para excluir!")

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

def listar_pacientes():
    for row in tree.get_children():
        tree.delete(row)

    with sqlite3.connect("prontuario_clinica_medica.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, data_nascimento, sexo FROM pacientes")
        for paciente in cursor.fetchall():
            tree.insert("", "end", values=(paciente[0], paciente[1], paciente[2], paciente[3]))

def pesquisar_paciente():
    termo = entry_pesquisa.get().strip().lower()
    for row in tree.get_children():
        tree.delete(row)

    with sqlite3.connect("prontuario_clinica_medica.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, data_nascimento, sexo FROM pacientes WHERE nome LIKE ?", ('%' + termo + '%',))
        for paciente in cursor.fetchall():
            tree.insert("", "end", values=(paciente[0], paciente[1], paciente[2], paciente[3]))

app = ttk.Window(title="Prontuário Médico", themename="morph")
app.geometry("700x500")

frame = ttk.Frame(app, padding=20)
frame.pack(expand=True, fill="both")

notebook = ttk.Notebook(frame)
notebook.pack(expand=True, fill="both")

frame_cadastro = ttk.Frame(notebook, padding=20)
notebook.add(frame_cadastro, text="Cadastro")

frame_lista = ttk.Frame(notebook, padding=20)
notebook.add(frame_lista, text="Pacientes")

ttk.Label(frame_cadastro, text="Nome:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_nome = ttk.Entry(frame_cadastro, width=50)
entry_nome.grid(row=0, column=1, padx=10, pady=5, sticky="w")

ttk.Label(frame_cadastro, text="Data de Nascimento:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_data = ttk.Entry(frame_cadastro, width=50)
entry_data.grid(row=1, column=1, padx=10, pady=5, sticky="w")

ttk.Label(frame_cadastro, text="Sexo:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
combo_sexo = ttk.Combobox(frame_cadastro, values=["M", "F", "Outro"], width=48)
combo_sexo.grid(row=2, column=1, padx=10, pady=5, sticky="w")
combo_sexo.current(0)

ttk.Label(frame_cadastro, text="Contato:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_contato = ttk.Entry(frame_cadastro, width=50)
entry_contato.grid(row=3, column=1, padx=10, pady=5, sticky="w")

ttk.Label(frame_cadastro, text="Queixa Principal:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
entry_queixa = ttk.Entry(frame_cadastro, width=50)
entry_queixa.grid(row=4, column=1, padx=10, pady=5, sticky="w")

ttk.Label(frame_cadastro, text="Histórico Clínico:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
entry_historico = ttk.Entry(frame_cadastro, width=50)
entry_historico.grid(row=5, column=1, padx=10, pady=5, sticky="w")

btn_adicionar = ttk.Button(frame_cadastro, text="Cadastrar Paciente", bootstyle="success", command=adicionar_paciente)
btn_adicionar.grid(row=6, column=0, columnspan=2, pady=10)

columns = ("ID", "Nome", "Data de Nascimento", "Sexo")
tree = ttk.Treeview(frame_lista, columns=columns, show="headings")
tree.pack(expand=True, fill="both", pady=10)
for col in columns:
    tree.heading(col, text=col)

ttk.Label(frame_lista, text="Pesquisar Paciente:").pack()
entry_pesquisa = ttk.Entry(frame_lista, width=50)
entry_pesquisa.pack()
btn_pesquisar = ttk.Button(frame_lista, text="Pesquisar", bootstyle="info", command=pesquisar_paciente)
btn_pesquisar.pack()

btn_excluir = ttk.Button(frame_lista, text="Excluir", bootstyle="danger", command=excluir_paciente)
btn_excluir.pack()

listar_pacientes()
app.mainloop()
