import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def conectar_banco():
    conexao = sqlite3.connect("tarefas.db")
    return conexao


def criar_tabela():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute("CREATE table if not exists usuarios (email text primary key, nome text, senha text)")
    
    cursor.execute ('''create table if not exists tarefas
                    (id integer primary key,conteudo text,esta_concluida integer,email_usuario text,
                    FOREIGN KEY(email_usuario) REFERENCES usuarios(email))''')
    
    conexao.commit()
    
def criar_conta(cadastrar):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT COUNT (email) FROM usuarios WHERE email=?", (cadastrar['email'],))
    conexao.commit()
    
    quantidade_de_emails = cursor.fetchone()
    if (quantidade_de_emails[0] > 0):
        print ("email já cadastrado, tente novamente")
        return False
    
    senha_criptografada = generate_password_hash (cadastrar['senha'])
    cursor.execute("INSERT into usuarios(email,nome,senha) VALUES (?,?,?)", (cadastrar ['email'], cadastrar['usuario'], senha_criptografada))
    conexao.commit()
    return True

def login(formulario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute('''SELECT (senha) FROM usuarios WHERE email = ?''',(formulario['email'],))
    conexao.commit()
    senha_criptografada = cursor.fetchone()
    return check_password_hash(senha_criptografada[0],formulario['senha'])

def excluir_usuario(email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM tarefas WHERE email_usuario=?',(email,))
    cursor.execute('DELETE FROM usuarios WHERE email=?',(email,))
    conexao.commit()
    return True
   
    
    

# PARTE PRINCIPAL DO PROGRAMA
if __name__ == '__main__':
    criar_tabela()