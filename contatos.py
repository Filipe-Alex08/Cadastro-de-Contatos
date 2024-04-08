# import requests
from flask import Flask, render_template, request, abort, session, redirect
from http import HTTPStatus
from secrets import token_hex
from repositorio import RepositorioContato, RepositorioWebhook

app = Flask(__name__)

app.config.from_mapping(SECRET_KEY=token_hex())
repoContato = RepositorioContato('contatos.sqlite')
repoWebhook = RepositorioWebhook('contatos.sqlite')



########## ---------- Informações de erros -------- ##########

@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(erro):
    return (render_template('erro.jinja', codigo=HTTPStatus.NOT_FOUND, 
        mensagem="Página não encontrada"), HTTPStatus.NOT_FOUND)

@app.errorhandler(HTTPStatus.BAD_REQUEST)
def bad_request(erro):
    return render_template('erro.jinja', codigo=HTTPStatus.BAD_REQUEST,
        mensagem="Não foi possível realizar operação"), HTTPStatus.BAD_REQUEST

@app.errorhandler(HTTPStatus.METHOD_NOT_ALLOWED)
def method_not_allowed(erro):
    if request.method == 'GET':
        return (render_template('erro.jinja', codigo=HTTPStatus.NOT_FOUND, 
            mensagem="Página não encontrada"), HTTPStatus.NOT_FOUND)
    else:
        return (render_template('erro.jinja', codigo=HTTPStatus.METHOD_NOT_ALLOWED, 
            mensagem="Método não permitido"), HTTPStatus.METHOD_NOT_ALLOWED) 



########## ---------- Informações das Paginas de Contatos -------- ##########

@app.route('/contatos', methods=['GET'])
def mostrar_contatos():
    tipo = request.args.get('tipo', "")
    ordem = request.args.get('ordem', "")
    desc = request.args.get('desc', "")
    email_editado = request.args.get('email_editado', "")
    if tipo:
        if tipo == 'Todos':
            tipo = ''
        session['tipo'] = tipo
    else:
        tipo = session.get('tipo')
    if ordem:
        session['ordem'] = ordem
    else:
        ordem = session.get('ordem')
    if desc and desc.lower() == 'true':
        desc = True
        session['desc'] = True
    elif desc and desc.lower() == 'false':
        desc = False
        session['desc'] = False
    else:
        desc = session.get('desc')
    contatos = repoContato.filtrar_ordenar_contatos(tipo, ordem, desc)
    return render_template('contatos.jinja', contatos=contatos, 
        email_editado=email_editado)

@app.route('/salvar_contato', methods=['POST'])
def salvar_contato():
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    tipo = request.form.get('tipo')
    if not (nome and email and telefone and tipo):
        abort(HTTPStatus.BAD_REQUEST)
    repoContato.criar_contato(nome, email, telefone, tipo)
    webhooks = repoWebhook.consultar_todos_webhooks()
    # print(webhooks)
    for webhook in webhooks:
        try:
            requests.post(webhook, json={'nome': nome,
                'email': email, 'telefone': telefone,
                'tipo': tipo})
        except:
            print('Bad webhook url: ' + webhook)
    return redirect('/contatos')

@app.route('/remover_contato/<email>', methods=['POST'])
def remover_contato(email: str):
    if not email:
        abort(HTTPStatus.BAD_REQUEST)
    repoContato.remover_contato(email)
    return redirect('/contatos')

@app.route('/editar_contato/<email>', methods=['POST'])
def editar_contato(email: str):
    if not email:
        abort(HTTPStatus.BAD_REQUEST)
    return redirect(f'/contatos?email_editado={email}')

@app.route('/salvar_edicao', methods=['POST'])
def salvar_edicao():
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    tipo = request.form.get('tipo')
    if not (nome and email and telefone and tipo):
        abort(HTTPStatus.BAD_REQUEST)
    repoContato.alterar_contato(nome, email, telefone, tipo)
    return redirect('/contatos')

@app.route('/webhook', methods=['POST'])
def cadastrar_webhook():
    url = request.json.get('url')
    if not url:
        return 'NO URL', HTTPStatus.BAD_REQUEST
    repoWebhook.criar_webhook(url)
    return 'OK', HTTPStatus.OK

@app.route('/webhook', methods=['DELETE'])
def remover_webhook():
    url = request.json.get('url')
    if not url:
        return 'NO URL', HTTPStatus.BAD_REQUEST
    repoWebhook.remover_webhook(url)
    return 'OK', HTTPStatus.OK

if __name__ == '__main__':
    app.run(debug=True)