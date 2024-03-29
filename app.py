# Importando as bibliotecas necessárias do Flask e Werkzeug
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import NotFound
import math

# Importando as classes e objetos necessários do seu módulo "database"
from database import Character, db

# Criando uma instância do aplicativo Flask
app = Flask(__name__)
CORS(app)

# Configurando o URI do banco de dados PostgreSQL e inicializando o banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:22910922@localhost:5432/rickandmorty"
db.init_app(app)

# Definindo uma rota para a pesquisa de personagens
@app.route('/character', methods=['GET'])
def search_characters():
    try:
        # Obtendo os parâmetros da consulta da URL
        name = request.args.get('name')
        page = int(request.args.get('page', 1))
        per_page = 20

        # Calculando o índice inicial para a paginação
        start = (page - 1) * per_page
        
        # Consultando o banco de dados para personagens que correspondem ao nome fornecido
        characters = Character.query.filter(
            Character.name.ilike(f'%{name}%')
        ).all()

        # Calculando o total de páginas
        total_pages = math.ceil(len(characters) / per_page)
        
        # Obtendo os personagens para a página atual
        characters = characters[start:start+per_page]

        # Criando uma lista de dicionários com informações dos personagens encontrados
        character_list = []
        for character in characters:
            character_dict = {
                'id': character.id,
                'name': character.name,
                'status': character.status,
                'species': character.species,
                'image': character.image
            }
            character_list.append(character_dict)

        # Preparando a mensagem de retorno com base nos resultados da consulta
        return_message = ''
        if not character_list:
            return_message = 'Not found any character with the given name'
        else:
            return_message = "Characters found"

        # Retornando a resposta JSON com os resultados da consulta
        return jsonify({
            'success': True,
            'message': return_message,
            'data': character_list,
            "total_pages": total_pages
        }), 200

    except Exception as e:
        # Lidando com exceções e retornando uma resposta de erro do servidor
        return jsonify({
            'success': False,
            'message': 'Server Error',
            'data': None
        }), 500

# Definindo uma rota para obter informações de um personagem por ID
@app.route('/character/<int:character_id>', methods=['GET'])
def get_character_by_id(character_id):
    try:
        # Consultando o banco de dados para obter o personagem pelo ID fornecido
        character = Character.query.get_or_404(character_id)

        # Criando um dicionário com informações detalhadas do personagem
        character_details = {
            'id': character.id,
            'name': character.name,
            'status': character.status,
            'species': character.species,
            'type': character.type,
            'gender': character.gender,
            'origin_name': character.origin_name,
            'location_name': character.location_name,
            'image': character.image
        }

        # Retornando a resposta JSON com as informações detalhadas do personagem
        return jsonify({
            'success': True,
            'message': 'Character found!',
            'data': character_details
        }), 200

    except NotFound:
        # Lidando com a exceção NotFound (personagem não encontrado) e retornando resposta adequada
        return jsonify({
            'success': False,
            'message': 'Character not found!',
            'data': None
        }), 404

    except Exception as e:
        # Lidando com exceções gerais e retornando uma resposta de erro do servidor
        return jsonify({
            'success': False,
            'message': 'Server Error',
            'data': None
        }), 500

# Iniciando o aplicativo Flask se este script for executado diretamente
if __name__ == '__main__':
    app.run(debug=True)


























# "id": 1,
# "image": "https://rickandmortyapi.com/api/character/avatar/1.jpeg",
# "name": "Rick Sanchez",
# "species": "Human",
# "status": "Alive"


# from sqlalchemy import create_engine, db.Column, Integer, db.String, ForeignKey
# from sqlalchemy.orm import sessionmaker, relationship
# from sqlalchemy.ext.declarative import declarative_base


# engine = create_engine(
#     'postgresql://postgres:22910922@localhost:5432/rickandmorty')
# Base = declarative_base()
# Session = sessionmaker(bind=engine)
# session = Session()
