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
    return render_template('home.html')

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

    

# parte principal do
if __name__ == '__main__':
    app.run(debug=True)