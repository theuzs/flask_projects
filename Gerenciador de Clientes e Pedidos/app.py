from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função auxiliar para gerenciar a conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect('gerenciador.db')
    conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
    return conn

# Função para inicializar o banco de dados e criar as tabelas
def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Criando a tabela de clientes
    c.execute('''CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL,
                    telefone TEXT NOT NULL
                )''')
    
    # Criando a tabela de produtos
    c.execute('''CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    descricao TEXT NOT NULL,
                    preco REAL NOT NULL
                )''')
    
    # Criando a tabela de pedidos
    c.execute('''CREATE TABLE IF NOT EXISTS pedidos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_cliente INTEGER NOT NULL,
                    id_produto INTEGER NOT NULL,
                    data_pedido TEXT NOT NULL,
                    FOREIGN KEY (id_cliente) REFERENCES clientes(id),
                    FOREIGN KEY (id_produto) REFERENCES produtos(id)
                )''')
    
    conn.commit()
    conn.close()

# Rota inicial
@app.route('/')
def index():
    # Exibindo todos os pedidos no index
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""SELECT pedidos.id, clientes.nome AS cliente, produtos.nome AS produto, pedidos.data_pedido
                 FROM pedidos
                 JOIN clientes ON pedidos.id_cliente = clientes.id
                 JOIN produtos ON pedidos.id_produto = produtos.id""")
    pedidos = c.fetchall()
    conn.close()
    return render_template('index.html', pedidos=pedidos)

# Rotas para clientes
@app.route('/clientes')
def listar_clientes():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM clientes")
    clientes = c.fetchall()
    conn.close()
    return render_template('clientes.html', clientes=clientes)

@app.route('/add_cliente', methods=['GET', 'POST'])
def add_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)", (nome, email, telefone))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_clientes'))
    return render_template('add_cliente.html')

# Rotas para produtos
@app.route('/produtos')
def listar_produtos():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM produtos")
    produtos = c.fetchall()
    conn.close()
    return render_template('produtos.html', produtos=produtos)

@app.route('/add_produto', methods=['GET', 'POST'])
def add_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['preco']
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO produtos (nome, descricao, preco) VALUES (?, ?, ?)", (nome, descricao, preco))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_produtos'))
    return render_template('add_produto.html')

# Rotas para pedidos
@app.route('/pedidos')
def listar_pedidos():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""SELECT pedidos.id, clientes.nome AS cliente, produtos.nome AS produto, pedidos.data_pedido
                 FROM pedidos
                 JOIN clientes ON pedidos.id_cliente = clientes.id
                 JOIN produtos ON pedidos.id_produto = produtos.id""")
    pedidos = c.fetchall()
    conn.close()
    return render_template('pedidos.html', pedidos=pedidos)

@app.route('/add_pedido', methods=['GET', 'POST'])
def add_pedido():
    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        id_produto = request.form['id_produto']
        data_pedido = request.form['data_pedido']
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO pedidos (id_cliente, id_produto, data_pedido) VALUES (?, ?, ?)", 
                  (id_cliente, id_produto, data_pedido))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_pedidos'))
    
    # Recuperar clientes e produtos para o formulário de adição de pedido
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, nome FROM clientes")
    clientes = c.fetchall()
    c.execute("SELECT id, nome FROM produtos")
    produtos = c.fetchall()
    conn.close()
    
    return render_template('add_pedido.html', clientes=clientes, produtos=produtos)

if __name__ == '__main__':
    init_db()  # Inicializa o banco de dados quando o app é iniciado
    app.run(debug=True)
