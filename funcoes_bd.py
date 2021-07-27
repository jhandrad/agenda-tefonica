# Imports da lib padrão
import sqlite3
from contextlib import closing
from sqlite3.dbapi2 import Connection, Cursor

# Imports de terceiros

# Imports de móduos próprios

'''
Arquivo que contém as funções que alteram ou realizam consultas
ao banco de dados.

'''

def abre_conexao_cursor() -> tuple[Connection, Cursor]:
    conexao = sqlite3.connect("agenda.db")
    cursor = conexao.cursor()
    return conexao, cursor


def fecha_conexao_cursor(conexao: Connection, cursor: Cursor) -> None:
    cursor.close()
    conexao.close()
    

def cria_tabela_bd() -> None:
    conexao, cursor = abre_conexao_cursor()
    cursor.execute('''
                    create table agenda(
                        chave text,
                        nome text,
                        celular text,
                        fixo text,
                        fax text
                    )''')
    conexao.commit()
    fecha_conexao_cursor(conexao, cursor)


def adiciona_bd(values: dict) -> bool:
    conexao, cursor = abre_conexao_cursor()
    existe = False
    cursor.execute("select chave from agenda")
    while True:
        resultado = cursor.fetchone()
        if resultado == None:
            break
        if resultado[0] == values["-CHAVE-"]:
            existe = True
    if existe == False:
        cursor.execute('''
                        insert into agenda (chave, nome, celular,
                                            fixo, fax) 
                                        values(?, ?, ?, ?, ?)''',
                        (values["-CHAVE-"], values["-NOME-"],
                        values["-CELULAR-"], values["-FIXO-"],
                        values["-FAX-"]))
    conexao.commit()
    fecha_conexao_cursor(conexao, cursor)
    return not existe


def remove_bd(chave: str) -> bool:
    apagado = False
    conexao, cursor = abre_conexao_cursor()
    cursor.execute('''delete from agenda
                        where chave = ?''', (chave,))
    if cursor.rowcount == 1:
        conexao.commit()
        apagado = True
    fecha_conexao_cursor(conexao, cursor)
    return apagado


def retorna_contato_bd(chave: str) -> any:
    conexao, cursor = abre_conexao_cursor()
    cursor.execute('''select nome,celular,fixo,fax from agenda
                        where chave = ?''', (chave,))
    resultado = cursor.fetchone()
    if resultado == None:
        fecha_conexao_cursor(conexao, cursor)
        raise ValueError
    else:
        fecha_conexao_cursor(conexao, cursor)
        return resultado


def edita_contato_bd(chave: str, values: dict) -> None:
    conexao, cursor = abre_conexao_cursor()
    cursor.execute('''update agenda set chave = ?, nome = ?,
                        celular = ?, fixo = ?, fax = ?
                        where chave = ?''',
                        (values["-CHAVE-"], values["-NOME-"],
                        values["-CELULAR-"], values["-FIXO-"],
                        values["-FAX-"], chave))
    conexao.commit()
    fecha_conexao_cursor(conexao, cursor)


def retorna_nomes_bd() -> list:
    conexao, cursor = abre_conexao_cursor()
    lista = []
    cursor.execute("select nome from agenda")
    while True:
        resultado = cursor.fetchone()
        if resultado == None:
            break
        lista.append(resultado[0])
    fecha_conexao_cursor(conexao, cursor)
    return lista
