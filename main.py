import struct
import os

# Definição das estruturas
product_struct = struct.Struct('20s 20s 20s f')  # ID, Marca, Categoria, Preço
access_struct = struct.Struct('20s 20s 20s 20s')  # ID do Produto, User ID, Sessão, Tipo de Evento

# Caminhos dos arquivos
DATASETS_DIR = './datasets'
product_file_path = 'products.bin'
access_file_path = 'access.bin'
product_index_path = 'products_index.bin'
access_index_path = 'access_index.bin'

# Função para listar arquivos CSV na pasta datasets
def list_csv_files():
    files = [f for f in os.listdir(DATASETS_DIR) if f.endswith('.csv')]
    if not files:
        print("Nenhum arquivo CSV encontrado na pasta datasets.")
        return None
    print("\nEscolha um arquivo CSV:")
    for idx, file in enumerate(files):
        print(f"{idx + 1}. {file}")
    return files

# Função para carregar os arquivos binários
def load_data_to_binary(csv_file_name, file_type):
    """
    Carrega os dados de um CSV e insere no arquivo binário correto (produtos ou acessos).
    """
    csv_file_path = os.path.join(DATASETS_DIR, csv_file_name)
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            next(file)  # Ignorar a primeira linha (cabeçalho)
            for row in file:
                fields = row.strip().split(",")
                if file_type == 'product':
                    insert_product_data(fields)
                elif file_type == 'access':
                    insert_access_data(fields)
    except Exception as e:
        print(f"Erro ao carregar dados do CSV: {e}")

# Função para verificar se o arquivo binário existe, caso contrário, cria
def ensure_file_exists(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'wb'):
            pass  # Apenas cria o arquivo vazio

# Função para inserir dados no arquivo de produtos
def insert_product_data(fields):
    try:
        ensure_file_exists(product_file_path)
        with open(product_file_path, 'ab') as product_file:
            # Ajustar os campos para inserção
            data = (fields[0].encode(), fields[1].encode(), fields[2].encode(), float(fields[3]))
            product_file.write(product_struct.pack(*data))
        rebuild_product_index()
    except ValueError as e:
        print(f"Erro ao processar linha {fields}: {e}")
    except Exception as e:
        print(f"Erro ao inserir dados de produtos: {e}")

# Função para inserir dados no arquivo de acessos
def insert_access_data(fields):
    try:
        ensure_file_exists(access_file_path)
        with open(access_file_path, 'ab') as access_file:
            # Ajustar os campos para inserção
            data = (fields[0].encode(), fields[1].encode(), fields[2].encode(), fields[3].encode())
            access_file.write(access_struct.pack(*data))
        rebuild_access_index()
    except ValueError as e:
        print(f"Erro ao processar linha {fields}: {e}")
    except Exception as e:
        print(f"Erro geral ao inserir dados de acessos: {e}")

# Função para reconstruir o índice de produtos
def rebuild_product_index():
    try:
        ensure_file_exists(product_file_path)
        ensure_file_exists(product_index_path)
        
        with open(product_file_path, 'rb') as product_file, open(product_index_path, 'wb') as index_file:
            pos = 0
            while True:
                data = product_file.read(product_struct.size)
                if not data:
                    break
                product_id = data[:20].decode().strip()
                index_file.write(struct.pack('20s I', product_id.encode(), pos))
                pos += product_struct.size
    except Exception as e:
        print(f"Erro ao reconstruir índice de produtos: {e}")

# Função para reconstruir o índice de acessos
def rebuild_access_index():
    try:
        ensure_file_exists(access_file_path)
        ensure_file_exists(access_index_path)
        
        with open(access_file_path, 'rb') as access_file, open(access_index_path, 'wb') as index_file:
            pos = 0
            while True:
                data = access_file.read(access_struct.size)
                if not data:
                    break
                product_id = data[:20].decode().strip()
                index_file.write(struct.pack('20s I', product_id.encode(), pos))
                pos += access_struct.size
    except Exception as e:
        print(f"Erro ao reconstruir índice de acessos: {e}")

