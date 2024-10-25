import os
import struct

# Definindo o tamanho fixo dos campos de acesso
campos_acesso = {'User_id': 10, 'data_ultimo_acesso': 20, 'quantidade_acessos': 5, 'nome': 30, 'sessao': 10}
tamanho_registro = sum(campos_acesso.values())

# Função para gerar índice de acessos (ordenado por ID de usuário)
def gerar_indice_acesso(nome_arquivo, nome_indice):
    with open(nome_arquivo, 'rb') as arquivo, open(nome_indice, 'wb') as indice:
        pos = 0
        while True:
            registro = arquivo.read(tamanho_registro)
            if not registro:
                break
            chave = registro[:10].decode('utf-8').strip()  # User_id
            indice.write(struct.pack('10s i', chave.encode('utf-8'), pos))
            pos += tamanho_registro

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
    dados_ajustados = tuple(ajustar_tamanho(dados[campo], tamanho).encode('utf-8') for campo, tamanho in campos_acesso.items())
    dados_binarios = struct.pack('10s20s5s30s10s', *dados_ajustados)
    
    # Inserir no arquivo binário
    with open('dados_acesso_fixo.bin', 'ab') as bin_file:
        bin_file.write(dados_binarios)
    
    # Atualizar o índice
    atualizar_indice_acesso()

# Função de remoção de acesso por User_id com atualização de índice
def remover_acesso_por_id(id_remocao):
    registros = []
    encontrado = False

    with open('dados_acesso_fixo.bin', 'rb') as bin_file:
        while True:
            registro = bin_file.read(tamanho_registro)  
            if not registro:
                break 

            id_atual = registro[:campos_acesso['User_id']].strip().decode('utf-8')
            if id_atual == str(id_remocao):
                encontrado = True
                continue  # Ignorar o registro a ser removido
            registros.append(registro)

    if encontrado:
        # Sobrescrever o arquivo com os registros restantes
        with open('dados_acesso_fixo.bin', 'wb') as bin_file:
            for registro in registros:
                bin_file.write(registro)
        
        # Atualizar o índice após a remoção
        atualizar_indice_acesso()
        print(f"Usuário com ID {id_remocao} removido.")
    else:
        print(f"Usuário com ID {id_remocao} não encontrado.")
