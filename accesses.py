import os
import struct

# Definindo o tamanho fixo dos campos de acesso
campos_acesso = {'User_id': 10, 'data_ultimo_acesso': 20, 'quantidade_acessos': 5, 'nome': 30, 'sessao': 10}
tamanho_registro = sum(campos_acesso.values())
formato = '10s20s30s10s20s'

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

# Função para gerar índice de acessos (ordenado por User_id)
def gerar_indice_acesso(arquivo_dados, arquivo_indice):
    with open(arquivo_dados, 'rb') as f_dados, open(arquivo_indice, 'wb') as f_indice:
        while True:
            registro = f_dados.read(40)  

            if not registro:
                break

            if len(registro) < 10:
                print("Registro inválido ou incompleto:", registro)
                continue  

            try:
                chave = int(registro[:10].decode('utf-8').strip())  
            except ValueError as e:
                print(f"Erro ao converter chave: {e}. Registro: {registro}")
                continue  
            f_indice.write(chave.to_bytes(4, 'little'))  

# Função para atualizar o índice após inserção
def atualizar_indice_acesso():
    gerar_indice_acesso('dados_acesso_fixo.bin', 'indice_acesso.idx')

# Função de pesquisa binária utilizando o índice
def pesquisa_binaria_por_indice_acesso(nome_indice, chave_procurada):
    with open(nome_indice, 'rb') as indice:
        tamanho_registro_indice = struct.calcsize('10s i')
        low = 0
        indice.seek(0, 2)
        high = indice.tell() // tamanho_registro_indice - 1

        while low <= high:
            mid = (low + high) // 2
            pos = mid * tamanho_registro_indice
            indice.seek(pos)
            chave_indice, pos_arquivo = struct.unpack('10s i', indice.read(tamanho_registro_indice))
            chave_indice = chave_indice.decode('utf-8').strip()
            
            if chave_indice == chave_procurada:
                return pos_arquivo
            elif chave_indice < chave_procurada:
                low = mid + 1
            else:
                high = mid - 1
        return -1

# Função de inserção de dados com atualização de índice
def inserir_dados_acesso(dados):
    # Converte o ID do acesso para inteiro
    id_novo = int(dados['User_id'])
    dados_ajustados = tuple(ajustar_tamanho(dados[campo], tamanho).encode('utf-8') for campo, tamanho in campos_acesso.items())

    posicao_inserir = None
    registros = []

    with open('dados_acesso_fixo.bin', 'rb') as bin_file:
        while True:
            registro = bin_file.read(tamanho_registro)
            if not registro:
                break
            
            id_str = registro[:10].strip().decode('utf-8')
            if id_str.isdigit():  
                id_atual = int(id_str)

                if registro[-1] == b'1':  
                    continue

                if id_novo < id_atual:  
                    posicao_inserir = len(registros)
                    break
            registros.append(registro)

    if posicao_inserir is None:
        posicao_inserir = len(registros)

    registros.insert(posicao_inserir, struct.pack(formato, *dados_ajustados))

    # Sobrescreve o arquivo com os registros atualizados
    with open('dados_acesso_fixo.bin', 'wb') as bin_file:
        for registro in registros:
            bin_file.write(registro)
    print(f"acesso com ID {id_novo} inserido com sucesso.")

# Função de remoção de acesso por User_id com atualização de índice
def remover_acesso_por_id(id_remocao):
    registros = []
    encontrado = False

    with open('dados_acesso_fixo.bin', 'rb') as bin_file:
        while True:
            registro = bin_file.read(tamanho_registro)  
            if not registro:
                break 

            id_str = registro[:10].strip().decode('utf-8')
            if id_str.isdigit():  # Verifica se é um número válido
                id_atual = int(id_str)
                
                if id_atual == id_remocao and registro[-1] != b'1':  
                    encontrado = True
                    registro = registro[:-1] + b'1' 
            registros.append(registro)

    if encontrado:
        with open('dados_acesso_fixo.bin', 'wb') as bin_file:
            for registro in registros:
                bin_file.write(registro)
        print(f"Acesso com ID {id_remocao} marcado como excluído.")
    else:
        print(f"Acesso com ID {id_remocao} não encontrado.")
