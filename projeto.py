import requests
import pandas as pd
import json
import random

# Dicionário de mapeamento de funções para IDs e nomes dos responsáveis
responsaveis_por_funcao = {
    0: {"id": "x", "nome": "Bruno Moreira"},
    1.1: {"id": "x", "nome": "Bruno Moreira"},
    1.2: {"id": "x", "nome": "Bruno Moreira"},
    2: {"id": "x", "nome": "Bruno Moreira"},
    3.1: {"id": "x", "nome": "Bruno Moreira"},
    3.2: {"id": "x", "nome": "Bruno Moreira"},
    4: {"id": "x", "nome": "Bruno Moreira"},
    5: {"id": "x", "nome": "Bruno Moreira"}  # Exemplo para a função 5
}

# Função para enviar mensagem ao Teams com a menção ao responsável
def enviar_mensagem_webhook_com_botoes(webhook_url, funcao, funcao_ajuda_escolhida):
    if funcao_ajuda_escolhida not in responsaveis_por_funcao:
        print(f"Não há responsável cadastrado para a função {funcao_ajuda_escolhida}.")
        return

    mention_id = responsaveis_por_funcao[funcao_ajuda_escolhida]["id"]
    mention_name = responsaveis_por_funcao[funcao_ajuda_escolhida]["nome"]

    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.4",
                    "type": "AdaptiveCard",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": f"🚨 Função {funcao} tem mais de um caminhão complexo e precisa de ajuda! 🚨",
                            "weight": "Bolder",
                            "size": "Medium"
                        },
                        {
                            "type": "TextBlock",
                            "text": f"<at>{mention_name}</at>, a função {funcao_ajuda_escolhida} foi escolhida para ajudar. Clique em uma opção abaixo:",
                            "wrap": True
                        }
                    ],
                    "msteams": {
                        "entities": [
                            {
                                "type": "mention",
                                "text": f"<at>{mention_name}</at>",
                                "mentioned": {
                                    "id": mention_id,
                                    "name": mention_name
                                }
                            }
                        ]
                    },
                    "actions": [
                        {
                            "type": "Action.Submit",
                            "title": "Estou indo ajudar",
                            "data": {
                                "acao": "indo_ajudar",
                                "funcao": funcao_ajuda_escolhida,
                                "mention_id": mention_id
                            }
                        },
                        {
                            "type": "Action.Submit",
                            "title": "Não consigo ajudar",
                            "data": {
                                "acao": "nao_posso_ajudar",
                                "funcao": funcao_ajuda_escolhida,
                                "mention_id": mention_id
                            }
                        }
                    ]
                }
            }
        ]
    }
    
    response = requests.post(webhook_url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print("Mensagem enviada com sucesso ao Teams!")
    else:
        print(f"Erro ao enviar mensagem: {response.status_code}, {response.text}")

# Condição para verificar se o veículo é complexo
def eh_complexo(linha, funcao):
    def trata_valor(valor):
        if pd.isna(valor):
            return ''
        return str(valor).upper()

    opc = trata_valor(linha.get('OPCIONAIS', ''))
    modelo = trata_valor(linha.get('MODELO', ''))
    gas = trata_valor(linha.get('GÁS', ''))
    smac = trata_valor(linha.get('SMAC', ''))

    if funcao == 0:
        return '8X2' in modelo
    elif funcao == 1.1:
        return 'COOLING' in opc
    elif funcao == 1.2:
        return '8X2' in modelo
    elif funcao == 2:
        return 'HD FRONT' in opc and 'HD HAI' in opc
    elif funcao == 3.1:
        return 'N_MODULE' in modelo
    elif funcao == 3.2:
        return 'N_MODULE' in modelo
    elif funcao == 4:
        return 'GÁS' in gas
    elif funcao == 5:
        return 'SMAC' in smac
    return False

# Mapeamento de funções
def obter_funcao(posto):
    posto_map = {
        '01': 0, '02': 0, '03': 0, '04': 0, '05': 0, '06': 0, '07': 1.1, '111': 1.1, '112': 1.1,
        '113': 1.1, '114': 1.1, '115': 1.1, '116': 1.1, '117': 1.1, '118': 1.1, '121': 1.2,
        '122': 1.2, '123': 1.2, '124': 1.2, '125': 1.2, '21': 2, '22': 2, '23': 2, '24': 2, 
        'TT1': 3.1, '311': 3.1, '312': 3.1, 'TT2': 3.1, '313': 3.1, '321': 3.2, '322': 3.2, 
        'TT3': 3.2, '41': 4, '42': 4, '43': 4, '44': 4, '51': 5, '52': 5, '53': 5, '54': 5, '55': 5
    }
    return posto_map.get(posto, None)

# Função para processar a resposta e verificar se apenas a pessoa mencionada pode interagir
def processar_resposta(usuario_id, dados_interacao):
    mention_id = dados_interacao.get('mention_id')
    
    if usuario_id == mention_id:
        return "Resposta aceita. Obrigado por confirmar!"
    else:
        return "Desculpe, apenas a pessoa mencionada pode interagir com este botão."

def main():
    webhook_url = "https://scaniaazureservices.webhook.office.com/webhookb2/7ace8702-0055-4e89-915d-475118122f26@3bc062e4-ac9d-4c17-b4dd-3aad637ff1ac/IncomingWebhook/a47eaf96360e42bf86a2583d65269c18/aca8d18c-d67d-44ba-8fec-dcc307167dbe/V2RzH-2H4TpuE0JomcY9bhfyhT-dFU06BGFlTA_wVhAbU1"

    url = 'https://controltower.br.scania.com/system/webdev/MainScreen_ControlTower/fila_popid'
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        try:
            resultado = resposta.json()
            
            if 'Truck' in resultado:
                resultado = resultado['Truck']
            else:
                print("A resposta não contém a chave 'Truck'.")
                return
                
        except json.JSONDecodeError as e:
            print("Erro ao decodificar JSON:", e) 
            return
    else:
        print("Erro na resposta da API:", resposta.status_code)
        return

    df_veiculos = pd.read_csv('mix_nov.csv', sep=';', encoding='utf-8')
    df_veiculos['POPID'] = df_veiculos['POPID'].astype(str).str.strip()

    colunas_remover = ["SCOB", "MIX", "MU", "COR", "REPLAN", "SEQ", "SORDER", "FFU", "CHASSIS HEIGHT", 
                       "RPX", "LATERAL", "HIGH LINE", "CAB MOD", "COD CHASSIS", "LEVEL", "CHASSI", 
                       "COMPRIM", "CAB MOD", "RETARDER", "TANQUE", "LNG", "DW", "FOU", "ABS", 
                       "BARRA TRASEIRA", "DEF", "RHD", "AUX CAB COOLER", 'ENTRADA LINHA REAL', 
                       'BARRA 2°E DIANT', 'COD POPID', 'SEQ.']
    df_veiculos.drop(colunas_remover, axis=1, inplace=True)

    postos = {}
    for item in resultado:
        popid = item.get('popid')
        posto = item.get('posto')
        if popid and posto:
            postos[popid.strip()] = posto

    veiculos_complexos = {0: [], 1.1: [], 1.2: [], 2: [], 3.1: [], 3.2: [], 4: [], 5: []}
    todos_postos = list(postos.values())

    for popid, posto in postos.items():
        funcao = obter_funcao(posto) 
        if funcao is not None:
            veiculo = df_veiculos[df_veiculos['POPID'] == popid]
            if not veiculo.empty:
                linha_veiculo = veiculo.iloc[0]
                if eh_complexo(linha_veiculo, funcao):
                    if popid not in veiculos_complexos[funcao]:
                        veiculos_complexos[funcao].append((popid, posto))

    print("Veículos complexos por função:")
    for funcao, veiculos in veiculos_complexos.items():
        if veiculos:
            print(f"Função {funcao}:")
            for popid, posto in veiculos:
                print(f"  Veículo com POPID {popid} no posto {posto}.")
    
    funcoes_sem_veiculos = {f for f, veiculos in veiculos_complexos.items() if not veiculos}
    funcoes_com_mais_de_um = {f for f, veiculos in veiculos_complexos.items() if len(veiculos) > 1}
    
    funcoes_que_podem_ajudar = {}
    
    for funcao in funcoes_com_mais_de_um:
        if funcao == 5 and len(veiculos_complexos[funcao]) < 3:
            continue  
        print(f"\nFunção {funcao} tem mais de um caminhão complexo e precisa de ajuda.")
        
        funcoes_possiveis_ajuda = []
        for funcao_ajuda in funcoes_sem_veiculos:
            if funcao_ajuda != 0:  
                proximos_veiculos = [postos.get(v[0]) for v in veiculos_complexos[funcao] if v[0] in postos]
                futuros_veiculos = proximos_veiculos[:4]
                if not any(obter_funcao(posto) == funcao_ajuda for posto in futuros_veiculos):
                    funcoes_possiveis_ajuda.append(funcao_ajuda)
        
        if funcoes_possiveis_ajuda:
            funcoes_que_podem_ajudar[funcao] = funcoes_possiveis_ajuda

    funcoes_ja_chamadas = []

    for funcao, possiveis_ajudas in funcoes_que_podem_ajudar.items():
        if possiveis_ajudas:
            funcoes_disponiveis = list(set(possiveis_ajudas) - set(funcoes_ja_chamadas))
            if funcoes_disponiveis:
                funcao_ajuda_escolhida = random.choice(funcoes_disponiveis)
                funcoes_ja_chamadas.append(funcao_ajuda_escolhida)
                enviar_mensagem_webhook_com_botoes(webhook_url, funcao, funcao_ajuda_escolhida)

if __name__ == "__main__":
    main()
