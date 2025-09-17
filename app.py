from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def carregar_livros():
    livros = []
    try:
        with open('livros.txt', 'r', encoding='utf-8') as f:
            for linha in f:
                cod, titulo, autor, categoria, ano = linha.strip().split('|')
                livros.append({
                    'cod': cod,
                    'titulo': titulo,
                    'autor': autor,
                    'categoria': categoria,
                    'ano': ano
                })
    except FileNotFoundError:
        pass
    return livros

@app.route('/')
def home():
    livros = carregar_livros()
    return render_template('index.html', livros=livros)

@app.route('/inserir', methods=['POST'])
def inserir():
    tipo = request.form.get('tipoInsercao')
    codigo = request.form.get('codigo')
    nome = request.form.get('nome')

    if not tipo or not codigo or not nome:
        return "Erro: Todos os campos são obrigatórios!", 400

    with open('dados.txt', 'a', encoding='utf-8') as f:
        f.write(f"{tipo}|{codigo}|{nome}\n")

    print(f"[DEBUG] Recebido -> Tipo: {tipo}, Código: {codigo}, Nome: {nome}")

    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
