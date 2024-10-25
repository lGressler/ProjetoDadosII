import os
import struct

# Definindo o tamanho fixo dos campos de produto
campos_produto = {'Id_produto': 10, 'marca': 20, 'nome': 30, 'preco': 10, 'categoria': 20}
tamanho_registro = sum(campos_produto.values())
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

# Função para gerar índice de produto (ordenado por ID)
def gerar_indice_produto(arquivo_dados, arquivo_indice):
    with open(arquivo_dados, 'rb') as f_dados, open(arquivo_indice, 'wb') as f_indice:
        while True:
            registro = f_dados.read(40)  

            if not registro:
                break

            if len(registro) < 10:
                print("Registro inválido ou incompleto:", registro)
                continue  

            try:
                chave = int(registro[:10].decode('utf-8').strip())  # ID do produto
            except ValueError as e:
                print(f"Erro ao converter chave: {e}. Registro: {registro}")
                continue  

            f_indice.write(chave.to_bytes(4, 'little')) 

# Função para atualizar o índice após inserção
def atualizar_indice_produto():
    gerar_indice_produto('dados_produto_fixo.bin', 'indice_produto.idx')

#Função de pesquisa binaria dos slides

# procedure pesq_bin(chave, inicio, fim, pos: integer; achou: boolean);
# var
#     meio: integer;
# begin
#  achou:= falso;
#  if (fim-inicio) > 0
#     then begin
#         meio:= int((inicio+fim)/2)+1;
#         seek(arq, meio);
#         read(arq, registro);
#  if registro.chave = chave
#     then begin
#         achou:= true;
#         pos:= meio;
#     end
#  else if registro.chave > chave
#         then pesq_bin(chave, inicio, meio, pos, achou)
#     else pesq_bin(chave, meio, fim, pos, achou);
#   end
# end;

# Função de pesquisa binária utilizando o índice
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

# Função de inserção de dados com atualização de índice
def inserir_dados_produto(dados):
    # Converte o ID do produto para inteiro
    id_novo = int(dados['Id_produto'])
    dados_ajustados = tuple(ajustar_tamanho(dados[campo], tamanho).encode('utf-8') for campo, tamanho in campos_produto.items())

    posicao_inserir = None
    registros = []

    with open('dados_produto_fixo.bin', 'rb') as bin_file:
        while True:
            registro = bin_file.read(tamanho_registro)
            if not registro:
                break
            
            # Verifica se o campo ID do produto não está vazio
            id_str = registro[:10].strip().decode('utf-8')
            if id_str.isdigit():  # Somente processa se for numérico
                id_atual = int(id_str)

                # Pula registros que estão marcados como excluídos
                if registro[-1] == b'1':  
                    continue

                # Define a posição para inserir o novo registro caso seja menor
                if id_novo < id_atual:  
                    posicao_inserir = len(registros)
                    break
            registros.append(registro)

    # Se o novo registro é maior que todos, insere no final
    if posicao_inserir is None:
        posicao_inserir = len(registros)

    # Insere o novo registro na posição correta
    registros.insert(posicao_inserir, struct.pack(formato, *dados_ajustados))

    # Sobrescreve o arquivo com os registros atualizados
    with open('dados_produto_fixo.bin', 'wb') as bin_file:
        for registro in registros:
            bin_file.write(registro)
    print(f"Produto com ID {id_novo} inserido com sucesso.")

# Função de remoção de produto por ID com atualização de índice
def remover_produto_por_id(id_remocao):
    registros = []
    encontrado = False

    with open('dados_produto_fixo.bin', 'rb') as bin_file:
        while True:
            registro = bin_file.read(tamanho_registro)
            if not registro:
                break
            
            # Verifique se o campo ID do produto não está vazio
            id_str = registro[:10].strip().decode('utf-8')
            if id_str.isdigit():  # Verifica se é um número válido
                id_atual = int(id_str)
                
                # Se o ID atual é igual ao de remoção e o registro não está excluído
                if id_atual == id_remocao and registro[-1] != b'1':  
                    encontrado = True
                    registro = registro[:-1] + b'1'  # Marca como excluído
            registros.append(registro)

    if encontrado:
        # Sobrescreve o arquivo com os registros atualizados
        with open('dados_produto_fixo.bin', 'wb') as bin_file:
            for registro in registros:
                bin_file.write(registro)
        print(f"Produto com ID {id_remocao} marcado como excluído.")
    else:
        print(f"Produto com ID {id_remocao} não encontrado.")

