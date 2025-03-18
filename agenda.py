import sqlite3
import PySimpleGUI as sg
#import schedule
import time
from PySimpleGUI import Push, VSeparator, HSeparator

sg.theme("DarkGray")
fonte = ("Helvica", 11, "bold")

# Criar e conectar ao banco de dados
conn = sqlite3.connect("agenda.db")
cursor = conn.cursor()
#banco de dados
# Criar tabela se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        dia INTEGER NOT NULL,
        mes INTEGER NOT NULL,
        horario TEXT NOT NULL,
        descricao TEXT
    )
''')
conn.commit()

# Função para inserir um novo evento no banco de dados
def salvar_evento(nome, dia, mes, descricao):
    cursor.execute("INSERT INTO eventos (nome, dia, mes, descricao) VALUES (?, ?, ?, ?)", (nome, dia, mes, descricao))
    conn.commit()

# Função para buscar todos os eventos
def listar_eventos():
    cursor.execute("SELECT * FROM eventos")
    return cursor.fetchall()

# Função para excluir um evento
def excluir_evento(id_evento):
    cursor.execute("DELETE FROM eventos WHERE id = ?", (id_evento,))
    conn.commit()

# Função para atualizar um evento
def editar_evento(id_evento, nome, dia, mes, descricao):
    cursor.execute("UPDATE eventos SET nome=?, dia=?, mes=?, descricao=? WHERE id=?", (nome, dia, mes, descricao, id_evento))
    conn.commit()

# Função para criar a tela inicial
def telaInicial():
    layout = [
        [sg.Image(filename="./imagem/img.png")],
        [sg.Push(), sg.Text("NOME DO EVENTO", font=fonte), sg.Push()],
        [sg.Push(), sg.Input(font=fonte, key="nome"), sg.Push()],
        [sg.Push(), sg.Text("DATA", font=fonte), sg.Push()],
        [sg.Push(), sg.Text("Dia:", font=fonte), sg.Combo([str(i) for i in range(1, 32)], font=fonte, key="dia"), 
         sg.Text("Mês:", font=fonte), sg.Combo([str(i) for i in range(1, 13)], font=fonte, key="mes"), sg.Text("HORA", font=(fonte)), sg.Input(key="horario", font=fonte, size=(5,1)), sg.Push()],
        [sg.Text(" ")],
        [sg.Push(), sg.Text("DESCRIÇÃO", font=fonte), sg.Push()],
        [sg.Push(), sg.Multiline(key="descricao", size=(30, 3), font=(fonte)), sg.Push()],
        [sg.HSeparator()],
        [sg.Push(), sg.Button("SAIR", font=fonte, key="sair", button_color=("White", "#ED2024")), sg.Button("VER EVENTOS", font=fonte, key="detalhes", button_color=("White", "#008080")),
         sg.Button("SALVAR", font=fonte, key="salvar", button_color=("White", "#228B22")), sg.Push()]
    ]

    return sg.Window("AGENDA", finalize=True, layout=layout, size=(600, 500), element_justification="center")

def TelaDetalhes():
    eventos = listar_eventos()

    layout = [
        [sg.Push(), sg.Text("DETALHES DOS EVENTOS", font=fonte), sg.Push()],
        [sg.Table(values=eventos, headings=["ID", "Nome", "Dia", "Mês", "Descrição"],
                  auto_size_columns=False, justification="center",
                  col_widths=[5, 15, 5, 5, 30], key="tabela_eventos",
                  enable_events=True, select_mode=sg.TABLE_SELECT_MODE_BROWSE, font=(fonte), size=(20,20))],
        [sg.HSeparator()],
        [sg.Push(), 
         sg.Button("SAIR", font=fonte, key="voltar", button_color=("White", "#ED2024")),
         sg.Button("EXCLUIR", font=fonte, key="excluir", button_color=("White", "#8B0000")),
         sg.Button("EDITAR", font=fonte, key="editar", button_color=("White", "#008080")),
         sg.Push()]
    ]

    return sg.Window("DETALHES", finalize=True, layout=layout, size=(600, 500), element_justification="center")


def TelaEditar(id_evento, nome_atual, dia_atual, mes_atual, descricao_atual):
    layout = [
        [sg.Push(), sg.Text("EDITAR EVENTO", font=fonte), sg.Push()],
        [sg.Push(), sg.Text("NOME DO EVENTO", font=fonte), sg.Push()],
        [sg.Push(), sg.Input(font=fonte, key="nome", default_text=nome_atual), sg.Push()],
        [sg.Push(), sg.Text("DATA", font=fonte), sg.Push()],
        [sg.Push(), sg.Text("Dia:", font=fonte), sg.Combo([str(i) for i in range(1, 32)], font=fonte, key="dia", default_value=str(dia_atual)),
         sg.Text("Mês:", font=fonte), sg.Combo([str(i) for i in range(1, 13)], font=fonte, key="mes", default_value=str(mes_atual)), sg.Push()],
        [sg.Text(" ")],
        [sg.Push(), sg.Text("DESCRIÇÃO", font=fonte), sg.Push()],
        [sg.Push(), sg.Multiline(key="descricao", size=(30, 3), font=(fonte), default_text=descricao_atual), sg.Push()],
        [sg.HSeparator()],
        [sg.Push(), sg.Button("CANCELAR", font=fonte, key="cancelar", button_color=("White", "#ED2024")), sg.Button("SALVAR", font=fonte, key="salvar_edicao", button_color=("White", "#228B22")), sg.Push()]
    ]

    return sg.Window("EDITAR EVENTO", finalize=True, layout=layout, size=(600, 350), element_justification="center")

janela1, janela2, janela3 = telaInicial(), None, None

while True:
    window, event, values = sg.read_all_windows()

    if event == "sair" or event == sg.WIN_CLOSED:
        break
    
    if event == "detalhes":
        janela1.hide()
        janela2 = TelaDetalhes()
    if event == "voltar":
        janela1.un_hide()
        janela2.Close()

    if event == "cancelar":
        janela3.close()
        janela2 = TelaDetalhes()

    if event == "salvar":
        escolha = sg.PopupYesNo("DESEJA SALVAR")
        if escolha == "Yes":    
            nome = values["nome"]
            dia = values["dia"]
            mes = values["mes"]
            descricao = values["descricao"]
            salvar_evento(nome, dia, mes, descricao)
            sg.Popup("SALVO COM SUCESSO !!")
            janela1.Close()
            janela1 = telaInicial()
    
    if event == "excluir":
        try:
            selecionado = values["tabela_eventos"][0]  # Obtém o índice da linha selecionada
            id_evento = listar_eventos()[selecionado][0]    # Obtém o ID do evento
            confirmacao = sg.popup_yes_no(f"Tem certeza que deseja excluir o evento ID {id_evento}?")

            if confirmacao == "Yes":
                excluir_evento(id_evento)  # Chama a função para excluir
                sg.popup("Evento excluído com sucesso!")
                janela2.close()
                janela2 = TelaDetalhes()  # Reabre a tela para atualizar os dados
        except IndexError:
            sg.popup("Selecione um evento para excluir.")
    
    if event == "salvar_edicao":
        escolha = sg.PopupYesNo("DESEJA SALVAR?")
        if escolha == "Yes":    
            nome = values["nome"]
            dia = values["dia"]
            mes = values["mes"]
            descricao = values["descricao"]
            
            # Chama a função para editar o evento no banco de dados
            editar_evento(id_evento, nome, dia, mes, descricao)
            
            sg.Popup("EVENTO EDITADO COM SUCESSO !!")
            janela3.close()  # Fecha a janela de edição
            janela2 = TelaDetalhes()  # Reabre a janela de detalhes para atualizar a lista de eventos


    if event == "editar":
        try:
            selecionado = values["tabela_eventos"][0]  # Obtém o índice da linha selecionada
            evento_selecionado = listar_eventos()[selecionado]
            id_evento = evento_selecionado[0]
            nome_atual = evento_selecionado[1]
            dia_atual = evento_selecionado[2]
            mes_atual = evento_selecionado[3]
            descricao_atual = evento_selecionado[4]
            janela2.hide()
            janela3 = TelaEditar(id_evento, nome_atual, dia_atual, mes_atual, descricao_atual)

        except IndexError:
            sg.popup("Selecione um evento para editar.")
