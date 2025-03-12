import json
import re

def carregar_definicao_lexica(arquivo_json):
    with open(arquivo_json, 'r', encoding='utf-8') as f:
        return json.load(f)

def ler_arquivo_texto(arquivo_txt):
    with open(arquivo_txt, 'r', encoding='utf-8') as f:
        return f.read()

def extrair_tokens(texto):
    padrao = r"\"{3}[\s\S]*?\"{3}|'{3}[\s\S]*?'{3}|#[^\n]*|\w+|\d+\.?\d*(?:[eE][+-]?\d+)?|[^a-zA-Z0-9\s]|\s+"
    return re.findall(padrao, texto, re.UNICODE)

def analisar_texto(texto, definicao_lexica):
    tokens_identificados = []
    
    tokens = extrair_tokens(texto)

    for token in tokens:
        
        if re.fullmatch(r"\s+", token, re.UNICODE):
            continue

        token_encontrado = False

        for regra in definicao_lexica["tokens"]:
            if "keywords" in regra:  
                if token in regra["keywords"] and re.fullmatch(r"^\b" + token + r"\b", token, re.UNICODE):  
                    tokens_identificados.append({
                        "token": token,
                        "name": regra["name"]
                    })
                    token_encontrado = True
                    break  

        
        if not token_encontrado:
            for regra in definicao_lexica["tokens"]:
                if "regex" in regra and re.fullmatch(regra["regex"], token, re.UNICODE):  
                    tokens_identificados.append({
                        "token": token,
                        "name": regra["name"]
                    })
                    token_encontrado = True
                    break  

        
        if not token_encontrado:
            print(f"Token desconhecido: {token}")  
            tokens_identificados.append({
                "token": token,
                "name": "DESCONHECIDO"
            })

    return tokens_identificados

def salvar_resultado(tokens, arquivo_saida):
    
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        json.dump(tokens, f, indent=2, ensure_ascii=False)
    print(f"Resultado salvo em {arquivo_saida}")

def main():
    
    arquivo_json = "definicao_lexica.json"
    arquivo_txt = "entrada.txt"
    arquivo_saida = "resultado_analise.json"

    
    definicao_lexica = carregar_definicao_lexica(arquivo_json)
    texto = ler_arquivo_texto(arquivo_txt)

    tokens = analisar_texto(texto, definicao_lexica)

    salvar_resultado(tokens, arquivo_saida)

if __name__ == "__main__":
    main()