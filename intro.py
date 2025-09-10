"""
Trabalho Arquivos Indexados - Algoritmos e Estruturas de Dados II
Aluno: Kaique Alexandre Souza Kubota
Curso: Análise e Desenvolvimento de Sistemas - 2° Ano T1
--------------------------------------
! Dificuldades:
! Parte de salvar e carregar os dados das árvores em arquivos txt 
! Algumas funções de consulta
! Funções de empréstimo e devolução
"""

import os
from datetime import datetime, timedelta

# Definindo classes

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
        self.cod_curso = cod_curso
        self.cod_cidade = cod_cidade

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

# Funções do arquivo txt

def salvar_em_txt(nome_arquivo, lista_registros):

    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        for registro in lista_registros:
            f.write("|".join(str(valor) for valor in registro) + "\n")

def carregar_txt(nome_arquivo):

    registros = []
    if not os.path.exists(nome_arquivo):
        return registros
    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            linha = linha.strip()
            if linha:
                registros.append(linha.split('|'))
    return registros

def reconstruir_arvores(lista_registros, tipo):
    raiz = None
    for r in lista_registros:
        if tipo == "cidades":
            registro = Cidades(int(r[0]), r[1], r[2])
            raiz = inserir(raiz, registro.cod_cidade, registro)
        elif tipo == "cursos":
            registro = Cursos(int(r[0]), r[1])
            raiz = inserir(raiz, registro.cod_curso, registro)
        elif tipo == "alunos":
            registro = Alunos(int(r[0]), r[1], int(r[2]), int(r[3]))
            raiz = inserir(raiz, registro.cod_aluno, registro)
        elif tipo == "autores":
            registro = Autores(int(r[0]), r[1], int(r[2]))
            raiz = inserir(raiz, registro.cod_autor, registro)
        elif tipo == "categorias":
            registro = Categorias(int(r[0]), r[1])
            raiz = inserir(raiz, registro.cod_categoria, registro)
        elif tipo == "emprestimos":
            registro = Emprestimos(int(r[0]), int(r[1]), int(r[2]), r[3], r[4], r[5])
            raiz = inserir(raiz, registro.cod_emprestimo, registro)
    return raiz


# Funções da Árvore

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

def percorrer_em_ordem(raiz, func):

    if raiz:
        percorrer_em_ordem(raiz.esquerda, func)
        func(raiz)
        percorrer_em_ordem(raiz.direita, func)

def encontrar_minimo(no):
    atual = no
    while atual and atual.esquerda:
        atual = atual.esquerda
    return atual

def leitura_exaustiva(raiz):
    percorrer_em_ordem(raiz, lambda no: print(f"Código: {no.codigo} | Registro: {vars(no.registro)}"))

# Funções Principais

def exibir_aluno(arvore_alunos, arvore_cursos, arvore_cidades, cod_aluno):
    aluno_no = buscar(arvore_alunos, cod_aluno)

    if not aluno_no:
        print(f"Aluno com código {cod_aluno} não encontrado.")
        return
    aluno = aluno_no.registro
    curso_no = buscar(arvore_cursos, aluno.cod_curso)
    curso_desc = curso_no.registro.descricao if curso_no else "Curso não encontrado"
    cidade_no = buscar(arvore_cidades, aluno.cod_cidade)
    cidade_desc, estado = (cidade_no.registro.descricao, cidade_no.registro.estado) if cidade_no else ("Cidade não encontrada", "-")
    print(f"\nCódigo: {aluno.cod_aluno}\nNome: {aluno.nome}\nCurso: {curso_desc}\nCidade: {cidade_desc} - {estado}\n")

def exibir_autor(arvore_autores, arvore_cidades, cod_autor):
    autor_no = buscar(arvore_autores, cod_autor)

    if not autor_no:
        print(f"Autor com código {cod_autor} não encontrado.")
        return
    autor = autor_no.registro
    cidade_no = buscar(arvore_cidades, autor.cod_cidade)
    cidade_desc, estado = (cidade_no.registro.descricao, cidade_no.registro.estado) if cidade_no else ("Cidade não encontrada", "-")
    print(f"\nCódigo: {autor.cod_autor}\nNome: {autor.nome}\nCidade: {cidade_desc} - {estado}\n")

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
        cidade_autor, estado_autor = (cidade_no.registro.descricao, cidade_no.registro.estado) if cidade_no else ("Cidade não encontrada", "-")
    else:
        autor, cidade_autor, estado_autor = None, "Autor não encontrado", "-"
    categoria_no = buscar(arvore_categorias, livro.cod_categoria)
    categoria_desc = categoria_no.registro.descricao if categoria_no else "Categoria não encontrada"
    print(f"\nCódigo do Livro: {livro.cod_livro}\nTítulo: {livro.titulo}\nAutor: {autor.nome if autor else 'Desconhecido'}\nCidade do Autor: {cidade_autor} - {estado_autor}\nCategoria: {categoria_desc}\nAno de Publicação: {livro.ano_publicacao}\nDisponibilidade: {livro.disponibilidade}\n")

