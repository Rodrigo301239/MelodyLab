from flask import Flask, render_template, request, url_for, redirect, flash, session
app = Flask(__name__)
app.secret_key = "chave_muito_segura"
import database

# Cria um dicionário e usuários e senha, SERÁ MIGRADO PARA O BANCO DE DADOS


@app.route('/') #rota para a página inicial
def index():
    return render_template('index.html')

@app.route('/home')
def home():
     musicas = database.pegar_musicas(session ['usuario'])
     return render_template('home.html',musicas = musicas)



@app.route("/login",methods = ["GET","POST"])
def login():
    if request.method == "POST":
        form =  request.form
        if database.login(form) == True:
           session['usuario']= form ['email']
           return redirect(url_for('home'))
        
        else:
            return ("erro")
    else:
        return render_template('login.html')

@app.route('/cadastro',methods = ["GET","POST"]) #rota para a página de login
def cadastro():
    if request.method == "POST":
        form = request.form
        if database.criar_conta(form) == True:
            return render_template('login.html')
        
        else:
            return ("erro")
    else:
        return render_template('cadastro.html')
    
@app.route('/apagar')
def excluir_usuario():
    email = session['usuario']

    if database.excluir_usuario(email):
        return redirect(url_for('login'))
    else:
        return "Ocorreu um erro ao excluir o usuário"

@app.route('/criar',methods = ["GET","POST"])
def criar():
    if request.method == "GET":
        return render_template('criar.html')
    
    elif request.method == "POST":
        form = request.form
        nome_musica = form ['nome_musica']
        artista = form ['artista']
        status = form ['status']
        imagem = form ['imagem']
        letra = form ['letra']
        id_usuario = session ['usuario']
        database.criar_musica (id_usuario, nome_musica, artista, status, letra, imagem)
        return redirect(url_for('home'))
    
    else:
        return "agua gelada"
    
    
@app.route('/editar', methods = ["GET","POST"])
def editar():
    if request.method == "GET":
        return render_template('editar.html')
    
    else:
        print("davi viado")
    
  
    

    

# parte principal do
if __name__ == '__main__':
    app.run(debug=True)