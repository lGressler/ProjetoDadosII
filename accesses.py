import os

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
    dados_ajustados = ''.join(ajustar_tamanho(dados[campo], tamanho) for campo, tamanho in campos_acesso.items())
    with open('dados_acesso_fixo.bin', 'ab') as bin_file:
        bin_file.write(dados_ajustados.encode('utf-8') + b'\n')
