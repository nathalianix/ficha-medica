import sqlite3

def criar_banco_e_tabelas():
    conexao = sqlite3.connect("prontuario_clinica_medica.db")
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
