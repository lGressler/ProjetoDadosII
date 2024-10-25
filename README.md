# Estrutura do Projeto
O projeto está organizado em diferentes módulos para lidar com produtos e acessos, utilizando arquivos binários para armazenar dados. Aqui estão os principais módulos e suas funções:

## Arquivo main.py
Este arquivo contém a função principal do programa, além de menus para acessar e operar os dados de produtos e acessos.

### Funções:
```python
ajustar_tamanho(campo, tamanho)
Ajusta o tamanho de um campo de texto, preenchendo espaços em branco para garantir que cada campo tenha o tamanho correto, ou cortando se exceder o limite.

csv_para_binario_produto(arquivo_csv, arquivo_bin)
Converte um arquivo CSV de produtos em um arquivo binário, com tamanhos de campos fixos. Usa a função ajustar_tamanho para garantir o tamanho correto de cada campo.

csv_para_binario_acesso(arquivo_csv, arquivo_bin)
Converte um arquivo CSV de acessos em um arquivo binário de campos fixos, semelhante à função de produtos.

menu()
Exibe o menu principal do programa, permitindo ao usuário escolher entre as opções de acessar o menu de produtos, menu de acessos ou sair do programa.

menuProdutos()
Exibe as opções relacionadas a produtos, como mostrar dados, realizar pesquisa binária, consultar dados, inserir, remover ou salvar informações de produtos.

menuAcessos()
Exibe as opções relacionadas aos dados de acessos, incluindo mostrar, realizar pesquisa binária, inserir, remover e salvar dados de acessos.

main()
A função principal que executa o programa, converte os arquivos CSV para binário, e controla a navegação pelos menus, chamando as funções específicas de produtos e acessos.

Arquivo products.py
Este arquivo contém as funções relacionadas à manipulação dos dados binários de produtos.

Funções:
ajustar_tamanho(campo, tamanho)
Ajusta o tamanho do campo como descrito anteriormente.

mostrar_dados_produtos()
Lê e exibe os dados dos produtos armazenados no arquivo binário dados_produto_fixo.bin.

pesquisa_binaria_produtos(nome_arquivo, chave_procurada)
Realiza uma pesquisa binária em um arquivo binário de produtos para localizar um produto específico com base no seu ID.

gerar_indice_produto(nome_arquivo, nome_indice)
Gera um arquivo de índice a partir dos dados de produtos, armazenando a chave (ID do produto) e a posição no arquivo binário, para otimizar futuras pesquisas.

pesquisa_binaria_por_indice(nome_indice, chave_procurada)
Realiza uma pesquisa binária no arquivo de índice para localizar a posição de um registro no arquivo binário de produtos.

inserir_dados_produto(dados)
Insere novos dados de produto no arquivo binário. Os dados são convertidos para binário utilizando a função ajustar_tamanho e são escritos no arquivo.

remover_produto_por_id(id_remocao)
Remove um produto do arquivo binário baseado no ID. Os dados são lidos e reescritos, exceto o produto que corresponde ao ID fornecido.
```

## Arquivo accesses.py
Este arquivo contém as funções relacionadas à manipulação dos dados binários de acessos de usuários.

### Funções:
```python
ajustar_tamanho(campo, tamanho)
Ajusta o tamanho do campo de texto, semelhante às funções dos outros módulos.

mostrar_dados_acessos()
Lê e exibe os dados dos acessos armazenados no arquivo binário dados_acesso_fixo.bin.

pesquisa_binaria_acessos(chave, campo='User_id')
Realiza uma pesquisa binária no arquivo de acessos para localizar um acesso específico com base no User_id.

inserir_dados_acesso(dados)
Insere novos dados de acesso no arquivo binário. Os campos são ajustados com a função ajustar_tamanho e os dados são convertidos para binário e gravados no arquivo.

remover_acesso_por_id(id_remocao)
Remove um acesso do arquivo binário baseado no ID. Todos os dados são lidos e os registros, exceto o que corresponde ao ID, são reescritos.
```

## Fluxo de Execução
Conversão CSV para Binário
Na inicialização do programa, as funções csv_para_binario_produto e csv_para_binario_acesso convertem os arquivos CSV em arquivos binários com tamanho de campos fixos. Isso garante que os registros ocupem um espaço constante no arquivo.

## Menus
Após a conversão, o menu principal é exibido, permitindo que o usuário escolha entre os menus de produtos e acessos. Cada menu oferece opções como visualização, inserção, remoção e pesquisa de dados.

## Manipulação de Dados
Nos menus de produtos e acessos, as funções relacionadas a pesquisa binária permitem ao usuário localizar registros de forma eficiente. A inserção e remoção de dados também são feitas de forma organizada, mantendo a estrutura dos arquivos binários.

## Geração de Índices
A função gerar_indice_produto cria um arquivo de índice para otimizar a busca de registros no arquivo binário de produtos, utilizando chaves e posições.