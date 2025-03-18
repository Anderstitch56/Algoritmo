import sqlite3
from datetime import datetime
import PySimpleGUI as sg
import os
import sys

def conectar_bd():
    """ Conecta ao banco de dados na pasta anterior ao executável """

    # Obtém o diretório onde o executável está rodando
    if getattr(sys, 'frozen', False):  # Se rodando como executável
        diretorio_atual = os.path.dirname(sys.executable)
    else:  # Se rodando como script Python
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))

    # Navega para o diretório pai
    diretorio_pai = os.path.dirname(diretorio_atual)

    # Define o caminho correto para o banco de dados (na pasta pai)
    caminho_banco = os.path.join(diretorio_pai, "agenda.db")  

    print(f"Tentando conectar ao banco de dados em: {caminho_banco}")  # Para depuração

    if not os.path.exists(caminho_banco):
        sg.popup_error("Banco de dados não encontrado!", caminho_banco)
        return None, None

    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()
    
    return conn, cursor

def verificar_eventos():
    conn, cursor = conectar_bd()
    
    if conn is None or cursor is None:
        return  

    hoje = datetime.now()
    dia_hoje = hoje.day
    mes_hoje = hoje.month
    
    cursor.execute("SELECT nome, descricao FROM eventos WHERE dia = ? AND mes = ?", (dia_hoje, mes_hoje))
    eventos = cursor.fetchall()

    if eventos:
        for evento in eventos:
            nome, descricao = evento
            sg.popup(f"Evento: {nome}", f"Descrição: {descricao}", title="Lembrete de Evento", font=("Helvetica", 12, "bold"))

    conn.close()

if __name__ == "__main__":
    verificar_eventos()
