from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cursos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelos
class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))
    carga_horaria = db.Column(db.Integer)
    instrutor = db.Column(db.String(100))
    inscricoes = db.relationship('Inscricao', backref='curso', lazy=True)

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    telefone = db.Column(db.String(20))
    inscricoes = db.relationship('Inscricao', backref='aluno', lazy=True)

class Inscricao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'), nullable=False)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)

# Rotas para Cursos
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cursos')
def listar_cursos():
    cursos = Curso.query.all()
    return render_template('cursos.html', cursos=cursos)

@app.route('/cursos/novo', methods=['GET', 'POST'])
def novo_curso():
    if request.method == 'POST':
        curso = Curso(
            nome=request.form['nome'],
            descricao=request.form['descricao'],
            carga_horaria=request.form['carga_horaria'],
            instrutor=request.form['instrutor']
        )
        db.session.add(curso)
        db.session.commit()
        flash('Curso cadastrado com sucesso!')
        return redirect(url_for('listar_cursos'))
    return render_template('novo_curso.html')

@app.route('/cursos/editar/<int:id>', methods=['GET', 'POST'])
def editar_curso(id):
    curso = Curso.query.get_or_404(id)
    if request.method == 'POST':
        curso.nome = request.form['nome']
        curso.descricao = request.form['descricao']
        curso.carga_horaria = request.form['carga_horaria']
        curso.instrutor = request.form['instrutor']
        db.session.commit()
        flash('Curso atualizado com sucesso!')
        return redirect(url_for('listar_cursos'))
    return render_template('editar_curso.html', curso=curso)

@app.route('/cursos/excluir/<int:id>')
def excluir_curso(id):
    curso = Curso.query.get_or_404(id)
    db.session.delete(curso)
    db.session.commit()
    flash('Curso excluído com sucesso!')
    return redirect(url_for('listar_cursos'))

# Rotas para Alunos
@app.route('/alunos')
def listar_alunos():
    alunos = Aluno.query.all()
    return render_template('alunos.html', alunos=alunos)

@app.route('/alunos/novo', methods=['GET', 'POST'])
def novo_aluno():
    if request.method == 'POST':
        aluno = Aluno(
            nome=request.form['nome'],
            email=request.form['email'],
            telefone=request.form['telefone']
        )
        db.session.add(aluno)
        db.session.commit()
        flash('Aluno cadastrado com sucesso!')
        return redirect(url_for('listar_alunos'))
    return render_template('novo_aluno.html')

@app.route('/alunos/editar/<int:id>', methods=['GET', 'POST'])
def editar_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    if request.method == 'POST':
        aluno.nome = request.form['nome']
        aluno.email = request.form['email']
        aluno.telefone = request.form['telefone']
        db.session.commit()
        flash('Aluno atualizado com sucesso!')
        return redirect(url_for('listar_alunos'))
    return render_template('editar_aluno.html', aluno=aluno)

@app.route('/alunos/excluir/<int:id>')
def excluir_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    db.session.delete(aluno)
    db.session.commit()
    flash('Aluno excluído com sucesso!')
    return redirect(url_for('listar_alunos'))

# Rotas para Inscrições
@app.route('/inscricoes')
def listar_inscricoes():
    inscricoes = Inscricao.query.all()
    return render_template('inscricoes.html', inscricoes=inscricoes)

@app.route('/inscricoes/nova', methods=['GET', 'POST'])
def nova_inscricao():
    if request.method == 'POST':
        inscricao = Inscricao(
            curso_id=request.form['curso_id'],
            aluno_id=request.form['aluno_id']
        )
        db.session.add(inscricao)
        db.session.commit()
        flash('Inscrição realizada com sucesso!')
        return redirect(url_for('listar_inscricoes'))
    cursos = Curso.query.all()
    alunos = Aluno.query.all()
    return render_template('nova_inscricao.html', cursos=cursos, alunos=alunos)

@app.route('/inscricoes/excluir/<int:id>')
def excluir_inscricao(id):
    inscricao = Inscricao.query.get_or_404(id)
    db.session.delete(inscricao)
    db.session.commit()
    flash('Inscrição cancelada com sucesso!')
    return redirect(url_for('listar_inscricoes'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)