def incluir_emprestimo(arvore_emprestimos, arvore_livros, arvore_categorias, arvore_alunos, arvore_cidades):

    print("\n - Novo Empréstimo -")
    cod_emprestimo = int(input("\nCódigo do Empréstimo: "))
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
    print(f"\nLivro: {livro.titulo}\nCategoria: {categoria_desc}")
    cod_aluno = int(input("\nCódigo do Aluno: "))
    aluno_no = buscar(arvore_alunos, cod_aluno)
    if not aluno_no:
        print("Aluno não encontrado!")
        return arvore_emprestimos
    aluno = aluno_no.registro
    cidade_no = buscar(arvore_cidades, aluno.cod_cidade)
    cidade_desc, estado = (cidade_no.registro.descricao, cidade_no.registro.estado) if cidade_no else ("Cidade não encontrada", "-")
    print(f"\nAluno: {aluno.nome}\nCidade: {cidade_desc} - {estado}")
    data_emprestimo = datetime.now().strftime("%d/%m/%Y")
    data_devolucao = (datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y")
    print(f"\nData Empréstimo: {data_emprestimo}\nData Devolução: {data_devolucao}")
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
    if datetime.now() > data_devolucao:
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
                print(f"\nCódigo do Livro: {livro_no.registro.cod_livro} | Título: {livro_no.registro.titulo}")
    percorrer_em_ordem(arvore_emprestimos, verificar_no)

def livros_atrasados(arvore_emprestimos, arvore_livros):
    print("\n- Livros Atrasados -")
    hoje = datetime.now()

    def verificar_no(no):
        emprestimo = no.registro
        if emprestimo.devolvido == "Não":
            data_dev = datetime.strptime(emprestimo.data_devolucao, "%d/%m/%Y")
            if hoje > data_dev:
                livro_no = buscar(arvore_livros, emprestimo.cod_livro)
                if livro_no:
                    print(f"Código do Livro: {livro_no.registro.cod_livro} | Título: {livro_no.registro.titulo} | Data prevista: {emprestimo.data_devolucao}")

    percorrer_em_ordem(arvore_emprestimos, verificar_no)

def quantidade_emprestimos_periodo(arvore_emprestimos, data_inicio, data_fim):
    print(f"\n- Quantidade de Empréstimos Entre {data_inicio} e {data_fim} -")
    
    data_inicio_dt = datetime.strptime(data_inicio, "%d/%m/%Y")
    data_fim_dt = datetime.strptime(data_fim, "%d/%m/%Y")
    contador = 0

    def verificar_no(no):
        nonlocal contador
        data_emprestimo = datetime.strptime(no.registro.data_emprestimo, "%d/%m/%Y")
        if data_inicio_dt <= data_emprestimo <= data_fim_dt:
            contador += 1
    
    percorrer_em_ordem(arvore_emprestimos, verificar_no)
    print(f"\nTotal de livros emprestados no período: {contador}")


def listar_livros_em_ordem(arvore_livros, raiz_autores, raiz_categorias):

    livros_disponiveis = livros_emprestados = 0
    
    def verificar_no(no):
        nonlocal livros_disponiveis, livros_emprestados
        livro = no.registro
        autor_no = buscar(raiz_autores, livro.cod_autor)
        nome_autor = autor_no.registro.nome if autor_no else "Autor não encontrado"
        categoria_no = buscar(raiz_categorias, livro.cod_categoria)
        nome_categoria = categoria_no.registro.descricao if categoria_no else "Categoria não encontrada"
        print(f"\nCódigo: {livro.cod_livro} | Título: {livro.titulo} | Autor: {nome_autor} | Categoria: {nome_categoria} | Disponibilidade: {livro.disponibilidade}")
        if livro.disponibilidade.lower() == "disponível":
            livros_disponiveis += 1
        else:
            livros_emprestados += 1
    percorrer_em_ordem(arvore_livros, verificar_no)
    print(f"\nRelação de Livros:\nLivros disponíveis: {livros_disponiveis}\nLivros emprestados: {livros_emprestados}")

def sobrescrever_arquivo(nome_arquivo, raiz):
    
    registros = []
    def coletar_registros(no):
        if no:
            coletar_registros(no.esquerda)
            registros.append([no.registro.cod_livro, no.registro.titulo, no.registro.cod_autor,
                              no.registro.cod_categoria, no.registro.ano_publicacao, no.registro.disponibilidade])
            coletar_registros(no.direita)
    coletar_registros(raiz)
    salvar_em_txt(nome_arquivo, registros)

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPressione Enter para continuar...")

"""
! FALTANDO NO MENU
7) Permitir as seguintes consultas:
7.1) Livros que estão emprestado 
7.2) Livros que estão com a devolução atrasada 
7.3) Quantidade de livros emprestados por período (data inicial e data final) 
"""

def menu_principal():
    global arvore_cidades, arvore_cursos, arvore_alunos, arvore_autores, arvore_categorias, arvore_livros, arvore_emprestimos

    while True:
        limpar_tela()
        print("\n - Sistema de Biblioteca - ")
        print("1. Inserir Cidade")
        print("2. Inserir Curso")
        print("3. Inserir Categoria")
        print("4. Inserir Autor")
        print("5. Inserir Aluno")
        print("6. Inserir Livro")
        print("7. Listar Livros")
        print("8. Realizar Empréstimo")
        print("9. Realizar Devolução")
        print("10. Consultas") 
        print("0. Sair e Salvar")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            cod = int(input("\nCódigo da Cidade: "))
            nome = input("Nome da Cidade: ")
            uf = input("UF: ")
            arvore_cidades = inserir(arvore_cidades, cod, Cidades(cod, nome, uf))
            print("\nCidade cadastrada com sucesso!")
            pausar()

        elif opcao == '2':
            cod = int(input("\nCódigo do Curso: "))
            nome = input("Nome do Curso: ")
            arvore_cursos = inserir(arvore_cursos, cod, Cursos(cod, nome))
            print("\nCurso cadastrado com sucesso!")
            pausar()

        elif opcao == '3':
            cod = int(input("\nCódigo da Categoria: "))
            nome = input("Nome da Categoria: ")
            arvore_categorias = inserir(arvore_categorias, cod, Categorias(cod, nome))
            print("\nCategoria cadastrada com sucesso!")
            pausar()

        elif opcao == '4':
            cod = int(input("\nCódigo do Autor: "))
            nome = input("Nome do Autor: ")
            cidade = int(input("Código da Cidade: "))
            arvore_autores = inserir(arvore_autores, cod, Autores(cod, nome, cidade))
            print("\nAutor cadastrado com sucesso!")
            pausar()

        elif opcao == '5':
            cod = int(input("\nCódigo do Aluno: "))
            nome = input("Nome do Aluno: ")
            curso = int(input("Código do Curso: "))
            cidade = int(input("Código da Cidade: "))
            arvore_alunos = inserir(arvore_alunos, cod, Alunos(cod, nome, curso, cidade))
            print("\nAluno cadastrado com sucesso!")
            pausar()

        elif opcao == '6':
            cod = int(input("\nCódigo do Livro: "))
            titulo = input("Título do Livro: ")
            autor = int(input("Código do Autor: "))
            categoria = int(input("Código da Categoria: "))
            ano = int(input("Ano: "))

            arvore_livros = inserir(arvore_livros, cod, Livros(cod, titulo, autor, categoria, ano))
            print("\nLivro cadastrado com sucesso!")
            pausar()

        elif opcao == '7':
            listar_livros_em_ordem(arvore_livros, arvore_autores, arvore_categorias)
            pausar()

        elif opcao == '8':
            arvore_emprestimos = incluir_emprestimo(arvore_emprestimos, arvore_livros, arvore_categorias, arvore_alunos, arvore_cidades)
            pausar()

        elif opcao == '9':
            realizar_devolucao(arvore_emprestimos, arvore_livros)
            pausar()

        elif opcao == '10': 
            menu_consultas()

        elif opcao == '0':
            salvar_livros()
            print("\nDados salvos!")
            break
        else:
            print("\nOpção inválida!")
            pausar()

def menu_consultas():
    global arvore_emprestimos, arvore_livros

    while True:
        limpar_tela()
        print("\n - Consultas - ")
        print("1. Livros emprestados")
        print("2. Livros com devolução atrasada")
        print("3. Quantidade de livros emprestados por período")
        print("0. Voltar ao menu principal")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            livros_emprestados(arvore_emprestimos, arvore_livros)
            pausar()

        elif opcao == '2':
            livros_atrasados(arvore_emprestimos, arvore_livros)
            pausar()

        elif opcao == '3':
            data_inicio = input("\nData inicial (dd/mm/aaaa): ")
            data_fim = input("Data final (dd/mm/aaaa): ")
            quantidade_emprestimos_periodo(arvore_emprestimos, data_inicio, data_fim)
            pausar()

        elif opcao == '0':
            break
        else:
            print("Opção inválida!")
            pausar()


def salvar_livros():
    salvar_em_txt("livros.txt", coletar_registros(arvore_livros, "livros"))
    salvar_em_txt("cidades.txt", coletar_registros(arvore_cidades, "cidades"))
    salvar_em_txt("cursos.txt", coletar_registros(arvore_cursos, "cursos"))
    salvar_em_txt("alunos.txt", coletar_registros(arvore_alunos, "alunos"))
    salvar_em_txt("autores.txt", coletar_registros(arvore_autores, "autores"))
    salvar_em_txt("categorias.txt", coletar_registros(arvore_categorias, "categorias"))
    salvar_em_txt("emprestimos.txt", coletar_registros(arvore_emprestimos, "emprestimos"))

def coletar_registros(no, tipo):
    registros = []

    def percorrer(n):
        if n:
            percorrer(n.esquerda)

            if tipo == "livros":
                registros.append([
                    n.registro.cod_livro,
                    n.registro.titulo,
                    n.registro.cod_autor,
                    n.registro.cod_categoria,
                    n.registro.ano_publicacao,
                    n.registro.disponibilidade
                ])
            elif tipo == "cidades":
                registros.append([
                    n.registro.cod_cidade,
                    n.registro.descricao,
                    n.registro.estado
                ])
            elif tipo == "cursos":
                registros.append([
                    n.registro.cod_curso,
                    n.registro.descricao
                ])
            elif tipo == "alunos":
                registros.append([
                    n.registro.cod_aluno,
                    n.registro.nome,
                    n.registro.cod_curso,
                    n.registro.cod_cidade
                ])
            elif tipo == "autores":
                registros.append([
                    n.registro.cod_autor,
                    n.registro.nome,
                    n.registro.cod_cidade
                ])
            elif tipo == "categorias":
                registros.append([
                    n.registro.cod_categoria,
                    n.registro.descricao
                ])
            elif tipo == "emprestimos":
                registros.append([
                    n.registro.cod_emprestimo,
                    n.registro.cod_livro,
                    n.registro.cod_aluno,
                    n.registro.data_emprestimo,
                    n.registro.data_devolucao,
                    n.registro.devolvido
                ])
            percorrer(n.direita)

    percorrer(no)
    return registros

# Árvores iniciais + Main
if __name__ == "__main__":
    arvore_cidades = None
    arvore_cursos = None
    arvore_alunos = None
    arvore_autores = None
    arvore_categorias = None
    arvore_livros = None
    arvore_emprestimos = None

    arvore_cidades = reconstruir_arvores(carregar_txt('cidades.txt'), "cidades")
    arvore_cursos = reconstruir_arvores(carregar_txt('cursos.txt'), "cursos")
    arvore_alunos = reconstruir_arvores(carregar_txt('alunos.txt'), "alunos")
    arvore_autores = reconstruir_arvores(carregar_txt('autores.txt'), "autores")
    arvore_categorias = reconstruir_arvores(carregar_txt('categorias.txt'), "categorias")
    arvore_livros = reconstruir_arvores(carregar_txt('livros.txt'), "livros")
    arvore_emprestimos = reconstruir_arvores(carregar_txt('emprestimos.txt'), "emprestimos")

    menu_principal()

salvar_em_txt("livros.txt", coletar_registros(arvore_livros, "livros"))
salvar_em_txt("cidades.txt", coletar_registros(arvore_cidades, "cidades"))
salvar_em_txt("cursos.txt", coletar_registros(arvore_cursos, "cursos"))
salvar_em_txt("alunos.txt", coletar_registros(arvore_alunos, "alunos"))
salvar_em_txt("autores.txt", coletar_registros(arvore_autores, "autores"))
salvar_em_txt("categorias.txt", coletar_registros(arvore_categorias, "categorias"))
salvar_em_txt("emprestimos.txt", coletar_registros(arvore_emprestimos, "emprestimos"))

"""
! Listar livros emprestados não está funcionando aparentemente
! Verificar exibição de algumas funções
! Melhorar exibição de títulos do menu
! Problema em salvar os livros, aparece no arquivo txt porem nao reconhece apos listar. pode ser diretório errado ou o arquivo txt de livros nao esta ne mesma pasta do py
"""