# Função para exibir os dados dos arquivos binários
def display_binary_data(file_type):
    try:
        ensure_file_exists(product_file_path if file_type == 'product' else access_file_path)
        
        if file_type == 'product':
            with open(product_file_path, 'rb') as product_file:
                while True:
                    data = product_file.read(product_struct.size)
                    if not data:
                        break
                    unpacked_data = product_struct.unpack(data)
                    print(f"Marca: {unpacked_data[0].decode().strip()}, ID: {unpacked_data[1].decode().strip()}, Hora_do_evento: {unpacked_data[2].decode().strip()}, Preço: {unpacked_data[3]}")
        elif file_type == 'access':
            with open(access_file_path, 'rb') as access_file:
                while True:
                    data = access_file.read(access_struct.size)
                    if not data:
                        break
                    unpacked_data = access_struct.unpack(data)
                    print(f"Produto ID: {unpacked_data[0].decode().strip()}, User ID: {unpacked_data[1].decode().strip()}, Sessão: {unpacked_data[2].decode().strip()}, Tipo de Evento: {unpacked_data[3].decode().strip()}")
    except Exception as e:
        print(f"Erro ao exibir dados: {e}")

# Função de pesquisa binária
def binary_search(file_type, product_id):
    index_file_path = product_index_path if file_type == 'product' else access_index_path
    data_file_path = product_file_path if file_type == 'product' else access_file_path
    record_struct = product_struct if file_type == 'product' else access_struct

    try:
        ensure_file_exists(index_file_path)
        
        with open(index_file_path, 'rb') as index_file:
            record_size = struct.calcsize('20s I')  # Tamanho do registro do índice
            left, right = 0, os.path.getsize(index_file_path) // record_size - 1
            while left <= right:
                mid = (left + right) // 2
                index_file.seek(mid * record_size)
                index_data = struct.unpack('20s I', index_file.read(record_size))
                current_id = index_data[0].decode().strip()
                if current_id.lower() == product_id.lower():  # Ignorando maiúsculas/minúsculas
                    pos = index_data[1]
                    with open(data_file_path, 'rb') as data_file:
                        data_file.seek(pos)
                        record = record_struct.unpack(data_file.read(record_struct.size))
                        print(record)
                        return
                elif current_id < product_id:
                    left = mid + 1
                else:
                    right = mid - 1
        print("Produto não encontrado.")
    except Exception as e:
        print(f"Erro durante a pesquisa: {e}")

# Função principal (menu)
def main_menu():
    while True:
        print("\nMenu:")
        print("1. Inserir dados de CSV para Produtos")
        print("2. Inserir dados de CSV para Acessos")
        print("3. Mostrar dados dos Produtos")
        print("4. Mostrar dados dos Acessos")
        print("5. Pesquisar produto por ID")
        print("6. Pesquisar acesso por ID do Produto")
        print("0. Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            csv_files = list_csv_files()
            if csv_files:
                csv_choice = int(input("\nEscolha o número do arquivo CSV para produtos: ")) - 1
                if 0 <= csv_choice < len(csv_files):
                    load_data_to_binary(csv_files[csv_choice], 'product')
        elif choice == '2':
            csv_files = list_csv_files()
            if csv_files:
                csv_choice = int(input("\nEscolha o número do arquivo CSV para acessos: ")) - 1
                if 0 <= csv_choice < len(csv_files):
                    load_data_to_binary(csv_files[csv_choice], 'access')
        elif choice == '3':
            display_binary_data('product')
        elif choice == '4':
            display_binary_data('access')
        elif choice == '5':
            product_id = input("Digite o ID do produto para pesquisa: ")
            binary_search('product', product_id)
        elif choice == '6':
            product_id = input("Digite o ID do produto para pesquisar acessos: ")
            binary_search('access', product_id)
        elif choice == '0':
            print("Saindo do programa.")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main_menu()
