# Imports da lib padrão

# Imports de terceiros
import PySimpleGUI as sg

# Imports de módulos próprios

'''
Arquivo de configuração dos layouts das telas e opções de design.
Mudanças na aparência do app devem ser feitas aqui.

'''

class ConfigDoApp():

    def __init__(self) -> None:
        self.tema = sg.theme("DarkGrey")
        self.tamanho_da_janela = (250,450)
    
    def layout_tela_inicial(self, values = []):
        return [[sg.Text("Contatos:")],
                [sg.Listbox(values, size=(100, 20),
                key="-LIST-", enable_events=True )],
                [sg.Button("Adicionar")]]
       
    def layout_tela_cadastro(self, nome = "", celular = "", fixo = "", fax = ""):
        return [[sg.Text("Nome*")],
                [sg.Input(key="-NOME-", default_text="{0}".format(nome))],
                [sg.Text("Telefone celular")],
                [sg.Input(key="-CELULAR-", default_text="{0}".format(celular))],
                [sg.Text("Telefone fixo")],
                [sg.Input(key="-FIXO-", default_text="{0}".format(fixo))],
                [sg.Text("Fax")],
                [sg.Input(key="-FAX-", default_text="{0}".format(fax))],
                [sg.Button("Salvar"), sg.Button("Cancelar")]]

    def layout_tela_contato(self):
        return  [[sg.Output(size=(200,6))],
                 [sg.Button("Editar"), sg.Button("Apagar")]]
    

                