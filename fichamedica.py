import sqlite3

def criar_banco_e_tabelas():
    conexao = sqlite3.connect("prontuario_clinica_medica.db")
    cursor = conexao.cursor()

    # Criação da tabela de pacientes
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

    # Criação da tabela de prontuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prontuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        descricao TEXT NOT NULL,
        data TEXT NOT NULL,
        FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
    )
    ''')

    conexao.commit()
    conexao.close()

def adicionar_paciente():
    conexao = sqlite3.connect("prontuario_clinica_medica.db")
    cursor = conexao.cursor()

    try:
        nome = input("Nome do paciente: ") or "Paciente Teste"
        data_nascimento = input("Data de nascimento {YYYY-MM-DD}: ") or "2000-01-01"
        sexo = input("Sexo (M, F, Outro): ") or "Outro"
        contato = input("Contato: ") or "00000000"
        queixa_principal = input("Queixa principal: ") or "Nenhuma"
        historico_clinico = input("Histórico clínico (opcional): ") or "Nenhum"

        # Print para depuração
        print(f"Inserindo paciente: {nome}, {data_nascimento}, {sexo}, {contato}, {queixa_principal}, {historico_clinico}")

        cursor.execute("INSERT INTO pacientes (nome, data_nascimento, sexo, contato, queixa_principal, historico_clinico) VALUES (?, ?, ?, ?, ?, ?)", 
                       (nome, data_nascimento, sexo, contato, queixa_principal, historico_clinico))
        conexao.commit()
        print("Paciente cadastrado com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao cadastrar paciente: {e}")
    finally:
        conexao.close()

def listar_pacientes():
    conexao = sqlite3.connect("prontuario_clinica_medica.db")
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT * FROM pacientes")
        pacientes = cursor.fetchall()

        # Print para depuração
        print(f"Pacientes encontrados: {pacientes}")

        if not pacientes:
            print("Nenhum paciente encontrado.")
            return

        for paciente in pacientes:
            print(f"ID: {paciente[0]}, Nome: {paciente[1]}, Data de Nascimento: {paciente[2]}, Sexo: {paciente[3]}, Contato: {paciente[4]}, Queixa Principal: {paciente[5]}, Histórico Clínico: {paciente[6]}")
    except sqlite3.Error as e:
        print(f"Erro ao listar pacientes: {e}")
    finally:
        conexao.close()

def cadastrar_prontuario():
    conexao = sqlite3.connect("prontuario_clinica_medica.db")
    cursor = conexao.cursor()

    listar_pacientes()
    try:
        paciente_id_str = input("Digite o ID do paciente: ") or "1"
        paciente_id = int(paciente_id_str)
        cursor.execute("SELECT 1 FROM pacientes WHERE id = ?", (paciente_id,))
        if cursor.fetchone() is None:
            print("Paciente não encontrado.")
            return

        descricao = input("Digite a descrição do prontuário: ") or "Descrição de teste"
        data = input("Digite a data do prontuário (YYYY-MM-DD): ") or "2023-01-01"

        print(f"Inserindo prontuário para o paciente ID {paciente_id}, Descrição: {descricao}, Data: {data}")

        cursor.execute("INSERT INTO prontuarios (paciente_id, descricao, data) VALUES (?, ?, ?)", (paciente_id, descricao, data))
        conexao.commit()
        print("Prontuário cadastrado com sucesso!")
    except ValueError:
        print("Erro: ID do paciente deve ser um número inteiro.")
    except sqlite3.Error as e:
        print(f"Erro ao cadastrar prontuário: {e}")
    finally:
        conexao.close()

def menu():
    criar_banco_e_tabelas()

    while True:
        print("\nMenu:")
        print("1. Cadastrar Paciente")
        print("2. Listar Pacientes")
        print("3. Cadastrar Prontuário")
        print("4. Sair")

        try:
            opcao_str = input("Escolha uma opção: ") or "4"
            opcao = int(opcao_str)
        except ValueError:
            print("Entrada inválida. Digite um número.")
            continue

        if opcao == 1:
            adicionar_paciente()
        elif opcao == 2:
            listar_pacientes()
        elif opcao == 3:
            cadastrar_prontuario()
        elif opcao == 4:
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    menu()

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
