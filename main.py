import csv
import products
import accesses
import struct

# Definindo o tamanho fixo dos campos de produto
campos_produto = {'Id_produto': 10, 'marca': 20, 'nome': 30, 'preco': 10, 'categoria': 20}

# Definindo o tamanho fixo dos campos de acesso
campos_acesso = {'User_id': 10, 'data_ultimo_acesso': 20, 'quantidade_acessos': 5, 'nome': 30, 'sessao': 10}

# Função para ajustar o tamanho dos campos
def ajustar_tamanho(campo, tamanho):
    return campo.ljust(tamanho)[:tamanho]

# Função para converter CSV para binário
def csv_para_binario_produto(arquivo_csv, arquivo_bin):
    with open(arquivo_csv, 'r', newline='', encoding='utf-8') as csv_file:
        leitor_csv = csv.DictReader(csv_file)
        with open(arquivo_bin, 'wb') as bin_file:
            for linha in leitor_csv:
                linha_binaria = ''.join(ajustar_tamanho(linha[campo], tamanho) for campo, tamanho in campos_produto.items())
                bin_file.write(linha_binaria.encode('utf-8') + b'\n')
                
# Função para converter CSV para binário
def csv_para_binario_acesso(arquivo_csv, arquivo_bin):
    with open(arquivo_csv, 'r', newline='', encoding='utf-8') as csv_file:
        leitor_csv = csv.DictReader(csv_file)
        with open(arquivo_bin, 'wb') as bin_file:
            for linha in leitor_csv:
                linha_binaria = ''.join(ajustar_tamanho(linha[campo], tamanho) for campo, tamanho in campos_acesso.items())
                bin_file.write(linha_binaria.encode('utf-8') + b'\n')

# Função para exibir o menu principal
def menu():
    print("\n Menu de opções: ")
    print("1. Menu de produtos ")
    print("2. Menu de acessos ")
    print("9. Sair")
    return input("Escolha uma opção: ")

# Função para exibir o menu de produtos 
def menuProdutos():
    print("1. Mostrar dados de produtos")
    print("2. Pesquisa binária nos dados de produtos")
    print("3. Consultar dados a partir da pesquisa binária")
    print("4. Inserir dados")  # Explicar como os dados foram ordenados e inseridos
    print("5. Voltar para o menu principal ")
    return input("Escolha uma opção: ")

# Função para exibir o menu de acessos 
def menuAcessos():
    print("1. Mostrar dados dos acessos")
    print("2. Pesquisa binária nos dados dos acessos")
    print("3. Consultar dados a partir da pesquisa binária")
    print("4. Inserir dados")  # Explicar como os dados foram ordenados e inseridos
    print("5. Voltar para o menu principal ")
    return input("Escolha uma opção: ")

# Função principal
def main():
    # Converter arquivos CSV para binários
    csv_para_binario_acesso('data/accesses.csv', 'dados_acesso_fixo.bin')
    csv_para_binario_produto('data/products.csv', 'dados_produto_fixo.bin')
    print("Conversão de CSV para binário concluída.")
    
    while True:
        opcao = menu()
        if opcao == '1':  # Menu de produtos
            while True:
                opcao_produto = menuProdutos()
                if opcao_produto == '1':
                    products.mostrar_dados_produtos()
                elif opcao_produto == '2':
                    chave = int(input("Digite o ID do produto para pesquisa: "))
                    resultado = products.pesquisa_binaria_produtos('dados_produto_fixo.bin', chave, 91)
                    if resultado != -1:
                        print(f"Produto encontrado no índice: {resultado}") 
                    else: 
                        print("Produto não encontrado.") 
                elif opcao_produto == '3':
                        print("Não operante no momento")
                elif opcao_produto == '4':
                    dados = {
                        'Id_produto': input("ID do produto: "),
                        'marca': input("Marca: "),
                        'nome': input("Nome: "),
                        'preco': input("Preço: "),
                        'categoria': input("Categoria: ")
                    }
                    products.inserir_dados_produto(dados)
                elif opcao_produto == '5':
                    break

        elif opcao == '2':  # Menu de acessos
            while True:
                opcao_acesso = menuAcessos()
                if opcao_acesso == '1':
                    accesses.mostrar_dados_acessos()
                elif opcao_acesso == '2':
                    chave = input("Digite o User ID para pesquisa: ")
                    resultado = accesses.pesquisa_binaria_acessos(chave)
                    if resultado is None:
                        print("Acesso não encontrado.")  
                elif opcao_acesso == '3':
                        print("Não operante no momento")
                elif opcao_acesso == '4':
                    dados = {
                        'User_id': input("User ID: "),
                        'data_ultimo_acesso': input("Data do último acesso: "),
                        'quantidade_acessos': input("Quantidade de acessos: "),
                        'nome': input("Nome: "),
                        'sessao': input("Sessão: ")
                    }
                    accesses.inserir_dados_acesso(dados)
                elif opcao_acesso == '5':
                    break

        elif opcao == '9':
            print("Saindo do programa.")
            break

# Executa o programa
if __name__ == "__main__":
    main()


