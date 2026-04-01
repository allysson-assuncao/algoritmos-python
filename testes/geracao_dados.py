import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# Inicializa o Faker configurado para o Brasil
fake = Faker('pt_BR')

def gerar_dados_vendas(quantidade_linhas=5000):
    # Dicionário de Categorias, Produtos e um preço base aproximado
    catalogo = {
        'Eletrônicos': [('Smartphone', 2500.00), ('Notebook', 4500.00), ('Fone Bluetooth', 150.00), ('Smartwatch', 300.00)],
        'Vestuário': [('Camiseta de Algodão', 59.90), ('Calça Jeans', 120.00), ('Tênis Esportivo', 250.00), ('Jaqueta', 199.90)],
        'Casa e Decoração': [('Luminária', 89.90), ('Jogo de Cama', 150.00), ('Quadro Decorativo', 60.00), ('Tapete', 200.00)],
        'Beleza': [('Perfume', 350.00), ('Creme Hidratante', 45.00), ('Kit Maquiagem', 120.00), ('Shampoo', 30.00)]
    }

    meios_acesso = ['Anúncio Instagram', 'Google Ads', 'Afiliado', 'Acesso Direto (Site)', 'E-mail Marketing', 'Busca Orgânica']
    formas_pagamento = ['Cartão de Crédito', 'Pix', 'Boleto']
    sexo_opcoes = ['F', 'M', 'Outro']
    dias_semana_pt = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']

    dados = []

    for _ in range(quantidade_linhas):
        # Seleciona Produto e Categoria
        categoria = random.choice(list(catalogo.keys()))
        produto_info = random.choice(catalogo[categoria])
        nome_produto = produto_info[0]

        # Gera uma pequena variação de preço (± 10%)
        variacao = random.uniform(0.9, 1.1)
        preco = round(produto_info[1] * variacao, 2)

        # Quantidade comprada
        quantidade = random.randint(1, 5)

        # Data e Horário (vendas do último ano até hoje)
        data_venda = fake.date_between(start_date='-1y', end_date='today')
        horario = fake.time_object()
        dia_semana = dias_semana_pt[data_venda.weekday()]

        # Dados do Cliente
        idade = random.randint(18, 75)
        sexo = random.choices(sexo_opcoes, weights=[0.5, 0.45, 0.05])[0]

        # Compra
        usou_cupom = random.choice(['Sim', 'Não'])

        # Regras de Pagamento (Parcelamento só faz sentido em Cartão de Crédito)
        forma_pagto = random.choices(formas_pagamento, weights=[0.6, 0.3, 0.1])[0]
        if forma_pagto == 'Cartão de Crédito':
            parcelas = random.randint(1, 12)
        else:
            parcelas = 1

        # Localização (Utilizando o Faker para gerar dados do Brasil)
        uf = fake.state_abbr()
        cidade = fake.city()

        # Canal de aquisição
        acesso = random.choice(meios_acesso)

        # Adiciona a linha de dados
        dados.append({
            'Categoria': categoria,
            'Nome Do Produto': nome_produto,
            'Preço (R$)': preco,
            'Quantidade': quantidade,
            'Data': data_venda.strftime('%d/%m/%Y'),
            'Horário': horario.strftime('%H:%M:%S'),
            'Dia da Semana': dia_semana,
            'Idade Do Cliente': idade,
            'Sexo': sexo,
            'Usou Cupom': usou_cupom,
            'Forma de Pagamento': forma_pagto,
            'Parcelas': parcelas,
            'Cidade': cidade,
            'UF': uf,
            'Meio de Acesso': acesso
        })

    # Converte a lista de dicionários para um DataFrame do Pandas
    df = pd.DataFrame(dados)
    return df

# Define a quantidade de linhas (ex: 500)
numero_de_linhas = 50000

print(f"Gerando {numero_de_linhas} linhas de dados de vendas...")
df_vendas = gerar_dados_vendas(numero_de_linhas)

# Salva o DataFrame em um arquivo Excel (.xlsx)
nome_arquivo = 'dados_vendas_simulados.xlsx'
df_vendas.to_excel(nome_arquivo, index=False)

print(f"Sucesso! Os dados foram salvos no arquivo: {nome_arquivo}")
