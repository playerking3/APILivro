from flask import Flask, jsonify, request, session
from main import app, db
from models import Livro, Usuario
from flask_bcrypt import check_password_hash

@app.route('/livro', methods=['GET'])
def get_livro():
    livros = Livro.query.all()
    livros_dic = []
    for livro in livros:
        livro_dic = {
            'id_livro': livro.id_livro,
            'titulo': livro.titulo,
            'autor': livro.autor,
            'ano_publicacao': livro.ano_publicacao
        }
        livros_dic.append(livro_dic)
    return jsonify(
        mensagem='Lista de Livros',
        livros= livros_dic
    )

@app.route('/livro', methods=['POST'])
def post_livro():
    livro = request.json
    novoLivro = Livro(
        id_livro=livro.get('id_livro'),
        titulo = livro.get('titulo'),
        autor = livro.get('autor'),
        ano_publicacao = livro.get('ano_publicacao')
    )
    db.session.add(novoLivro)
    db.session.commit()

    return jsonify(
        mensagem='Livro cadastrado com sucesso',
        livro={
            'id_livro': novoLivro.id_livro,
            'titulo': novoLivro.titulo,
            'autor': novoLivro.autor,
            'ano_publicacao': novoLivro.ano_publicacao
        }
    )


@app.route('/livro/<int:id_livro>', methods=['PUT'])
def put_livro(id_livro):
    # Verifica se o usuário está autenticado
    if 'id_usuario' in session:
        # Obtém o livro pelo ID fornecido
        livro = Livro.query.get(id_livro)

        if livro:
            # Atualiza os dados do livro com base nos dados enviados
            data = request.json
            livro.titulo = data.get('titulo', livro.titulo)
            livro.autor = data.get('autor', livro.autor)
            livro.ano_publicacao = data.get('ano_publicacao', livro.ano_publicacao)

            # Salva as mudanças no banco de dados
            db.session.commit()

            return jsonify(
                mensagem='Livro atualizado com sucesso',
                livro={
                    'id_livro': livro.id_livro,
                    'titulo': livro.titulo,
                    'autor': livro.autor,
                    'ano_publicacao': livro.ano_publicacao
                }
            )

        else:
            return jsonify({'mensagem': 'Livro não encontrado'})
    else:
        return jsonify({'mensagem': 'Requer Autorização'})

@app.route('/livro/<int:id_livro>', methods=['DELETE'])
def delete_livro(id_livro):
    # Verifica se o usuário está autenticado
    if 'id_usuario' in session:
        # Obtém o livro pelo ID fornecido
        livro = Livro.query.get(id_livro)

        if livro:
            # Remove o livro do banco de dados
            db.session.delete(livro)
            db.session.commit()

            return jsonify({'mensagem': 'Livro excluído com sucesso'})
        else:
            return jsonify({'mensagem': 'Livro não encontrado'})
    else:
        return jsonify({'mensagem': 'Requer Autorização'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')

    # Consulta o usuário no banco de dados pelo email fornecido
    usuarios = Usuario.query.filter_by(email=email).first()
    senha = check_password_hash(usuarios.senha, senha)

    # Verifica se o e-mail está cadastrado e se a senha está correta
    if usuarios and senha:
        # Salva o email do usuário na sessão
        session['id_usuario'] = usuarios.id_usuario
        return jsonify({'mensagem': 'Login com sucesso'}), 200
    else:
        # Se as credenciais estiverem incorretas, retorna uma mensagem de erro
        return jsonify({'mensagem': 'Email ou senha inválido'})

# Rota para fazer logout
@app.route('/logout', methods=['POST'])
def logout():
    # Remove o email da sessão, efetivamente fazendo logout
    session.pop('id_usuario', None)
    return jsonify({'mensagem': 'Logout bem Sucedido'})