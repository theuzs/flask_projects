from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('estoque.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('estoque.db')
    c = conn.cursor()
    c.execute("SELECT * FROM produtos")
    produtos = c.fetchall()
    conn.close()
    return render_template('index.html', produtos=produtos)

@app.route('/add_produto', methods=['GET', 'POST'])
def add_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = request.form['quantidade']
        preco = request.form['preco']
        conn = sqlite3.connect('estoque.db')
        c = conn.cursor()
        c.execute("INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)", (nome, quantidade, preco))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_produto.html')

@app.route('/delete_produto/<int:id>')
def delete_produto(id):
    conn = sqlite3.connect('estoque.db')
    c = conn.cursor()
    c.execute("DELETE FROM produtos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
