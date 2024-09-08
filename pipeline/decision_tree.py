class DecisionTree:
    def __init__(self):
        """
        Inicializa a árvore de decisão, que servirá como base para a formação automática do menu inicial do chatbot.

        A árvore de decisão contém várias categorias e subcategorias relacionadas a Python, suas características, bibliotecas, 
        aplicações e recursos comunitários. Cada categoria pode ter perguntas e respostas associadas.
        """
        self.tree = {
            "Sobre Python": {
                "História do Python": {
                    "O que é Python?": "Python é uma linguagem de programação de alto nível, criada por Guido van Rossum e lançada em 1991.",
                    "Quem criou o Python?": "Guido van Rossum é o criador do Python. Ele iniciou o projeto no final dos anos 1980.",
                    "Quando o Python foi lançado?": "Python foi lançado pela primeira vez em 1991.",
                },
                "Características do Python": {
                    "Sintaxe do python": "Python é conhecido por sua sintaxe clara e legível, que facilita a leitura e escrita de código.",
                    "Tipagem de dados em Python": "Python é uma linguagem de tipagem dinâmica, o que significa que você não precisa declarar o tipo das variáveis explicitamente.",
                    "Paradigmas de programação em Python": "Python suporta múltiplos paradigmas de programação, incluindo programação orientada a objetos, imperativa e funcional.",
                },
                "Bibliotecas e Frameworks": {
                    "Principais bibliotecas em Python": "Algumas das principais bibliotecas de Python incluem NumPy, Pandas, Matplotlib e Scikit-learn.",
                    "Frameworks populares em Python": "Frameworks populares incluem Django e Flask para desenvolvimento web, e TensorFlow e PyTorch para Machine Learning.",
                    "Como instalar bibliotecas em Python?": "Você pode instalar bibliotecas usando o comando 'pip install nome_da_biblioteca'.",
                }
            },
            "Aplicações do Python": {
                "Desenvolvimento Web": {
                    "Frameworks para web em Python": "Os frameworks populares para desenvolvimento web em Python incluem Django, Flask e FastAPI.",
                    "Desenvolvimento de APIs em Python": "Você pode usar frameworks como Flask-RESTful e FastAPI para criar APIs RESTful em Python.",
                    "Ferramentas e bibliotecas em Python": "Ferramentas como Jinja2 para templates e SQLAlchemy para ORM são amplamente usadas no desenvolvimento web com Python.",
                },
                "Análise de Dados": {
                    "Bibliotecas para análise de dados em Python": "Bibliotecas como Pandas e NumPy são amplamente utilizadas para análise de dados em Python.",
                    "Visualização de dados em Python": "Para visualização de dados, você pode usar bibliotecas como Matplotlib, Seaborn e Plotly.",
                    "Estatísticas e Machine Learning em Python": "Bibliotecas como Scikit-learn e Statsmodels são usadas para estatísticas e Machine Learning em Python.",
                },
                "Automação": {
                    "Automação de tarefas em Python": "Python é frequentemente usado para automatizar tarefas repetitivas e rotineiras.",
                    "Scripts para automação em Python": "Você pode escrever scripts Python para tarefas como renomear arquivos, manipular planilhas e interagir com APIs.",
                    "Ferramentas úteis para automação em Python": "Bibliotecas como Selenium e PyAutoGUI podem ser úteis para automação de tarefas em Python.",
                }
            },
            "Comandos e Funcionalidades": {
                "Comandos Básicos": {
                    "Como executar scripts Python?": "Você pode executar scripts Python usando o comando 'python nome_do_script.py'.",
                    "Como usar a REPL em Python?": "Para usar a REPL do Python, digite 'python' no terminal e você entrará no modo interativo do Python.",
                    "Como lidar com erros comuns em Python?": "Leia a mensagem de erro cuidadosamente e procure por soluções na documentação ou em fóruns.",
                },
                "Funções Avançadas": {
                    "O que são decoradores em Python?": "Decoradores são uma forma de modificar o comportamento de funções ou métodos sem alterar seu código.",
                    "Como criar geradores em Python?": "Geradores são criados usando a palavra-chave 'yield' e são usados para criar iteradores personalizados.",
                    "Uso de context managers em Python": "Context managers são usados para gerenciar recursos como arquivos e conexões de rede de forma eficiente.",
                },
                "Boas Práticas": {
                    "Estilo de código em Python": "Siga as diretrizes do PEP 8 para garantir um estilo de código limpo e consistente.",
                    "Testes e debugging em Python": "Escreva testes unitários e use ferramentas de debugging como pdb para identificar e corrigir bugs.",
                    "Documentação de código do Python": "Documente seu código usando docstrings e mantenha um README atualizado para facilitar a compreensão e manutenção.",
                }
            },
            "Recursos e Comunidade": {
                "Documentação": {
                    "Onde encontrar documentação oficial do Python?": "A documentação oficial do Python pode ser encontrada em https://docs.python.org.",
                    "Tutoriais recomendados do Python": "Tutoriais recomendados podem ser encontrados em sites como Real Python e W3Schools.",
                    "Livros e cursos para Python": "Livros populares incluem 'Automate the Boring Stuff with Python' e 'Python Crash Course'.",
                },
                "Comunidade": {
                    "Principais fóruns e grupos sobre Python": "Fóruns e grupos populares incluem Stack Overflow e Reddit r/learnpython.",
                    "Eventos e conferências sobre Python": "Eventos como PyCon e Meetups locais são ótimas oportunidades para aprender e se conectar com outros desenvolvedores.",
                    "Contribuições para projetos open-source em Python": "Contribua para projetos open-source no GitHub e participe de hackathons para ganhar experiência prática.",
                }
            }
        }
        self.index = self.build_index()

    def build_index(self):
        """
        Constrói um índice que mapeia caminhos completos para opções de menu.

        Este índice é usado para facilitar a correspondência de texto com opções de menu.

        Returns:
            dict: Um dicionário onde as chaves são caminhos completos (em minúsculas) e os valores são as opções de menu.
        """
        index = {}
        
        def add_to_index(menu, path=""):
            for key, value in menu.items():
                full_path = f"{path}/{key}".strip("/")
                index[full_path.lower()] = key
                if isinstance(value, dict):
                    add_to_index(value, full_path)
        
        add_to_index(self.tree)
        return index

    def map_text_to_option(self, text):
        """
        Mapeia o texto de entrada para o número da opção correspondente na árvore de decisão.

        Args:
            text (str): O texto fornecido pelo usuário.

        Returns:
            int or None: O número da opção correspondente se encontrada, caso contrário, retorna None.
        """
        text = text.lower()
        for i, (key, value) in enumerate(self.tree.items(), 1):
            if text in key.lower() or key.lower() in text:
                return i
        return None

    def map_option_to_text(self, option_number):
        """
        Mapeia o número da opção para o texto da opção correspondente na árvore de decisão.

        Args:
            option_number (int): O número da opção.

        Returns:
            str or None: O texto da opção correspondente se o número estiver dentro do intervalo, caso contrário, retorna None.
        """
        options = list(self.tree.keys())
        if 1 <= option_number <= len(options):
            return options[option_number - 1]
        return None
