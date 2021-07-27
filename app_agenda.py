# imports da lib padrão

# imports de terceiros
from typing import Literal
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Window

# imports de módulos próprios

from classes import Agenda
from configuracoes import ConfigDoApp

'''Interface gráfica e funções das telas.'''

class App():

    def __init__(self) -> None:
        self.agenda = Agenda()
        self.config = ConfigDoApp()
        self.tela_principal = None
        self.tela_cadastro = None
        self.tela_contato = None
        self.status = None

    def janela_principal(self, values = []) -> Window:
        layout = self.config.layout_tela_inicial()
        return sg.Window("Agenda", layout,
                        size = self.config.tamanho_da_janela,
                        finalize=True)

    def janela_cadastro(self, nome = "", celular = "",
                        fixo = "", fax = "") -> Window:
        layout = self.config.layout_tela_cadastro(nome, celular,
                                                  fixo, fax)
        return sg.Window("Adicionar", layout,
                        size= self.config.tamanho_da_janela,
                        finalize=True)

    def janela_contato(self) -> Window:
        layout = self.config.layout_tela_contato()
        return sg.Window("Contato", layout, size=(200,150), finalize=True)

    def le_tela_contato(self, nome: str) -> None: 
        # tela exibida quando um contato é selecionado
        while True:
                window, event, values = sg.read_all_windows()
                if (window in [self.tela_principal, self.tela_contato]
                    and event == sg.WIN_CLOSED):
                    self.tela_contato.close()
                    self.tela_contato_active = False
                    break
                if window == self.tela_principal and (event == "Adicionar"
                                                      or values["-LIST-"]):
                    self.tela_contato.close()
                    self.tela_contato_active = False
                    break
                if window == self.tela_contato and event == "Editar":
                    self.tela_contato.close()
                    self.tela_contato_active = False
                    dados = self.agenda.retorna_dados(nome)
                    self.tela_cadastro_active = True
                    self.tela_cadastro = self.janela_cadastro(dados[0],
                                                              dados[1],
                                                              dados[2],
                                                              dados[3])
                    self.tela_principal.hide()
                    self.le_tela_cadastro(nome=dados[0], edicao=True)
                    self.tela_cadastro_active = False
                    self.tela_principal.un_hide()
                    break
                if window == self.tela_contato and event == "Apagar":
                    self.tela_contato.close()
                    self.tela_contato_active = False
                    try:
                        self.tela_remove_contato(nome)
                    except:
                        sg.popup_error("Erro na remoção",title=("ERRO"))
                    break
        return

    def le_tela_cadastro(self, edicao: bool, nome = "") -> Literal[-1, 0]:
        # tela para cadastrar dados de um novo contato ou editar existente

        while True:
            event, values = self.tela_cadastro.read()
            if event == sg.WIN_CLOSED:
                self.tela_cadastro.close()
                return -1
            if event == "Cancelar":
                self.tela_cadastro.close()
                break
            if event == "Salvar":
                try:
                    if edicao == True:
                        self.agenda.edita_contato(nome, values)
                    elif edicao == False:
                        self.agenda.adiciona_contato(values)
                except:
                    sg.popup_error("O CAMPO NOME É OBRIGATÓRIO",title=("ERRO"))
                    continue
                self.tela_cadastro.close()
                break
        return 0

    def le_tela_principal(self) -> None:
        pass

    def tela_remove_contato(self, nome: str) -> None:

        resultado = sg.popup_ok_cancel("Apagar contato?")
        if resultado == "OK":
            self.agenda.remove_contato(nome)
            return
        return 

    def inicializa_agenda(self) -> None:

        self.tela_principal = self.janela_principal()
        self.tela_cadastro_active = False
        self.tela_contato_active = False
        while True:
            contatos = self.agenda.retorna_nomes()
            self.tela_principal["-LIST-"].update(contatos)
            event, values = self.tela_principal.read()
            if event == sg.WIN_CLOSED:
                break
            if (values["-LIST-"] and event != "Adicionar"
                and not self.tela_contato_active):

                self.tela_contato_active = True
                self.tela_contato = self.janela_contato()
                print(self.agenda.exibe_contato(values["-LIST-"][0]))
                self.le_tela_contato(values["-LIST-"][0])
            if event == "Adicionar" and not self.tela_cadastro_active:
                self.tela_cadastro_active = True
                self.tela_cadastro = self.janela_cadastro()
                self.tela_principal.hide()
                self.status = self.le_tela_cadastro(edicao=False)
                self.tela_cadastro_active = False
                if self.status == -1:
                    break
                self.tela_principal.un_hide()
        self.tela_principal.close()

app = App()
app.inicializa_agenda()