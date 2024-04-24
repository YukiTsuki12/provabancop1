from flask import Flask, render_template,request, url_for, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/prova_banco'
app.secret_key = '3pMPj15C01Zj2Gjs1e'
db=SQLAlchemy(app)

mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['prova_banco']
mongo_collection = mongo_db['User']


class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    email = db.Column(db.String(40))
    password = db.Column(db.String(40))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

def create_tables():
    with app.app_context():
        db.create_all()

create_tables()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'name' in session:
        logins = Usuarios.query.all()
        return render_template('home.html', name=session['name'],logins=logins)
    else:
        return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name=request.form['name']
        password=request.form['password']

        usuariaLogin = Usuarios.query.filter_by(name=name).first()

        if usuariaLogin:
            if usuariaLogin.password == password:
                session['name'] = usuariaLogin.name
                return redirect(url_for('home'))
            else:
                return f'Senha incorreta'
        else:
            return render_template('login.html', error='Nome de usuario invalido ou password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']

        usuario = Usuarios(name,email, password)
        db.session.add(usuario)
        db.session.commit()

        usuarioResultado=db.session.query(Usuarios).filter(Usuarios.id==1)

        mongo_collection.insert_one({'name': name, 'email': email, 'password': password})

        if mongo_collection.status_code == 200:
            return redirect(url_for('login'))
        for resultado in usuarioResultado:
            print(resultado.name)
        return redirect(url_for('login', name=name))
    else:
        return render_template('register.html')


@app.route('/deslogar')
def deslogar():
    session.pop('name', None)
    return redirect(url_for('home'))


@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({'message': 'Nome e email sao obrigatorios'}), 400

    mongo_collection.delete_one({'name': name, 'email': email})
    deleted_user = Usuarios.query.filter_by(name=name, email=email).first()

    if deleted_user:
        db.session.delete(deleted_user)
        db.session.commit()
        return jsonify({'message': 'Usuario excluido com sucesso'}), 200
    else:
        return jsonify({'message': 'Usuario nao encontrado'}), 404
    
@app.route('/edit_user/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    data = request.get_json()
    new_name = data.get('name')
    new_email = data.get('email')
    new_password = data.get('password')

    user = Usuarios.query.get(user_id)
    if user:
        old_name = user.name  
        old_email = user.email 
        
        user.name = new_name if new_name else user.name
        user.email = new_email if new_email else user.email
        user.password = new_password if new_password else user.password
        db.session.commit()
    else:
        return jsonify({'message': 'Usuario nao encontrado no PostgreSQL'}), 404

    filtro = {"name": old_name, "email": old_email} 
    novo_valor = {}
    if new_name:
        novo_valor["name"] = new_name
    if new_email:
        novo_valor["email"] = new_email
    if new_password:
        novo_valor["password"] = new_password

    resultado = mongo_collection.update_many(filtro, {"$set": novo_valor})

    if resultado.modified_count > 0:
        return jsonify({'message': 'Usuario editado com sucesso'}), 200
    else:
        return jsonify({'message': 'Usuario nao encontrado no MongoDB'}), 404

if __name__ == '__main__':
    app.run(debug=True)
