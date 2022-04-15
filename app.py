






import email
from mailbox import NotEmptyError
from msilib.schema import Class
from pickle import GET

from unicodedata import name
from xml.etree.ElementTree import Comment
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json
import mysql.connector
from sqlalchemy import true



app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/meubanco' 
#root = Usuario, : = espaço para senha, @ = provedor (ip ou localhost) 
# / = nome do bando de dados.

banco = SQLAlchemy(app)
#SQLAlchemy recebe o Flask (app)

db = SQLAlchemy(app) #processo de automatização da criação do banco

#criação do model
class usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100))
    
    def to_json(self):
        return {"id": self.id, "nome": self.nome, "email": self.email }
    
#selecionar usuarios
@app.route("/usuarios", methods=["GET"])
def seleciona_usuarios():
  usuario_class =  usuario.query.all()
  usuario_json = [usuario.to_json() for usuario in usuario_class ]
  print(usuario_json)
  return gerar_response(200, "usuarios", usuario_json, "Okay")
  

#selecionar usuario individual
@app.route("/usuario/<id>", methods=["GET"])
def seleciona_usuario(id):
    usuario_class = usuario.query.filter_by(id=id).first()
    usuario_json = usuario_class.to_json()
    
    return gerar_response(200, "usuario", usuario_json)


#Cadastrar um usuario
@app.route("/usuario", methods=["POST"])
def cria_usuario():
    body = request.get_json()
    
    
    #validar algum erro
    try:
        global usuario
        usuario = usuario(nome = body["nome"], email = body["email"]) #cria usuario
        db.session.add(usuario) #abre sessão e add classe
        db.session.commit() #comita o que foi escrito
        
        return gerar_response(201, "usuario", usuario.to_json(), "Criado com Sucesso")

    except Exception as e:
       print(e)
       return gerar_response(400, "usuario", {}, "Erro ao cadastrar usuario")

    
#atualizar o usuario
@app.route("/usuario/<id>", methods = ["PUT"])
def atualiza_usuario(id):
    usuario_class = usuario.query.filter_by(id=id).first() #pega o usuario
    body = request.get_json() #pega as modificações
    
    try:
        if('nome' in body):
          usuario_class.nome = body["nome"]
          
        if('email' in body):  
          usuario_class.email = body["email"]
          
        db.session.add(usuario_class)
        db.session.commit()
        
        return gerar_response(200, "usuario", usuario_class.to_json(), "Atualizado com Sucesso")
    
    except Exception as e:
        print(e)
        return gerar_response(400, "usuario", {}, "Erro ao atualizar")
       
    

#deletar o usuario
@app.route("/usuario/<id>", methods = ["DELETE"])
def deleta_usuario(id):
    usuario_class = usuario.query.filter_by(id=id).first() #pega o usuario
    
    try:
        db.session.delete(usuario_class)
        db.session.commit()
        return gerar_response(200, "usuario", usuario_class.to_json(), "Deletado com Sucesso!")
    
    except Exception as e:
        print(e)
        return gerar_response(400, "usuario", {}, "Erro ao Deletar")
    
    


    
#gerar response automatico
def gerar_response(status, nome_do_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_do_conteudo] = conteudo
    
    if(mensagem):
        body["mensagem"] = mensagem
        
    return Response(json.dumps(body), status=status, mimetype="aplication/json")
    


app.run()








