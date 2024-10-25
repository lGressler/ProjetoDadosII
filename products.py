import os
import struct

# Definindo o tamanho fixo dos campos de produto
campos_produto = {'Id_produto': 10,
                  'marca': 20,
                  'nome': 30,
                  'preco': 10,
                  'categoria': 20
                }
tamanho_registro = 10 + 20 + 30 + 10 + 20
formato = '10s20s30s10s20s'

# Função para ajustar o tamanho dos campos
def ajustar_tamanho(campo, tamanho):
    return campo.ljust(tamanho)[:tamanho]

# Função para mostrar dados de produtos
def mostrar_dados_produtos():
    if os.path.exists('dados_produto_fixo.bin'):
        with open('dados_produto_fixo.bin', 'rb') as bin_file:
            for linha in bin_file:
                print(linha.decode('utf-8').strip())
    else:
        print("Arquivo binário de produtos não encontrado.")

# Função de pesquisa binária padrão
def pesquisa_binaria_produtos(nome_arquivo, chave_procurada):
    with open(nome_arquivo, 'rb') as arquivo:
        low = 0  # Inicializando low
        arquivo.seek(0, 2)
        tamanho_arquivo = arquivo.tell()
        high = tamanho_arquivo // tamanho_registro - 1

        while low <= high:
            mid = (low + high) // 2
            pos = mid * tamanho_registro
            arquivo.seek(pos)
            registro = arquivo.read(tamanho_registro)
            chave_registro = int(registro[:10].decode('utf-8').strip())
            
            if chave_registro == chave_procurada:
                return pos
            elif chave_registro < chave_procurada:
                low = mid + 1
            else:
                high = mid - 1
        return -1

# Função para gerar índice ordenado de IDs
def gerar_indice_produto(nome_arquivo, nome_indice):
    with open(nome_arquivo, 'rb') as arquivo, open(nome_indice, 'wb') as indice:
        pos = 0
        while True:
            registro = arquivo.read(tamanho_registro)
            if not registro:
                break
            chave = int(registro[:10].decode('utf-8').strip())
            indice.write(struct.pack('i i', chave, pos))
            pos += tamanho_registro

# Função de pesquisa binária utilizando índice
def pesquisa_binaria_por_indice(nome_indice, chave_procurada):
    with open(nome_indice, 'rb') as indice:
        tamanho_registro_indice = struct.calcsize('i i')
        low = 0
        indice.seek(0, 2)
        high = indice.tell() // tamanho_registro_indice - 1

        while low <= high:
            mid = (low + high) // 2
            pos = mid * tamanho_registro_indice
            indice.seek(pos)
            chave_indice, pos_arquivo = struct.unpack('i i', indice.read(tamanho_registro_indice))
            
            if chave_indice == chave_procurada:
                return pos_arquivo
            elif chave_indice < chave_procurada:
                low = mid + 1
            else:
                high = mid - 1
        return -1

def inserir_dados_produto(dados):
    formato = '10s20s30s10s20s' 
    dados_ajustados = tuple(ajustar_tamanho(dados[campo], tamanho).encode('utf-8') for campo, tamanho in campos_produto.items())
    dados_binarios = struct.pack(formato, *dados_ajustados)
    with open('dados_produto_fixo.bin', 'ab') as bin_file:
        bin_file.write(dados_binarios)
        
def remover_produto_por_id(id_remocao):
    registros = []
    encontrado = False

    with open('dados_produto_fixo.bin', 'rb') as bin_file:
        while True:
            registro = bin_file.read(sum(campos_produto.values()))  
            if not registro:
                break 

     
            id_atual = registro[:campos_produto['Id_produto']].strip().decode('utf-8')
            if id_atual == str(id_remocao):
                encontrado = True
                continue  
            registros.append(registro)

    with open('dados_produto_fixo.bin', 'wb') as bin_file:
        for registro in registros:
            bin_file.write(registro)

    if encontrado:
        print(f"Produto com ID {id_remocao} removido.")
    else:
        print(f"Produto com ID {id_remocao} não encontrado.")

