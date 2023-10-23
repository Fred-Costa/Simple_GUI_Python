import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QComboBox
from PyQt5.QtGui import QIntValidator
import sqlite3


class RegistoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registo de Pessoas")
        self.setGeometry(100, 100, 400, 300)

        self.initUI()
        self.initDB()

    def initUI(self):
        # Criação de widgets e layout da interface

        self.layout = QVBoxLayout()

        self.label_nome = QLabel("Nome:")
        self.input_nome = QLineEdit(self)
        self.layout.addWidget(self.label_nome)
        self.layout.addWidget(self.input_nome)

        self.label_sobrenome = QLabel("Sobrenome:")
        self.input_sobrenome = QLineEdit(self)
        self.layout.addWidget(self.label_sobrenome)
        self.layout.addWidget(self.input_sobrenome)

        self.label_idade = QLabel("Idade:")
        self.input_idade = QLineEdit(self)
        self.input_idade.setValidator(QIntValidator())
        self.layout.addWidget(self.label_idade)
        self.layout.addWidget(self.input_idade)

        self.label_genero = QLabel("Gênero:")
        self.input_genero = QComboBox(self)
        self.input_genero.addItem("Masculino")
        self.input_genero.addItem("Feminino")
        self.input_genero.addItem("Outro")
        self.layout.addWidget(self.label_genero)
        self.layout.addWidget(self.input_genero)

        self.label_telefone = QLabel("Número de Telefone:")
        self.input_telefone = QLineEdit(self)
        self.input_telefone.setValidator(QIntValidator())
        self.input_telefone.setMaxLength(9)  # Aceita apenas 9 números
        self.layout.addWidget(self.label_telefone)
        self.layout.addWidget(self.input_telefone)

        self.label_email = QLabel("E-mail:")
        self.input_email = QLineEdit(self)
        self.layout.addWidget(self.label_email)
        self.layout.addWidget(self.input_email)

        self.btn_registar = QPushButton("Registar")
        self.btn_registar.clicked.connect(self.registar)
        self.layout.addWidget(self.btn_registar)

        self.setLayout(self.layout)

    def initDB(self):
        # Conexão com base de dados SQLite

        self.conn = sqlite3.connect("registo.db")
        self.c = self.conn.cursor()
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS registos (
                nome TEXT,
                sobrenome TEXT,
                idade INTEGER,
                genero TEXT,
                telefone TEXT,
                email TEXT
            )
        ''')
        self.conn.commit()

    def registar(self):
        # Função para pegar informações do formulário e guardar estas na base de dados

        nome = self.input_nome.text()
        sobrenome = self.input_sobrenome.text()
        idade = self.input_idade.text()
        genero = self.input_genero.currentText()
        telefone = self.input_telefone.text()
        email = self.input_email.text()

        if nome and sobrenome and idade and telefone and email:
            try:
                idade = int(idade)
                # Verifica se o registo já existe no banco de dados
                self.c.execute("SELECT * FROM registos WHERE nome=? AND sobrenome=? AND telefone=? AND email=?",
                               (nome, sobrenome, telefone, email))
                registo_existente = self.c.fetchone()
                if registo_existente:
                    QMessageBox.critical(self, "Erro", "Este registo já existe na base de dados")
                else:
                    self.c.execute("INSERT INTO registos VALUES (?, ?, ?, ?, ?, ?)",
                                   (nome, sobrenome, idade, genero, telefone, email))
                self.conn.commit()

                # Limpar os campos após o registo
                self.input_nome.clear()
                self.input_sobrenome.clear()
                self.input_idade.clear()
                self.input_telefone.clear()
                self.input_email.clear()

                QMessageBox.information(self, "Sucesso", "Registo feito com sucesso.")
            except ValueError:
                QMessageBox.critical(self, "Erro", "Idade deve ser um número inteiro.")
        else:
            QMessageBox.critical(self, "Erro", "Por favor, preencha todos os campos.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegistoApp()
    window.show()
    sys.exit(app.exec_())
