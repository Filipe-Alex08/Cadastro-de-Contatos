from json import load, dump

def obter_contatos():
    with open('banco.json', 'r', encoding='utf-8') as arquivo_json:
        contatos = load(arquivo_json)
    return contatos

def filtrar_contatos(tipo: str = "", ordem: str = "", desc: bool = False):
    print(desc)
    with open('banco.json', 'r', encoding='utf-8') as arquivo_json:
        contatos = load(arquivo_json)
    if tipo:
        contatos = [c for c in contatos if c.get('tipo') == tipo]
    if ordem:
        contatos.sort(key=lambda c: c.get(ordem), reverse=bool(desc))
    return contatos

def gravar_contato(novo_contato: dict):
    with open('banco.json', 'r+', encoding='utf-8') as arquivo_json:
        contatos: list = load(arquivo_json)
        contatos.append(novo_contato)
        arquivo_json.seek(0)
        dump(contatos, arquivo_json, indent=True, ensure_ascii=False)
        arquivo_json.truncate()
    return contatos

def apagar_contato(email: str):
    with open('banco.json', 'r+', encoding='utf-8') as arquivo_json:
        contatos: list = load(arquivo_json)
        remover = None
        for contato in contatos:
            if contato.get('email') == email:
                remover = contato
                break
        if contato:
            contatos.remove(contato)
            arquivo_json.seek(0)
            dump(contatos, arquivo_json, indent=True, ensure_ascii=False)
            arquivo_json.truncate()
    return contatos

def substituir_contato(novo_contato: dict):
    with open('banco.json', 'r+', encoding='utf-8') as arquivo_json:
        contatos: list = load(arquivo_json)
        indice = None
        for i in range(len(contatos)):
            if contatos[i].get('email') == novo_contato.get('email'):
                indice = i
                break
        if indice:
            contatos.pop(i)
            contatos.insert(i, novo_contato)
            arquivo_json.seek(0)
            dump(contatos, arquivo_json, indent=True, ensure_ascii=False)
            arquivo_json.truncate()
    return contatos
