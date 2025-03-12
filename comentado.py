import json
import re

def carregar_definicao_lexica(arquivo_json):
    """Carrega a definição léxica do arquivo JSON"""
    with open(arquivo_json, 'r', encoding='utf-8') as f:
        return json.load(f)

def ler_arquivo_texto(arquivo_txt):
    """Lê o conteúdo do arquivo de entrada"""
    with open(arquivo_txt, 'r', encoding='utf-8') as f:
        return f.read()

def extrair_tokens(texto):
    """
    Divide o texto em tokens considerando palavras, números (incluindo notação científica),
    símbolos, strings/comentários de múltiplas linhas e comentários de linha única
    """
    padrao = r"\"{3}[\s\S]*?\"{3}|'{3}[\s\S]*?'{3}|#[^\n]*|\w+|\d+\.?\d*(?:[eE][+-]?\d+)?|[^a-zA-Z0-9\s]|\s+"
    return re.findall(padrao, texto, re.UNICODE)

def analisar_texto(texto, definicao_lexica):
    """Analisa o texto e identifica os tokens conforme a definição JSON"""
    tokens_identificados = []
    
    # Extrai tokens corretamente usando regex
    tokens = extrair_tokens(texto)

    for token in tokens:
        # Ignora espaços em branco
        if re.fullmatch(r"\s+", token, re.UNICODE):
            continue

        token_encontrado = False

        # Verifica se o token é uma palavra-chave
        for regra in definicao_lexica["tokens"]:
            if "keywords" in regra:  # Se a regra for para palavras-chave
                if token in regra["keywords"] and re.fullmatch(r"^\b" + token + r"\b", token, re.UNICODE):  # Garante que é uma palavra inteira
                    tokens_identificados.append({
                        "token": token,
                        "name": regra["name"]
                    })
                    token_encontrado = True
                    break  # Para na primeira palavra-chave correspondente

        # Se não for palavra-chave, verifica se corresponde à expressão regular
        if not token_encontrado:
            for regra in definicao_lexica["tokens"]:
                if "regex" in regra and re.fullmatch(regra["regex"], token, re.UNICODE):  # Verifica se "regex" existe
                    tokens_identificados.append({
                        "token": token,
                        "name": regra["name"]
                    })
                    token_encontrado = True
                    break  # Para na primeira regra correspondente

        # Se não encontrar nenhum padrão
        if not token_encontrado:
            print(f"Token desconhecido: {token}")  # Log para depuração
            tokens_identificados.append({
                "token": token,
                "name": "DESCONHECIDO"
            })

    return tokens_identificados

def salvar_resultado(tokens, arquivo_saida):
    """Salva os tokens identificados em um arquivo JSON"""
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        json.dump(tokens, f, indent=2, ensure_ascii=False)
    print(f"Resultado salvo em {arquivo_saida}")

def main():
    # Definir caminhos dos arquivos
    arquivo_json = "definicao_lexica.json"
    arquivo_txt = "entrada.txt"
    arquivo_saida = "resultado_analise.json"

    # Carregar definição léxica e texto de entrada
    definicao_lexica = carregar_definicao_lexica(arquivo_json)
    texto = ler_arquivo_texto(arquivo_txt)

    # Analisar e gerar tokens
    tokens = analisar_texto(texto, definicao_lexica)

    # Salvar resultado em um arquivo JSON
    salvar_resultado(tokens, arquivo_saida)

if __name__ == "__main__":
    main()