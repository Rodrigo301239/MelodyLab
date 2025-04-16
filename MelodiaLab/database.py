import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def conectar_banco():
    conexao = sqlite3.connect("musicas.db")
    return conexao


def criar_tabela():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute("CREATE table if not exists usuarios (email text primary key, nome text, senha text)")
    
    cursor.execute("CREATE table if not exists musicas (id integer primary key,id_usuario text, nome_musica text, artista text, status text, letra text, imagem text)")
    
    
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
    cursor.execute("INSERT into usuarios (email,nome,senha) VALUES (?,?,?)", (cadastrar ['email'], cadastrar['usuario'], senha_criptografada))
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
    cursor.execute('DELETE FROM musicas WHERE id_usuario=?',(email,))
    cursor.execute('DELETE FROM usuarios WHERE email=?',(email,))
    conexao.commit()
    return True

def criar_musica(id_usuario,nome_musica, artista, status, imagem, letra):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("INSERT into musicas (id_usuario,nome_musica, artista, status, letra, imagem) VALUES (?,?,?,?,?,?)", (id_usuario, nome_musica, artista, status, letra, imagem))
    conexao.commit()
    cursor.close()
    conexao.close()
    return True


def pegar_musicas (email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT * FROM musicas WHERE id_usuario = ?", (email,))
    return cursor.fetchall()

def buscar_musicas(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT * FROM musicas WHERE id = ?",(id,))
    id = cursor.fetchone()
    
    return id


def editar_musicas(id,email,nome_musica, artista, status, letra, imagem):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("UPDATE musicas SET nome_musica = ?,artista = ?,status = ?,imagem = ?,letra = ? WHERE id_usuario = ? AND id = ?"
                   ,(nome_musica,artista,status,imagem,letra,email,id))
    
    conexao.commit()
    cursor.close()
    conexao.close()
    
def excluir_musica(id):
    conexao = conectar_banco()
    cursor = conexao.cursor() 
    
    cursor.execute("DELETE FROM musicas WHERE id = ?", (id,))
    conexao.commit()
    cursor.close()
    conexao.close()
    
    return True
    

# PARTE PRINCIPAL DO PROGRAMA
if __name__ == '__main__':
    criar_tabela()