import sys
import pickle
import os
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QLineEdit, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Cebrac")
        self.setGeometry(100, 100, 400, 200)

        # Carregar dados salvos (ou criar dados iniciais se não existirem)
        try:
            with open("computers_data.pickle", "rb") as arquivo:
                dados = pickle.load(arquivo)
                self.computers_laboratory = dados.get("laboratory", 16)
                self.computers_maintenance = dados.get("maintenance", 4)
        except FileNotFoundError:
            self.computers_laboratory = 16
            self.computers_maintenance = 4

        # Criando os widgets de texto fixo com as informações iniciais
        self.texto_fixo1 = QLabel(f"PCs Laboratório: {self.computers_laboratory}", self)
        self.texto_fixo2 = QLabel(f"PCs Manutenção: {self.computers_maintenance}", self)

        # Criando entradas para identificação do PC e motivo da manutenção
        self.input_identificacao = QLineEdit(self)
        self.input_motivo = QLineEdit(self)

        # Criando um layout vertical para os widgets
        layout = QVBoxLayout()
        layout.addWidget(self.texto_fixo1)
        layout.addWidget(self.texto_fixo2)
        layout.addWidget(QLabel("Identificação do PC:", self))
        layout.addWidget(self.input_identificacao)
        layout.addWidget(QLabel("Motivo da Manutenção:", self))
        layout.addWidget(self.input_motivo)

        # Criando botões para transferir
        botao_manutencao = QPushButton("Para a Manutenção", self)
        botao_laboratorio = QPushButton("Para o Laboratório", self)

        # Conectando os botões aos métodos correspondentes
        botao_manutencao.clicked.connect(self.to_maintenance)
        botao_laboratorio.clicked.connect(self.to_laboratory)

        # Adicionando os botões ao layout
        layout.addWidget(botao_manutencao)
        layout.addWidget(botao_laboratorio)

        # Criando um widget central para o layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def to_maintenance(self):
        identificacao = self.input_identificacao.text()
        motivo = self.input_motivo.text()
        if self.computers_laboratory >= 1:
            if identificacao and motivo:
                try:
                    identificacao_int = int(identificacao)
                    self.computers_laboratory -= 1
                    self.computers_maintenance += 1
                    self.atualizar_textos()
                    self.salvar_dados()
                    self.open_csv()
                except ValueError:
                    QMessageBox.warning(self, "Aviso", "A identificação deve ser um número inteiro!")
            else:
                QMessageBox.warning(self, "Aviso", "Preencha a identificação e o motivo.")
        else:
            QMessageBox.warning(self, "Aviso", "Não tem computadores suficientes no laboratório.")
    def to_laboratory(self):
        if self.computers_maintenance >0:
            self.computers_maintenance -= 1
            self.computers_laboratory += 1
            self.atualizar_textos()
            self.salvar_dados()
        else:
            QMessageBox.warning(self, "Aviso", "Você precisa de mais computadores de manutenção para enviar para o laboratório")
        # self.computers_maintenance -= 1
        # self.computers_laboratory += 1
        # self.atualizar_textos()
        # self.salvar_dados()

    def atualizar_textos(self):
        self.texto_fixo1.setText(f"PCs Laboratório: {max(self.computers_laboratory, 0)}")
        self.texto_fixo2.setText(f"PCs Manutenção: {max(self.computers_maintenance, 0)}")

    def salvar_dados(self):
        dados = {"laboratory": max(self.computers_laboratory, 0), "maintenance": max(self.computers_maintenance, 0)}
        with open("computers_data.pickle", "wb") as arquivo:
            pickle.dump(dados, arquivo)
    def open_csv(self):
        # Verifica se o arquivo já existe
        arquivo_existe = os.path.exists('computers_log.csv')
        
        with open('computers_log.csv', 'a', newline='') as salvar_arquivo:
            # Defina os nomes das colunas
            colunas = ["identificaçcao", "problema"]
            writer = csv.writer(salvar_arquivo)
            # Escreva o cabeçalho apenas se o arquivo não existir
            if not arquivo_existe:
                writer.writerow(colunas)
            # Escreva os dados
            writer.writerow([self.input_identificacao.text(), self.input_motivo.text()])
        
        with open('computers_log.csv', 'r') as leitor_arquivo:
            leitor = csv.reader(leitor_arquivo)
            for linha in leitor:
                print(linha)

            
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())