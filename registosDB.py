import sqlite3

# Conexao a base de dados
conn = sqlite3.connect("registo.db")
c = conn.cursor()

# Lê os registos da tabela 'registos'
c.execute("SELECT * FROM registos")
registos = c.fetchall()

# Fechar a conexão com a base de dados
conn.close()

# Criar e escrever os registos em um ficheiro de texto
registos_unicos = set()
with open("registos.txt", "w", encoding="utf-8") as ficheiro:
    for ficheiro in registos:
        nome, sobrenome, idade, genero, telefone, email = ficheiro
        chave_registo = f"{nome} {sobrenome} {telefone} {email}"

        if chave_registo not in registos_unicos:
            ficheiro.write(f"Nome: {nome}\n")
            ficheiro.write(f"Sobrenome: {sobrenome}\n")
            ficheiro.write(f"Idade: {idade}\n")
            ficheiro.write(f"Gênero: {genero}\n")
            ficheiro.write(f"Número de Telefone: {telefone}\n")
            ficheiro.write(f"E-mail: {email}\n")
            ficheiro.write("\n")
            registos_unicos.add(chave_registo)

print("Registos guardados em registos.txt.")
