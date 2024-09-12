import time
import os
import sys
from pipeline.decision_tree import DecisionTree
from pipeline.text_processing import process_text
import requests
import unidecode
from fuzzywuzzy import fuzz

def normalize_input(user_input):
    """
    Normaliza a entrada do usuário para comparação.

    Args:
        user_input (str): A entrada do usuário.

    Returns:
        str: A entrada do usuário normalizada.
    """
    user_input = user_input.strip().lower()
    user_input = unidecode.unidecode(user_input)
    return user_input

def map_keyword_to_index(keyword, menu):
    """
    Mapeia uma palavra-chave para um índice do menu.

    Args:
        keyword (str): Palavra-chave fornecida pelo usuário.
        menu (list): Lista de opções do menu.

    Returns:
        int or None: O índice da opção do menu correspondente à palavra-chave, ou None se não encontrado.
    """
    keyword_normalized = normalize_input(keyword)
    for index, option in enumerate(menu, start=1):
        if fuzz.partial_ratio(normalize_input(option), keyword_normalized) > 80:  
            return index
    return None

class Chatbot:
    def __init__(self):
        self.decision_tree = DecisionTree()
        self.current_menu = self.decision_tree.tree
        self.previous_menus = []
        self.last_option = ""

    def show_menu(self):
        """
        Exibe o menu atual para o usuário.
        """
        print("\n" + "="*30)
        print("Escolha uma das opções:")
        for idx, option in enumerate(self.current_menu, start=1):
            print(f"{idx}. {option}")
        print("5. Voltar")
        print("6. Sair")
        print("="*30)

    def navigate(self, user_input):
        """
        Navega pelo menu com base na entrada do usuário.

        Args:
            user_input (str): Entrada do usuário.

        Returns:
            tuple: Uma tupla contendo uma mensagem para o usuário e um booleano indicando se deve continuar ou não.
        """
        processed_input = process_text(user_input)
        normalized_input = normalize_input(' '.join(processed_input))

        if normalized_input == "sair":
            print("Encerrando o chatbot...")
            print("\nAgradecemos por usar o chatbot! Até a próxima!")     
            return sys.exit(0) 
        
        elif normalized_input == "voltar":
            if self.previous_menus:
                self.current_menu = self.previous_menus.pop()
                return "Voltando ao menu anterior...", False
            else:
                return "Você já está no menu inicial.", False
        else:
            index = None
            if normalized_input.isdigit():
                index = int(normalized_input)
            elif any(fuzz.partial_ratio(normalize_input(option), normalized_input) > 80 for option in self.current_menu):
                for option in self.current_menu:
                    if fuzz.partial_ratio(normalize_input(option), normalized_input) > 80:
                        index = list(self.current_menu.keys()).index(option) + 1
                        break
            else:
                index = map_keyword_to_index(user_input, self.current_menu)

            if index and 1 <= index <= len(self.current_menu):
                option = list(self.current_menu.keys())[index - 1]
                if isinstance(self.current_menu[option], dict):
                    self.previous_menus.append(self.current_menu)
                    self.current_menu = self.current_menu[option]
                    return f"Você escolheu {option}. O que mais você gostaria de saber?", False
                else:
                    final_text = self.current_menu[option]
                    prompt = (
                        f"Por favor, forneça uma explicação detalhada sobre '{option}'. "
                        f"O contexto é: {final_text}"
                    )
                    llm_response = self.query_llm(prompt)
                    return (
                        f"{final_text}\n\nAqui você confere mais detalhes sobre a opção escolhida:\n\n"
                        f"{llm_response}\n\n"
                    ), True
            else:
                return "Opção inválida. Por favor, escolha uma opção válida.", False

    def query_llm(self, prompt, max_tokens=100000):  
        """
        Consulta o modelo de linguagem para gerar uma resposta com base no prompt fornecido.

        Args:
            prompt (str): O prompt para o modelo de linguagem.
            max_tokens (int): Número máximo de tokens para gerar. Padrão é 100000.

        Returns:
            str: Texto gerado pelo modelo de linguagem.
        """
        model_id = "EleutherAI/gpt-neo-2.7B"
        url = f"https://api-inference.huggingface.co/models/{model_id}"
        headers = {"Authorization": "Bearer <SUA_CHAVE_API_AQUI>"}
        data = {"inputs": prompt, "parameters": {"max_length": max_tokens, "temperature": 0.5}}

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            response_data = response.json()

            if isinstance(response_data, list) and len(response_data) > 0:
                generated_text = response_data[0].get('generated_text', '').strip()
                
                if generated_text.startswith(prompt):
                    generated_text = generated_text[len(prompt):].strip()
                
                return generated_text
            else:
                return 'Não foi possível gerar uma resposta adequada.'
        except requests.exceptions.RequestException as e:
            return f"Erro ao consultar o LLM: {e}"

    def run(self):
        """
        Inicia o loop principal do chatbot.
        """
        while True:
            self.show_menu()
            user_input = input("Digite sua escolha: ")
            response, ask_to_continue = self.navigate(user_input)
            print("\n" + "="*30)
            print(response)
            print("="*30)

            if ask_to_continue:
                user_input = input("Deseja continuar? (1 para Sim / 2 para Não): ")
                normalized_input = normalize_input(user_input)

                match normalized_input:
                    case "1" | "sim":
                        continue
                    case "2" | "não" | "nao":
                        print("\nAgradecemos por usar o chatbot! Até a próxima!")
                        break
                    case _:
                        print("Opção inválida. Tente novamente.")
            elif response.startswith("Encerrando"):
                print("\nAgradecemos por usar o chatbot! Até a próxima!\n\n")
                break

if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.run()
