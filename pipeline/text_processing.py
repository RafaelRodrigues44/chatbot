from gensim.utils import simple_preprocess
from spellchecker import SpellChecker
import spacy
from collections import Counter
import unidecode


nlp = spacy.load('pt_core_news_sm')

spell = SpellChecker(language='pt')

def process_text(text):
    """
    Processa o texto fornecido realizando normalização, tokenização, correção ortográfica e lematização.

    Etapas do processamento:
    1. Normaliza o texto, removendo acentos e caracteres especiais.
    2. Tokeniza o texto em uma lista de palavras.
    3. Corrige a ortografia dos tokens usando um corretor ortográfico.
    4. Lematiza os tokens, reduzindo-os à sua forma base.

    Args:
        text (str): O texto a ser processado.

    Returns:
        list: Uma lista de tokens lematizados.
    """

    text = unidecode.unidecode(text)

    tokens = simple_preprocess(text, deacc=True)

    tokens = [spell.candidates(token).pop() if spell.candidates(token) else token for token in tokens]

    doc = nlp(' '.join(tokens))
    lemmatized_tokens = [token.lemma_ for token in doc]

    return lemmatized_tokens

def get_word_frequency(tokens):
    """
    Calcula a frequência das palavras a partir de uma lista de tokens.

    Args:
        tokens (list): Uma lista de tokens.

    Returns:
        Counter: Um objeto `Counter` contendo a frequência de cada token na lista.
    """
    return Counter(tokens)
