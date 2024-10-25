import os
import struct

# Definindo o tamanho fixo dos campos de acesso
campos_acesso = {'User_id': 10,
                 'data_ultimo_acesso': 20,
                 'quantidade_acessos': 5,
                 'nome': 30,
                 'sessao': 10
                }

# Função para ajustar o tamanho dos campos
def ajustar_tamanho(campo, tamanho):
    return campo.ljust(tamanho)[:tamanho]

# Função para mostrar dados de acessos
def mostrar_dados_acessos():
    if os.path.exists('dados_acesso_fixo.bin'):
        with open('dados_acesso_fixo.bin', 'rb') as bin_file:
            for linha in bin_file:
                print(linha.decode('utf-8').strip())
    else:
        print("Arquivo binário de acessos não encontrado.")

def pesquisa_binaria_acessos(chave, campo='User_id'):
    # Cálculo do tamanho total do registro
    tamanho_registro = sum(campos_acesso.values())
    
    with open('dados_acesso_fixo.bin', 'rb') as bin_file:
        bin_file.seek(0, os.SEEK_END)
        registros = bin_file.tell() // tamanho_registro
        
        inicio, fim = 0, registros - 1
        
        while inicio <= fim:
            meio = (inicio + fim) // 2
            bin_file.seek(meio * tamanho_registro)
            registro = bin_file.read(tamanho_registro).decode('utf-8').strip()
            
            # Lendo os campos baseando-se nos tamanhos fixos
            valor_campo = registro[:campos_acesso[campo]].strip()  
            
            if valor_campo == chave:
                print(f"Registro encontrado: {registro}")
                return registro
            elif valor_campo < chave:
                inicio = meio + 1
            else:
                fim = meio - 1
                
        print("Registro não encontrado.")
        return None

# Função para inserir novos dados de acessos
def inserir_dados_acesso(dados):
    formato = '10s20s30s10s20s' 
    dados_ajustados = tuple(ajustar_tamanho(dados[campo], tamanho).encode('utf-8') for campo, tamanho in campos_acesso.items())
    dados_binarios = struct.pack(formato, *dados_ajustados)
    with open('dados_acesso_fixo.bin', 'ab') as bin_file:
        bin_file.write(dados_binarios)

def remover_acesso_por_id(id_remocao):
    registros = []
    encontrado = False

    with open('dados_acesso_fixo.bin', 'rb') as bin_file:
        while True:
            registro = bin_file.read(sum(campos_acesso.values()))  
            if not registro:
                break 
            id_atual = registro[:campos_acesso['User_id']].strip().decode('utf-8')
            if id_atual == str(id_remocao):
                encontrado = True
                continue  
            registros.append(registro)

    with open('dados_acesso_fixo.bin', 'wb') as bin_file:
        for registro in registros:
            bin_file.write(registro)

    if encontrado:
        print(f"User com ID {id_remocao} removido.")
    else:
        print(f"User com ID {id_remocao} não encontrado.")