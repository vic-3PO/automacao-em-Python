# Projeto Comparativo de Valores

Este projeto consiste em uma aplicação web desenvolvida em Python para comparar valores de produtos encontrados no Mercado Livre. A aplicação utiliza técnicas de web scraping com Selenium para coletar informações como nome do produto, valor, vendedor, parcelamento, avaliação e cupons de desconto. Os dados coletados são exibidos em uma tabela na interface web.

## Funcionalidades

- Varredura de links específicos do Mercado Livre para capturar informações de produtos.
- Exibição dos dados capturados em uma tabela na interface web.
- Opção para o usuário especificar a quantidade de itens a serem capturados.
- Possibilidade de busca por qualquer item no Mercado Livre através de um campo na interface.
- Armazenamento dos dados em um banco de dados SQLite local na máquina do usuário.
- Cálculo e exibição do valor médio dos itens pesquisados na interface.

## Pré-requisitos

- Python 3.x
- Flask
- Selenium
- Chrome WebDriver
- SQLite

## Instalação

1. Clone este repositório para o seu ambiente local:
   ```
   git clone https://github.com/seu_usuario/seu_projeto.git
   ```

2. Navegue até o diretório do projeto:
   ```
   cd seu_projeto
   ```

3. Instale as dependências utilizando o `pip`:
   ```
   pip install -r requirements.txt
   ```

4. Certifique-se de ter o Chrome WebDriver instalado e configurado corretamente.

## Uso

1. Inicie o servidor Flask executando o arquivo `app.py`:
   ```
   python app.py
   ```

2. Acesse a aplicação em seu navegador web no endereço `http://127.0.0.1:5000/`.

3. Na página inicial, insira o termo de pesquisa e a quantidade desejada de itens.

4. Clique no botão "Pesquisar" para iniciar a busca.

5. Os resultados da busca serão exibidos em uma tabela na mesma página.

## Observações

- Os dados coletados serão armazenados no arquivo `mercadolivre.db` no diretório `C:\mercadolivre` da máquina do usuário.
- Certifique-se de que o ambiente virtual do projeto esteja ativado antes de iniciar o servidor Flask.
- Para fins de desenvolvimento, o modo de depuração (`debug`) está ativado. Certifique-se de desativá-lo em um ambiente de produção.
