import tkinter as tk
from tkinter import scrolledtext
import threading
import sys
import time
import Servidor 
import locale

# Configurar a localização para o padrão brasileiro
locale.setlocale(locale.LC_TIME, 'pt_BR.utf-8')

# Variável global para armazenar a data e hora da última atualização
ultima_atualizacao = ""

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

    sys.stdout = StdoutRedirector(text_widget)

# Função para chamar a função Servidor.interface() em uma thread separada
def executar_interface():
    Servidor.interface()

# Função para atualizar a área de texto em tempo real
def atualizar_info():
    global ultima_atualizacao
    ultima_atualizacao = ""  # Limpar a última atualização ao final
    text_widget.after(1000, atualizar_info)  # Atualizar a cada segundo

# Inicializar a janela tkinter
root = tk.Tk()
root.title("Servidor - IOT Tomate Cereja")

# Criar um rótulo para descrever a área de texto
label = tk.Label(root, text="ATUALIZAÇÕES DO SERVIDOR:")
label.pack()

# Criar uma área de texto para exibir informações
text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
text_widget.pack()

# Redirecionar a saída para a área de texto
redirecionar_saida()

# Iniciar a função Servidor.interface() em uma thread separada
interface_thread = threading.Thread(target=executar_interface)
interface_thread.start()

# Iniciar a atualização da área de texto em tempo real
atualizar_info()

root.mainloop()
