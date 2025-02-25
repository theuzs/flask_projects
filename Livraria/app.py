from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para inicializar o banco de dados
def init_db():
    conn = sqlite3.connect('estoque.db')
    c = conn.cursor()
    
    # Tabela de Autores
    c.execute('''
        CREATE TABLE IF NOT EXISTS autores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            nacionalidade TEXT NOT NULL,
            biografia TEXT NOT NULL
        )
    ''')

    # Tabela de Livros
    c.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            isbn TEXT NOT NULL UNIQUE,
            edicao TEXT NOT NULL,
            editora TEXT NOT NULL,
            ano_publicacao INTEGER NOT NULL,
            preco_capa REAL NOT NULL,
            categoria TEXT NOT NULL
        )
    ''')

    # Tabela de Relacionamento Livro-Autor
    c.execute('''
        CREATE TABLE IF NOT EXISTS livro_autor (
            livro_id INTEGER,
            autor_id INTEGER,
            FOREIGN KEY(livro_id) REFERENCES livros(id),
            FOREIGN KEY(autor_id) REFERENCES autores(id),
            PRIMARY KEY(livro_id, autor_id)
        )
    ''')

    # Tabela de Estoque
    c.execute('''
        CREATE TABLE IF NOT EXISTS estoque (
            livro_id INTEGER,
            quantidade INTEGER NOT NULL,
            data_entrada TEXT NOT NULL,
            data_saida TEXT,
            FOREIGN KEY(livro_id) REFERENCES livros(id)
        )
    ''')

    # Tabela de Vendas
    c.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            livro_id INTEGER,
            quantidade INTEGER NOT NULL,
            data_venda TEXT NOT NULL,
            FOREIGN KEY(livro_id) REFERENCES livros(id)
        )
    ''')

    conn.commit()
    conn.close()

# Função para conexão com o banco de dados
def get_db():
    conn = sqlite3.connect('estoque.db')
    conn.row_factory = sqlite3.Row
    return conn

# Rota para a página inicial
@app.route('/')

def index():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT l.id, l.titulo, l.isbn, l.editora, l.preco_capa, l.categoria,
               COALESCE(SUM(e.quantidade), 0) AS estoque
        FROM livros l
        LEFT JOIN estoque e ON l.id = e.livro_id
        GROUP BY l.id
    """)
    livros = c.fetchall()
    conn.close()
    return render_template('index.html', livros=livros)


# Rota para adicionar autor
@app.route('/add_autor', methods=['GET', 'POST'])
def add_autor():
    if request.method == 'POST':
        nome = request.form['nome']
        nacionalidade = request.form['nacionalidade']
        biografia = request.form['biografia']
        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO autores (nome, nacionalidade, biografia) VALUES (?, ?, ?)", 
                  (nome, nacionalidade, biografia))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_autor.html')

# Rota para adicionar livro
@app.route('/add_livro', methods=['GET', 'POST'])
def add_livro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        isbn = request.form['isbn']
        edicao = request.form['edicao']
        editora = request.form['editora']
        ano_publicacao = request.form['ano_publicacao']
        preco_capa = request.form['preco_capa']
        categoria = request.form['categoria']
        
        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO livros (titulo, isbn, edicao, editora, ano_publicacao, preco_capa, categoria) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                  (titulo, isbn, edicao, editora, ano_publicacao, preco_capa, categoria))
        conn.commit()
        livro_id = c.lastrowid
        autores = request.form.getlist('autores')
        
        for autor_id in autores:
            c.execute("INSERT INTO livro_autor (livro_id, autor_id) VALUES (?, ?)", (livro_id, autor_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM autores")
    autores = c.fetchall()
    conn.close()
    
    return render_template('add_livro.html', autores=autores)

# Rota para controle de entrada de estoque
@app.route('/entrada_estoque/<int:livro_id>', methods=['GET', 'POST'])
def entrada_estoque(livro_id):
    if request.method == 'POST':
        quantidade = request.form['quantidade']
        data_entrada = request.form['data_entrada']
        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO estoque (livro_id, quantidade, data_entrada) VALUES (?, ?, ?)", 
                  (livro_id, quantidade, data_entrada))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('entrada_estoque.html', livro_id=livro_id)

# Rota para controle de saída de estoque
@app.route('/saida_estoque/<int:livro_id>', methods=['GET', 'POST'])
def saida_estoque(livro_id):
    if request.method == 'POST':
        quantidade = request.form['quantidade']
        data_saida = request.form['data_saida']
        conn = get_db()
        c = conn.cursor()
        c.execute("UPDATE estoque SET quantidade = quantidade - ? , data_saida = ? WHERE livro_id = ?", 
                  (quantidade, data_saida, livro_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('saida_estoque.html', livro_id=livro_id)

if __name__ == '__main__':
    init_db()  # Inicializa o banco de dados
    app.run(debug=True)
