import csv
import json
import os
from typing import List, Dict, Any


class DataConverter:
    """
    Classe especialista para conversão bidirecional entre formatos JSON e CSV.
    Garante o fechamento correto de handles de arquivo e tratamento de erros.
    """

    @staticmethod
    def json_to_csv(json_file_path: str, csv_file_path: str) -> None:
        """
        Converte um arquivo JSON (contendo uma lista de objetos) em um arquivo CSV.
        """
        if not os.path.exists(json_file_path):
            raise FileNotFoundError(f"O arquivo JSON não foi encontrado: {json_file_path}")

        try:
            with open(json_file_path, mode='r', encoding='utf-8') as json_file:
                data: Any = json.load(json_file)

            # Garante que o JSON de entrada seja uma lista de dicionários
            if not isinstance(data, list):
                # Se for um único objeto, encapsula em uma lista
                if isinstance(data, dict):
                    data = [data]
                else:
                    raise ValueError("O formato do JSON deve ser um objeto ou uma lista de objetos.")

            if not data:
                print(f"Aviso: O arquivo {json_file_path} está vazio. Gerando CSV apenas com cabeçalho (se aplicável).")
                return

            # Extrai os cabeçalhos a partir das chaves do primeiro dicionário
            headers: List[str] = list(data[0].keys())

            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                # Usando DictWriter para mapear dicionários diretamente para as colunas do CSV
                writer = csv.DictWriter(csv_file, fieldnames=headers)
                writer.writeheader()

                for row in data:
                    # Tratamento preventivo: se houver dicionários/listas aninhados, converte para string
                    # para evitar que a formatação pura do CSV quebre.
                    processed_row = {}
                    for key, value in row.items():
                        if isinstance(value, (dict, list)):
                            processed_row[key] = json.dumps(value, ensure_ascii=False)
                        else:
                            processed_row[key] = value
                    
                    writer.writerow(processed_row)

            print(f"Sucesso: {json_file_path} convertido para {csv_file_path}")

        except json.JSONDecodeError as e:
            print(f"Erro de sintaxe no JSON: {e}")
            raise
        except Exception as e:
            print(f"Erro inesperado na conversão JSON -> CSV: {e}")
            raise

    @staticmethod
    def csv_to_json(csv_file_path: str, json_file_path: str, indent: int = 4) -> None:
        """
        Converte um arquivo CSV em um arquivo JSON (uma lista de objetos).
        """
        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"O arquivo CSV não foi encontrado: {csv_file_path}")

        try:
            data: List[Dict[str, Any]] = []

            with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
                # DictReader usa a primeira linha automaticamente como chaves do dicionário
                csv_reader = csv.DictReader(csv_file)
                
                for row in csv_reader:
                    # Tenta inferir tipos ou decodificar strings que eram JSONs aninhados
                    processed_row = {}
                    for key, value in row.items():
                        if value is None:
                            processed_row[key] = None
                            continue
                        
                        clean_value = value.strip()
                        # Tentativa de conversão de estruturas complexas salvas como string
                        if (clean_value.startswith('{') and clean_value.endswith('}')) or \
                           (clean_value.startswith('[') and clean_value.endswith(']')):
                            try:
                                processed_row[key] = json.loads(clean_value)
                            except json.JSONDecodeError:
                                processed_row[key] = clean_value
                        else:
                            processed_row[key] = clean_value
                    
                    data.append(processed_row)

            with open(json_file_path, mode='w', encoding='utf-8') as json_file:
                # ensure_ascii=False mantém caracteres acentuados legíveis (PT-BR)
                json.dump(data, json_file, indent=indent, ensure_ascii=False)

            print(f"Sucesso: {csv_file_path} convertido para {json_file_path}")

        except Exception as e:
            print(f"Erro inesperado na conversão CSV -> JSON: {e}")
            raise


# --- Exemplo Prático de Uso ---
if __name__ == "__main__":
    # 1. Mock de dados para teste
    sample_json_data = [
        {"id": 1, "nome": "Alairton", "cargo": "Analista Sênior", "tecnologias": ["Python", "Docker"]},
        {"id": 2, "nome": "Maria", "cargo": "Desenvolvedora", "tecnologias": ["SQL", "IRIS"]}
    ]
    
    # Criando um arquivo JSON temporário para testar
    with open("input.json", "w", encoding="utf-8") as f:
        json.dump(sample_json_data, f, indent=4, ensure_ascii=False)

    print("--- Iniciando Testes de Conversão ---")
    
    # Executando JSON -> CSV
    DataConverter.json_to_csv("input.json", "output.csv")
    
    # Executando CSV -> JSON (gerando um novo arquivo para comparar)
    DataConverter.csv_to_json("output.csv", "output_final.json")