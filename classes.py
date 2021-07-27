# imports da lib padrão
from typing import Type
from functools import total_ordering
import os
# imports de terceiros

# imports de módulos próprios
import funcoes_bd

'''
Arquivo que contem as classes responsáveis pelo funcionamento
da agenda. Poderiamos dizer que é o back-end.

'''

class ListaUnica(): # classe legada da versão sem BD

    def __init__(self, tipo_elemento: Type) -> None:
        self.tipo_dos_elementos = tipo_elemento
        self.lista = []

    def __iter__(self):
        return iter(self.lista)

    def __len__(self) -> int:
        return len(self.lista)

    def __getitem__(self, indice: int):
        return self.lista[indice]

    def adiciona_elemento(self, elemento) -> bool:
        if (self.verifica_tipo(elemento) and not
            self.pesquisa_elemento(elemento)):

            self.lista.append(elemento)
            return True

        return False

    def remove_elemento(self, elemento) -> bool:
        if len(self.lista) > 0 and self.pesquisa_elemento(elemento):
            self.lista.remove(elemento)
            return True
        return False

    def verifica_tipo(self, elemento) -> bool:
        return type(elemento) == self.tipo_dos_elementos
    
    def pesquisa_elemento(self, elemento) -> bool:
        return elemento in self.lista
        

class ListaDeContatos(ListaUnica): # classe legada da versão sem BD
    
    def __init__(self) -> None:
        super().__init__(Contato)


@total_ordering
class Contato():
    
    def __init__(self, values: dict) -> None:
        self.nome = values["-NOME-"]
        self.celular = values["-CELULAR-"]
        self.fixo = values["-FIXO-"]
        self.fax = values["-FAX-"]

    def __str__(self) -> str:
        contato = (
        "Nome: {0}\nCelular: {1}\nFixo: {2}\nFax:{3}".format(
                                                        self.nome,
                                                        self.celular,
                                                        self.fixo,
                                                        self.fax))

        return contato

    def __eq__(self, o: object) -> bool:
        return self.__chave == o.__chave

    def __lt__(self, o: object) -> bool:
        return self.nome < o.nome

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def chave(self) -> str:
        return self.__chave

    @nome.setter
    def nome(self, valor: str) -> None:
        if valor == None or not valor.strip():
            raise ValueError("Nome não pode ser nulo nem em branco")
        self.__nome = valor
        self.__chave = Contato.cria_chave(valor)

    @staticmethod
    def cria_chave(cls: str) -> str:
        return cls.strip().lower()

    def edita_contato(self, values: dict) -> None:
        self.nome = values["-NOME-"]
        self.celular = values["-CELULAR-"]
        self.fixo = values["-FIXO-"]
        self.fax = values["-FAX-"]

    def retorna_dados(self) -> dict:
        resultado = {"-CHAVE-": self.__chave,
                     "-NOME-": self.__nome,
                     "-CELULAR-": self.celular,
                     "-FIXO-": self.fixo,
                     "-FAX-": self.fax}
        return resultado


class Agenda():

    def __init__(self) -> None:
        novo = not os.path.isfile("agenda.db")
        if novo:
            funcoes_bd.cria_tabela_bd() 

    def adiciona_contato(self, values: dict) -> bool:
        dados_contato = self.cria_contato_retorna_dados(values)
        return funcoes_bd.adiciona_bd(dados_contato)

    def remove_contato(self, nome: str) -> bool:
        chave = self.cria_chave(nome)
        return funcoes_bd.remove_bd(chave) 

    def exibe_contato(self, nome: str) -> Contato:
        chave = self.cria_chave(nome)
        dados_bd = funcoes_bd.retorna_contato_bd(chave)
        values = {"-NOME-": dados_bd[0],
                  "-CELULAR-": dados_bd[1],
                  "-FIXO-": dados_bd[2],
                  "-FAX-": dados_bd[3]}
        contato = Contato(values)
        return contato

    def edita_contato(self, nome: str, values: dict) -> None:
        dados_contato = self.cria_contato_retorna_dados(values)
        chave = self.cria_chave(nome)
        funcoes_bd.edita_contato_bd(chave, dados_contato)

    def retorna_dados(self, nome: str) -> any:
        chave = self.cria_chave(nome)
        dados_bd = funcoes_bd.retorna_contato_bd(chave)
        return dados_bd

    def retorna_nomes(self) -> list:
        return funcoes_bd.retorna_nomes_bd()

    def cria_chave(self, nome: str) -> str:
        return nome.lower().strip()

    def cria_contato_retorna_dados(self, values: dict) -> dict:
        contato = Contato(values)
        return contato.retorna_dados()

