"""
Trabalho Arquivos Indexados - Algoritmos e Estruturas de Dados II
Aluno: Kaique Alexandre Souza Kubota
Curso: Análise e Desenvolvimento de Sistemas - 2° Ano T1
"""

import os 
from datetime import datetime, timedelta

# Definição das classes

class Cidades: 
    def __init__(self, cod_cidade, descricao, estado): 
        self.cod_cidade = cod_cidade
        self.descricao = descricao 
        self.estado = estado

class Cursos:
    def __init__(self, cod_curso, descricao):
        self.cod_curso = cod_curso
        self.descricao = descricao

class Alunos:
    def __init__(self, cod_aluno, nome, cod_curso, cod_cidade):
        self.cod_aluno = cod_aluno
        self.nome = nome
        self.cod_cidade = cod_cidade
        self.cod_curso = cod_curso

class Autores: 
    def __init__(self, cod_autor, nome, cod_cidade):
        self.cod_autor = cod_autor
        self.nome = nome
        self.cod_cidade = cod_cidade

class Categorias:
    def __init__(self, cod_categoria, descricao):
        self.cod_categoria = cod_categoria
        self.descricao = descricao

class Livros:
    def __init__(self, cod_livro, titulo, cod_autor, cod_categoria, ano_publicacao, disponibilidade='disponível'):
        self.cod_livro = cod_livro
        self.titulo = titulo
        self.cod_autor = cod_autor
        self.cod_categoria = cod_categoria
        self.ano_publicacao = ano_publicacao
        self.disponibilidade = disponibilidade

class Emprestimos:
    def __init__(self, cod_emprestimo, cod_livro, cod_aluno, data_emprestimo, data_devolucao, devolvido='Não'):
        self.cod_emprestimo = cod_emprestimo
        self.cod_livro = cod_livro
        self.cod_aluno = cod_aluno
        self.data_emprestimo = data_emprestimo
        self.data_devolucao = data_devolucao
        self.devolvido = devolvido

class NoArvore:
    def __init__(self, codigo, registro):
        self.codigo = codigo
        self.registro = registro
        self.esquerda = None
        self.direita = None

# Funções para salvar em disco no formato txt

def salvar_em_txt(nome_arquivo, lista_registros):
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        for registro in lista_registros:
            linha = "|".join(str(valor) for valor in registro)
            f.write(linha + "\n")

def carregar_de_txt(nome_arquivo):
    registros = []
    if not os.path.exists(nome_arquivo):
        return registros

    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            linha = linha.strip()
            if linha:
                campos = linha.split('|')
                registros.append(campos)
    return registros

def reconstruir_arvore_livros(lista_registros):
    raiz = None
    for r in lista_registros:
        livro = Livros(
            int(r[0]), 
            r[1],      
            int(r[2]),  
            int(r[3]),  
            int(r[4]),  
            r[5]         
        )
        raiz = inserir(raiz, livro.cod_livro, livro)
    return raiz

# Funções da árvore

def inserir(raiz, codigo, registro):
    if raiz is None:
        return NoArvore(codigo, registro)
    
    if codigo < raiz.codigo:
        raiz.esquerda = inserir(raiz.esquerda, codigo, registro)
    elif codigo > raiz.codigo:
        raiz.direita = inserir(raiz.direita, codigo, registro)
    else:
        print(f"Código {codigo} já existe na árvore")
    return raiz

def buscar(raiz, codigo):
    if raiz is None or raiz.codigo == codigo:
        return raiz
    
    if codigo < raiz.codigo:
        return buscar(raiz.esquerda, codigo)
    else:
        return buscar(raiz.direita, codigo)
    
def excluir(raiz, codigo):
    if raiz is None:
        return raiz
    
    if codigo < raiz.codigo:
        raiz.esquerda = excluir(raiz.esquerda, codigo)
    elif codigo > raiz.codigo:
        raiz.direita = excluir(raiz.direita, codigo)
    else:
        if raiz.esquerda is None:
            return raiz.direita
        elif raiz.direita is None:
            return raiz.esquerda
        
        temp = encontrar_minimo(raiz.direita)
        raiz.codigo = temp.codigo
        raiz.registro = temp.registro
        raiz.direita = excluir(raiz.direita, temp.codigo)
    
    return raiz

def leitura_exaustiva(raiz):
    def mostrar(no):
        print(f"Código: {no.codigo} | Registro: {vars(no.registro)}")
    percorrer_em_ordem(raiz, mostrar)

def encontrar_minimo(no):
    atual = no
    while atual and atual.esquerda:
        atual = atual.esquerda
    return atual

