import pandas as pd
import random
from faker import Faker
from datetime import datetime

# Inicializa o Faker
fake = Faker('pt_BR')

def gerar_dados_vendas(quantidade_linhas=50000):
    # Catálogo de produtos expandido: 'Nome', Preço Base
    catalogo = {
        'Eletrônicos': [('Smartphone Top', 4500.0), ('Smartphone Intermediário', 1800.0), ('Notebook Gamer', 7500.0), ('Notebook Básico', 2500.0), ('Smart TV 55', 3200.0), ('Fone Bluetooth', 250.0), ('Smartwatch', 800.0)],
        'Vestuário': [('Camiseta de Algodão', 59.9), ('Calça Jeans', 149.9), ('Tênis Esportivo', 350.0), ('Jaqueta de Couro', 499.9), ('Vestido Estampado', 189.9), ('Moletom', 120.0)],
        'Casa e Decoração': [('Luminária de Chão', 199.9), ('Jogo de Cama 400 Fios', 250.0), ('Sofá Retrátil', 2200.0), ('Quadro Decorativo', 90.0), ('Tapete Sala', 350.0), ('Poltrona', 600.0)],
        'Beleza': [('Perfume Importado', 450.0), ('Perfume Nacional', 120.0), ('Kit Skincare', 280.0), ('Creme Anti-idade', 150.0), ('Base Maquiagem', 90.0), ('Shampoo Profissional', 80.0)],
        'Esporte e Lazer': [('Bicicleta Aro 29', 1500.0), ('Whey Protein', 140.0), ('Bola de Futebol', 80.0), ('Kit Halteres', 180.0), ('Barraca de Camping', 450.0)],
        'Livros': [('Box Ficção', 120.0), ('Livro Finanças', 50.0), ('Biografia', 65.0), ('Livro Técnico TI', 150.0)],
        'Games': [('Console Nova Geração', 4200.0), ('Controle Extra', 450.0), ('Jogo Lançamento', 350.0), ('Cadeira Gamer', 1200.0)]
    }

    # Distribuição geográfica (UF -> Cidades Principais e Probabilidade de cair no estado)
    estados_dist = {
        'SP': {'peso': 35, 'cidades': ['São Paulo', 'Campinas', 'Guarulhos', 'São Bernardo do Campo', 'Ribeirão Preto']},
        'RJ': {'peso': 12, 'cidades': ['Rio de Janeiro', 'Niterói', 'Duque de Caxias', 'Nova Iguaçu']},
        'MG': {'peso': 10, 'cidades': ['Belo Horizonte', 'Uberlândia', 'Contagem', 'Juiz de Fora']},
        'PR': {'peso': 8, 'cidades': ['Curitiba', 'Londrina', 'Maringá', 'Cascavel']},
        'RS': {'peso': 7, 'cidades': ['Porto Alegre', 'Caxias do Sul', 'Pelotas', 'Canoas']},
        'SC': {'peso': 6, 'cidades': ['Florianópolis', 'Joinville', 'Blumenau', 'São José']},
        'BA': {'peso': 5, 'cidades': ['Salvador', 'Feira de Santana', 'Vitória da Conquista']},
        'PE': {'peso': 4, 'cidades': ['Recife', 'Jaboatão dos Guararapes', 'Olinda']},
        'CE': {'peso': 4, 'cidades': ['Fortaleza', 'Caucaia', 'Juazeiro do Norte']},
        'DF': {'peso': 3, 'cidades': ['Brasília', 'Taguatinga', 'Ceilândia']},
        'GO': {'peso': 3, 'cidades': ['Goiânia', 'Aparecida de Goiânia', 'Anápolis']},
        'PA': {'peso': 2, 'cidades': ['Belém', 'Ananindeua', 'Santarém']},
        'AM': {'peso': 1, 'cidades': ['Manaus', 'Parintins']}
    }
    ufs = list(estados_dist.keys())
    pesos_ufs = [estados_dist[uf]['peso'] for uf in ufs]

    meios_acesso = ['Google Ads', 'Anúncio Instagram', 'Afiliado', 'Acesso Direto (Site)', 'E-mail Marketing', 'Busca Orgânica']
    dias_semana_pt = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']

    dados = []

    for i in range(quantidade_linhas):
        # 1. PERFIL DO CLIENTE
        # Idade: Curva normal (média 35 anos, desvio padrão 12). Limites entre 18 e 75.
        idade = int(random.gauss(35, 12))
        idade = max(18, min(75, idade))

        sexo = random.choices(['F', 'M', 'Outro'], weights=[0.52, 0.46, 0.02])[0]

        uf = random.choices(ufs, weights=pesos_ufs)[0]
        cidade = random.choice(estados_dist[uf]['cidades'])

        # 2. DEFINIÇÃO DA CATEGORIA COM BASE NO PERFIL (Viés de Compra)
        pesos_cat = {
            'Eletrônicos': 15, 'Vestuário': 20, 'Casa e Decoração': 15,
            'Beleza': 15, 'Esporte e Lazer': 10, 'Livros': 10, 'Games': 5
        }

        if sexo == 'F':
            pesos_cat['Beleza'] += 20
            pesos_cat['Vestuário'] += 10
            pesos_cat['Casa e Decoração'] += 15
        elif sexo == 'M':
            pesos_cat['Eletrônicos'] += 15
            pesos_cat['Esporte e Lazer'] += 15
            pesos_cat['Games'] += 10

        if idade < 30:
            pesos_cat['Games'] += 20
            pesos_cat['Eletrônicos'] += 15
            pesos_cat['Vestuário'] += 10
        elif idade > 50:
            pesos_cat['Casa e Decoração'] += 20
            pesos_cat['Livros'] += 15

        categorias = list(pesos_cat.keys())
        prob_cat = list(pesos_cat.values())
        categoria = random.choices(categorias, weights=prob_cat)[0]

        # 3. ESCOLHA DO PRODUTO E PREÇO
        produto_info = random.choice(catalogo[categoria])
        nome_produto = produto_info[0]

        # Variação agressiva de preço (de 30% de desconto a 20% mais caro)
        variacao = random.uniform(0.70, 1.20)
        preco_unitario = round(produto_info[1] * variacao, 2)

        # Lógica de Quantidade: Itens muito caros costumam ser comprados em unidade
        if preco_unitario > 1500:
            quantidade = random.choices([1, 2], weights=[0.95, 0.05])[0]
        elif preco_unitario < 100:
            quantidade = random.choices([1, 2, 3, 4, 5], weights=[0.5, 0.25, 0.15, 0.05, 0.05])[0]
        else:
            quantidade = random.choices([1, 2, 3], weights=[0.75, 0.20, 0.05])[0]

        valor_total_compra = preco_unitario * quantidade

        # 4. DATAS E HORÁRIOS (Ligeiro viés para compras de noite/tarde)
        data_venda = fake.date_between(start_date='-2y', end_date='today')
        dia_semana = dias_semana_pt[data_venda.weekday()]

        hora = int(random.gauss(16, 5)) # Pico às 16h, variando para tarde e noite
        hora = max(0, min(23, hora))
        minuto = random.randint(0, 59)
        horario_str = f"{hora:02d}:{minuto:02d}:{random.randint(0,59):02d}"

        # 5. PAGAMENTO, PARCELAS E CUPOM
        usou_cupom = random.choices(['Sim', 'Não'], weights=[0.3, 0.7])[0]

        # Compras altas vão pro crédito. Compras baixas vão pro Pix.
        if valor_total_compra > 1000:
            forma_pagto = random.choices(['Cartão de Crédito', 'Pix', 'Boleto'], weights=[0.85, 0.10, 0.05])[0]
        elif valor_total_compra < 150:
            forma_pagto = random.choices(['Cartão de Crédito', 'Pix', 'Boleto'], weights=[0.35, 0.55, 0.10])[0]
        else:
            forma_pagto = random.choices(['Cartão de Crédito', 'Pix', 'Boleto'], weights=[0.60, 0.30, 0.10])[0]

        if forma_pagto == 'Cartão de Crédito':
            if valor_total_compra > 2000:
                parcelas = random.randint(6, 12)
            elif valor_total_compra > 500:
                parcelas = random.randint(2, 6)
            else:
                parcelas = random.randint(1, 3)
        else:
            parcelas = 1

        # 6. CANAL DE AQUISIÇÃO (Viés: jovens clicam mais em insta/redes sociais, orgânico e email pra mais velhos)
        if idade < 30:
            acesso = random.choices(meios_acesso, weights=[0.2, 0.4, 0.1, 0.1, 0.05, 0.15])[0]
        else:
            acesso = random.choices(meios_acesso, weights=[0.2, 0.15, 0.1, 0.2, 0.2, 0.15])[0]

        # Adiciona a linha de dados
        dados.append({
            'Data': data_venda.strftime('%d/%m/%Y'),
            'Horário': horario_str,
            'Dia da Semana': dia_semana,
            'Categoria': categoria,
            'Nome Do Produto': nome_produto,
            'Preço Unitário (R$)': preco_unitario,
            'Quantidade': quantidade,
            'Valor Total (R$)': round(valor_total_compra, 2),
            'Usou Cupom': usou_cupom,
            'Forma de Pagamento': forma_pagto,
            'Parcelas': parcelas,
            'Meio de Acesso': acesso,
            'Idade Do Cliente': idade,
            'Sexo': sexo,
            'Cidade': cidade,
            'UF': uf
        })

        # Mostra o progresso no console a cada 5000 linhas
        if (i + 1) % 5000 == 0:
            print(f"Gerado {i + 1} de {quantidade_linhas} registros...")

    df = pd.DataFrame(dados)
    return df

# Execução
quantidade_desejada = 50000

print(f"Iniciando a geração de {quantidade_desejada} linhas com padrões realistas...")
df_vendas_realista = gerar_dados_vendas(quantidade_desejada)

nome_arquivo = 'dados_vendas_consultoria.xlsx'
print(f"Salvando dados no arquivo '{nome_arquivo}'. Isso pode levar alguns segundos...")
df_vendas_realista.to_excel(nome_arquivo, index=False)

print(f"Finalizado! O arquivo {nome_arquivo} está pronto para análise de BI/Consultoria.")
