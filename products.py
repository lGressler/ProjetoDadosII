import os

# Definindo o tamanho fixo dos campos de produto
campos_produto = {'Id_produto': 10, 'marca': 20, 'nome': 30, 'preco': 10, 'categoria': 20}

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

# Função de pesquisa binária em produtos
def pesquisa_binaria_produtos(chave, campo='Id_produto'):
    with open('dados_produto_fixo.bin', 'rb') as bin_file:
        bin_file.seek(0, os.SEEK_END)
        tamanho_registro = sum(campos_produto.values()) + 1  # +1 para nova linha
        registros = bin_file.tell() // tamanho_registro
        inicio, fim = 0, registros - 1
        while inicio <= fim:
            meio = (inicio + fim) // 2
            bin_file.seek(meio * tamanho_registro)
            registro = bin_file.read(tamanho_registro).decode('utf-8').strip()
            campos = registro.split()
            valor_campo = campos[0]  # Valor do campo "Id_produto"
            if valor_campo == chave:
                print(f"Registro encontrado: {registro}")
                return registro
            elif valor_campo < chave:
                inicio = meio + 1
            else:
                fim = meio - 1
        print("Registro não encontrado.")
        return None

# Função para inserir novos dados de produtos
def inserir_dados_produto(dados):
    dados_ajustados = ''.join(ajustar_tamanho(dados[campo], tamanho) for campo, tamanho in campos_produto.items())
    with open('dados_produto_fixo.bin', 'ab') as bin_file:
        bin_file.write(dados_ajustados.encode('utf-8') + b'\n')