def percorrer_em_ordem(raiz, verificar_no):
    if raiz:
        percorrer_em_ordem(raiz.esquerda, verificar_no)
        verificar_no(raiz)
        percorrer_em_ordem(raiz.direita, verificar_no)

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Funções principais

def exibir_aluno(arvore_alunos, arvore_cursos, arvore_cidades, cod_aluno):
    aluno_no = buscar(arvore_alunos, cod_aluno)

    if not aluno_no:
        print(f"Aluno com código {cod_aluno} não encontrado.")
        return

    aluno = aluno_no.registro

    curso_no = buscar(arvore_cursos, aluno.cod_curso)
    curso_desc = curso_no.registro.descricao if curso_no else "Curso não encontrado"

    cidade_no = buscar(arvore_cidades, aluno.cod_cidade)
    if cidade_no:
        cidade_desc = cidade_no.registro.descricao
        estado = cidade_no.registro.estado
    else:
        cidade_desc = "Cidade não encontrada"
        estado = "-"

    print(f"""
    Código: {aluno.cod_aluno}
    Nome: {aluno.nome}
    Curso: {curso_desc}
    Cidade: {cidade_desc} - {estado}
    """)

def exibir_autor(arvore_autores, arvore_cidades, cod_autor):
    autor_no = buscar(arvore_autores, cod_autor)

    if not autor_no:
        print(f"Autor com código {cod_autor} não encontrado.")
        return

    autor = autor_no.registro

    cidade_no = buscar(arvore_cidades, autor.cod_cidade)
    if cidade_no:
        cidade_desc = cidade_no.registro.descricao
        estado = cidade_no.registro.estado
    else:
        cidade_desc = "Cidade não encontrada"
        estado = "-"

    print(f"""
    Código: {autor.cod_autor}
    Nome: {autor.nome}
    Cidade: {cidade_desc} - {estado}
    """)

def exibir_livro(arvore_livros, arvore_autores, arvore_cidades, arvore_categorias, cod_livro):
    livro_no = buscar(arvore_livros, cod_livro)
    if not livro_no:
        print(f"Livro com código {cod_livro} não encontrado.")
        return

    livro = livro_no.registro

    autor_no = buscar(arvore_autores, livro.cod_autor)
    if autor_no:
        autor = autor_no.registro
        cidade_no = buscar(arvore_cidades, autor.cod_cidade)
        if cidade_no:
            cidade_autor = cidade_no.registro.descricao
            estado_autor = cidade_no.registro.estado
        else:
            cidade_autor = "Cidade não encontrada"
            estado_autor = "-"
    else:
        autor = None
        cidade_autor = "Autor não encontrado"
        estado_autor = "-"

    categoria_no = buscar(arvore_categorias, livro.cod_categoria)
    categoria_desc = categoria_no.registro.descricao if categoria_no else "Categoria não encontrada"

    print(f"""
    Código do Livro: {livro.cod_livro}
    Título: {livro.titulo}
    Autor: {autor.nome if autor else 'Desconhecido'}
    Cidade do Autor: {cidade_autor} - {estado_autor}
    Categoria: {categoria_desc}
    Ano de Publicação: {livro.ano_publicacao}
    Disponibilidade: {livro.disponibilidade}
    """)

