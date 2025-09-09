# Sistema de Gerenciamento de Biblioteca – Arquivos Indexados

## 📌 Descrição

Este projeto implementa um sistema de biblioteca utilizando Árvores Binárias para gerenciar índices em memória e arquivos TXT para armazenamento persistente de dados. O sistema permite:

- Cadastro de livros, autores, categorias, alunos, cursos e cidades.
- Registro de empréstimos e devoluções.
- Consulta e listagem de livros, incluindo quantidade de livros disponíveis e emprestados.
- Visualização de livros atrasados e quantidade de empréstimos em um período específico.
- Integração com front-end HTML simples usando Flask, permitindo interatividade via navegador.

## ⚙️ Funcionalidades

### Sistema de Dados
- **Árvores Binárias:** armazenamento e busca eficiente de livros, autores, alunos, categorias, cursos e cidades.
- **TXT:** persistência de livros, garantindo que dados não se percam entre execuções.

### Funcionalidades do Sistema
- Cadastrar livros, autores, categorias, cursos, alunos e cidades.
- Registrar empréstimos e devoluções de livros.
- Consultar livros disponíveis, emprestados e atrasados.
- Listar todos os livros com autor, categoria e disponibilidade.
- Contabilizar quantidade de empréstimos por período.

### Front-end
- Página inicial com links para cadastro e listagem.
- Formulários para cadastro de livros, autores, alunos e registro de empréstimos.
- Listagem interativa de livros e relatórios de empréstimos.

## 🚀 Como executar

1. Clone este repositório:
 ```bash
   git clone https://github.com/seu-usuario/sistema-biblioteca.git
 ```   
2. Instale o Flask (ou outro servidor web se desejar):
 ```bash
pip install flask
```

3. Execute o arquivo principal do sistema:
  ```bash
python main.py
 ```

4. Abra o navegador e acesse:
 ```bash
http://127.0.0.1:5000
 ```

---

Feito com 💻 e 🧠, por Kaique.

--- 
