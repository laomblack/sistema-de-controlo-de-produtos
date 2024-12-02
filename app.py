from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Banco de dados simples em memória
produtos = {}

class Produto:
    def __init__(self, nome, descricao, preco, quantidade):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.quantidade = quantidade

    def __str__(self):
        return f"{self.nome} - {self.descricao} - R${self.preco:.2f} - {self.quantidade} em estoque"

@app.route('/')
def index():
    return render_template('editar.html', produtos=produtos)

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = float(request.form['preco'])
        quantidade = int(request.form['quantidade'])

        # Adicionando o novo produto ao dicionário de produtos
        id_produto = len(produtos) + 1  # Gerando um ID único
        produtos[id_produto] = {
            'nome': nome,
            'descricao': descricao,
            'preco': preco,
            'quantidade': quantidade
        }

        return redirect(url_for('index'))

    return render_template('editar.html')

@app.route('/editar/<int:id_produto>', methods=['GET', 'POST'])
def editar_produto(id_produto):
    produto = produtos.get(id_produto)
    if not produto:
        return "Produto não encontrado", 404

    if request.method == 'POST':
        produto['nome'] = request.form['nome']
        produto['descricao'] = request.form['descricao']
        produto['preco'] = float(request.form['preco'])
        produto['quantidade'] = int(request.form['quantidade'])

        return redirect(url_for('index'))

    return render_template('editar.html', produto=produto, id_produto=id_produto)

@app.route('/excluir/<int:id_produto>')
def excluir_produto(id_produto):
    if id_produto in produtos:
        del produtos[id_produto]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
