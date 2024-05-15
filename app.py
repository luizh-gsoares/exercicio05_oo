from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# SECRET KEY
app.secret_key = 'PaoDoceFrango2024'

# UPLOAD
UPLOAD_FOLDER = 'C:/Users/luizh/OneDrive/Documentos/Flask/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# BANCO DE DADOS 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///minhabase.sqlite3'
db = SQLAlchemy(app)
app.app_context().push()


# CLASSE USUARIO
class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, unique=True)
    senha = db.Column(db.String)
    
    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha

# CRIAÇÃO DE BANCO DE DADOS
with app.app_context():
    db.create_all()
    
# ROTA DE LOGIN
@app.route("/login", methods=['POST', 'GET'])
def login() : 
    if request.method == 'POST' :        
        # PEGA OS DADOS ENVIADOS PELO FORMULÁRIO VIA POST
        nome_form = request.form['nome']
        senha_form = request.form['senha']
        
        # VERIFICA SE HÁ UM NOME NA TABELA QUE CORRESPONDE AO
        # ENVIADO PELO FORMULÁRIO POST.
        user = Usuario.query.filter_by(nome = nome_form).first()
        
        # VERIFICA SE A SENHA CORRESPONDE AO DO BANCO        
        if ((user) and (user.senha == senha_form)) :
            session['username'] = nome_form
            return render_template('index.html', mensagem = "Você está logado como : ", usuario_logado = session['username'], usuarios = Usuario.query.all())
        else :
            return render_template('login.html', mensagem = 'Usuário ou senha incorretos.')
            
    return render_template('login.html')

# ROTA DE USUARIOS
@app.route("/usuario", methods=['POST','GET'])
def adicionarUsuario() :
    # COMO A REQUISIÇÃO POST IRÁ SE COMPORTAR?
    if request.method == 'POST' :
        # PEGA OS DADOS ENVIADOS PELO FORMULÁRIO VIA POST
        nome_form = request.form['nome']
        senha_form = request.form['senha']
        
        # SE NA TABELA USUÁRIO TEM ALGUEM COM O MESMO NOME, BUSCA O
        # PRIMEIRO. CONSEQUENTEMENTE, RETORNA VERDADEIRO OU FALSO.
        # SERVE PARA VERIFICAR SE EXISTE USUÁRIO
        if Usuario.query.filter_by(nome = nome_form).first():
            return render_template('register.html', mensagem = "Usuário já existe. Tente outro nome.")
        else :
            user = Usuario(nome_form, senha_form)
            db.session.add(user)
            db.session.commit()
            return render_template('register.html', mensagem = 'Usuário criado com sucesso. Faça o login.')   
    return render_template('register.html')
    

    

# ROTA DE UPLOAD
@app.route("/upload", methods=['POST', 'GET'])
def upload():
    if 'username' in session:
        # COMO A REQUISIÇÃO POST IRÁ SE COMPORTAR?
        if request.method == 'POST':
            # BUSCA O ARQUIVO PELO NAME, DEPOIS DE ENVIADO NO HTML
            file = request.files['arquivo']
            
            # SALVA O ARQUIVO NA PASTA INDICADA NA VARIAVEL UPLOAD
            savePath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(savePath)
            
            # RETORNA AO HTML COM MENSAGEM DE SUCESSO
            return render_template('upload.html', mensagem = "Seu upload foi realizado com sucesso !!!")
        return render_template('upload.html', usuario_logado = session['username'])
    return render_template('index.html', mensagem = 'Faça o login para acessar esta página.')

# Rota para o logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', usuario_logado = session['username'], usuarios = Usuario.query.all())

    return render_template('index.html')

if __name__ == "__main__":
    db.create_all()
    app.run()