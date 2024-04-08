import json
from repositorio import RepositorioContato

repo = RepositorioContato('contatos.sqlite')

with open('banco.json', 'r', encoding='utf-8') as arquivo_json:
    dados = json.load(arquivo_json)

for contato in dados:
    repo.criar_contato(contato['nome'], contato['email'], 
        contato['telefone'], contato['tipo'])
