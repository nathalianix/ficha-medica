import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Criar banco de dados e tabelas
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

# Função para adicionar paciente ao banco
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
        cursor.execute("INSERT INTO pacientes (nome, data_nascimento, sexo, contato, queixa_principal, historico_clinico) VALUES (?, ?, ?, ?, ?, ?)", 
                       (nome, data_nascimento, sexo, contato, queixa_principal, historico_clinico))
        conexao.commit()

    messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")
    listar_pacientes()

# Função para listar pacientes na interface
def listar_pacientes():
    for row in tree.get_children():
        tree.delete(row)

    with sqlite3.connect("prontuario_clinica_medica.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, data_nascimento, sexo FROM pacientes")
        for paciente in cursor.fetchall():
            tree.insert("", "end", values=paciente)

# Criar janela principal
root = tk.Tk()
root.title("Cadastro de Pacientes")
root.geometry("600x500")

# Criar campos de entrada
tk.Label(root, text="Nome:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Data de Nascimento (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_data = tk.Entry(root)
entry_data.grid(row=1, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Sexo:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
combo_sexo = ttk.Combobox(root, values=["M", "F", "Outro"])
combo_sexo.grid(row=2, column=1, padx=10, pady=5, sticky="w")
combo_sexo.current(0)

tk.Label(root, text="Contato:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_contato = tk.Entry(root)
entry_contato.grid(row=3, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Queixa Principal:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
entry_queixa = tk.Entry(root)
entry_queixa.grid(row=4, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Histórico Clínico:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
entry_historico = tk.Entry(root)
entry_historico.grid(row=5, column=1, padx=10, pady=5, sticky="w")

# Botão para adicionar paciente
btn_adicionar = tk.Button(root, text="Cadastrar Paciente", command=adicionar_paciente)
btn_adicionar.grid(row=6, column=0, columnspan=2, pady=10)

# Criar tabela para exibir pacientes
tree = ttk.Treeview(root, columns=("ID", "Nome", "Nascimento", "Sexo"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nome", text="Nome")
tree.heading("Nascimento", text="Nascimento")
tree.heading("Sexo", text="Sexo")
tree.grid(row=7, column=0, columnspan=2, pady=10)

# Chama função para criar banco
criar_banco()
listar_pacientes()

# Rodar aplicação
root.mainloop()
