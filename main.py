import tkinter as tk
from tkinter import scrolledtext
import threading
import sys
import time
import Servidor 
import locale
from pathlib import Path
import getpass
from datetime import datetime

locale.setlocale(locale.LC_TIME, 'pt_BR.utf-8') # Configurar a localização para o padrão brasileiro
ultima_atualizacao = "" # Variável global para armazenar a data e hora da última atualização
dados = ""  # Variável global para armazenar os dados
data_atual = datetime.now() # Obtém a data atual
data_string = data_atual.strftime('%d%m%Y') # Formata a data no padrão brasileiro (dd/mm/aaaa)

#Função que coleta o nome do usuario logado na maquina
def get_username():
    return getpass.getuser()

#Cria o arquivo .txt para salvar as informações do servidor (log)
def create_log_file():
    data_atual = datetime.now() # Obtém a data atual
    data_string = data_atual.strftime('%d%m%Y') # Formata a data no padrão brasileiro (dd/mm/aaaa)
    name_user = get_username()
    log_file = f"C:\\Users\\{name_user}\\Desktop\\LogSERVIDOR\\{data_string}_Servidor_LOG.txt"
    path = Path(f"C:\\Users\\{name_user}\\Desktop\\LogSERVIDOR")
    path.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'a') as arquivo:
        pass
    return log_file

# Função para redirecionar a saída para a área de texto
def redirecionar_saida():
    class StdoutRedirector(object):
        def __init__(self, widget):
            self.widget = widget

        def write(self, str):
            global ultima_atualizacao
            if not ultima_atualizacao:
                ultima_atualizacao = time.strftime("%d/%m/%Y %H:%M")
                texto = f"{ultima_atualizacao}: {str}"
            else:
                texto = str
            self.widget.insert(tk.END, texto)
            self.widget.see(tk.END)

            LOG = create_log_file()

            # Escrever os dados no arquivo log
            with open(LOG, "a") as arquivo:
                arquivo.write(texto + "\n")

    sys.stdout = StdoutRedirector(text_widget)

# Função para coletar dados a cada 1 minuto e atualizar o rótulo
def coletar_e_atualizar():
    global dados
    while True:
        dados = Servidor.info_interface()  
        atualizar_label()
        time.sleep(5)  # Atualizar a cada 60 segundos 

# Função para atualizar o rótulo com os dados coletados
def atualizar_label():
    label_dados.config(text=f"{dados}")

# Função para atualizar a área de texto em tempo real
def atualizar_info():
    global ultima_atualizacao
    ultima_atualizacao = ""  # Limpar a última atualização ao final
    text_widget.after(1000, atualizar_info)  # Atualizar a cada segundo

# Inicializar a janela tkinter
root = tk.Tk()
root.title("Servidor - Tomate Cereja")

# Criar um rótulo para descrever a área de texto
label = tk.Label(root, text="ATUALIZAÇÕES DO SERVIDOR", fg="red")
label.pack()

# Criar uma área de texto para exibir informações
text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
text_widget.pack()

# Redirecionar a saída para a área de texto
redirecionar_saida()

# Iniciar a função Servidor.interface() em uma thread separada
def executar_interface():
    Servidor.interface()

interface_thread = threading.Thread(target=executar_interface)
interface_thread.start()

# Criar um rótulo para exibir os dados coletados
label_dados = tk.Label(root, text=f"{dados}")
label_dados.pack()

# Iniciar a thread para coletar dados e atualizar o rótulo
coleta_thread = threading.Thread(target=coletar_e_atualizar)
coleta_thread.start()

# Iniciar a atualização da área de texto em tempo real
atualizar_info()

root.mainloop()
