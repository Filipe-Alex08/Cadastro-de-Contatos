from typing import List
import sqlite3

class RepositorioContato(object):

    @staticmethod
    def dicionario_contato(tupla_dados: tuple) -> dict:

        nome, email, telefone, tipo = tupla_dados

        return {'nome': nome, 'email': email, 
            'telefone': telefone, 'tipo': tipo}
        
    def __init__(self, nome_db: str) -> None:

        self.nome_db = nome_db
        self.connection = None
        self.cursor = None

        self.criar_tabela()
        
    def criar_tabela(self) -> None:

        query = 'CREATE TABLE IF NOT EXISTS contato (nome TEXT, email TEXT PRIMARY KEY, telefone TEXT, tipo TEXT);'
        self.abrir_conexao()
        self.cursor.execute(query)
        self.connection.commit()
        self.fechar_conexao()
        
    def abrir_conexao(self) -> None:

        self.connection = sqlite3.connect(self.nome_db)
        self.cursor = self.connection.cursor()
        
    def fechar_conexao(self) -> None:

        self.cursor.close()
        self.connection.close()
        self.connection = None
        self.cursor = None

    def criar_contato(self, nome: str, email: str, telefone: str, tipo: str) -> None:

        query = 'INSERT INTO contato (nome, email, telefone, tipo) VALUES (?, ?, ?, ?);'
        self.abrir_conexao()
        self.cursor.execute(query, (nome, email, telefone, tipo))
        self.connection.commit()
        self.fechar_conexao()
    
    def consultar_todos_contatos(self) -> List[dict]:

        query = 'SELECT nome, email, telefone, tipo FROM contato;'
        self.abrir_conexao()
        self.cursor.execute(query)
        contatos = self.cursor.fetchall()
        self.fechar_conexao()

        for i in range(len(contatos)):
            contatos[i] = self.dicionario_contato(contatos[i])
        
        return contatos
    
    def filtrar_ordenar_contatos(self, tipo: str = '', 
        ordem: str = '', desc: bool = False) -> List[dict]:

        query_base = 'SELECT nome, email, telefone, tipo FROM contato'
        query_filtro =  " WHERE tipo = ?"
        query_ordem = ' ORDER BY '
        query_desc = ' DESC'
        final = ';'

        query = query_base
        argumentos = ()
        if tipo:
            query += query_filtro
            argumentos += (tipo,)
        if ordem in ('nome', 'email', 'telefone', 'tipo'):
            query += query_ordem + ordem
            if desc:
                query += query_desc
        query += final

        print(query, argumentos)

        self.abrir_conexao()
        self.cursor.execute(query, argumentos)
        contatos = self.cursor.fetchall()
        self.fechar_conexao()

        for i in range(len(contatos)):
            contatos[i] = self.dicionario_contato(contatos[i])
        
        return contatos
    
    def alterar_contato(self, nome: str, email: str, telefone: str, tipo: str) -> None:

        query = 'UPDATE contato SET nome = ?, email = ?, telefone = ?, tipo = ? WHERE email = ?;'
        self.abrir_conexao()
        self.cursor.execute(query, (nome, email, telefone, tipo, email))
        self.connection.commit()
        self.fechar_conexao()
    
    def remover_contato(self, email: str) -> None:

        query = 'DELETE FROM contato WHERE email = ?;'
        self.abrir_conexao()
        self.cursor.execute(query, (email,))
        self.connection.commit()
        self.fechar_conexao()

class RepositorioWebhook(object):
        
    def __init__(self, nome_db: str) -> None:

        self.nome_db = nome_db
        self.connection = None
        self.cursor = None

        self.criar_tabela()
        
    def criar_tabela(self) -> None:

        query = 'CREATE TABLE IF NOT EXISTS webhook (url TEXT PRIMARY KEY);'
        self.abrir_conexao()
        self.cursor.execute(query)
        self.connection.commit()
        self.fechar_conexao()
        
    def abrir_conexao(self) -> None:

        self.connection = sqlite3.connect(self.nome_db)
        self.cursor = self.connection.cursor()
        
    def fechar_conexao(self) -> None:

        self.cursor.close()
        self.connection.close()
        self.connection = None
        self.cursor = None

    def criar_webhook(self, url: str) -> None:

        query = 'INSERT INTO webhook (url) VALUES (?);'
        self.abrir_conexao()
        self.cursor.execute(query, (url,))
        self.connection.commit()
        self.fechar_conexao()
    
    def consultar_todos_webhooks(self) -> List[dict]:

        query = 'SELECT url FROM webhook;'
        self.abrir_conexao()
        self.cursor.execute(query)
        webhooks = self.cursor.fetchall()
        self.fechar_conexao()

        for i in range(len(webhooks)):
            webhooks[i] = webhooks[i][0]
        
        return webhooks
    
    def remover_webhook(self, url: str) -> None:

        query = 'DELETE FROM webhook WHERE url = ?;'
        self.abrir_conexao()
        self.cursor.execute(query, (url,))
        self.connection.commit()
        self.fechar_conexao()