def incluir_emprestimo(arvore_emprestimos, arvore_livros, arvore_categorias, arvore_alunos, arvore_cidades):
    print("\n - Novo Empréstimo -")
    cod_emprestimo = int(input("Código do Empréstimo: "))
    
    cod_livro = int(input("Código do Livro: "))
    livro_no = buscar(arvore_livros, cod_livro)
    if not livro_no:
        print("Livro não encontrado!")
        return arvore_emprestimos
    
    livro = livro_no.registro
    if livro.disponibilidade != "disponível":
        print("Esse livro já está emprestado!")
        return arvore_emprestimos
    
    categoria_no = buscar(arvore_categorias, livro.cod_categoria)
    categoria_desc = categoria_no.registro.descricao if categoria_no else "Categoria não encontrada"
    
    print(f"\nLivro: {livro.titulo}")
    print(f"Categoria: {categoria_desc}")
    
    cod_aluno = int(input("Código do Aluno: "))
    aluno_no = buscar(arvore_alunos, cod_aluno)
    if not aluno_no:
        print("Aluno não encontrado!")
        return arvore_emprestimos
    
    aluno = aluno_no.registro
    
    cidade_no = buscar(arvore_cidades, aluno.cod_cidade)
    if cidade_no:
        cidade_desc = cidade_no.registro.descricao
        estado = cidade_no.registro.estado
    else:
        cidade_desc = "Cidade não encontrada"
        estado = "-"
    
    print(f"\nAluno: {aluno.nome}")
    print(f"Cidade: {cidade_desc} - {estado}")
    
    data_emprestimo = datetime.now().strftime("%d/%m/%Y")
    data_devolucao = (datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y")
    
    print(f"\nData Empréstimo: {data_emprestimo}")
    print(f"Data Devolução: {data_devolucao}")
    
    confirmar = input("\nConfirmar empréstimo? (s/n): ").strip().lower()
    if confirmar != 's':
        print("Operação cancelada.")
        return arvore_emprestimos
    
    livro.disponibilidade = "emprestado"
    emprestimo = Emprestimos(cod_emprestimo, cod_livro, cod_aluno, data_emprestimo, data_devolucao, "Não")
    arvore_emprestimos = inserir(arvore_emprestimos, cod_emprestimo, emprestimo)
    
    print("\nEmpréstimo realizado com sucesso!")
    return arvore_emprestimos

def realizar_devolucao(arvore_emprestimos, arvore_livros):
    print("\n- Devolução de Livros -")
    cod_emprestimo = int(input("Código do Empréstimo: "))
    
    emprestimo_no = buscar(arvore_emprestimos, cod_emprestimo)
    if not emprestimo_no:
        print("Empréstimo não encontrado!")
        return
    
    emprestimo = emprestimo_no.registro
    
    if emprestimo.devolvido == "Sim":
        print("Este empréstimo já foi devolvido.")
        return
    
    data_devolucao = datetime.strptime(emprestimo.data_devolucao, "%d/%m/%Y")
    hoje = datetime.now()
    
    if hoje > data_devolucao:
        print("Atenção: O livro está com devolução atrasada!")
    
    confirmar = input("Confirmar devolução? (s/n): ").strip().lower()
    if confirmar != 's':
        print("Operação cancelada.")
        return
    
    livro_no = buscar(arvore_livros, emprestimo.cod_livro)
    if livro_no:
        livro_no.registro.disponibilidade = "disponível"
    
    emprestimo.devolvido = "Sim"
    
    print("\nDevolução realizada com sucesso!")

def livros_emprestados(arvore_emprestimos, arvore_livros):
    print("\n- Livros Emprestados -")
    
    def verificar_no(no):
        emprestimo = no.registro
        if emprestimo.devolvido == "Não":
            livro_no = buscar(arvore_livros, emprestimo.cod_livro)
            if livro_no:
                print(f"Código do Livro: {livro_no.registro.cod_livro} | Título: {livro_no.registro.titulo}")

    percorrer_em_ordem(arvore_emprestimos, verificar_no)

def livros_atrasados(arvore_emprestimos, arvore_livros):
    print("\n- Livros Atrasados -")

    hoje = datetime.now()
    
    def verificar_no(no):
        emprestimo = no.registro
        if emprestimo.devolvido == "Não":
            data_devolucao = datetime.strptime(emprestimo.data_devolucao, "%d/%m/%Y")
            if hoje > data_devolucao:
                livro_no = buscar(arvore_livros, emprestimo.cod_livro)
                if livro_no:
                    print(f"Código do Livro: {livro_no.registro.cod_livro} | Título: {livro_no.registro.titulo} | Data prevista: {emprestimo.data_devolucao}")
    
    percorrer_em_ordem(arvore_emprestimos, verificar_no)

def quantidade_emprestimos_periodo(arvore_emprestimos, data_inicio, data_fim):
    print(f"\n- Quantidade de Empréstimos Entre {data_inicio} E {data_fim} -")
    
    data_inicio_dt = datetime.strptime(data_inicio, "%d/%m/%Y")
    data_fim_dt = datetime.strptime(data_fim, "%d/%m/%Y")
    
    contador = 0

    def verificar_no(no):
        nonlocal contador
        emprestimo = no.registro
        data_emprestimo = datetime.strptime(emprestimo.data_emprestimo, "%d/%m/%Y")
        if data_inicio_dt <= data_emprestimo <= data_fim_dt:
            contador += 1

    percorrer_em_ordem(arvore_emprestimos, verificar_no)
    print(f"Total de livros emprestados no período: {contador}")

def listar_livros_em_ordem(arvore_livros, raiz_autores, raiz_categorias):
    livros_disponiveis = 0
    livros_emprestados = 0

    def verificar_no(no):
        nonlocal livros_disponiveis, livros_emprestados
        livro = no.registro

        autor_no = buscar(raiz_autores, livro.cod_autor)
        nome_autor = autor_no.registro.nome if autor_no else "Autor não encontrado"

        categoria_no = buscar(raiz_categorias, livro.cod_categoria)
        nome_categoria = categoria_no.registro.descricao if categoria_no else "Categoria não encontrada"

        print(f"Código: {livro.cod_livro} | "
              f"Título: {livro.titulo} | "
              f"Autor: {nome_autor} | "
              f"Categoria: {nome_categoria} | "
              f"Disponibilidade: {livro.disponibilidade}")

        if livro.disponibilidade.lower() == "disponível":
            livros_disponiveis += 1
        else:
            livros_emprestados += 1

    percorrer_em_ordem(arvore_livros, verificar_no)

    print("\nResumo:")
    print(f"Livros disponíveis: {livros_disponiveis}")
    print(f"Livros emprestados: {livros_emprestados}")

def sobrescrever_arquivo(nome_arquivo, raiz):
    registros = []

    def coletar_registros(no):
        if no:
            coletar_registros(no.esquerda)
            registros.append([
                no.registro.cod_livro,
                no.registro.titulo,
                no.registro.cod_autor,
                no.registro.cod_categoria,
                no.registro.ano_publicacao,
                no.registro.disponibilidade
            ])
            coletar_registros(no.direita)

    coletar_registros(raiz)
    salvar_em_txt(nome_arquivo, registros)

# Árvores
arvore_livros = None
arvore_autores = None
arvore_cidades = None
arvore_categorias = None
arvore_cursos = None
arvore_alunos = None
arvore_emprestimos = None

dados_txt = carregar_de_txt('livros.txt')
arvore_livros = reconstruir_arvore_livros(dados_txt)

realizar_devolucao(arvore_emprestimos, arvore_livros)
livros_emprestados(arvore_emprestimos, arvore_livros)
livros_atrasados(arvore_emprestimos, arvore_livros)
quantidade_emprestimos_periodo(arvore_emprestimos, "01/09/2025", "05/09/2025")
novo_livro = Livros(105, "Estruturas de Dados", 1, 2, 2025, "disponível")

arvore_livros = inserir(arvore_livros, novo_livro.cod_livro, novo_livro)

with open('livros.txt', 'a', encoding='utf-8') as f:
    f.write(f"{novo_livro.cod_livro}|{novo_livro.titulo}|{novo_livro.cod_autor}|{novo_livro.cod_categoria}|{novo_livro.ano_publicacao}|{novo_livro.disponibilidade}\n")


"""
# Inserindo cidades
arvore_cidades = inserir(arvore_cidades, 1, Cidades(1, "Assis", "SP"))
arvore_cidades = inserir(arvore_cidades, 2, Cidades(2, "Marília", "SP"))

# Inserindo cursos
arvore_cursos = inserir(arvore_cursos, 10, Cursos(10, "Análise e Desenvolvimento de Sistemas"))
arvore_cursos = inserir(arvore_cursos, 11, Cursos(11, "Engenharia Química"))

# Inserindo aluno
aluno1 = Alunos(100, "Kaique", 10, 1)
arvore_alunos = inserir(arvore_alunos, aluno1.cod_aluno, aluno1)

# Inserindo autor
autor1 = Autores(200, "Machado de Assis", 2)
arvore_autores = inserir(arvore_autores, autor1.cod_autor, autor1)

# Teste
exibir_aluno(arvore_alunos, arvore_cursos, arvore_cidades, 100)
exibir_autor(arvore_autores, arvore_cidades, 200)

# Inserir cidade
arvore_cidades = inserir(arvore_cidades, 1, Cidades(1, "Assis", "SP"))

# Inserir autor
autor1 = Autores(100, "Machado de Assis", 1)
arvore_autores = inserir(arvore_autores, autor1.cod_autor, autor1)

# Inserir categoria
categoria1 = Categorias(200, "Romance")
arvore_categorias = inserir(arvore_categorias, categoria1.cod_categoria, categoria1)

# Inserir livro
livro1 = Livros(300, "Dom Casmurro", 100, 200, 1899)
arvore_livros = inserir(arvore_livros, livro1.cod_livro, livro1)

# Teste
exibir_livro(arvore_livros, arvore_autores, arvore_cidades, arvore_categorias, 300)

# Dados de teste
arvore_cidades = inserir(arvore_cidades, 1, Cidades(1, "Assis", "SP"))
arvore_categorias = inserir(arvore_categorias, 1, Categorias(1, "Romance"))
arvore_alunos = inserir(arvore_alunos, 1, Alunos(1, "Kaique", 10, 1))
arvore_livros = inserir(arvore_livros, 1, Livros(1, "Dom Casmurro", 100, 1, 1899))

# Teste de inclusão
arvore_emprestimos = incluir_emprestimo(arvore_emprestimos, arvore_livros, arvore_categorias, arvore_alunos, arvore_cidades)
"""
